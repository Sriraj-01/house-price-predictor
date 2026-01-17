import pandas as pd
import numpy as np
from pathlib import Path


IN_PATH = "data/processed/cleaned.csv"
OUT_PATH = "data/processed/features.csv"


def extract_bhk(title):
    if pd.isna(title):
        return np.nan
    try:
        return int(str(title).split()[0])
    except:
        return np.nan
    
def infer_bhk(carpet_area):
    if pd.isna(carpet_area):
        return np.nan
    if carpet_area < 600:
        return 1
    elif carpet_area < 900:
        return 2
    elif carpet_area < 1300:
        return 3
    else:
        return 4

def main():
    print("Loading cleaned data...")
    df = pd.read_csv(IN_PATH)
    print("Input shape:", df.shape)

    if "Carpet Area" in df.columns:
        df["BHK"] = df["Carpet Area"].apply(infer_bhk)

    # Limit society cardinality
    if "Society" in df.columns:
        top_societies = df["Society"].value_counts().nlargest(100).index
        df["Society"] = df["Society"].where(
            df["Society"].isin(top_societies),
            "Other"
        )

    # Drop raw text fields if present
    drop_text = ["Description"]
    df = df.drop(columns=drop_text, errors="ignore")
    print("After feature engineering:", df.shape)

    Path("data/processed").mkdir(parents=True, exist_ok=True)
    df.to_csv(OUT_PATH, index=False)
    print("Saved features to:", OUT_PATH)


if __name__ == "__main__":
    main()
