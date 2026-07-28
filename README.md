# SQL & Python Analytics Portfolio - From Practice to Production
**NOTE:** AI was used for scaffolding/planning this portfolio, not for the conclusions themselves.
**Tools:** SQL (Snowflake), Python (Pandas, Matplotlib), SQLLite  
**Goal:** Build SQL fluency on a structured sample dataset, then apply every skill to a real-world e-commerce dataset and answer genuine business questions.

For more details, please check out my website by clicking these two links:

https://app.notion.com/p/Olist-Brazilian-E-Commerce-Python-Visualization-Layer-3ab6f1589ccd80279a3ecb83a22fb08f?source=copy_link
https://app.notion.com/p/Olist-Brazilian-E-Commerce-Python-Visualization-Layer-3ab6f1589ccd80279a3ecb83a22fb08f

This portfolio has two stages - intentionally. Stage 1 is where the syntax becomes reflexive. Stage 2 is where it becomes useful.

---

## Stage 1 - SQL Fluency on Sample Data (TPC-H / Snowflake)

**Dataset:** Snowflake's built-in `SNOWFLAKE_SAMPLE_DATA.TPCH_SF1` - a standardized benchmark database with customers, orders, lineitems, suppliers, and parts. Relational, clean, zero setup.

**Why this first:** Real datasets have messy schemas, nulls, and ambiguous relationships. Learning syntax on clean data means errors come from you, not the data - which is how you actually learn.

### Concepts practiced and verified

| Concept | Status |
|---------|--------|
| SELECT / WHERE / ORDER BY | ✅ Done |
| Multi-table JOINs (INNER, LEFT) | ✅ Done |
| GROUP BY / HAVING | ✅ Done |
| Subqueries | ✅ Done |
| Window functions (ROW_NUMBER, PARTITION BY) | ✅ Done |
| CASE statements | ✅ Done |
| CTEs | ✅ Done |

**Practice files:** See `/practice/broken_queries.sql` - each query has deliberate bugs to find and fix. 

---

## Stage 2 - Real Analysis on Olist E-Commerce Data

**Dataset:** [Olist Brazilian E-Commerce](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce)-— ~100k real, anonymized orders across 9 relational tables (2016–2018). Customers, sellers, products, payments, reviews, geolocation.

**Why this second:** Same SQL skills as Stage 1 - applied to a schema with real ambiguity, real nulls, and real business questions that don't have obvious answers until you query them.

### Business Questions Answered

| # | Question | Key Techniques |
|---|----------|---------------|
| 1 | Does delivery delay predict lower review scores? | JOIN, DATEDIFF, CASE, GROUP BY |
| 2 | Which product categories drive the most revenue? | 3-table JOIN, GROUP BY, ORDER BY |
| 3 | What does repeat purchase behavior look like? | CTE, ROW_NUMBER, PARTITION BY |
| 4 | Where are sellers concentrated vs. their customers? | 4-table JOIN, GROUP BY, NULLIF |
| 5 | What does multi-payment behavior look like? | Subquery, GROUP BY, HAVING |

### Key Findings

## Key Findings

### Data Quality Audit
Audited 99,441 orders before analysis - identified 3% missing delivery
dates (2,965 records), excluded from time-sensitive queries. Confirmed
zero duplicate order IDs, zero zero/negative prices across 112,650 items,
and zero logically impossible delivery dates. Dataset is reliable with
one known gap in delivery data.

---

### Q1: Does delivery delay predict lower review scores?
Yes, strongly. On-time orders averaged 4.29 stars. Orders 1-3 days late
dropped to 3.77. Orders 4-7 days late fell to 2.32. Orders over one week
late averaged 1.73 - a 2.56 point drop from on-time. Delivery timeliness
is the single biggest lever on customer satisfaction in this dataset.

