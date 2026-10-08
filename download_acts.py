import os
from datasets import load_dataset

print("Downloading dataset from Hugging Face...")

# 1. Download the dataset into your local cache
dataset = load_dataset("geekyrakshit/indian-legal-acts")

# 2. Convert the 'central' split (all Central Acts) to a pandas DataFrame
df = dataset["central"].to_pandas()

# 3. Save it to your current folder as CSV and Parquet
output_csv = "indian_central_acts.csv"
output_parquet = "indian_central_acts.parquet"

df.to_csv(output_csv, index=False)
df.to_parquet(output_parquet, index=False)

print(f"Done! Saved {len(df)} acts to:")
print(f" - {os.path.abspath(output_csv)}")
print(f" - {os.path.abspath(output_parquet)}")
