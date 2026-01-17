import pandas as pd
import numpy as np
from pathlib import Path
from utils import convert_price, convert_area, extract_floor


RAW_PATH = "data/raw/house_prices.csv"
OUT_PATH = "data/processed/cleaned.csv"

def main():
    print("Loading data...")
    df = pd.read_csv(RAW_PATH)

    df = df.drop(columns=["Index","Title","Description","Price(in rupees)"], errors="ignore")

    df["Amount(in rupees)"] = df["Amount(in rupees)"].apply(convert_price)
    df["Carpet Area"] = df["Carpet Area"].apply(convert_area)

    if "Super Area" in df.columns:
        df["Super Area"] = df["Super Area"].apply(convert_area)

    if "Floor" in df.columns:
        df["Floor"] = df["Floor"].apply(extract_floor)

    df = df.dropna(subset=["Amount(in rupees)","Carpet Area"])
    df = df[df["Amount(in rupees)"] > 100000]
    df = df[df["Carpet Area"] > 100]

    Path("data/processed").mkdir(parents=True, exist_ok=True)
    df.to_csv(OUT_PATH, index=False)

    print("Saved cleaned data.")

if __name__ == "__main__":
    main()
