"""Generate a deliberately messy e-commerce orders dataset (reproducible, seed=42).

Injected defects: missing values (NaN + placeholder tokens), exact + near duplicates,
inconsistent casing/spelling/labels, mixed date formats, currency symbols in numbers,
impossible values (negative qty, age 999, discount 150%), and extreme outliers.
"""
import numpy as np
import pandas as pd

rng = np.random.default_rng(42)
N, N_CUST = 1000, 300

first = ["Aarav","Vivaan","Aditya","Rohan","Karan","Neha","Priya","Anjali","Sneha","Pooja",
         "Rahul","Amit","Sanjay","Kavya","Isha","Manish","Deepak","Ritu","Simran","Vikram"]
last = ["Sharma","Verma","Malviya","Patel","Gupta","Joshi","Singh","Jain","Mishra","Yadav"]
cities = ["Indore","Bhopal","Mumbai","Delhi","Bangalore","Pune"]
cats = {"Electronics":8000,"Clothing":900,"Home & Kitchen":1800,"Books":350,"Beauty":650,"Sports":2200}

cust = pd.DataFrame({
    "customer_id": np.arange(1001, 1001 + N_CUST),
    "customer_name": [f"{rng.choice(first)} {rng.choice(last)}" for _ in range(N_CUST)],
    "gender": rng.choice(["Male","Female"], N_CUST, p=[.52,.48]),
    "age": np.clip(rng.normal(34, 10, N_CUST).round(), 19, 70).astype(int),
    "city": rng.choice(cities, N_CUST, p=[.3,.2,.15,.15,.12,.08]),
})

o = pd.DataFrame({"order_id": [f"ORD-{i:05d}" for i in range(1, N + 1)],
                  "customer_id": rng.choice(cust.customer_id, N)})
o = o.merge(cust, on="customer_id", how="left")
o["order_date"] = pd.Timestamp("2024-01-01") + pd.to_timedelta(np.sort(rng.integers(0, 365, N)), unit="D")
o["product_category"] = rng.choice(list(cats), N, p=[.2,.25,.2,.12,.13,.10])
o["unit_price"] = (o.product_category.map(cats) * rng.uniform(.6, 1.5, N)).round(0)
o["quantity"] = rng.choice([1,2,3,4,5], N, p=[.4,.25,.15,.12,.08])
o["discount_pct"] = rng.choice([0,5,10,15,20,25], N, p=[.35,.2,.15,.15,.1,.05])
o["payment_method"] = rng.choice(["UPI","Credit Card","Debit Card","Cash on Delivery","Net Banking"], N, p=[.4,.2,.15,.15,.1])
o["delivery_status"] = rng.choice(["Delivered","Shipped","Pending","Cancelled","Returned"], N, p=[.7,.1,.08,.07,.05])

# --- extreme outliers (kept consistent with total) ---
idx = rng.choice(N, 8, replace=False);  o.loc[idx, "quantity"] = rng.choice([250, 300, 500, 999], 8)
idx = rng.choice(N, 10, replace=False); o.loc[idx, "unit_price"] *= 12
o["total_amount"] = (o.quantity * o.unit_price * (1 - o.discount_pct / 100)).round(2)

# --- impossible values ---
o["age"] = o["age"].astype(object)
idx = rng.choice(N, 12, replace=False); o.loc[idx, "age"] = rng.choice([-5, 0, 150, 999], 12)
idx = rng.choice(N, 6, replace=False);  o.loc[idx, "quantity"] = rng.choice([-1, -2, 0], 6)
idx = rng.choice(N, 7, replace=False);  o.loc[idx, "discount_pct"] = rng.choice([150, -10], 7)
idx = rng.choice(N, 4, replace=False);  o.loc[idx, "unit_price"] = -o.loc[idx, "unit_price"].abs()

# --- near duplicates (same order_id, will be messed up independently) ---
o = pd.concat([o, o.sample(25, random_state=1)], ignore_index=True)

