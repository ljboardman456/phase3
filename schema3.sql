-- total sales per day
SELECT DATE(o.order_time) AS day, SUM(b.total_amount) AS total_sales
FROM Orders o
JOIN Bills b ON o.id = b.order_id
GROUP BY day;

-- most popular menu items
SELECT mi.name, SUM(od.quantity) AS total_sold
FROM OrderDetails od
JOIN MenuItems mi ON od.menu_item_id = mi.id
GROUP BY mi.name
ORDER BY total_sold DESC
LIMIT 5;
