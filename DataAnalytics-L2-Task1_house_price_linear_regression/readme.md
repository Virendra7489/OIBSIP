# 🏠 Predicting House Prices with Linear Regression

A beginner-friendly, well-explained machine learning project that predicts house sale prices using **Linear Regression**, with **Ridge** and **Lasso** as a bonus comparison. The notebook is written to read like a conversation: every step explains *why* it's being done, not just *what* the code does.

---

## 📌 Overview

Given a table of houses (area, location, rooms, age, quality, etc.), how well can a plain linear regression guess what each one sold for? This project walks through the full workflow, from raw data to model diagnostics, and shows how to interpret the results like a human rather than just reading a score.

**Dataset:** [Kaggle: House Prices - Advanced Regression Techniques](https://www.kaggle.com/competitions/house-prices-advanced-regression-techniques) (Ames, Iowa housing data).
If the Kaggle file isn't available, the notebook automatically generates **synthetic practice data**, so it runs out of the box.

---

## 🔍 What's Inside

1. Load the data and explore it (EDA)
2. Decide which features matter, and explain why
3. Handle missing values and encode categorical columns
4. Correlation heatmap
5. Train / test split (80/20)
6. Train a Linear Regression model
7. Evaluate with **MSE, RMSE and R²**
8. Plot actual vs. predicted values
9. Residual analysis
10. Coefficient analysis (what actually moves the price?)
11. Bonus: Ridge and Lasso regularisation

---

## 🧱 Features Used

To keep the model readable, 8 of the 80 original columns were selected and renamed:

| Feature | Original column | Meaning |
|---|---|---|
| `price` | `SalePrice` | Sale price (**target**) |
| `area` | `GrLivArea` | Above-ground living area (sq ft) |
| `location` | `Neighborhood` | Neighbourhood name |
| `rooms` | `TotRmsAbvGrd` | Total rooms above ground |
| `age` | `YrSold - YearBuilt` | Age of the house when sold |
| `quality` | `OverallQual` | Overall material/finish rating (1–10) |
| `garage` | `GarageCars` | Garage capacity (cars) |
| `basement_area` | `TotalBsmtSF` | Basement size (sq ft) |
| `lot_frontage` | `LotFrontage` | Street frontage (ft), has real missing values |

---

## ⚙️ Methodology Highlights

- **Leak-free preprocessing:** imputing, scaling and encoding live inside a scikit-learn `Pipeline`, so the test set never influences training.
- **Missing values:** numeric columns filled with the median (robust to skew); categorical with the most frequent value.
- **Encoding:** one-hot encoding for `location`, dropping one category to avoid the dummy variable trap.
- **Scaling:** numeric features are standardised so coefficients are directly comparable.
- **Evaluation:** metrics reported on both train and test sets to spot overfitting.
- **Regularisation:** `RidgeCV` and `LassoCV` choose their own penalty via cross-validation on the training set only.

---

## 📊 Evaluation Metrics

| Metric | What it tells you |
|---|---|
| **MSE** | Average squared error (punishes big misses) |
| **RMSE** | Typical prediction error, in dollars |
| **R²** | Share of price variation the model explains (1.0 = perfect) |

> Run the notebook to see the exact numbers for your data.

---

## 🚀 Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/<your-username>/<your-repo-name>.git
cd <your-repo-name>
```

### 2. Install dependencies

```bash
pip install numpy pandas matplotlib seaborn scikit-learn jupyter ipykernel kagglehub
```

### 3. Get the data (optional)

- Download `train.csv` from the [Kaggle competition page](https://www.kaggle.com/competitions/house-prices-advanced-regression-techniques) and place it in the project folder, **or**
- Let the notebook download it via `kagglehub` (requires Kaggle credentials), **or**
- Do nothing: the notebook will generate synthetic data automatically.

### 4. Run the notebook

```bash
jupyter notebook house_price_linear_regression.ipynb
```

---

## 📁 Project Structure

```
├── house_price_linear_regression.ipynb   # Main notebook
├── train.csv                             # Kaggle data (not included, add yourself)
└── README.md
```

---

## 🧠 Key Takeaways

- `quality` and `area` are the strongest drivers of price; `age` pulls it down.
- `rooms` and `area` overlap heavily (**multicollinearity**), so the `rooms` coefficient should be read with caution.
- Residual plots matter more than the headline R²: they reveal whether a straight-line model is really a good fit.
- On clean data with few features, Ridge and Lasso give only small gains. Their value grows with many or highly correlated features.

---

## 🔮 Future Improvements

- Model `log(price)` to handle skew and funnel-shaped residuals
- Add more of the 80 Ames columns and let Lasso select the useful ones
- Investigate the biggest individual prediction errors
- Try interaction terms (e.g. `area × quality`)
- Use k-fold cross-validation for a more reliable performance estimate

---

## ⚠️ Limitations

Linear regression assumes straight-line relationships, roughly constant error spread, and features that aren't too correlated. Real housing data bends all three rules, which is why the diagnostic plots are included. Coefficients show **associations, not causation**.

---

## 🛠️ Tech Stack

`Python 3.12` · `pandas` · `NumPy` · `scikit-learn` · `matplotlib` · `seaborn` · `Jupyter`

---

## 📚 References

- [scikit-learn documentation](https://scikit-learn.org/stable/)
- [Kaggle: House Prices - Advanced Regression Techniques](https://www.kaggle.com/competitions/house-prices-advanced-regression-techniques)

---

