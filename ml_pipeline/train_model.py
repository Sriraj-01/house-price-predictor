import pandas as pd
import numpy as np
from pathlib import Path
import joblib

from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder
from sklearn.impute import SimpleImputer
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

from xgboost import XGBRegressor


DATA_PATH = "data/processed/features.csv"
MODEL_OUT = "backend/model/house_price_model.pkl"


def main():
    print("Loading feature data...")
    df = pd.read_csv(DATA_PATH)
    print("Dataset shape:", df.shape)

    # -----------------------
    # Detect target column safely
    # -----------------------
    target_candidates = [c for c in df.columns if "amount" in c.lower()]
    if len(target_candidates) != 1:
        raise ValueError(f"Expected exactly 1 target column, found: {target_candidates}")

    target_col = target_candidates[0]
    print("Using target column:", target_col)

    # -----------------------
    # Drop extreme outliers (top 1%)
    # -----------------------
    upper = df[target_col].quantile(0.99)
    df = df[df[target_col] < upper]

    # -----------------------
    # Separate X and y
    # -----------------------
    y = np.log1p(df[target_col])  # LOG TARGET (CRITICAL)
    leakage_cols = [c for c in df.columns if "price" in c.lower()]
    X = df.drop(columns=[target_col] + leakage_cols)

    # -----------------------
    # Fix numeric columns wrongly treated as categorical
    # -----------------------
    for col in ["Bathroom", "Balcony", "Car Parking"]:
        if col in X.columns:
            X[col] = pd.to_numeric(X[col], errors="coerce")

    # -----------------------
    # Drop near-empty columns
    # -----------------------
    null_frac = X.isnull().mean()
    drop_all_null = null_frac[null_frac > 0.95].index.tolist()
    if drop_all_null:
        print("Dropping near-empty columns:", drop_all_null)
        X = X.drop(columns=drop_all_null)

    # -----------------------
    # Column separation
    # -----------------------
    num_cols = X.select_dtypes(include=["int64", "float64"]).columns.tolist()
    cat_cols = X.select_dtypes(include=["object"]).columns.tolist()

    print("Numerical columns:", num_cols)
    print("Categorical columns:", cat_cols)

    # -----------------------
    # Preprocessing
    # -----------------------
    num_pipeline = Pipeline([
        ("imputer", SimpleImputer(strategy="median"))
    ])

    cat_pipeline = Pipeline([
        ("imputer", SimpleImputer(strategy="most_frequent")),
        ("onehot", OneHotEncoder(handle_unknown="ignore", min_frequency=100))
    ])

    preprocessor = ColumnTransformer([
        ("num", num_pipeline, num_cols),
        ("cat", cat_pipeline, cat_cols)
    ])

    # -----------------------
    # Model
    # -----------------------
    model = XGBRegressor(
        n_estimators=400,
        max_depth=6,
        learning_rate=0.05,
        subsample=0.8,
        colsample_bytree=0.8,
        random_state=42,
        n_jobs=-1
    )

    pipe = Pipeline([
        ("preprocessor", preprocessor),
        ("model", model)
    ])

    # -----------------------
    # Train / test split
    # -----------------------
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    print("Training model...")
    pipe.fit(X_train, y_train)

    # -----------------------
    # Evaluation (back-transform)
    # -----------------------
    preds_log = pipe.predict(X_test)
    preds = np.expm1(preds_log)
    y_test_actual = np.expm1(y_test)

    mae = mean_absolute_error(y_test_actual, preds)
    rmse = np.sqrt(mean_squared_error(y_test_actual, preds))
    r2 = r2_score(y_test_actual, preds)

    print("\nModel Performance")
    print("-----------------")
    print(f"MAE  : ₹{mae:,.0f}")
    print(f"RMSE : ₹{rmse:,.0f}")
    print(f"R²   : {r2:.4f}")

    # -----------------------
    # Save model
    # -----------------------
    Path("backend/model").mkdir(parents=True, exist_ok=True)
    joblib.dump(pipe, MODEL_OUT)

    print("\nModel saved to:", MODEL_OUT)


if __name__ == "__main__":
    main()
