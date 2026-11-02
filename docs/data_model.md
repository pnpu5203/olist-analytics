# Data Model
---
**A galaxy schema**: three fact tables at different grains (`fct_orders`, `fct_order_items`, `fct_order_payments`) share conformed dimensions (`dim_customers`, `dim_products`, `dim_sellers`, `dim_date`).

## 1. Overview
---

| Table                | Type (fact/dim) | Grain                                               | Primary Key                       | Source                                                        |
| -------------------- | --------------- | --------------------------------------------------- | --------------------------------- | ------------------------------------------------------------- |
| `fct_orders`         | fact            | 1 đơn hàng                                          | `order_id`                        | `olist_orders_dataset`, `olist_order_reviews_dataset`         |
| `fct_order_items`    | fact            | 1 mặt hàng trong 1 đơn hàng                         | `order_id` + `order_item_id`      | `olist_orders_dataset`, `olist_order_items_dataset`           |
| `fct_order_payments` | fact            | 1 đợt thanh toán của 1 đơn hàng                     | `order_id` + `payment_sequential` | `olist_order_payments_dataset`                                |
| `dim_customers`      | dim             | 1 khách hàng duy nhất                               | `customer_unique_id`              | `olist_customers_dataset`                                     |
| `dim_sellers`        | dim             | 1 nhà bán hàng duy nhất                             | `seller_id`                       | `olist_sellers_dataset`                                       |
| `dim_products`       | dim             | 1 sản phẩm duy nhất                                 | `product_id`                      | `olist_products_dataset`, `product_category_name_translation` |
| `dim_date`           | dim             | 1 ngày dương lịch, từ `2016-01-01` đến `2018-12-31` | `date`                            | *tự thêm bên ngoài*                                           |

## 2. Entity Relationship Diagram (ERD)
---

![hero image](docs/images/ERD.png)

### **Fact Tables**
---
#### `fct_orders`: ghi lại lịch sử bán hàng.
	
- Grain: Mỗi dòng là **1 đơn hàng**.
- Khoá chính: `order_id`.
- Measures: `delivery_days`, `review_score`, `item_count`, `order_value`.
- Khoá ngoại: `customer_unique_id`, `order_date`.
- Nguồn: `olist_orders_dataset`, `olist_order_reviews_dataset`.

#### `fct_order_items`: ghi lại thông tin chi tiết đơn hàng.
	
