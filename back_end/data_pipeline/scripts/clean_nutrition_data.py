# back_end/data_pipeline/scripts/clean_nutrition_data.py
import os

import pandas as pd

INPUT_PATH = "data/raw/nutrition_raw.csv"
OUTPUT_PATH = "data/processed/nutrition_cleaned.csv"

def convert_numerical_columns(df: pd.DataFrame, columns: list[str]) -> pd.DataFrame:
    """
    Converts given columns to numeric type, coercing errors.

    Args:
        df (pd.DataFrame): The dataset
        columns (list): Column names to convert

    Returns:
        pd.DataFrame: Updated dataset with numeric types
    """
    for col in columns:
        df.loc[:, col] = pd.to_numeric(df[col], errors='coerce')
    return df


def drop_invalid_headers(df: pd.DataFrame) -> pd.DataFrame:
    """
    Removes rows that repeat header labels or contain invalid placeholders.

    Returns:
        pd.DataFrame: Cleaned dataset
    """
    return df[
        (df["Gender"].str.lower() != "gender") &
        (df["Activity Level"].str.lower() != "activity level") &
        (df["Fitness Goal"].str.lower() != "fitness goal") &
        (df["Dietary Preference"].str.lower() != "dietary preference")
        ].copy()


def strip_whitespace(df: pd.DataFrame) -> pd.DataFrame:
    """
    Removes leading/trailing spaces in string columns.

    Returns:
        pd.DataFrame: Dataset with trimmed strings
    """
    for col in df.columns:
        if pd.api.types.is_object_dtype(df[col]) or pd.api.types.is_string_dtype(df[col]):
            df.loc[:, col] = df[col].astype(str).str.strip()
    return df


def normalize_categories(df: pd.DataFrame) -> pd.DataFrame:
    """
    Harmonizes categorical fields to avoid redundant classes.

    Returns:
        pd.DataFrame: Dataset with normalized categories
    """
    replacements = {
        "Fitness Goal": {
            "Weight Maintenance": "Maintenance"
        }
    }

    for col, mapping in replacements.items():
        df.loc[:, col] = df[col].replace(mapping)

    return df


def filter_outliers(df: pd.DataFrame) -> pd.DataFrame:
    """
    Removes physiologically implausible values.

    Returns:
        pd.DataFrame: Dataset without extreme outliers
    """
    return df[
        (df["Age"].between(10, 100)) &
        (df["Height"].between(100, 250)) &
        (df["Weight"].between(30, 250)) &
        (df["Daily Calorie Target"].between(800, 5000))
        ].copy()


def clean_nutrition_dataset(df: pd.DataFrame) -> pd.DataFrame:
    """
    Cleans the raw nutrition dataset for NLP training and habit tracking.

    Steps:
    - Convert numeric fields
    - Remove header errors
    - Trim whitespace
    - Normalize categories
    - Remove physiologically impossible values

    Returns:
        pd.DataFrame: Cleaned dataset
    """
    df = strip_whitespace(df)
    df = drop_invalid_headers(df)
    df = convert_numerical_columns(df, [
        "Age", "Height", "Weight", "Daily Calorie Target", "Protein", "Carbohydrates", "Fat"])
    df = normalize_categories(df)
    df = filter_outliers(df)
    return df


def run():
    df = pd.read_csv(INPUT_PATH)
    print(f"Loaded raw dataset: {df.shape}")

    cleaned = clean_nutrition_dataset(df)
    print(f"Cleaned dataset: {cleaned.shape}")

    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    cleaned.to_csv(OUTPUT_PATH, index=False)
    print(f"Cleaned dataset saved to: {OUTPUT_PATH}")


if __name__ == "__main__":
    run()