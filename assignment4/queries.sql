-- Retrieve all the customer details from the CUSTOMER table.
SELECT * FROM CUSTOMER;

-- Retrieve the product name and price for all the products available in the PRODUCT table.
SELECT product_name, product_price FROM PRODUCT;

-- Retrieve the category name and the total number of products in each category from the CATEGORY and PRODUCT tables.
SELECT catregory_name, COUNT(*) as total_products FROM PRODUCT p JOIN CATEGORY c ON p.category_id = c.category_id GROUP BY catregory_name;

-- Retrieve the details of all the products with their respective retailer names from the PRODUCT and RETAILER tables.
SELECT p.product_name, p.product_price, r.retailer_name AS retailer_name FROM PRODUCT p JOIN RETAILER r ON p.retailer_id = r.retailer_id;

-- Retrieve the product feedback details along with the customer and product details for a specific product from the PRODUCTFEEDBACK, CUSTOMER, and PRODUCT tables.
SELECT pf.review, c.customer_name, c.customer_email, p.product_name, p.details FROM PRODUCTFEEDBACK pf JOIN CUSTOMER c ON pf.customer_id = c.customer_id JOIN PRODUCT p ON pf.product_id = p.product_id;

-- Retrieve the details of all the orders along with their respective payment details from the ORDERS and PAYMENT tables.
SELECT o.order_id, o.time_date, o.status, p.mode, p.details FROM ORDERS o JOIN PAYMENT p ON o.payment_id = p.payment_id;

-- Show the total count of products in each category:

SELECT c.catregory_name, COUNT(p.product_id) as total_count
FROM PRODUCT p
JOIN CATEGORY c ON p.category_id = c.category_id
GROUP BY c.category_id;

-- Show the average product price in each category:

SELECT c.catregory_name, AVG(p.product_price) as avg_price
FROM PRODUCT p
JOIN CATEGORY c ON p.category_id = c.category_id
GROUP BY c.category_id;

-- Show the total sales revenue for each retailer:

SELECT r.Retailer_name, SUM(c.total_cost) as total_sales
FROM ORDERS o
JOIN RETAILER r ON o.retailer_id = r.retailer_id
JOIN cart c on c.cart_id=o.cart_id
GROUP BY r.retailer_id;

-- Show the total count of orders for each delivery partner:

SELECT dp.type, COUNT(o.order_id) as total_orders
FROM ORDERS o
JOIN DELIVERY_PARTNER dp ON o.delivery_partner_id = dp.delivery_partner_id
GROUP BY dp.delivery_partner_id;

-- Show the most popular product in each category (based on number of orders):

SELECT c.catregory_name, p.product_name, COUNT(o.order_id) as total_orders
FROM PRODUCT p
JOIN cart cart on cart.cart_id
JOIN CATEGORY c ON p.category_id = c.category_id
JOIN ORDERS o
GROUP BY c.category_id, p.product_id
HAVING COUNT(o.order_id) = (SELECT MAX(total_orders)
                            FROM (SELECT COUNT(o2.order_id) as total_orders
                                  FROM ORDERS o2
                                  JOIN PRODUCT p2
                                  GROUP BY p2.product_id) AS temp
                            );

-- Show the average age of customers who have made at least one order:

SELECT AVG(c.customer_age) as avg_age
FROM CUSTOMER c
WHERE EXISTS (SELECT 1
              FROM ORDERS o
              WHERE o.customer_id = c.customer_id);

-- Show the total count of orders for each customer, sorted in descending order:

SELECT o.customer_id, c.customer_name, COUNT(o.order_id) as total_orders
FROM ORDERS o
JOIN CUSTOMER c ON o.customer_id = c.customer_id
GROUP BY o.customer_id
ORDER BY total_orders DESC;

-- Show the number of products in each category that have received at least one feedback:

SELECT c.catregory_name, COUNT(DISTINCT p.product_id) as total_products
FROM PRODUCT p
JOIN CATEGORY c ON p.category_id = c.category_id
JOIN PRODUCTFEEDBACK pf ON p.product_id = pf.product_id
GROUP BY c.category_id;

-- Show the total sales revenue for each month (based on order date):

SELECT MONTH(o.time_date) as month, SUM(c.total_cost) as total_sales
FROM ORDERS o
JOIN cart c on c.cart_id = o.cart_id
GROUP BY month;

-- Show the most active retailers (based on number of orders):

SELECT r.Retailer_name, COUNT(o.order_id) as total_orders
FROM ORDERS o
JOIN RETAILER r ON o.retailer_id = r.retailer_id
GROUP BY r.retailer_id
ORDER BY total_orders DESC;
