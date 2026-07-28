# Olist Brazilian E-Commerce — Python Visualization Layer

Exploratory analysis and visualization of ~100,000 orders from the [Olist
dataset](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce) (2016-2018),
built with `pandas`, `matplotlib`, and `seaborn`. This extends a companion
SQL-based analysis of the same dataset into Python.

## Key findings

- **Late deliveries hurt satisfaction badly.** Orders delivered late average a
  **2.57/5** review score, versus **4.29/5** for on-time or early orders — an
  85% gap.
- **8.1%** of delivered orders arrived after their estimated delivery date.
- **Health & beauty** is the top revenue-generating product category.
- **São Paulo (SP)** drives the largest share of revenue by customer state,
  consistent with its status as Brazil's largest economic hub.

## Charts

| | |
|---|---|
| ![Monthly orders & revenue](charts/01_monthly_orders_revenue.png) | ![Delivery delay distribution](charts/02_delivery_delay_distribution.png) |
| ![Review score vs delivery](charts/03_review_score_vs_delivery.png) | ![Top categories by revenue](charts/04_top_categories_revenue.png) |
| ![Payment type share](charts/05_payment_type_share.png) | ![Revenue by state](charts/06_revenue_by_state.png) |

## Project structure

```
olist-ecommerce-viz/
├── analyze.py          # main analysis + chart-generation script
├── requirements.txt    # Python dependencies
├── data/                # place the 9 Olist CSVs here (not included — see below)
└── charts/              # generated PNG charts (output of analyze.py)
```

## Setup & usage

1. Download the dataset from
   [Kaggle: Brazilian E-Commerce Public Dataset by Olist](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce)
   and place the 9 CSV files in the `data/` folder.
2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Run the analysis:
   ```
   python analyze.py
   ```
4. Charts are written to `charts/` and key stats are printed to the console.

## Methodology notes

- Delivery-timing analysis only includes orders with status `delivered`,
  since cancelled/unavailable orders have no delivery date and would distort
  the delay calculation.
- The delivery-delay histogram is clipped to ±30 days for readability; a
  small number of extreme outliers (logistics failures) would otherwise
  compress the rest of the distribution.
- Revenue figures are the sum of item price across all order items,
  excluding freight.

## Related work

See the companion SQL-based analysis of this same dataset for schema design
and query-level exploration (JOINs, aggregations, window functions).
