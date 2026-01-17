import pandas as pd
import numpy as np


def convert_price(x):
    if pd.isna(x):
        return np.nan

    x = str(x).lower().replace(",", "").strip()

    try:
        if "lac" in x:
            return float(x.replace("lac", "")) * 100000
        if "cr" in x:
            return float(x.replace("cr", "")) * 10000000
        return float(x)
    except:
        return np.nan


def convert_area(x):
    if pd.isna(x):
        return np.nan
    try:
        x = str(x).lower().replace("sqft", "").replace("sq. ft.", "").strip()
        return float(x)
    except:
        return np.nan


def extract_floor(x):
    if pd.isna(x):
        return np.nan
    try:
        return int(str(x).split()[0])
    except:
        return np.nan
