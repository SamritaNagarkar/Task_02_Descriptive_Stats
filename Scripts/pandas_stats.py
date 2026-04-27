import pandas as pd
import os

# Setting up paths
script_dir = os.path.dirname(os.path.abspath(__file__))
data_dir = os.path.join(script_dir, "..", "data")
results_dir = os.path.join(script_dir, "..", "results")
os.makedirs(results_dir, exist_ok=True)

data_files = [f for f in os.listdir(data_dir) if f.endswith(".csv")]
if not data_files:
    raise FileNotFoundError("No CSV file found in data/ folder.")

data_path = os.path.join(data_dir, data_files[0])
output_path = os.path.join(results_dir, "pandas_summary.txt")

# Load dataset
df = pd.read_csv(data_path)

numeric_cols = df.select_dtypes(include=["number"]).columns.tolist()
categorical_cols = df.select_dtypes(exclude=["number"]).columns.tolist()


# Helper functions for writing output
def write_section_header(f, title):
    f.write(f"\n{title}\n")
    f.write("=" * len(title) + "\n")


def write_dataset_overview(f, dataframe):
    write_section_header(f, "Dataset Overview:")
    f.write(f"Shape: {dataframe.shape}\n\n")

    f.write("Data Types:\n")
    f.write(f"{dataframe.dtypes}\n\n")

    f.write("Info:\n")
    dataframe.info(buf=f)
    f.write("\n")


def write_missing_values(f, dataframe):
    write_section_header(f, "Missing Values")
    missing_counts = dataframe.isnull().sum()
    missing_percent = (missing_counts / len(dataframe)) * 100

    for col in dataframe.columns:
        f.write(f"{col}: {missing_counts[col]} ({missing_percent[col]:.2f}%)\n")


def write_describe_sections(f, dataframe):
    write_section_header(f, "Numwric summary statistics")
    if len(dataframe.select_dtypes(include=["number"]).columns) > 0:
        f.write(f"{dataframe.describe()}\n")
    else:
        f.write("No numeric columns found.\n")

    write_section_header(f, "Categorical summary statistics")
    if len(dataframe.select_dtypes(exclude=["number"]).columns) > 0:
        f.write(f"{dataframe.describe(include=['object'])}\n")
    else:
        f.write("No categorical columns found.\n")


def write_column_level_analysis(f, dataframe):
    write_section_header(f, "Column Level Analysis")

    for col in dataframe.columns:
        f.write(f"\nColumn: {col}\n")
        f.write("-" * (8 + len(col)) + "\n")

        if pd.api.types.is_numeric_dtype(dataframe[col]):
            f.write("Type: Numeric\n")
            f.write(f"Count: {dataframe[col].count()}\n")
            f.write(f"Mean: {dataframe[col].mean()}\n")
            f.write(f"Min: {dataframe[col].min()}\n")
            f.write(f"Max: {dataframe[col].max()}\n")
            f.write(f"Median: {dataframe[col].median()}\n")
            f.write(f"Std Dev: {dataframe[col].std(ddof=0)}\n")
        else:
            vc = dataframe[col].value_counts(dropna=True)
            f.write("Type: Categorical\n")
            f.write(f"Count: {dataframe[col].count()}\n")
            f.write(f"Unique values: {dataframe[col].nunique(dropna=True)}\n")

            if len(vc) > 0:
                f.write(f"Mode: {vc.index[0]} ({vc.iloc[0]})\n")
                f.write("Top 5 values:\n")
                f.write(f"{vc.head(5)}\n")
            else:
                f.write("No non-null values available.\n")


def grouped_numeric_summary(dataframe, group_cols):
    if not numeric_cols:
        return None

    grouped = dataframe.groupby(group_cols)[numeric_cols].agg(
        ["count", "mean", "min", "max", "median", "std"]
    )

    return grouped


def grouped_group_sizes(dataframe, group_cols):
    return dataframe.groupby(group_cols).size().sort_values(ascending=False)


# WRITE OUTPUT
with open(output_path, "w", encoding="utf-8") as f:
    f.write("Pandas descriptive statistics\n")
    f.write(f"Dataset file: {os.path.basename(data_path)}\n")

    # dataset-level
    write_dataset_overview(f, df)
    write_missing_values(f, df)
    write_describe_sections(f, df)
    write_column_level_analysis(f, df)

    # grouped by page_id
    write_section_header(f, "Grouped Analysis by page_id")
    page_group_sizes = grouped_group_sizes(df, "page_id")
    f.write(f"Number of page_id groups: {page_group_sizes.shape[0]}\n\n")

    f.write("Top 10 page_id groups by row count\n")
    f.write(f"{page_group_sizes.head(10)}\n\n")

    page_numeric = grouped_numeric_summary(df, "page_id")
    if page_numeric is not None:
        f.write("Numeric grouped summary by page_id (first 10 groups)\n")
        f.write(f"{page_numeric.head(10)}\n")

    # grouped by page_id + ad_id
    write_section_header(f, "Grouped Analysis by page_id + ad_id")
    page_ad_group_sizes = grouped_group_sizes(df, ["page_id", "ad_id"])
    f.write(f"Number of page_id + ad_id groups: {page_ad_group_sizes.shape[0]}\n\n")

    f.write("Top 10 page_id + ad_id groups by row count\n")
    f.write(f"{page_ad_group_sizes.head(10)}\n\n")

    page_ad_numeric = grouped_numeric_summary(df, ["page_id", "ad_id"])
    if page_ad_numeric is not None:
        f.write("Numeric grouped summary by page_id + ad_id (first 10 groups)\n")
        f.write(f"{page_ad_numeric.head(10)}\n")

print("Pandas analysis complete.")
print(f"Results saved to: {output_path}")