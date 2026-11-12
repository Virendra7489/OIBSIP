# Retail Sales: Exploratory Data Analysis

A store records every sale it makes, but a raw table of 1,000 transactions doesn't tell you much on its own. I wanted to turn it into answers a store manager could actually use: **when** do we sell the most, **who** is buying, and **what** really brings in the money?

This is one of my data analytics portfolio projects. I built it in a Jupyter Notebook with Python, pandas, matplotlib and seaborn.

---

## What I wanted to find out

1. When are sales strongest and weakest (by month, quarter and weekday)?
2. Who are the customers (age and gender)?
3. Which products and categories sell the most, and which earn the most?
4. Which numbers move together?
5. Is anything hiding in the data that isn't obvious at first glance?

---

## The dataset

- **Source:** Retail Sales Dataset from Kaggle
- **Size:** 1,000 transactions, 9 columns, from 1 Jan 2023 to 1 Jan 2024
- **Columns:** Transaction ID, Date, Customer ID, Gender, Age, Product Category, Quantity, Price per Unit, Total Amount
- **Data quality:** no missing values, no duplicates, and `Total Amount` matches `Quantity × Price per Unit` in all 1,000 rows

The CSV isn't in this repo. Download it from Kaggle and place `retail_sales_dataset.csv` in the project folder.

---

## What I found

**Spending is uneven.** The average sale is 456, but the median is only 135. A minority of big purchases pull the average up, and most of that comes from *what* people buy (unit price), not *how many* they buy. Nearly everyone buys 1 to 4 units.

**Sales swing through the year.** May was the strongest month (53,150) and September the weakest (23,620). October then jumped by about 97% over September, and Q4 was the best quarter overall.

**Customers are evenly spread.** Ages run from 18 to 64 with no single dominant age. The gender split is 51% female and 49% male, and both spend about the same per transaction (455 to 457).

**The three categories are close.** Electronics earns the most (34.4% of revenue), then Clothing (34.1%) and Beauty (31.5%). Clothing has the most orders, but that doesn't make it the revenue leader.

**Most units sold is not the same as most money earned.** Clothing at a unit price of 300 sold the most units, but Electronics at 500 earned the most revenue.

**Premium items carry the business.** Items priced above the median are only 40% of transactions but bring in **88% of revenue**. This was the most surprising finding for me.

**Age alone tells you very little.** Age and spend have almost no correlation (r = -0.06). But when I split age group by category, real differences appear. For example, 35-44 year-olds spend about 577 per Beauty purchase, while 55+ spend about 333.

**Weekends win.** Saturday is the best day (78,815) and Thursday the quietest (53,835), a gap of about 46%.

---

## What I'd recommend

1. **Plan stock and staffing around the swings.** May is about 1.4x an average month and September only 0.6x. Prepare ahead of the peak and use the slow month for planned promotions.
2. **Protect the premium segment.** It earns 88% of revenue from 40% of sales, so keep those items well stocked and use bundles and upsells instead of discounts.
3. **Target by age and category together,** not by age alone.
4. **Put extra staff and promotions on Saturdays.**

---

## What's inside the notebook

| Step | What I did |
|------|-----------|
| Inspection | Shape, data types, nulls, duplicates, and a revenue integrity check |
| Descriptive stats | Mean, median, mode and standard deviation |
| Time series | Monthly and quarterly sales trends (line charts) |
| Customers | Age distribution, age groups and gender split |
| Products | Top 10 products and revenue by category |
| Correlation | Heatmap of the numerical variables |
| Extra digging | Age group × category spend, and premium share of sales vs revenue |
| Bonus | Revenue by day of the week |
| Conclusion | Recommendations and limitations |

Every chart has a written observation under it, so the notebook reads like a story and not just a pile of plots.

---

## Honest limitations

- **About one year of data.** I can see swings, but can't prove they are seasonal. That would need at least two years. (The single day in January 2024 is left out of the trend charts so it doesn't look like a fake crash.)
- **No product names.** I treated a "product" as a category at a price point, for example *Clothing @ 300*.
- **No cost data,** so this is about revenue, not profit.
- **Small groups.** Splitting 1,000 transactions by age group and category leaves only about 60 to 80 per group, so those differences are hints and not proof.
- **One purchase per customer,** so repeat buying and customer lifetime value can't be studied.

---

## How to run it

```bash
pip install pandas numpy matplotlib seaborn jupyter

# add retail_sales_dataset.csv to this folder, then:
jupyter notebook Retail_Sales_EDA.ipynb
```

Then choose **Kernel → Restart & Run All**.

---

## Tech stack

Python · pandas · NumPy · matplotlib · seaborn · Jupyter Notebook

---

## What I'd do next

- Add cost data and analyse profit, not just revenue
- Build a Power BI dashboard from the same data
- Check whether the premium-share finding holds on a second retail dataset

---

## About me

I'm **Virendra Malviya**, a BCA student from Indore, learning data analytics (SQL, Python, Excel and Power BI) and looking for data analyst roles. I'm building a portfolio of small, honest projects like this one.

If something in my analysis looks off, I'd love to hear about it. Feel free to open an issue.

- GitHub: [virendra7489](https://github.com/virendra7489)