"""CodeAlpha Data Analytics Internship - Task 2: Exploratory Data Analysis

Dataset: books scraped from books.toscrape.com (output of CodeAlpha_WebScraping).

Questions asked before looking at the data
  Q1. How are prices and ratings distributed? Any outliers?
  Q2. Does price relate to rating? (are better-rated books pricier?)
  Q3. Do categories differ in price?
  Q4. Is the rating mix the same across categories?
  Q5. What data-quality problems need fixing?

Usage:
    python eda.py                     # uses data/books.csv, else data/sample_books.csv
    python eda.py path/to/books.csv
"""
import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from scipy import stats

BASE = Path(__file__).parent
OUT = BASE / "outputs"
OUT.mkdir(exist_ok=True)
sns.set_theme(style="whitegrid")
BLUE = "#457b9d"
report = []


def say(line=""):
    report.append(line)
    print(line)


def save(fig, name):
    fig.tight_layout()
    fig.savefig(OUT / name, dpi=150)
    plt.close(fig)


# ---------------------------------------------------------------- load ---
arg = Path(sys.argv[1]) if len(sys.argv) > 1 else None
path = arg or next(p for p in [BASE / "data" / "books.csv", BASE / "data" / "sample_books.csv"] if p.exists())
df = pd.read_csv(path)
say(f"# EDA Report\n\nDataset: `{path.name}`\n")
if "sample" in path.name:
    say("> **Note:** this run used the synthetic sample file. Re-run on the real scraped `books.csv`.\n")

# ----------------------------------------------------------- structure ---
say("## 1. Structure")
say(f"- Rows: {len(df)}, columns: {df.shape[1]}")
say("- Types: " + ", ".join(f"{c} ({t})" for c, t in df.dtypes.astype(str).items()))
missing = df.isna().sum()
say(f"- Missing values: {int(missing.sum())}" + (f" ({missing[missing > 0].to_dict()})" if missing.sum() else ""))
dups = int(df.duplicated(subset="product_url").sum())
say(f"- Duplicate products: {dups}")
say(f"- Categories: {df['category'].nunique()}")

# ---------------------------------------------------------- univariate ---
say("\n## 2. Distributions (Q1)")
p = df["price_gbp"]
say(f"- Price: mean £{p.mean():.2f}, median £{p.median():.2f}, std £{p.std():.2f}, range £{p.min():.2f}-£{p.max():.2f}")
say(f"- Price skewness: {p.skew():.2f}")
q1, q3 = p.quantile([0.25, 0.75])
lo, hi = q1 - 1.5 * (q3 - q1), q3 + 1.5 * (q3 - q1)
n_out = int(((p < lo) | (p > hi)).sum())
say(f"- Price outliers (IQR rule, bounds £{lo:.2f}-£{hi:.2f}): {n_out}")
rc = df["rating"].value_counts(normalize=True).sort_index().mul(100).round(1)
say("- Rating share: " + ", ".join(f"{k}★ {v}%" for k, v in rc.items()))
say(f"- In stock: {df['in_stock'].mean():.1%}")

fig, axes = plt.subplots(1, 3, figsize=(15, 4))
sns.histplot(p, bins=25, kde=True, color=BLUE, ax=axes[0]).set(title="Price distribution (£)", xlabel="Price")
sns.countplot(x=df["rating"], color=BLUE, ax=axes[1]).set(title="Rating counts", xlabel="Stars")
sns.boxplot(x=p, color="#a8dadc", ax=axes[2]).set(title="Price boxplot (outlier check)", xlabel="Price")
save(fig, "1_distributions.png")

top = df["category"].value_counts()
fig, ax = plt.subplots(figsize=(7, 5))
top.head(12)[::-1].plot.barh(color=BLUE, ax=ax)
ax.set(title="Books per category (top 12)", xlabel="Books")
save(fig, "2_category_counts.png")

# --------------------------------------------------------- relationships --
say("\n## 3. Price vs rating (Q2)")
rho, pv = stats.spearmanr(df["price_gbp"], df["rating"])
say(f"- Spearman correlation: rho = {rho:.3f}, p = {pv:.3f}")
groups = [g["price_gbp"].values for _, g in df.groupby("rating")]
h, pk = stats.kruskal(*groups)
say(f"- Kruskal-Wallis (price across rating levels): H = {h:.2f}, p = {pk:.3f}")
say("- **Conclusion:** " + ("price differs by rating." if pk < 0.05 else
    "no evidence that price depends on rating (fail to reject H0 at 5%)."))

fig, ax = plt.subplots(figsize=(7, 4))
sns.boxplot(data=df, x="rating", y="price_gbp", color="#a8dadc", ax=ax).set(title="Price by rating", xlabel="Stars", ylabel="Price (£)")
save(fig, "3_price_by_rating.png")

say("\n## 4. Price by category (Q3)")
big = top[top >= 10].index
sub = df[df["category"].isin(big)]
h2, pk2 = stats.kruskal(*[g["price_gbp"].values for _, g in sub.groupby("category")])
say(f"- Kruskal-Wallis across {len(big)} categories with >=10 books: H = {h2:.2f}, p = {pk2:.3f}")
med = sub.groupby("category")["price_gbp"].median().sort_values()
say(f"- Cheapest median: {med.index[0]} (£{med.iloc[0]:.2f}); priciest median: {med.index[-1]} (£{med.iloc[-1]:.2f})")
say("- **Conclusion:** " + ("category prices differ significantly." if pk2 < 0.05 else
    "category price differences are not statistically significant."))

order = med.index[::-1]
fig, ax = plt.subplots(figsize=(8, 6))
sns.boxplot(data=sub, y="category", x="price_gbp", order=order, color="#a8dadc", ax=ax).set(title="Price by category", xlabel="Price (£)", ylabel="")
save(fig, "4_price_by_category.png")

say("\n## 5. Rating mix across categories (Q4)")
ct = pd.crosstab(sub["category"], sub["rating"])
chi2, pc, dof, _ = stats.chi2_contingency(ct)
say(f"- Chi-square test of independence: chi2 = {chi2:.1f}, dof = {dof}, p = {pc:.3f}")
say("- **Conclusion:** " + ("rating mix depends on category." if pc < 0.05 else "no evidence that rating mix depends on category."))
fig, ax = plt.subplots(figsize=(7, 6))
sns.heatmap(ct.div(ct.sum(axis=1), axis=0), annot=True, fmt=".0%", cmap="Blues", ax=ax).set(title="Rating share within category", xlabel="Stars", ylabel="")
save(fig, "5_rating_by_category_heatmap.png")

# ------------------------------------------------------------- quality ---
say("\n## 6. Data issues found (Q5)")
issues = []
if dups:
    issues.append(f"{dups} duplicate products to drop")
if missing.sum():
    issues.append(f"{int(missing.sum())} missing values")
if n_out:
    issues.append(f"{n_out} price outliers to review (possibly legitimate premium titles)")
small = int((top < 10).sum())
if small:
    issues.append(f"{small} categories have fewer than 10 books, too small for reliable statistics")
if df["in_stock"].mean() > 0.97:
    issues.append("almost every book is in stock, so `in_stock` has little analytical value")
if p.skew() > 0.5:
    issues.append("prices are right-skewed; consider a log transform for modelling")
for i in issues or ["none detected"]:
    say(f"- {i}")

(OUT / "eda_report.md").write_text("\n".join(report), encoding="utf-8")
print(f"\nSaved report and charts to {OUT}")
