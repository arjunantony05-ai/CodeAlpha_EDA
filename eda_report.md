# EDA Report

Dataset: `sample_books.csv`

> **Note:** this run used the synthetic sample file. Re-run on the real scraped `books.csv`.

## 1. Structure
- Rows: 659, columns: 6
- Types: title (str), category (str), price_gbp (float64), rating (int64), in_stock (bool), product_url (str)
- Missing values: 0
- Duplicate products: 0
- Categories: 16

## 2. Distributions (Q1)
- Price: mean £35.89, median £36.38, std £12.96, range £10.00-£59.99
- Price skewness: -0.12
- Price outliers (IQR rule, bounds £0.48-£71.95): 0
- Rating share: 1★ 21.4%, 2★ 20.5%, 3★ 19.4%, 4★ 18.4%, 5★ 20.3%
- In stock: 98.3%

## 3. Price vs rating (Q2)
- Spearman correlation: rho = 0.007, p = 0.857
- Kruskal-Wallis (price across rating levels): H = 3.59, p = 0.465
- **Conclusion:** no evidence that price depends on rating (fail to reject H0 at 5%).

## 4. Price by category (Q3)
- Kruskal-Wallis across 15 categories with >=10 books: H = 20.09, p = 0.127
- Cheapest median: Poetry (£30.47); priciest median: Music (£47.32)
- **Conclusion:** category price differences are not statistically significant.

## 5. Rating mix across categories (Q4)
- Chi-square test of independence: chi2 = 56.3, dof = 56, p = 0.464
- **Conclusion:** no evidence that rating mix depends on category.

## 6. Data issues found (Q5)
- 1 categories have fewer than 10 books, too small for reliable statistics
- almost every book is in stock, so `in_stock` has little analytical value