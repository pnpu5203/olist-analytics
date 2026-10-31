# olist-analytics project
---

## Lược đồ ERD

**Fact Tables**

> `fct_order_items`: ghi lại lịch sử bán hàng.
	
- Grain: Mỗi dòng là **1 sản phẩm nằm trong 1 đơn hàng**.
- Khoá chính: (`order_id` + `order_item_id`).
- Measures: `price`, `freight_value`, `review_score`.
- Khoá ngoại: `customer_id`, `seller_id`, `product_id`.
- Nguồn: `olist_orders_dataset` join với `olist_order_items_dataset`, join tiếp với `olist_order_reviews_dataset` để lấy điểm đánh giá `review_score` (nếu 1 đơn hàng có nhiều hơn 1 đánh giá thì lấy trung bình).

> `fct_order_payments`: ghi lại các giao dịch thanh toán.
	
- Grain: Mỗi dòng là **1 đợt thanh toán của 1 đơn hàng**.
- Khoá chính: (`order_id` + `payment_sequential`).
- Measures: `payment_installments`, `payment_value`.
- Khoá ngoại: `customer_unique_id`.
- Nguồn: `olist_order_payments_dataset`

**Dimension Tables**

> `dim_customers`: danh sách các khách hàng unique và thông tin khách hàng.
	
- Grain: Mỗi dòng là **1 khách hàng duy nhất.
- Khoá chính: `customer_unique_id`.
- Nguồn: `olist_order_payments_dataset`.

>`dim_products`: danh sách sản phẩm và thông tin sản phẩm.
	
- Grain: Mỗi dòng là **1 sản phẩm duy nhất.
- Khoá chính: `product_id`.
- Nguồn: `olist_products_dataset` và `product_category_name_translation`.

>`dim_sellers`: danh sách các nhà bán hàng unique và thông tin nhà bán hàng.
	
- Grain: Mỗi dòng là **1 nhà bán hàng duy nhất.**
- Khoá chính: `seller_id`.
- Nguồn: `olist_sellers_dataset`.

> `dim_date`: chứa thông tin về ngày tháng năm.
	
- Grain: Mỗi dòng là **1 ngày duy nhất trong năm.**
- Khoá chính: `date`.
- Nguồn: tự thêm bên ngoài.