| Delay Bucket     | Orders | Avg Review Score |
|------------------|--------|-----------------|
| On Time          | 88,658 | 4.29            |
| 1-3 Days Late    | 2,651  | 3.77            |
| 4-7 Days Late    | 1,777  | 2.32            |
| Over 1 Week Late | 3,273  | 1.73            |

---

### Q2: Which product categories drive the most revenue?
Beauty & health (beleza_saude) led total revenue at $1.44M across 8,836
orders at an avg item price of $130. Watches & gifts (relogios_presentes)
had the highest avg item price at $201 with 5,624 orders - a premium
low-volume segment vs. a high-volume mid-price category. Two different
business models in the top 2 rows.

| Category                | Orders | Total Revenue   | Avg Item Price |
|-------------------------|--------|-----------------|---------------|
| beleza_saude            | 8,836  | $1,441,248.07   | $130.16        |
| relogios_presentes      | 5,624  | $1,305,541.61   | $201.14        |
| cama_mesa_banho         | 9,417  | $1,241,681.72   | $93.30         |
| esporte_lazer           | 7,720  | $1,156,656.48   | $114.34        |
| informatica_acessorios  | 6,689  | $1,059,272.40   | $116.51        |

---

### Q3: What does repeat purchase behavior look like?
96% of customers purchased exactly once and never returned. Of ~99k
customers, only 2,997 placed a second order. Olist's growth depends
almost entirely on new customer acquisition - retention is near zero.

| Order Rank | Customers |
|------------|-----------|
| 1          | 96,096    |
| 2          | 2,997     |
| 3          | 252       |
| 4          | 49        |
| 5+         | 39        |

---

### Q4: Where are sellers concentrated vs. their customers?
São Paulo (SP) dominates with 1,849 sellers serving 68,227 customers at
a 36.9 customers-per-seller ratio. States like Bahia (BA, 29.5 ratio)
and Ceará (CE, 6.8 ratio) show far lower seller presence relative to
demand - pointing to geographic expansion opportunities in underserved
regions.

| State | Sellers | Customers | Customers per Seller |
|-------|---------|-----------|---------------------|
| SP    | 1,849   | 68,227    | 36.9                |
| MG    | 244     | 7,842     | 32.1                |
| PR    | 349     | 7,551     | 21.6                |
| RJ    | 171     | 4,315     | 25.2                |
| BA    | 19      | 560       | 29.5                |

---

### Q5: What does multi-payment behavior look like?
97% of orders used a single payment method at an avg order value of
$161.22. Only 2,246 orders split across two payment types, averaging
slightly less at $150.88. Brazil's installment-based credit culture
allows customers to split large purchases across months on a single
payment method — reducing the need for multiple payment types even on
higher-value orders.

| Payment Types Used | Orders | Avg Order Value |
|--------------------|--------|----------------|
| 1                  | 97,194 | $161.22         |
| 2                  | 2,246  | $150.88         |

---

## Repository Structure

```
sql-analytics-portfolio/
│
├── README.md
│
├── practice/
│   └── broken_queries.sql        ← Stage 1 reps — fix the bugs
│
└── queries/                      ← Stage 2 — real Olist analysis
    ├── 01_delivery_delay_vs_reviews.sql
    ├── 02_revenue_by_category.sql
    ├── 03_repeat_purchases.sql
    ├── 04_seller_vs_customer_geography.sql
    └── 05_multi_payment_behavior.sql
```

---

## How to Reproduce

**Stage 1 (sample data)**
1. Sign up for a free Snowflake trial at https://signup.snowflake.com/
2. Open a worksheet — `SNOWFLAKE_SAMPLE_DATA.TPCH_SF1` is pre-loaded, nothing to download
3. Work through `/practice/broken_queries.sql`, fix each query, run it

**Stage 2 (Olist)**
1. Download the 9 CSVs from [Kaggle](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce)
2. Load each CSV into Snowflake as its own table
3. Run each `.sql` file in `/queries/` in order
4. Phase 3: connect Python to Snowflake, visualize findings in Streamlit


