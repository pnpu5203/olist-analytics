# Olist-analytics Project
---
_End-to-end analytics engineering project: raw Olist e-commerce data → BigQuery → dbt → Power BI._

![dbt](https://img.shields.io/badge/dbt-FF694B?style=for-the-badge&logo=dbt&logoColor=white) ![BigQuery](https://img.shields.io/badge/BigQuery-4285F4?style=for-the-badge&logo=googlebigquery&logoColor=white) ![SQL](https://img.shields.io/badge/SQL-336791?style=for-the-badge&logoColor=white) ![Power BI](https://img.shields.io/badge/Power_BI-F2C811?style=for-the-badge&logo=powerbi&logoColor=black) ![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white) ![Git](https://img.shields.io/badge/Git-F05032?style=for-the-badge&logo=git&logoColor=white)

---
*hero image for the Dashboard coming in next phases*


## 1. Business Problem
---
### **Company & Business Model**

- **Olist:** A B2B2C e-commerce enabler platform in Brazil that empowers small and medium-sized businesses (SMBs) to list and sell their products across major Brazilian marketplaces (such as Mercado Livre, Americanas, and Amazon) under a unified Olist storefront brand.
	
- **Revenue Mechanism**: Typically generates revenue through a take-rate commission on Gross Merchandise Value (GMV), complemented by a fixed monthly subscription fee per active seller.

### **Business Questions**

To evaluate marketplace performance and revenue generation using the Olist dataset, the analytics workflow focuses on the following metric-driven questions:

#### **# Revenue & Order Scale**

- **Q1. Monthly GMV Trend:** How do total Monthly GMV and Completed Orders Volume change over time, and in which specific months do they peak?
    
- **Q2. Average Order Value:** What is the monthly trend of Average Order Value (AOV), and how does order value vary across different price tiers?

#### **# Category Performance**

- **Q3. Top Revenue Categories:** What are the Top 10 Product Categories by Revenue, and what exact percentage does each category contribute to the total Revenue?

#### **# Operational Efficiency & Logistics**

- **Q4. Delivery Lead Time:** What is the Average Delivery Lead Time (in days) from order approved to customer delivery, and how does it vary by state?
    
- **Q5. On-time Delivery Rate:** What is the monthly On-time Delivery Rate (percentage of orders delivered on and before the estimated delivery date), and among late orders, how many days late are they on average?

#### **# Order Risk & Reliability**

- **Q6. Order Cancellation Rate:** What is the monthly order cancellation rate, and which product categories have the highest cancellation rate (categories with at least N orders)?

#### **# Customer Satisfaction**

- **Q7. Review Score Distribution:** What is the average review score per month, and what exact percentage of total orders fall into each rating tier (from 1 to 5 stars)?


## 2. Key insights
---

*Coming in next phases*
*(This section highlights the data analysis approach)*


## 3. Architecture
---

*Coming in next phases:*
- [ ] *Data flow diagram: Kaggle CSV → load script → BigQuery `raw` → dbt (staging → intermediate → marts) → Power BI*
- [ ] *Tech Stack Table: Tools | What are they used for?*


## 4. Data Model

```mermaid
erDiagram
    dim_customers ||--o{ fct_orders : "customer_unique_id"
    dim_customers ||--o{ fct_order_items : "customer_unique_id"
    dim_customers ||--o{ fct_order_payments : "customer_unique_id"
    dim_date      ||--o{ fct_orders : "order_date"
    dim_date      ||--o{ fct_order_items : "order_date"
    dim_date      ||--o{ fct_order_payments : "order_date"
	dim_sellers   ||--o{ fct_order_items : "seller_id"
	dim_products  ||--o{ fct_order_items : "product_id"

    fct_orders {
        string    order_id PK
        string    customer_unique_id FK
        date      order_date FK
        string    order_status
        int       delivery_days
        numeric   order_value
        int       item_count
        bool      is_delivered
        bool      is_canceled
        float     review_score
        timestamp order_purchase_timestamp
        timestamp order_approved_at
        timestamp order_delivered_carrier_date
        timestamp order_delivered_customer_date
        timestamp order_estimated_delivery_date
    }
    fct_order_items {
        string    order_id PK
        int       order_item_id PK
        string    customer_unique_id FK
        date      order_date FK
        string    order_status
        string    product_id FK
        string    seller_id FK
        numeric   price
        numeric   freight_value
    }
    fct_order_payments {
        string    order_id PK
        integer   payment_sequential PK
        string    customer_unique_id FK
        date      order_date FK
        string    payment_type
        integer   payment_installments
        numeric   payment_value
    }
    dim_customers {
        string customer_unique_id PK
        string customer_zip_code_prefix 
        string customer_city
        string customer_state
    }
    dim_sellers {
        string seller_id PK
        string seller_zip_code_prefix 
        string seller_city
        string seller_state
    }
    dim_products {
        string product_id PK
        string product_category_name 
        string product_category_name_eng
        int    product_name_length
        int    product_description_length
        int    product_photo_qty
        float  product_weight_g
        float  product_length_cm
        float  product_height_cm
        float  product_width_cm
    }
    dim_date {
        date   date PK
        string day_name
        int    month
        string month_name
        int    year
        date   year_month
        string quarter
        bool is_weekend
    }
```

The warehouse follows a **galaxy schema**: three fact tables at different grains share conformed dimensions (`dim_customers`, `dim_products`, `dim_sellers`, `dim_date`).

- `fct_orders`: one row per order (status, delivery, review)
- `fct_order_items`: one row per item in an order (price, freight)
- `fct_order_payments`: one row per payment of an order

Keeping each fact at its natural grain avoids double-counting when an order has multiple items or payments.

*💡 **Detailed Documentation:** For a comprehensive breakdown of the schema design, table relationships, and field dictionaries, please refer to the [Data Model Documentation](docs/data_model.md).*


## 5. dbt Project
---

*Coming in next phases*



## 6. Repository structure
---

```
olist-analytics/                  <-- Root workspace
├── .gitignore                    <-- Files/folders to ignore
├── requirements.txt              <-- Packages/dependencies
├── README.md                     <-- 📌 README (shows in the Github homepage)
├── docs/                         <-- Contains design documents & Schema diagrams
└── olist_analytics/              <-- The folder containing dbt project
    ├── dbt_project.yml           <-- Overall dbt configuration
    ├── models/                                  
    ├── analyses/
    ├── tests/
    └── macros/
```


## 7. How to run
---

*Coming in next phases*
*(Others who follow the directions must be able to get the project running)*


## 8. What I learned / Next steps
---

*Coming in next phases*


## 9. Contact
---

*Add LinkedIn & Email*

