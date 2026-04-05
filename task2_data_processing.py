# task2_data_processing.py

import pandas as pd
import os
import glob

# Step 1: find latest JSON file inside data folder
files = glob.glob("data/trends_*.json")

if not files:
    print("No JSON file found in data folder")
    exit()

latest_file = max(files, key=os.path.getctime)

# Load JSON into DataFrame
df = pd.read_json(latest_file)

print(f"Loaded {len(df)} stories from {latest_file}")

# ---------------- CLEANING ---------------- #

# 1. Remove duplicates based on post_id
df = df.drop_duplicates(subset="post_id")
print(f"After removing duplicates: {len(df)}")

# 2. Remove missing values (important fields)
df = df.dropna(subset=["post_id", "title", "score"])
print(f"After removing nulls: {len(df)}")

# 3. Fix data types
df["score"] = df["score"].astype(int)
df["num_comments"] = df["num_comments"].astype(int)

# 4. Remove low-quality stories (score < 5)
df = df[df["score"] >= 5]
print(f"After removing low scores: {len(df)}")

# 5. Remove extra spaces in title
df["title"] = df["title"].str.strip()

# ---------------- SAVE CSV ---------------- #

# ensure data folder exists
if not os.path.exists("data"):
    os.makedirs("data")

output_file = "data/trends_clean.csv"

df.to_csv(output_file, index=False)

print(f"\nSaved {len(df)} rows to {output_file}")

# ---------------- SUMMARY ---------------- #

print("\nStories per category:")
print(df["category"].value_counts())
