# CodeAlpha_EDA

Task 2 of the CodeAlpha Data Analytics Internship: exploratory data analysis of the
book dataset scraped in `CodeAlpha_WebScraping`.

## Questions asked first
1. How are prices and ratings distributed? Any outliers?
2. Does price relate to rating?
3. Do categories differ in price?
4. Is the rating mix the same across categories?
5. What data-quality problems need fixing?

## Method
- Structure check: shape, types, missing values, duplicates.
- Distributions and outliers: histogram + KDE, boxplot, IQR rule, skewness.
- Hypothesis tests (non-parametric, because prices are not normally distributed):
  Spearman correlation, Kruskal-Wallis (price by rating, price by category),
  chi-square test of independence (rating by category).
- Automatic data-issue detection (duplicates, sparse categories, low-variance columns).

## Run
```bash
pip install -r requirements.txt
python eda.py                # uses data/books.csv, falls back to data/sample_books.csv
```
Outputs: `outputs/eda_report.md` and 5 charts.

## Findings
Dataset: 1,000 books across 50 categories scraped from books.toscrape.com.

- Average price is £35.07 and the average rating is 2.92 out of 5.
- Every book is in stock, so the in_stock column adds no analytical value.
- Hypothesis tests (Spearman, Kruskal-Wallis, chi-square) on price vs rating, price by category and rating by category are in eda_report.md, with the charts in this repo.
