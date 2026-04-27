import csv
import os
import math
from collections import Counter

# Setting up paths

script_dir = os.path.dirname(os.path.abspath(__file__))
data_dir = os.path.join(script_dir, "..", "data")
results_dir = os.path.join(script_dir, "..", "results")
os.makedirs(results_dir, exist_ok=True)

data_files = [f for f in os.listdir(data_dir) if f.endswith(".csv")]
if not data_files:
    raise FileNotFoundError("No CSV file found in data/ folder.")

data_path = os.path.join(data_dir, data_files[0])
output_path = os.path.join(results_dir, "pure_python_summary.txt")

# Helper functions for data analysis
def clean_value(value):
    return value.strip()


def is_missing(value):
    return value is None or clean_value(value) == ""


def is_number(value):
    try:
        float(clean_value(value))
        return True
    except:
        return False


def infer_column_type(values):
    non_missing = [v for v in values if not is_missing(v)]

    if len(non_missing) == 0:
        return "empty"

    numeric_count = sum(1 for v in non_missing if is_number(v))

    if numeric_count / len(non_missing) >= 0.9:
        return "numeric"

    return "categorical"


def compute_numeric_stats(values):
    clean_numbers = []

    for v in values:
        if is_missing(v):
            continue
        if is_number(v):
            clean_numbers.append(float(clean_value(v)))

    if len(clean_numbers) == 0:
        return None

    clean_numbers.sort()
    n = len(clean_numbers)
    mean_val = sum(clean_numbers) / n

    if n % 2 == 0:
        median_val = (clean_numbers[n // 2 - 1] + clean_numbers[n // 2]) / 2
    else:
        median_val = clean_numbers[n // 2]

    variance = sum((x - mean_val) ** 2 for x in clean_numbers) / n
    std_dev = math.sqrt(variance)

    return {
        "count": n,
        "mean": mean_val,
        "min": min(clean_numbers),
        "max": max(clean_numbers),
        "median": median_val,
        "std_dev": std_dev
    }


def compute_categorical_stats(values):
    clean_values = [v for v in values if not is_missing(v)]

    if len(clean_values) == 0:
        return None

    counter = Counter(clean_values)
    mode_value, mode_freq = counter.most_common(1)[0]

    return {
        "count": len(clean_values),
        "unique": len(counter),
        "mode": mode_value,
        "mode_freq": mode_freq,
        "top_5": counter.most_common(5)
    }


def load_rows(file_path):
    rows = []

    with open(file_path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        columns = reader.fieldnames

        for row in reader:
            rows.append(row)

    return rows, columns


def group_rows(rows, group_keys):
    grouped = {}

    for row in rows:
        key = tuple(row[k] for k in group_keys)

        if key not in grouped:
            grouped[key] = []

        grouped[key].append(row)

    return grouped


def analyze_rows(rows, columns):
    total_rows = len(rows)
    total_columns = len(columns)

    missing_counts = {}
    column_types = {}
    numeric_results = {}
    categorical_results = {}

    for col in columns:
        values = [row[col] for row in rows]

        missing_counts[col] = sum(1 for v in values if is_missing(v))
        inferred_type = infer_column_type(values)
        column_types[col] = inferred_type

        if inferred_type == "numeric":
            numeric_results[col] = compute_numeric_stats(values)
        elif inferred_type == "categorical":
            categorical_results[col] = compute_categorical_stats(values)

    return {
        "row_count": total_rows,
        "column_count": total_columns,
        "missing_counts": missing_counts,
        "column_types": column_types,
        "numeric_results": numeric_results,
        "categorical_results": categorical_results
    }


def write_analysis_block(f, title, analysis):
    f.write(f"\n{title}\n")
    f.write("=" * len(title) + "\n")

    f.write(f"Total rows: {analysis['row_count']}\n")
    f.write(f"Total columns: {analysis['column_count']}\n\n")

    f.write("Column Type Inference:\n")
    for col, dtype in analysis["column_types"].items():
        f.write(f"{col}: {dtype}\n")

    f.write("\nMissing Values:\n")
    for col, count in analysis["missing_counts"].items():
        f.write(f"{col}: {count}\n")

    f.write("\nNumeric Columns:\n")
    for col, stats in analysis["numeric_results"].items():
        f.write(f"\n{col}\n")
        if stats is None:
            f.write("No valid numeric data\n")
            continue
        for key, value in stats.items():
            f.write(f"{key}: {value}\n")

    f.write("\nCategorical Columns:\n")
    for col, stats in analysis["categorical_results"].items():
        f.write(f"\n{col}\n")
        if stats is None:
            f.write("No valid categorical data\n")
            continue
        f.write(f"count: {stats['count']}\n")
        f.write(f"unique: {stats['unique']}\n")
        f.write(f"mode: {stats['mode']} ({stats['mode_freq']})\n")
        f.write("top 5 values:\n")
        for val, cnt in stats["top_5"]:
            f.write(f"  {val}: {cnt}\n")


# Main execution
rows, columns = load_rows(data_path)

dataset_analysis = analyze_rows(rows, columns)

grouped_by_page = group_rows(rows, ["page_id"])
grouped_by_page_ad = group_rows(rows, ["page_id", "ad_id"])

with open(output_path, "w", encoding="utf-8") as f:
    f.write("Pure python descriptive statistics\n")
    f.write(f"Dataset file: {os.path.basename(data_path)}\n")

    write_analysis_block(f, "Dataset Level Analysis", dataset_analysis)

    f.write("\nGrouped Analysis by page_id\n")
    f.write(f"Number of groups: {len(grouped_by_page)}\n\n")

    # write only first 10 groups to keep output manageable
    for idx, (group_key, group_rows_list) in enumerate(grouped_by_page.items()):
        if idx >= 10:
            f.write("\n...additional page_id groups omitted for brevity...\n")
            break

        label = f"Group page_id={group_key[0]}"
        analysis = analyze_rows(group_rows_list, columns)
        write_analysis_block(f, label, analysis)

    f.write("\nGrouped Anlaysis by page_id + ad_id\n")
    f.write(f"Number of groups: {len(grouped_by_page_ad)}\n\n")

    # write only first 10 groups to keep output manageable
    for idx, (group_key, group_rows_list) in enumerate(grouped_by_page_ad.items()):
        if idx >= 10:
            f.write("\n...additional page_id + ad_id groups omitted for brevity...\n")
            break

        label = f"Group page_id={group_key[0]}, ad_id={group_key[1]}"
        analysis = analyze_rows(group_rows_list, columns)
        write_analysis_block(f, label, analysis)

print("Pure Python analysis complete.")
print(f"Results saved to: {output_path}")