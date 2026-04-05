# task3_analysis.py

import pandas as pd
import numpy as np
import os

# ---------------- LOAD DATA ---------------- #

file_path = "data/trends_clean.csv"

if not os.path.exists(file_path):
    print("CSV file not found. Run Task 2 first.")
    exit()

df = pd.read_csv(file_path)

print(f"Loaded data: {df.shape}")

# print first 5 rows
print("\nFirst 5 rows:")
print(df.head())

# ---------------- BASIC STATS ---------------- #

avg_score = df["score"].mean()
avg_comments = df["num_comments"].mean()

print(f"\nAverage score   : {avg_score:.2f}")
print(f"Average comments: {avg_comments:.2f}")

# ---------------- NUMPY ANALYSIS ---------------- #

scores = df["score"].to_numpy()

print("\n--- NumPy Stats ---")

# mean, median, std
print("Mean score   :", np.mean(scores))
print("Median score :", np.median(scores))
print("Std deviation:", np.std(scores))

# max and min
print("Max score    :", np.max(scores))
print("Min score    :", np.min(scores))

# category with most stories
category_counts = df["category"].value_counts()
top_category = category_counts.idxmax()
print(f"\nMost stories in: {top_category} ({category_counts.max()} stories)")

# most commented story
max_comments_row = df.loc[df["num_comments"].idxmax()]
print(f"\nMost commented story: \"{max_comments_row['title']}\" — {max_comments_row['num_comments']} comments")

# ---------------- ADD NEW COLUMNS ---------------- #

# engagement = num_comments / (score + 1)
df["engagement"] = df["num_comments"] / (df["score"] + 1)

# is_popular = score > average score
df["is_popular"] = df["score"] > avg_score

# ---------------- SAVE FILE ---------------- #

output_path = "data/trends_analysed.csv"
df.to_csv(output_path, index=False)

print(f"\nSaved to {output_path}")

