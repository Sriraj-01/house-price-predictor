import pandas as pd

df = pd.read_csv("data/processed/features.csv")

print("Shape:", df.shape)
print("\nColumns:")
for c in df.columns:
    print(c)

print("\nTarget stats:")
print(df["Amount(in rupees)"].describe())
