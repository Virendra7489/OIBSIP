# Messy E-Commerce Orders — Data Cleaning & Restoration Workflow

A production-grade, systematic data cleaning pipeline built to transform a deliberately messy e-commerce dataset (~1,000 transaction records) into a clean, validated, and analysis-ready format.

Every cleaning rule, missing-value strategy, and outlier adjustment is explicitly documented, justified, and audited using an automated decision log.

---

## 🛠️ Technical Stack & Tools

* **Language:** Python 3.12+
* **Libraries:** `pandas`, `numpy`, `matplotlib`
* **Environment:** Jupyter Notebook / IPython Kernel

---

## 📊 Dataset Overview (`messy_orders.csv`)

The raw dataset simulates transactional data from an Indian e-commerce platform across customer demographics, order items, pricing structures, payment gateways, and delivery statuses. It features several real-world data defects injected by design:

* **Hidden Nulls:** Standard `NaN` values mixed with textual placeholders (`?`, `-`, `N/A`, `null`, `none`).
* **Complex Duplicates:** Exact identical rows along with *near-duplicates* (same `order_id`, but varying degrees of formatting or missing fields).
* **Format Variations:** 4 distinct date formats (`2024-03-15`, `15/03/2024`, `March 15, 2024`, `15-Mar-2024`), unstripped currency symbols (`₹`, `Rs.`), thousands separators, and mixed text casing.
* **Range Anomalies:** Invalid or impossible values such as negative age (`-5`), age `999`, zero/negative quantities, and discounts exceeding 100%.
* **Extreme Outliers:** Large entry errors in quantity and pricing.

---

## ⚙️ Cleaning Pipeline Order & Logic

The sequence of cleaning steps is designed so that early operations do not mask underlying errors or corrupt later analytical logic:

| Step | Operation | Purpose |
| :--- | :--- | :--- |
| **1. Load & Data Quality Report** | Inspection & baseline snapshot | Quantify initial data defects, invalid types, placeholders, and duplicate counts. |
| **2. Standardisation** | Format & string cleanup | Convert placeholders to `NaN`, trim spaces, standardize text labels, strip currency symbols, and parse dates uniformly (Day-First). Must precede deduplication. |
| **3. Duplicate Removal** | Deduplication | Drop exact copies first. For repeated `order_id` records, retain the single copy with the fewest missing values to preserve max data. |
| **4. Missing Data Handling** | Context-aware imputation | Set impossible range values to `NaN`. Impute customer details from past orders; use domain-appropriate statistical fallbacks elsewhere. |
| **5. Outlier Detection & Capping** | IQR-based bounding | Calculate fences on complete data. Cap extreme entry errors using category-level fences; recompute mathematical fields (`total_amount`). |
| **6. Data Type Correction** | Type enforcement | Enforce final explicit dtypes (`string`, `category`, `Int64`, `float64`, `datetime64[ns]`). |
| **7. Before vs. After Summary** | Audit & verification | Evaluate identical metric tests against raw vs. cleaned data to verify 100% resolution. |
| **8. Export & Logging** | File output & validation | Save clean CSV, summary report, and decision log. Validate via re-import assertions. |

---

## 📋 Imputation & Handling Strategy Matrix

| Column | Chosen Strategy | Justification |
| :--- | :--- | :--- |
| `order_id` / `customer_id` | **Row Deletion** | Primary keys. A record without an identifier cannot be safely matched, and fabricating IDs violates data integrity. |
| `order_date` | **Forward Fill (`ffill`)** | Orders are logged sequentially; missing dates match neighboring sequential order timestamps. |
| `customer_name`, `gender`, `age`, `city` | **Cross-Record Customer Lookup** | Attributes belong to the customer, not the order. Sourcing values from repeat customer entries is far more accurate than global metrics. |
| `age` *(Fallback)* | **Median** | Robust against remaining right-skewed age values. |
| `gender`, `city`, `customer_name` *(Fallback)* | **Constant `'Unknown'`** | Mode imputation would artificially inflate the majority class and fabricate personal details. |
| `product_category`, `delivery_status` | **Constant `'Unknown'`** | Cannot be inferred from other fields; guessing would distort inventory and fulfillment analysis. |
| `payment_method` | **Mode** | Low-cardinality categorical feature dominated by UPI transactions. |
| `quantity` | **Median (Rounded)** | Discrete, skewed count metric. The median gives a realistic whole-unit order volume. |
| `unit_price` | **Category Median** | Prices vary drastically between categories (e.g., *Books* vs. *Electronics*). Global median would heavily distort values. |
| `discount_pct` | **Constant `0`** | Unrecorded discounts most plausibly represent full-price purchases ($0\%$ discount is the mode). |
| `total_amount` | **Mathematical Derivations** | Recomputed using: $\text{Quantity} \times \text{Unit Price} \times (1 - \text{Discount } \% / 100)$. |

---

## 📈 Quality Metrics: Before vs. After

| Metric | Before Cleaning | After Cleaning | Status / Improvement |
| :--- | :---: | :---: | :--- |
| **Row Count** | 1,045 | 990 | 55 invalid / duplicate records removed |
| **Missing Values (Nulls + Placeholders)** | 496 | 0 | 100% resolved / imputed |
| **Exact Duplicate Rows** | 20 | 0 | Fully deduplicated |
| **Duplicate `order_id` Entries** | 45 | 0 | Primary key uniqueness achieved |
| **Value-Range Anomalies** | 29 | 0 | Invalid entries set to NaN & imputed |
| **Columns with Correct Dtype** | 8 / 14 | 14 / 14 | 100% data type compliance |
| **Overall Dtype Accuracy** | **57.1%** | **100.0%** | Analysis-ready |

---

## 📂 Deliverables & Repository Structure

```text
.
├── messy_orders.csv            # Raw input dataset with injected defects
├── Task3_Data_Cleaning.ipynb   # Main Jupyter notebook containing cleaning logic & visualizations
├── cleaned_orders.csv          # Sanitized, production-ready dataset
├── cleaning_decision_log.csv   # Granular step-by-step audit log (actions & row counts)
├── before_after_summary.csv    # Summary comparative metrics table
└── README.md                   # Repository documentation
```

---

## 🚀 How to Run



1. **Install required packages:**
   ```bash
   pip install pandas numpy matplotlib jupyter
   ```

2. **Launch the notebook:**
   ```bash
   jupyter notebook Task3_Data_Cleaning.ipynb
   ```
```

I have updated the document with a human-styled `README.md` file tailored specifically to your data cleaning pipeline, including step explanations, baseline comparison tables, and full project context.