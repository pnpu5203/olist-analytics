# olist-analytics project
---
## Define grain of each table in the schema

- `fct_order_items`: Mỗi dòng trong bảng này là **1 sản phẩm trong 1 đơn hàng** (`order_id` + `order_item_id`).
- `fct_order_payments`: Mỗi dòng là **1 đợt thanh toán của 1 đơn hàng** (`order_id` + `payment_sequential`).
- `dim_customers`: Mỗi dòng là **1 khách hàng duy nhất** (`customer_id`).
- `dim_products`: Mỗi dòng là **1 sản phẩm duy nhất** (`product_id`).
- `dim_sellers`: Mỗi dòng là **1 nhà bán hàng duy nhất** (`seller_id`).
- `dim_date`: Mỗi dòng là **1 ngày duy nhất trong năm** (`date`).

## Business Questions & KPIs

1. **Doanh thu tổng theo tháng (Monthly GMV):**
   * *Định nghĩa KPI:* Tổng giá trị hàng hóa (tổng cột `price` + `freight_value` trong bảng order items) của các đơn hàng có trạng thái là "delivered" (đã giao), tính theo tháng đặt hàng (`order_purchase_timestamp`).
2. **Số lượng đơn hàng hoàn thành theo thời gian (Completed Orders Volume):** 
   * *Định nghĩa KPI:* Tổng số lượng `order_id` duy nhất có trạng thái "delivered", nhóm theo tháng/năm đặt hàng.
3. **Thời gian giao hàng trung bình (Average Delivery Lead Time):** 
   * *Định nghĩa KPI:* Số ngày trung bình tính từ khi xác nhận thanh toán (`order_approved_at`) đến khi thực tế giao hàng thành công cho khách (`order_delivered_customer_date`), tính trên các đơn đã hoàn thành.
1. **Giá trị trung bình mỗi đơn hàng (AOV - Average Order Value):** 
   * *Định nghĩa KPI:* Tổng GMV chia cho tổng số lượng đơn hàng hoàn thành trong cùng khoảng thời gian.
5. **Top 10 danh mục sản phẩm có doanh thu cao nhất (Top Product Categories by Revenue):**
   * *Định nghĩa KPI:* Tổng GMV đóng góp bởi từng danh mục sản phẩm (product category name), sắp xếp giảm dần và lấy top 10.
6. **Tỷ lệ hủy đơn hàng (Order Cancellation Rate):** 
   * *Định nghĩa KPI:* Tỷ lệ phần trăm giữa số lượng đơn hàng có trạng thái "canceled" chia cho tổng số lượng tất cả các đơn hàng trên hệ thống.


**Mapping table**

| #   | Business question                                           | Fact table      | Dimension(s)                      | Columns used                                                   | KPI formula                                                                                |
| --- | ----------------------------------------------------------- | --------------- | --------------------------------- | -------------------------------------------------------------- | ------------------------------------------------------------------------------------------ |
| 1   | GMV theo tháng thay đổi thế nào?                            | fct_order_items | dim_date, dim_orders_logistics,   | price, freight_value, order_status, order_purchased_timestamp  | SUM(price + freight_value), chỉ tính đơn 'delivered', nhóm theo tháng                      |
| 2   | Số lượng đơn hàng hoàn thành theo thời gian diễn ra ra sao? | fct_order_items | dim_date,<br>dim_orders_logistics | order_id, order_status                                         | COUNTDISTINCT(order_id), chỉ tính đơn 'delivered'                                          |
| 3   | Thời gian giao hàng trung bình là bao lâu?                  | fct_order_items | dim_orders_logistics              | order_delivered_customer_date, order_approved_at, order_status | AVG(order_delivered_customer_date - order_approved_at), chỉ tính đơn 'delivered'           |
| 4   | Giá trị trung bình mỗi đơn hàng đạt mức nào?                | fct_order_items | dim_date                          | price, freight_value, order_id                                 | Tổng GMV chia cho tổng số lượng order_id hoàn thành trong cùng khoảng thời gian.           |
| 5   | Top 10 những danh mục nào có doanh thu cao nhất?            | fct_order_items | dim_products                      | price, freight_value, product_category_name_eng                | SUM(price + freight_value) nhóm theo danh mục sản phẩm, sắp xếp giảm dần và lấy top 10.    |
| 6   | Tỷ lệ huỷ đơn hàng chiếm bao nhiêu phần trăm?               | fct_order_items | dim_date, dim_orders_logistics    | order_id, order_status                                         | (Số lượng order_id có trạng thái "canceled" / Tổng số lượng order_id trên hệ thống) * 100. |