# --- inconsistent formatting ---
def vary(s, mapping):
    out = []
    for v in s:
        opts = mapping.get(v, [v])
        w = [1.0] if len(opts) == 1 else [.55] + [.45 / (len(opts) - 1)] * (len(opts) - 1)
        out.append(str(rng.choice(opts, p=w)))
    return pd.Series(out, index=s.index)

o["gender"] = vary(o.gender, {"Male": ["Male","male","M","m","MALE"," Male"], "Female": ["Female","female","F","f","FEMALE","Female "]})
o["city"] = vary(o.city, {"Indore": ["Indore","indore","INDORE","Indore "], "Delhi": ["Delhi","New Delhi","delhi"],
                          "Bangalore": ["Bangalore","Bengaluru","bangalore"], "Bhopal": ["Bhopal","bhopal"],
                          "Mumbai": ["Mumbai","mumbai","MUMBAI"], "Pune": ["Pune","pune"]})
o["product_category"] = vary(o.product_category, {"Electronics": ["Electronics","electronics","ELECTRONICS"],
    "Clothing": ["Clothing","clothing","Clothes"], "Home & Kitchen": ["Home & Kitchen","Home&Kitchen","home and kitchen"],
    "Books": ["Books","books"], "Beauty": ["Beauty","beauty "], "Sports": ["Sports","sports","SPORTS"]})
o["payment_method"] = vary(o.payment_method, {"UPI": ["UPI","upi","Upi"], "Credit Card": ["Credit Card","credit card","CC"],
    "Debit Card": ["Debit Card","debit card"], "Net Banking": ["Net Banking","net banking"],
    "Cash on Delivery": ["Cash on Delivery","COD","cod"]})
o["delivery_status"] = vary(o.delivery_status, {k: [k, k.lower(), k.upper()] for k in
    ["Delivered","Shipped","Pending","Cancelled","Returned"]})
o["customer_name"] = [rng.choice([n, n.upper(), n.lower(), f"  {n} ", n.replace(" ", "  ")]) for n in o.customer_name]

fmts = ["%Y-%m-%d", "%d/%m/%Y", "%B %d, %Y", "%d-%b-%Y"]
o["order_date"] = [d.strftime(fmts[rng.integers(0, 4)]) for d in o.order_date]

def fmt_price(v):
    r = rng.random()
    if r < .50: return f"{v:.2f}"
    if r < .70: return f"₹{v:,.2f}"
    if r < .85: return f"Rs. {v:,.0f}"
    return f"{v:,.0f}"
o["unit_price"] = o.unit_price.map(fmt_price)
o["total_amount"] = o.total_amount.map(lambda v: f"{v:.2f}" if rng.random() < .8 else f"₹{v:,.2f}")
o["age"] = [f"{a} yrs" if (isinstance(a, (int, np.integer)) and rng.random() < .08) else a for a in o.age]

# --- missing values (real NaN + placeholder tokens) ---
tokens = ["N/A", "?", "-", "", "NA"]
rates = {"customer_id": .01, "customer_name": .02, "gender": .05, "age": .08, "city": .04, "order_date": .02,
         "product_category": .02, "unit_price": .05, "quantity": .03, "discount_pct": .06,
         "total_amount": .04, "payment_method": .04, "delivery_status": .02}
o = o.astype(object)
for col, r in rates.items():
    rows = rng.choice(len(o), int(len(o) * r), replace=False)
    o.loc[o.index[rows], col] = [rng.choice(tokens) if rng.random() < .6 else np.nan for _ in rows]

# --- exact duplicates + shuffle ---
o = pd.concat([o, o.sample(20, random_state=2)], ignore_index=True)
o = o.sample(frac=1, random_state=3).reset_index(drop=True)
o.to_csv("messy_orders.csv", index=False, encoding="utf-8")
print(o.shape)
