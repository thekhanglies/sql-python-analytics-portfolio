"""
Olist Brazilian E-Commerce — Python Visualization Layer
Extends the SQL portfolio analysis with pandas + matplotlib/seaborn charts.

Author: Crez
"""

import os
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import seaborn as sns

DATA_DIR = r"C:\Users\khang\OneDrive\Documents\Kaggle Datasets"
OUT_DIR = r"C:\Users\khang\OneDrive\Desktop\olist_charts"
os.makedirs(OUT_DIR, exist_ok=True)

sns.set_theme(style="whitegrid", palette="deep")
plt.rcParams["figure.dpi"] = 120
plt.rcParams["savefig.bbox"] = "tight"

# ---------------------------------------------------------------------------
# 1. LOAD
# ---------------------------------------------------------------------------
orders = pd.read_csv(f"{DATA_DIR}/olist_orders_dataset.csv",
                      parse_dates=["order_purchase_timestamp", "order_approved_at",
                                   "order_delivered_carrier_date", "order_delivered_customer_date",
                                   "order_estimated_delivery_date"])
customers = pd.read_csv(f"{DATA_DIR}/olist_customers_dataset.csv")
items = pd.read_csv(f"{DATA_DIR}/olist_order_items_dataset.csv", parse_dates=["shipping_limit_date"])
payments = pd.read_csv(f"{DATA_DIR}/olist_order_payments_dataset.csv")
reviews = pd.read_csv(f"{DATA_DIR}/olist_order_reviews_dataset.csv")
products = pd.read_csv(f"{DATA_DIR}/olist_products_dataset.csv")
sellers = pd.read_csv(f"{DATA_DIR}/olist_sellers_dataset.csv")
cat_translation = pd.read_csv(f"{DATA_DIR}/product_category_name_translation.csv")

print(f"orders: {orders.shape}, items: {items.shape}, payments: {payments.shape}, "
      f"reviews: {reviews.shape}, products: {products.shape}, customers: {customers.shape}")

# ---------------------------------------------------------------------------
# 2. CLEAN / MERGE — build one analysis-ready table
# ---------------------------------------------------------------------------
delivered = orders[orders["order_status"] == "delivered"].copy()

delivered["delivery_delay_days"] = (
    delivered["order_delivered_customer_date"] - delivered["order_estimated_delivery_date"]
).dt.total_seconds() / 86400

delivered["actual_delivery_days"] = (
    delivered["order_delivered_customer_date"] - delivered["order_purchase_timestamp"]
).dt.total_seconds() / 86400

delivered["order_month"] = delivered["order_purchase_timestamp"].dt.to_period("M").dt.to_timestamp()

order_value = items.groupby("order_id").agg(
    order_price=("price", "sum"),
    order_freight=("freight_value", "sum"),
    n_items=("order_item_id", "count")
).reset_index()

products_named = products.merge(cat_translation, on="product_category_name", how="left")
products_named["product_category_name_english"] = (
    products_named["product_category_name_english"].fillna(products_named["product_category_name"])
)

items_named = items.merge(
    products_named[["product_id", "product_category_name_english"]], on="product_id", how="left"
)

reviews_dedup = reviews.sort_values("review_answer_timestamp").drop_duplicates("order_id", keep="last")

master = (
    delivered
    .merge(customers, on="customer_id", how="left")
    .merge(order_value, on="order_id", how="left")
    .merge(reviews_dedup[["order_id", "review_score"]], on="order_id", how="left")
)

print(f"master analysis table: {master.shape}")

# ---------------------------------------------------------------------------
# 3. CHART 1 — Monthly order volume & revenue trend
# ---------------------------------------------------------------------------
monthly = master.groupby("order_month").agg(
    orders=("order_id", "count"),
    revenue=("order_price", "sum")
).reset_index()
monthly = monthly[(monthly["order_month"] >= "2017-01-01") & (monthly["order_month"] <= "2018-08-01")]

fig, ax1 = plt.subplots(figsize=(11, 5))
ax1.bar(monthly["order_month"], monthly["orders"], color="#4C72B0", width=20, label="Orders")
ax1.set_ylabel("Orders per month", color="#4C72B0")
ax1.set_xlabel("Month")
ax1.set_title("Monthly Order Volume & Revenue (2017–2018)")

ax2 = ax1.twinx()
ax2.plot(monthly["order_month"], monthly["revenue"], color="#C44E52", marker="o", linewidth=2, label="Revenue (R$)")
ax2.set_ylabel("Revenue (R$)", color="#C44E52")
ax2.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"{x/1000:.0f}k"))
ax2.grid(False)

fig.tight_layout()
fig.savefig(f"{OUT_DIR}/01_monthly_orders_revenue.png")
plt.close(fig)

