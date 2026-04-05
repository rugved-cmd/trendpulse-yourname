# task4_visualization.py

import pandas as pd
import matplotlib.pyplot as plt
import os

# ---------------- LOAD DATA ---------------- #

file_path = "data/trends_analysed.csv"

if not os.path.exists(file_path):
    print("File not found. Run Task 3 first.")
    exit()

df = pd.read_csv(file_path)

# create outputs folder
if not os.path.exists("outputs"):
    os.makedirs("outputs")

# ---------------- CHART 1: TOP 10 STORIES ---------------- #

# sort by score and take top 10
top10 = df.sort_values(by="score", ascending=False).head(10)

# shorten long titles
top10["short_title"] = top10["title"].apply(lambda x: x[:50] + "..." if len(x) > 50 else x)

plt.figure()
plt.barh(top10["short_title"], top10["score"])
plt.xlabel("Score")
plt.ylabel("Title")
plt.title("Top 10 Stories by Score")
plt.gca().invert_yaxis()

plt.savefig("outputs/chart1_top_stories.png")
plt.close()

# ---------------- CHART 2: STORIES PER CATEGORY ---------------- #

category_counts = df["category"].value_counts()

plt.figure()
plt.bar(category_counts.index, category_counts.values)
plt.xlabel("Category")
plt.ylabel("Number of Stories")
plt.title("Stories per Category")

plt.savefig("outputs/chart2_categories.png")
plt.close()

# ---------------- CHART 3: SCATTER ---------------- #

plt.figure()

# separate popular and non-popular
popular = df[df["is_popular"] == True]
not_popular = df[df["is_popular"] == False]

plt.scatter(popular["score"], popular["num_comments"], label="Popular")
plt.scatter(not_popular["score"], not_popular["num_comments"], label="Not Popular")

plt.xlabel("Score")
plt.ylabel("Number of Comments")
plt.title("Score vs Comments")
plt.legend()

plt.savefig("outputs/chart3_scatter.png")
plt.close()

# ---------------- DASHBOARD ---------------- #

fig, axes = plt.subplots(1, 3, figsize=(18, 5))

# chart 1 in dashboard
axes[0].barh(top10["short_title"], top10["score"])
axes[0].set_title("Top Stories")
axes[0].invert_yaxis()

# chart 2 in dashboard
axes[1].bar(category_counts.index, category_counts.values)
axes[1].set_title("Categories")

# chart 3 in dashboard
axes[2].scatter(popular["score"], popular["num_comments"], label="Popular")
axes[2].scatter(not_popular["score"], not_popular["num_comments"], label="Not Popular")
axes[2].set_title("Score vs Comments")
axes[2].legend()

fig.suptitle("TrendPulse Dashboard")

plt.savefig("outputs/dashboard.png")
plt.close()

print("Saved: outputs/chart1_top_stories.png")
print("Saved: outputs/chart2_categories.png")
print("Saved: outputs/chart3_scatter.png")
print("Saved: outputs/dashboard.png")