- Grain: Mỗi dòng là **1 sản phẩm nằm trong 1 đơn hàng**.
- Khoá chính: (`order_id` + `order_item_id`).
- Measures: `price`, `freight_value`.
- Khoá ngoại: ``customer_unique_id``, `seller_id`, `product_id`, `order_date.
- Nguồn: `olist_orders_dataset`, `olist_order_items_dataset`.

#### `fct_order_payments`: ghi lại các giao dịch thanh toán.
	
- Grain: Mỗi dòng là **1 đợt thanh toán của 1 đơn hàng**.
- Khoá chính: (`order_id` + `payment_sequential`).
- Measures: `payment_installments`, `payment_value`.
- Khoá ngoại: `customer_unique_id`, `order_date`.
- Nguồn: `olist_order_payments_dataset`

### **Dimension Tables**
---
#### `dim_customers`: danh sách các khách hàng unique và thông tin khách hàng.
	
- Grain: Mỗi dòng là **1 khách hàng duy nhất.
- Khoá chính: `customer_unique_id`.
- Nguồn: `olist_customers_dataset`.

#### `dim_products`: danh sách sản phẩm và thông tin sản phẩm.
	
- Grain: Mỗi dòng là **1 sản phẩm duy nhất.
- Khoá chính: `product_id`.
- Nguồn: `olist_products_dataset`, `product_category_name_translation`.

#### `dim_sellers`: danh sách các nhà bán hàng unique và thông tin nhà bán hàng.
	
- Grain: Mỗi dòng là **1 nhà bán hàng duy nhất.**
- Khoá chính: `seller_id`.
- Nguồn: `olist_sellers_dataset`.

#### `dim_date`: chứa thông tin về ngày tháng năm.
	
- Grain: Mỗi dòng là **1 ngày dương lịch từ `2016-01-01` đến `2018-12-31`.**
- Khoá chính: `date`.
- Nguồn: *tự thêm bên ngoài*.

## 3. Business Questions & KPIs
---
### KPI definitions

- **Monthly GMV (Q1):** The total value of goods (`order_value` in the `fct_orders` table) for orders with a "delivered" status, calculated by the order month (`order_date`).

- **Completed Orders Volume (Q1):** The total number of unique `order_id` with the status "delivered", grouped by order month/year (`order_date`).

- **AOV - Average Order Value (Q2):** Total GMV divided by the total number of completed orders within the same time period, calculated by order month/year (`order_date`).

- **Top 10 Product Categories by Revenue (Q3):** Total revenue contributed by each product category name, sorted in descending order, with the top 10.

- **Average Delivery Lead Time (Q4):** The average number of days from payment confirmation (`order_approved_at`) to successful delivery to the customer (`order_delivered_customer_date`), calculated only for orders with a "delivered" status.

 - **On-time Delivery Rate (Q5):** Percentage of orders delivered on and before the estimated delivery date (`order_estimated_delivery_date`).

- **Order Cancellation Rate (Q6):** The percentage of orders with a "canceled" status divided by the total number of all orders in the system.

- **Average review score (Q7):** The average review score of all orders in the system, grouped by order month/year (`order_date`).

### Mapping table

| #   | Business question                                | Fact table      | Dimension(s) | Columns used                                                                         | KPI formula                                                                                                                                                                         |
| --- | ------------------------------------------------ | --------------- | ------------ | ------------------------------------------------------------------------------------ | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Q1  | How do total Monthly GMV change over time?       | fct_orders      | dim_date     | order_value, order_status, order_date                                                | `SUM(order_value)`<br><br>*(only 'delivered' orders are counted, grouped by month)*                                                                                                 |
| Q1  | How do Completed Orders Volume change over time? | fct_orders      | dim_date     | order_id, order_status                                                               | `COUNT(order_id)`<br><br>*(only 'delivered' orders are counted)*                                                                                                                    |
| Q2  | What is the AOV?                                 | fct_orders      | dim_date     | order_value, order_id, order_status                                                  | Total GMV divided by the total number of completed `order_id` within the same time period                                                                                           |
| Q3  | What are the top 10 highest-revenue categories?  | fct_order_items | dim_products | price, product_category_name_eng                                                     | `SUM(price)`<br><br>*(grouped by product category, sort in descending order and select the top 10)*                                                                                 |
| Q4  | What is the average delivery time?               | fct_orders      | -            | delivery_days, order_status                                                          | `AVG(delivery_days)`<br><br>*(only 'delivered' orders are counted)*                                                                                                                 |
| Q5  | What is the monthly On-time Delivery Rate?       | fct_orders      | dim_date     | order_id, order_status, order_estimated_delivery_date, order_delivered_customer_date | `(COUNT(order_id) where order_delivered_customer_date <= order_estimated_delivery_date / COUNT(`order_id`)) * 100`<br><br>*(only 'delivered' orders are counted, grouped by month)* |
| Q6  | What is the monthly order cancellation rate?     | fct_orders      | dim_date     | order_id, order_status, order_date                                                   | `(COUNT(order_id) where order_status = 'canceled' / COUNT(order_id)) * 100`<br><br>*(only 'delivered' orders are counted, grouped by month)*                                        |
| Q7  | What is the average review score per month?      | fct_orders      | dim_date     | order_status, review_score, order_date                                               | `AVG(review_score)`<br><br>*(only 'delivered' orders are counted, grouped by month)*                                                                                                |

## 4. Assumptions & decisions
---

>[!question]- What is the rule for **eliminating duplicate customer data**?
>
> - **Problem encountered:** When removing the `customer_id` field from the original dataset `olist_orders_dataset` and `olist_customers_dataset`, the records in the new `dim_customers` table will be duplicated, because the PK of the original `olist_customers_dataset` dataset is `order_id`.
> 
> - **Solution:** Only keep the `customer_unique_id` and related customer information (`customer_zip_code_prefix`, `customer_city`, `customer_state`) from the most recent order.

>[!question]- Why is **GMV** (Gross Merchandise Value) **included in freight** charges?
>
> - **GMV (Gross Merchandise Value):** This is the total amount paid by the buyer to the seller through the platform. This entire amount **does not** belong to the e-commerce platform.
>
>- **Actual Revenue:** This is the amount of money the e-commerce platform actually earns from those transactions. The platform's revenue typically comes from:
>  
>	- Commission fees charged to the seller.
>
>	- Advertising and marketing fees displayed on the platform.
>
>	- Shipping and warehousing service fees.

