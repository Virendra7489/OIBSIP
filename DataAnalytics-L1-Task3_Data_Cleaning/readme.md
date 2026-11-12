# Cleaning a Messy Dataset with Pandas

Real-world data is rarely tidy, and cleaning it is where most of an analyst's time actually goes. For this project I took a deliberately messy e-commerce orders file and cleaned it step by step, writing down **why** I made every decision, not just what I did.

The result is a notebook you can read top to bottom like a story: what was wrong, what I chose to do about it, and proof that it worked.

---

## The dataset

`messy_orders.csv` has about 1,000 online orders (customer, city, product, price, payment method, delivery status and so on).

One honest note: I couldn't pull a dataset from Kaggle for this, so I wrote a small script (`generate_messy_data.py`) that builds one and **breaks it on purpose** in the ways real data usually breaks. It uses a fixed seed, so you get the exact same mess every time you run it. The problems I planted:

- Missing values, both real blanks and sneaky placeholders like `?`, `-` and `N/A`
- Exact duplicate rows, plus "near" duplicates (same order ID, slightly different copies)
- The same thing written many ways (`M`, `male`, `MALE`, ` Male`; `Bengaluru` vs `Bangalore`; `COD` vs `Cash on Delivery`)
- Four different date formats in one column
- Prices stored as text like `₹1,299.00` or `Rs. 1299`
- Impossible values (age 999, negative quantity, a 150% discount)
- Extreme outliers (someone "ordering" 999 items, prices with an extra digit)

If you want to try it on a real Kaggle dataset (Titanic, Housing, etc.), the structure of the notebook carries over, but the column-specific cells will need adjusting.

## What I did

I followed this order on purpose, because the order matters:

1. **Data quality report**: counted nulls, placeholders, duplicates, type problems and impossible values before touching anything.
2. **Standardisation**: turned placeholders into real `NaN`, unified labels, converted text prices to numbers, and parsed all four date formats.
3. **Duplicates**: removed exact copies, then handled repeated order IDs by keeping the copy with the most complete information.
4. **Missing data**: picked a different strategy per column and explained each one in the notebook.
5. **Outliers**: IQR method, with Z-score alongside for comparison. Decided column by column whether to cap or keep.
6. **Data types**: IDs as strings, labels as categories, counts as integers, dates as datetime.
7. **Before vs. after**: one summary table to show the difference.
8. **Save**: cleaned CSV, plus a log of every action.

## Decisions I'm proudest of

A few choices where I stopped and thought rather than just calling `.fillna(mean)`:

- **Standardise before deduplicating.** Some duplicates only looked different because of formatting (`male` vs `Male`). Cleaning first revealed more of them.
- **Fill customer details from the customer's other orders.** If someone's age is missing in one row but present in their other orders, that's a much better answer than a column-wide median.
- **Median price per product category.** A global average would give a book a phone's price.
- **Outliers checked within each category.** Across the whole dataset, the IQR rule flagged 191 prices as outliers, but most were just normal electronics. Checked per category, only 11 were genuine errors.
- **"Unknown" instead of guessing.** For things like gender or delivery status, inventing a value would quietly distort later analysis.
- **Day-first dates.** `05/04/2024` is ambiguous, so I parse with explicit formats rather than letting pandas guess month-first.
- **Total amount is recalculated, not imputed.** It's a formula of other columns, so calculating it beats estimating it.

## Results

| Metric | Before | After |
|---|---|---|
| Rows | 1,045 | 990 |
| Missing values (nulls + placeholders) | 496 | 0 |
| Exact duplicate rows | 20 | 0 |
| Repeated order IDs | 45 | 0 |
| Impossible values | 29 | 0 |
| Columns with the correct dtype | 8 / 14 | 14 / 14 |

The 55 rows removed are 45 duplicates and 10 rows with no customer ID at all (a row you can't identify isn't worth keeping). The notebook finishes by reloading the saved file and asserting that it has no nulls, no duplicates and no impossible values.

## Files

```
├── Task3_Data_Cleaning.ipynb    # the main notebook, with explanations
├── generate_messy_data.py       # builds the messy dataset (seed = 42)
├── messy_orders.csv             # raw input
├── cleaned_orders.csv           # final output
├── cleaning_decision_log.csv    # every cleaning action and how many rows it touched
└── before_after_summary.csv     # the comparison table above
```

## Run it yourself

```bash
pip install pandas numpy matplotlib jupyter
python generate_messy_data.py      # optional, messy_orders.csv is already included
jupyter notebook Task3_Data_Cleaning.ipynb
```

Then run all the cells. It reads `messy_orders.csv` from the same folder.

## Tech stack

Python · pandas · NumPy · Matplotlib · Jupyter Notebook

## Things I'd do differently on real data

- Confirm the day-first date assumption with whoever owns the data instead of assuming.
- Imputing with medians shrinks variance a little, so I'd flag imputed rows with an indicator column if the data were going into a model.
- Report the "Unknown" groups alongside any category analysis so they don't get ignored.

## What I learned

Cleaning isn't about making every cell "look right". It's about making choices you can defend. Writing the reasoning next to the code made me catch things I'd have missed otherwise, like duplicates hiding behind capitalisation and "outliers" that were just expensive products.

---

Built by [Virendra Malviya](https://github.com/virendra7489) as part of my data analytics portfolio. Feedback and suggestions are welcome.