# back_end/data_pipeline/scripts/load_and_inspect.py

import os
import pandas as pd
from datasets import load_dataset

RAW_OUTPUT_PATH = "data/raw/nutrition_raw.csv"

CATEGORICAL_COLUMNS = [
    "Gender",
    "Activity Level",
    "Fitness Goal",
    "Dietary Preference"
]


def load_nutrition_dataset():
    """
    Loads the Hugging Face nutrition dataset into a pandas DataFrame.

    Returns:
        pd.DataFrame: Raw dataset
    """
    dataset = load_dataset("sarthak-wiz01/nutrition_dataset", split="train")
    return dataset.to_pandas()


def inspect_dataset(df: pd.DataFrame) -> dict:
    """
    Inspects the structure and quality of the dataset.

    Parameters:
        df (pd.DataFrame): The dataset to inspect

    Returns:
        dict: Summary including shape, nulls, dtypes, duplicates, sample
    """
    return {
        "shape": df.shape,
        "columns": df.columns.tolist(),
        "dtypes": df.dtypes.to_dict(),
        "null_values": df.isnull().sum().to_dict(),
        "duplicated_rows": int(df.duplicated().sum()),
        "sample_rows": df.head(5).to_dict(orient="records")
    }


def preview_value_distributions(df: pd.DataFrame) -> dict:
    """
    Shows unique value distributions for key categorical fields.

    Parameters:
        df (pd.DataFrame): The dataset

    Returns:
        dict: Column -> value counts dictionary for each categorical field
    """
    return {
        col: df[col].value_counts().to_dict()
        for col in CATEGORICAL_COLUMNS
        if col in df.columns
    }


def normalize_categorical_values(df: pd.DataFrame) -> pd.DataFrame:
    """
    Applies basic normalization to categorical fields: stripping spaces, title casing.

    Parameters:
        df (pd.DataFrame): The dataset

    Returns:
        pd.DataFrame: Dataset with normalized categorical fields
    """
    for col in CATEGORICAL_COLUMNS:
        if col in df.columns:
            df[col] = df[col].str.strip().str.title()
    return df


def save_raw_copy(df: pd.DataFrame, path: str = RAW_OUTPUT_PATH) -> None:
    """
    Saves a raw copy of the dataset as CSV.

    Parameters:
        df (pd.DataFrame): The dataset to save
        path (str): File path to save to
    """
    os.makedirs(os.path.dirname(path), exist_ok=True)
    df.to_csv(path, index=False)
    print(f"Raw dataset saved to: {path}")


def run():
    """
    Loads, inspects, cleans categorical values, and saves the raw nutrition dataset.
    """
    print("Loading dataset from Hugging Face...")
    df = load_nutrition_dataset()

    print("Inspecting dataset...")
    summary = inspect_dataset(df)
    for key, value in summary.items():
        print(f"\n--- {key.upper()} ---\n{value}")

    print("Value Distributions (Before Normalization)...")
    distros = preview_value_distributions(df)
    for col, counts in distros.items():
        print(f"\n{col}:")
        for val, count in counts.items():
            print(f"  - {val}: {count}")

    print("Normalizing categorical fields...")
    df = normalize_categorical_values(df)

    print("Saving raw copy...")
    save_raw_copy(df)


if __name__ == "__main__":
    run()