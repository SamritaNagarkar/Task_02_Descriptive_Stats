import polars as pl
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
output_path = os.path.join(results_dir, "polars_summary.txt")

# Loading dataset
df = pl.read_csv(data_path)

numeric_cols = [
    col for col, dtype in zip(df.columns, df.dtypes)
    if dtype in [pl.Int64, pl.Int32, pl.Float64, pl.Float32]
]

categorical_cols = [
    col for col in df.columns
    if col not in numeric_cols
]

# Writing output to text file
with open(output_path, "w", encoding="utf-8") as f:

    f.write("Polars Descriptive Statistics\n")
    f.write(f"Dataset file: {os.path.basename(data_path)}\n\n")

    # Dataset overview
    f.write("Dataset overview:\n")
    f.write(f"Shape: {df.shape}\n\n")

    f.write("Data Types\n")
    for col, dtype in zip(df.columns, df.dtypes):
        f.write(f"{col}: {dtype}\n")

    # Missing values
    f.write("\nMissing values\n")
    null_counts = df.null_count()

    for col in df.columns:
        count = null_counts[col][0]
        percent = (count / df.height) * 100
        f.write(f"{col}: {count} ({percent:.2f}%)\n")

    # Numeric summary
    f.write("\nNumeric Summary Statistics\n")

    if numeric_cols:
        numeric_summary = df.select(numeric_cols).describe()
        f.write(str(numeric_summary))
        f.write("\n")
    else:
        f.write("No numeric columns found.\n")

    # Categorical summary
    f.write("\nCategorical Summary Statistics\n")

    for col in categorical_cols:
        f.write(f"\nColumn: {col}\n")
        f.write(f"Count: {df.select(pl.col(col).drop_nulls().count()).item()}\n")
        f.write(f"Unique values: {df.select(pl.col(col).n_unique()).item()}\n")

        vc = df.group_by(col).len().sort("len", descending=True).head(5)

        if vc.height > 0:
            mode_value = vc[col][0]
            mode_freq = vc["len"][0]
            f.write(f"Mode: {mode_value} ({mode_freq})\n")
            f.write("Top 5 values:\n")
            f.write(str(vc))
            f.write("\n")

    # Grouped analysis by page_id
    f.write("\nGrouped Analysis by page_id\n")

    page_group_sizes = (
        df.group_by("page_id")
        .len()
        .sort("len", descending=True)
    )

    f.write(f"Number of page_id groups: {page_group_sizes.height}\n\n")
    f.write("Top 10 page_id groups by row count:\n")
    f.write(str(page_group_sizes.head(10)))
    f.write("\n\n")

    if numeric_cols:
        page_grouped_numeric = (
            df.group_by("page_id")
            .agg([
                pl.col(col).count().alias(f"{col}_count")
                for col in numeric_cols
            ] + [
                pl.col(col).mean().alias(f"{col}_mean")
                for col in numeric_cols
            ] + [
                pl.col(col).min().alias(f"{col}_min")
                for col in numeric_cols
            ] + [
                pl.col(col).max().alias(f"{col}_max")
                for col in numeric_cols
            ] + [
                pl.col(col).median().alias(f"{col}_median")
                for col in numeric_cols
            ] + [
                pl.col(col).std(ddof=0).alias(f"{col}_std")
                for col in numeric_cols
            ])
        )

        f.write("Numeric grouped summary by page_id (first 10 groups):\n")
        f.write(str(page_grouped_numeric.head(10)))
        f.write("\n")

    # Grouped analysis by page_id + ad_id
    f.write("\nGrouped Analysis by page_id + ad_id\n")

    page_ad_group_sizes = (
        df.group_by(["page_id", "ad_id"])
        .len()
        .sort("len", descending=True)
    )

    f.write(f"Number of page_id + ad_id groups: {page_ad_group_sizes.height}\n\n")
    f.write("Top 10 page_id + ad_id groups by row count:\n")
    f.write(str(page_ad_group_sizes.head(10)))
    f.write("\n\n")

    if numeric_cols:
        page_ad_grouped_numeric = (
            df.group_by(["page_id", "ad_id"])
            .agg([
                pl.col(col).count().alias(f"{col}_count")
                for col in numeric_cols
            ] + [
                pl.col(col).mean().alias(f"{col}_mean")
                for col in numeric_cols
            ] + [
                pl.col(col).min().alias(f"{col}_min")
                for col in numeric_cols
            ] + [
                pl.col(col).max().alias(f"{col}_max")
                for col in numeric_cols
            ] + [
                pl.col(col).median().alias(f"{col}_median")
                for col in numeric_cols
            ] + [
                pl.col(col).std(ddof=0).alias(f"{col}_std")
                for col in numeric_cols
            ])
        )

        f.write("Numeric grouped summary by page_id + ad_id (first 10 groups):\n")
        f.write(str(page_ad_grouped_numeric.head(10)))
        f.write("\n")


print("Polars analysis complete.")
print(f"Results saved to: {output_path}")