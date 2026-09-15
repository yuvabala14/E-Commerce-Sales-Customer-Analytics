-- E-Commerce Sales & Customer Analytics
-- SQL Analysis Queries
-- Database: ecommerce_analytics
-- MySQL 8.0

CREATE DATABASE IF NOT EXISTS ecommerce_analytics;
USE ecommerce_analytics;

-- 1. Check imported tables
SHOW TABLES;

-- 2. Top products by sales
SELECT Product_Name, Sales
FROM orders_analysis
ORDER BY Sales DESC;

-- 3. Top products by profit
SELECT Product_Name, Profit
FROM orders_analysis
ORDER BY Profit DESC;

-- 4. Top products by profit margin
SELECT Product_Name, ROUND(Profit_Margin, 2) AS Profit_Margin_Percent
FROM orders_analysis
ORDER BY Profit_Margin DESC;

-- 5. Sales by category
SELECT Category, ROUND(SUM(Sales), 2) AS Total_Sales
FROM orders_analysis
GROUP BY Category
ORDER BY Total_Sales DESC;

-- 6. Profit by category
SELECT Category, ROUND(SUM(Profit), 2) AS Total_Profit
FROM orders_analysis
GROUP BY Category
ORDER BY Total_Profit DESC;

-- 7. Sales, profit and margin by category
SELECT
    Category,
    ROUND(SUM(Sales), 2) AS Total_Sales,
    ROUND(SUM(Profit), 2) AS Total_Profit,
    ROUND(SUM(Profit) / NULLIF(SUM(Sales), 0) * 100, 2) AS Profit_Margin_Percent
FROM orders_analysis
GROUP BY Category
ORDER BY Total_Sales DESC;

-- 8. Customer count by state
SELECT State, COUNT(DISTINCT Customer_ID) AS Customer_Count
FROM customers
GROUP BY State
ORDER BY Customer_Count DESC;

-- 9. Top 10 cities by customer count
SELECT City, COUNT(DISTINCT Customer_ID) AS Customer_Count
FROM customers
GROUP BY City
ORDER BY Customer_Count DESC
LIMIT 10;

-- 10. Customers by age group
SELECT
    CASE
        WHEN Age <= 25 THEN '18-25'
        WHEN Age <= 35 THEN '26-35'
        WHEN Age <= 45 THEN '36-45'
        WHEN Age <= 55 THEN '46-55'
        ELSE '56+'
    END AS Age_Group,
    COUNT(DISTINCT Customer_ID) AS Customer_Count
FROM customers
GROUP BY Age_Group
ORDER BY
    CASE Age_Group
        WHEN '18-25' THEN 1
        WHEN '26-35' THEN 2
        WHEN '36-45' THEN 3
        WHEN '46-55' THEN 4
        ELSE 5
    END;

-- 11. Customer gender distribution
SELECT
    Gender,
    COUNT(DISTINCT Customer_ID) AS Customer_Count,
    ROUND(
        COUNT(DISTINCT Customer_ID) * 100.0 /
        (SELECT COUNT(DISTINCT Customer_ID) FROM customers),
        2
    ) AS Customer_Percentage
FROM customers
GROUP BY Gender
ORDER BY Customer_Count DESC;

-- 12. Category with the highest profit margin
SELECT
    Category,
    ROUND(SUM(Sales), 2) AS Total_Sales,
    ROUND(SUM(Profit), 2) AS Total_Profit,
    ROUND(SUM(Profit) / NULLIF(SUM(Sales), 0) * 100, 2) AS Profit_Margin_Percent
FROM orders_analysis
GROUP BY Category
ORDER BY Profit_Margin_Percent DESC
LIMIT 1;

-- 13. Full product performance
SELECT
    Product_Name,
    Category,
    ROUND(Sales, 2) AS Sales,
    ROUND(Profit, 2) AS Profit,
    ROUND(Profit_Margin, 2) AS Profit_Margin_Percent
FROM orders_analysis
ORDER BY Profit DESC;

-- 14. Reusable product performance view
CREATE OR REPLACE VIEW product_performance AS
SELECT
    Product_Name,
    Category,
    ROUND(Sales, 2) AS Sales,
    ROUND(Profit, 2) AS Profit,
    ROUND(Profit_Margin, 2) AS Profit_Margin_Percent
FROM orders_analysis;

-- 15. Verify the view
SELECT * FROM product_performance;

-- DATA LIMITATION:
-- orders_analysis contains aggregated product-level sales/profit.
-- It does not contain Customer_ID or order dates.
-- Therefore, customer demographics should not be joined to product sales
-- without a valid transaction-level relationship.
