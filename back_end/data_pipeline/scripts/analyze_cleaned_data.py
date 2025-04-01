# back_end/data_pipeline/scripts/analyze_cleaned_data.py

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

CLEANED_PATH = "data/processed/nutrition_cleaned.csv"
STATS_OUTPUT_PATH = "data/processed/cleaned_stats.csv"
VISUAL_OUTPUT_DIR = "data/processed/visuals"
NLP_OUTPUT_DIR = "data/processed/nlp_analysis"

os.makedirs(VISUAL_OUTPUT_DIR, exist_ok=True)
os.makedirs(NLP_OUTPUT_DIR, exist_ok=True)

def load_cleaned_dataset(path: str = CLEANED_PATH) -> pd.DataFrame:
    return pd.read_csv(path)

def describe_numerical(df: pd.DataFrame) -> pd.DataFrame:
    return df.describe()

def analyze_unique_categories(df: pd.DataFrame) -> dict:
    return {
        col: df[col].value_counts().to_dict()
        for col in df.select_dtypes(include="object").columns
    }

def plot_distributions(df: pd.DataFrame):
    num_cols = ["Age", "Height", "Weight", "Daily Calorie Target", "Protein", "Carbohydrates", "Fat"]
    for col in num_cols:
        plt.figure()
        sns.histplot(df[col], kde=True, bins=30)
        plt.title(f"Distribution: {col}")
        plt.savefig(os.path.join(VISUAL_OUTPUT_DIR, f"{col}_hist.png"))
        plt.close()

    cat_cols = ["Gender", "Activity Level", "Fitness Goal", "Dietary Preference"]
    for col in cat_cols:
        plt.figure()
        sns.countplot(data=df, x=col, order=df[col].value_counts().index)
        plt.title(f"Frequency: {col}")
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.savefig(os.path.join(VISUAL_OUTPUT_DIR, f"{col}_count.png"))
        plt.close()

def save_stats_summary(df: pd.DataFrame):
    stats = describe_numerical(df)
    stats.to_csv(STATS_OUTPUT_PATH)
    print(f"Descriptive statistics saved to: {STATS_OUTPUT_PATH}")

def plot_correlation_matrix(df: pd.DataFrame, method="pearson"):
    plt.figure(figsize=(10, 6))
    numeric_df = df.select_dtypes(include='number')
    corr = numeric_df.corr(method=method)
    sns.heatmap(corr, annot=True, cmap="coolwarm", fmt=".2f")
    plt.title(f"{method.capitalize()} Correlation Matrix")
    plt.tight_layout()
    plt.savefig(os.path.join(VISUAL_OUTPUT_DIR, f"correlation_{method}.png"))
    plt.close()

def distribution_by_group(df: pd.DataFrame, group_col: str):
    num_cols = df.select_dtypes(include='number').columns
    for col in num_cols:
        plt.figure()
        sns.histplot(data=df, x=col, hue=group_col, kde=True, multiple="stack")
        plt.title(f"{col} Distribution by {group_col}")
        plt.tight_layout()
        plt.savefig(os.path.join(VISUAL_OUTPUT_DIR, f"{col}_by_{group_col.replace(' ', '_')}.png"))
        plt.close()

def nlp_analysis(df: pd.DataFrame):
    text_cols = ["Breakfast Suggestion", "Lunch Suggestion", "Dinner Suggestion", "Snack Suggestion"]
    for col in text_cols:
        df[f"{col}_length"] = df[col].astype(str).apply(len)
        plt.figure()
        sns.histplot(df[f"{col}_length"], bins=20, kde=True)
        plt.title(f"Text Length Distribution: {col}")
        plt.tight_layout()
        plt.savefig(os.path.join(NLP_OUTPUT_DIR, f"length_{col.replace(' ', '_')}.png"))
        plt.close()

        subset = df[col].astype(str).dropna().head(50)
        tfidf = TfidfVectorizer().fit_transform(subset)
        similarity = cosine_similarity(tfidf)

        plt.figure(figsize=(10, 8))
        sns.heatmap(similarity, cmap="YlGnBu")
        plt.title(f"TF-IDF Cosine Similarity — {col} (Top 50)")
        plt.tight_layout()
        plt.savefig(os.path.join(NLP_OUTPUT_DIR, f"similarity_{col.replace(' ', '_')}.png"))
        plt.close()

def run():
    print("Loading cleaned dataset...")
    df = load_cleaned_dataset()
    print(f"Dataset shape: {df.shape}")

    print("Generating descriptive stats...")
    save_stats_summary(df)

    print("Category distributions...")
    for col, dist in analyze_unique_categories(df).items():
        print(f"\n— {col} —")
        for k, v in dist.items():
            print(f"{k}: {v}")

    print("Saving visualizations...")
    plot_distributions(df)

    print("Correlation Analysis...")
    plot_correlation_matrix(df, method="pearson")
    plot_correlation_matrix(df, method="spearman")

    print("Distributions by Fitness Goal...")
    distribution_by_group(df, group_col="Fitness Goal")

    print("Distributions by Gender...")
    distribution_by_group(df, group_col="Gender")

    print("NLP Preparation...")
    nlp_analysis(df)

    print("Full analysis complete.")

if __name__ == "__main__":
    run()
