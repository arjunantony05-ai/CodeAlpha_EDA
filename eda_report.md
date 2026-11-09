# EDA Report

Dataset: `books.csv`

## 1. Structure
- Rows: 1000, columns: 6
- Types: title (str), category (str), price_gbp (float64), rating (int64), in_stock (bool), product_url (str)
- Missing values: 0
- Duplicate products: 0
- Categories: 50

## 2. Distributions (Q1)
- Price: mean £35.07, median £35.98, std £14.45, range £10.00-£59.99
- Price skewness: -0.04
- Price outliers (IQR rule, bounds £-15.92-£85.48): 0
- Rating share: 1★ 22.6%, 2★ 19.6%, 3★ 20.3%, 4★ 17.9%, 5★ 19.6%
- In stock: 100.0%

## 3. Price vs rating (Q2)
- Spearman correlation: rho = 0.029, p = 0.356
- Kruskal-Wallis (price across rating levels): H = 1.56, p = 0.815
- **Conclusion:** no evidence that price depends on rating (fail to reject H0 at 5%).

## 4. Price by category (Q3)
- Kruskal-Wallis across 25 categories with >=10 books: H = 15.06, p = 0.919
- Cheapest median: Mystery (£25.38); priciest median: Womens Fiction (£43.58)
- **Conclusion:** category price differences are not statistically significant.

## 5. Rating mix across categories (Q4)
- Chi-square test of independence: chi2 = 92.5, dof = 96, p = 0.583
- **Conclusion:** no evidence that rating mix depends on category.

## 6. Data issues found (Q5)
- 25 categories have fewer than 10 books, too small for reliable statistics
- almost every book is in stock, so `in_stock` has little analytical value