import mysql.connector
from sqlalchemy import create_engine
import pandas as pd

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  passwd="Samridh!2qwaszx",
  database="demo1"
)
cursor=mydb.cursor()

print("\n\nShow the total number of orders and total revenue generated by each retailer in the last month.\n\n")
cursor.execute("SELECT r.retailer_id, COUNT(o.order_id) AS total_orders, SUM(o.total_cost) AS total_revenue FROM retailer r JOIN product p ON r.retailer_id = p.retailer_id JOIN orders o ON p.product_id = o.cart_id WHERE o.time_date >= DATE_SUB(NOW(), INTERVAL 1 MONTH) GROUP BY r.retailer_id;")
result=cursor.fetchall()
print(result)

print("\n\n-- 6. Show the total revenue generated by each delivery partner type.\n\n")
cursor.execute("SELECT dp.type, SUM(o.total_cost) AS total_revenue FROM delivery_partner dp JOIN orders o ON dp.delivery_partner_id = o.delivery_partner_id GROUP BY dp.type;")
result=cursor.fetchall()
print(result)