# ---------------------------------------------------------------------------
# 4. CHART 2 — Delivery delay distribution (early vs late)
# ---------------------------------------------------------------------------
delay = master["delivery_delay_days"].dropna()
delay_clipped = delay.clip(-30, 30)

fig, ax = plt.subplots(figsize=(10, 5))
sns.histplot(delay_clipped, bins=60, ax=ax, color="#4C72B0")
ax.axvline(0, color="black", linestyle="--", linewidth=1)
ax.set_xlabel("Days early (-) / late (+) vs. estimated delivery date")
ax.set_ylabel("Number of orders")
pct_late = (delay > 0).mean() * 100
ax.set_title(f"Delivery Timing vs. Estimate  ({pct_late:.1f}% of orders arrived late)")
fig.savefig(f"{OUT_DIR}/02_delivery_delay_distribution.png")
plt.close(fig)

# ---------------------------------------------------------------------------
# 5. CHART 3 — Review score vs. on-time / late delivery
# ---------------------------------------------------------------------------
review_delay = master.dropna(subset=["review_score", "delivery_delay_days"]).copy()
review_delay["on_time"] = review_delay["delivery_delay_days"] <= 0
review_delay["delivery_status"] = review_delay["on_time"].map({True: "On time / early", False: "Late"})

fig, ax = plt.subplots(figsize=(8, 5))
sns.barplot(
    data=review_delay, x="delivery_status", y="review_score", hue="delivery_status", ax=ax,
    estimator="mean", errorbar=("ci", 95), palette=["#55A868", "#C44E52"], legend=False
)
ax.set_ylim(0, 5)
ax.set_ylabel("Average review score (1–5)")
ax.set_xlabel("")
ax.set_title("Late Deliveries Correlate with Lower Review Scores")
for container in ax.containers:
    ax.bar_label(container, fmt="%.2f", padding=3)
fig.savefig(f"{OUT_DIR}/03_review_score_vs_delivery.png")
plt.close(fig)

# ---------------------------------------------------------------------------
# 6. CHART 4 — Top 10 product categories by revenue
# ---------------------------------------------------------------------------
cat_revenue = (
    items_named.merge(orders[["order_id", "order_status"]], on="order_id", how="left")
    .query("order_status == 'delivered'")
    .groupby("product_category_name_english")["price"].sum()
    .sort_values(ascending=False)
    .head(10)
    .sort_values()
)

fig, ax = plt.subplots(figsize=(9, 6))
cat_revenue.plot(kind="barh", ax=ax, color="#4C72B0")
ax.set_xlabel("Total revenue (R$)")
ax.set_ylabel("")
ax.set_title("Top 10 Product Categories by Revenue")
ax.xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"{x/1000:.0f}k"))
fig.savefig(f"{OUT_DIR}/04_top_categories_revenue.png")
plt.close(fig)

# ---------------------------------------------------------------------------
# 7. CHART 5 — Payment type distribution
# ---------------------------------------------------------------------------
pay_counts = payments["payment_type"].value_counts()

fig, ax = plt.subplots(figsize=(7, 6))
colors = sns.color_palette("deep", len(pay_counts))
wedges, texts, autotexts = ax.pie(
    pay_counts, labels=pay_counts.index, autopct="%1.1f%%", colors=colors, startangle=90
)
ax.set_title("Payment Method Share")
fig.savefig(f"{OUT_DIR}/05_payment_type_share.png")
plt.close(fig)

# ---------------------------------------------------------------------------
# 8. CHART 6 — Revenue by customer state (top 10)
# ---------------------------------------------------------------------------
state_revenue = (
    master.groupby("customer_state")["order_price"].sum()
    .sort_values(ascending=False)
    .head(10)
    .sort_values()
)

fig, ax = plt.subplots(figsize=(9, 6))
state_revenue.plot(kind="barh", ax=ax, color="#55A868")
ax.set_xlabel("Total revenue (R$)")
ax.set_ylabel("Customer state")
ax.set_title("Top 10 States by Revenue")
ax.xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"{x/1000:.0f}k"))
fig.savefig(f"{OUT_DIR}/06_revenue_by_state.png")
plt.close(fig)

# ---------------------------------------------------------------------------
# 9. Print summary stats used in the write-up
# ---------------------------------------------------------------------------
print("\n--- Key stats for README / write-up ---")
print(f"Total delivered orders analyzed: {len(master):,}")
print(f"% orders delivered late: {pct_late:.1f}%")
print(f"Avg review score on-time: {review_delay[review_delay.on_time]['review_score'].mean():.2f}")
print(f"Avg review score late:    {review_delay[~review_delay.on_time]['review_score'].mean():.2f}")
print(f"Top category by revenue: {cat_revenue.index[-1]}")
print(f"Top state by revenue: {state_revenue.index[-1]}")

print("\nAll charts saved to", OUT_DIR)