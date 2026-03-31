import sqlite3
import pandas as pd
conn = sqlite3.connect('shopmart.db')
cursor = conn.cursor()
orders = pd.read_excel('ecommerce_BIG_dataset.xlsx', sheet_name='Orders')
products = pd.read_excel('ecommerce_BIG_dataset.xlsx', sheet_name='Products')
customers = pd.read_excel('ecommerce_BIG_dataset.xlsx', sheet_name='Customers')
orders.to_sql('orders', conn, if_exists='replace', index=False)
products.to_sql('products', conn, if_exists='replace', index=False)
customers.to_sql('customers', conn, if_exists='replace', index=False)
query1 = """
SELECT 
    p.product_name,
    p.category,
    SUM(o.total_amount) AS total_revenue,
    SUM(o.quantity) AS total_units,
    AVG(o.total_amount) AS avg_order_value
FROM orders o
JOIN products p ON o.product_id = p.product_id
GROUP BY p.product_name, p.category
ORDER BY total_revenue DESC
LIMIT 10;
"""

top_products = pd.read_sql(query1, conn)
print(top_products)
query2 = """
SELECT 
    strftime('%Y', order_date) AS year,
    strftime('%m', order_date) AS month,
    COUNT(order_id) AS total_orders,
    SUM(total_amount) AS revenue
FROM orders
GROUP BY year, month
ORDER BY year, month;
"""

monthly_trend = pd.read_sql(query2, conn)
print(monthly_trend)
query3 = """
SELECT 
    c.region,
    SUM(o.total_amount) AS total_revenue,
    COUNT(o.order_id) AS total_orders
FROM orders o
JOIN customers c ON o.customer_id = c.customer_id
GROUP BY c.region
ORDER BY total_revenue DESC;
"""

regional_sales = pd.read_sql(query3, conn)
print(regional_sales)
query4 = """
SELECT 
    p.category,
    SUM(o.total_amount) AS revenue,
    COUNT(o.order_id) AS orders
FROM orders o
JOIN products p ON o.product_id = p.product_id
GROUP BY p.category
ORDER BY revenue DESC;
"""

category_perf = pd.read_sql(query4, conn)
print(category_perf)
query5 = """
SELECT *
FROM orders
WHERE total_amount > (
    SELECT AVG(total_amount) * 3 FROM orders
);
"""

anomalies = pd.read_sql(query5, conn)
print(anomalies)
top_products.to_csv('top_products.csv', index=False)
monthly_trend.to_csv('monthly_trend.csv', index=False)
regional_sales.to_csv('regional_sales.csv', index=False)
category_perf.to_csv('category_perf.csv', index=False)
anomalies.to_csv('anomalies.csv', index=False)
conn.close()

