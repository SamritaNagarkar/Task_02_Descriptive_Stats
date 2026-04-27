import pandas as pd
import os

script_dir = os.path.dirname(os.path.abspath(__file__))
data_dir = os.path.join(script_dir, "..", "data")

files = os.listdir(data_dir)
print("Files in data folder:", files)

if not files:
    print("No dataset found in data folder.")
    raise SystemExit

data_path = os.path.join(data_dir, files[0])
print("Using file:", data_path)

df = pd.read_csv(data_path)

print("\nShape of the dataset:")
print(df.shape)

print("\nColumns in the dataset:")
print(df.columns.tolist())

print("\nData types of each column:")
print(df.dtypes)

print("\nInfo about the dataset:")
df.info()

print("\nFirst 5 rows of the dataset:")
print(df.head())

print("\nMissing values in each column:")
print(df.isnull().sum().sort_values(ascending=False).head(15))