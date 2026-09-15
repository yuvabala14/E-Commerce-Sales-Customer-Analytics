import pandas as pd
import matplotlib.pyplot as plt

# Load datasets
orders = pd.read_csv(r"C:\Users\yuvab\Downloads\E-commerce_data_analytics_project\ecommerce_project_dataset\orders.csv")

products = pd.read_csv(r"C:\Users\yuvab\Downloads\E-commerce_data_analytics_project\ecommerce_project_dataset\products.csv")

customers = pd.read_csv(r"C:\Users\yuvab\Downloads\E-commerce_data_analytics_project\ecommerce_project_dataset\customers.csv")

# Display first 5 rows
print("ORDERS")
print(orders.head())

print("\nPRODUCTS")
print(products.head())

print("\nCUSTOMERS")
print(customers.head())# Check dataset sizes
print("\n--- DATASET SIZES ---")

print("Orders:", orders.shape)
print("Products:", products.shape)
print("Customers:", customers.shape)


# Check column names
print("\n--- COLUMN NAMES ---")

print("Orders columns:")
print(orders.columns.tolist())

print("\nProducts columns:")
print(products.columns.tolist())

print("\nCustomers columns:")
print(customers.columns.tolist())

print("\n--- DATASET SIZE ---")

print("Orders:", orders.shape)
print("Products:", products.shape)
print("Customers:", customers.shape)

# Check data types
print("\n--- DATA TYPES ---")

print("\nOrders:")
print(orders.dtypes)

print("\nProducts:")
print(products.dtypes)

print("\nCustomers:")
print(customers.dtypes)

# Check missing values
print("\n--- MISSING VALUES ---")

print("\nOrders:")
print(orders.isnull().sum())

print("\nProducts:")
print(products.isnull().sum())

print("\nCustomers:")
print(customers.isnull().sum())


# Check duplicate rows
print("\n--- DUPLICATE ROWS ---")

print("Orders duplicates:", orders.duplicated().sum())
print("Products duplicates:", products.duplicated().sum())
print("Customers duplicates:", customers.duplicated().sum())

# ==========================================
# STEP 6 - EXPLORE PRODUCT DATA
# ==========================================

print("\n--- PRODUCT CATEGORIES ---")
print(products["Category"].value_counts())

print("\n--- PRODUCT PRICE SUMMARY ---")
print(products[["Unit_Price", "Cost_Price"]].describe())

print("\n--- PRODUCT INFORMATION ---")
print(products.head(10))

# ==========================================
# STEP 7 - EXPLORE CUSTOMER DATA
# ==========================================

print("\n--- CUSTOMER GENDER ---")
print(customers["Gender"].value_counts())

print("\n--- CUSTOMER AGE SUMMARY ---")
print(customers["Age"].describe())

print("\n--- TOP 10 CITIES ---")
print(customers["City"].value_counts().head(10))

print("\n--- TOP 10 STATES ---")
print(customers["State"].value_counts().head(10))

# ==========================================
# STEP 8 - CHECK DATASET RELATIONSHIPS
# ==========================================

print("\n--- ORDER DATA ---")
print(orders.head(10))

print("\n--- ORDER LABELS ---")
print(orders["Row Labels"].tolist())

print("\n--- PRODUCT IDs ---")
print(products["Product_ID"].head(20).tolist())

# ==========================================
# STEP 9 - PREPARE ORDERS DATA
# ==========================================

print("\n--- ORDERS BEFORE CLEANING ---")
print(orders)

# Remove Grand Total row
orders_clean = orders[orders["Row Labels"] != "Grand Total"].copy()

print("\n--- ORDERS AFTER REMOVING GRAND TOTAL ---")
print(orders_clean)

print("\nNumber of order products:", len(orders_clean))

# ==========================================
# STEP 10 - BUSINESS KPI ANALYSIS
# ==========================================

print("\n--- BUSINESS KPIs ---")

# Total Sales
total_sales = orders_clean["Sum of Sales"].sum()

# Total Profit
total_profit = orders_clean["Sum of Profit"].sum()

# Overall Profit Margin
profit_margin = (total_profit / total_sales) * 100

print("Total Sales:", total_sales)
print("Total Profit:", total_profit)
print("Overall Profit Margin:", round(profit_margin, 2), "%")

# ==========================================
# STEP 11 - TOP CATEGORIES BY SALES
# ==========================================

print("\n--- TOP CATEGORIES BY SALES ---")

top_sales = orders_clean.sort_values(
    by="Sum of Sales",
    ascending=False
)

print(top_sales[["Row Labels", "Sum of Sales"]])

# ==========================================
# STEP 12 - TOP CATEGORIES BY PROFIT
# ==========================================

print("\n--- TOP CATEGORIES BY PROFIT ---")

top_profit = orders_clean.sort_values(
    by="Sum of Profit",
    ascending=False
)

print(top_profit[["Row Labels", "Sum of Profit"]])


# ==========================================
# STEP 13 - CATEGORY PROFIT MARGIN
# ==========================================

orders_clean["Profit_Margin"] = (
    orders_clean["Sum of Profit"] /
    orders_clean["Sum of Sales"]
) * 100

print("\n--- PROFIT MARGIN BY CATEGORY ---")

print(
    orders_clean[
        ["Row Labels", "Sum of Sales", "Sum of Profit", "Profit_Margin"]
    ].sort_values(
        by="Profit_Margin",
        ascending=False
    )
)


# ==========================================
# STEP 14 - CATEGORY PERFORMANCE ANALYSIS
# ==========================================

print("\n--- CATEGORY PERFORMANCE ---")

# Calculate sales and profit by category
category_analysis = products.groupby("Category").agg(
    Total_Sales=("Unit_Price", "sum"),
    Total_Cost=("Cost_Price", "sum")
).reset_index()

# Calculate profit
category_analysis["Profit"] = (
    category_analysis["Total_Sales"] -
    category_analysis["Total_Cost"]
)

# Calculate profit margin
category_analysis["Profit_Margin_%"] = (
    category_analysis["Profit"] /
    category_analysis["Total_Sales"] * 100
)

# Sort by profit
category_analysis = category_analysis.sort_values(
    by="Profit",
    ascending=False
)

print(category_analysis)

# ==========================================
# STEP 15 - COMBINE ORDERS AND PRODUCTS
# ==========================================

print("\n--- COMBINING ORDERS AND PRODUCTS ---")

# Rename order columns
orders_analysis = orders_clean.rename(columns={
    "Row Labels": "Product_Name",
    "Sum of Sales": "Sales",
    "Sum of Profit": "Profit"
})

# Merge orders with product information
orders_products = orders_analysis.merge(
    products,
    on="Product_Name",
    how="left"
)

print("\n--- COMBINED DATA ---")
print(orders_products)

print("\n--- COMBINED COLUMNS ---")
print(orders_products.columns.tolist())

# ==========================================
# STEP 16 - TOP SELLING PRODUCTS
# ==========================================

print("\n--- TOP 10 PRODUCTS BY SALES ---")

top_products = orders_products.sort_values(
    by="Sales",
    ascending=False
)

print(
    top_products[
        ["Product_Name", "Category", "Sales", "Profit"]
    ].head(10)
)

# ==========================================
# STEP 15A - CHECK DUPLICATE PRODUCT NAMES
# ==========================================

print("\n--- DUPLICATE PRODUCT NAMES ---")

duplicate_products = products[
    products["Product_Name"].duplicated(keep=False)
].sort_values("Product_Name")

print(duplicate_products)

print("\nNumber of duplicate product rows:",
      products["Product_Name"].duplicated().sum())

# ==========================================
# STEP 15B - FIX DUPLICATE PRODUCT NAMES
# ==========================================

print("\n--- PREPARING PRODUCT DATA ---")

# Create one row for each product name
products_summary = products.groupby(
    "Product_Name"
).agg(
    Category=("Category", "first"),
    Unit_Price=("Unit_Price", "mean"),
    Cost_Price=("Cost_Price", "mean")
).reset_index()

print("\n--- PRODUCT SUMMARY ---")
print(products_summary)

print("\nNumber of unique products:",
      len(products_summary))

# ==========================================
# STEP 16 - MERGE ORDERS WITH PRODUCTS
# ==========================================

print("\n--- MERGING ORDER AND PRODUCT DATA ---")

orders_analysis = orders_clean.rename(columns={
    "Row Labels": "Product_Name",
    "Sum of Sales": "Sales",
    "Sum of Profit": "Profit"
})

orders_products = orders_analysis.merge(
    products_summary,
    on="Product_Name",
    how="left"
)

print("\n--- MERGED DATA ---")
print(orders_products)

print("\nMerged dataset shape:")
print(orders_products.shape)

# ==========================================
# STEP 17 - TOP PRODUCTS ANALYSIS
# ==========================================

print("\n--- TOP PRODUCTS BY SALES ---")

top_sales = orders_products.sort_values(
    by="Sales",
    ascending=False
)

print(
    top_sales[
        ["Product_Name", "Category", "Sales", "Profit"]
    ].to_string(index=False)
)


print("\n--- TOP PRODUCTS BY PROFIT ---")

top_profit = orders_products.sort_values(
    by="Profit",
    ascending=False
)

print(
    top_profit[
        ["Product_Name", "Category", "Sales", "Profit"]
    ].to_string(index=False)
)


# ==========================================
# STEP 18 - SALES VS PROFIT ANALYSIS
# ==========================================

print("\n--- SALES VS PROFIT ---")

sales_profit = orders_products[
    ["Product_Name", "Category", "Sales", "Profit", "Profit_Margin"]
].sort_values(
    by="Sales",
    ascending=False
)

print(sales_profit.to_string(index=False))

# Step 19: Category Performance

category_performance = orders_products.groupby("Category").agg(
    Total_Sales=("Sales", "sum"),
    Total_Profit=("Profit", "sum")
).reset_index()

category_performance["Profit_Margin_%"] = (
    category_performance["Total_Profit"] /
    category_performance["Total_Sales"] * 100
)

category_performance = category_performance.sort_values(
    "Total_Sales",
    ascending=False
)

print(category_performance.to_string(index=False))

# Step 20: Customer Demographic Analysis

# Gender distribution
gender_analysis = customers["Gender"].value_counts()

print("\nCustomer Gender Distribution:")
print(gender_analysis)


# Age analysis
print("\nCustomer Age Statistics:")
print(customers["Age"].describe())


# State distribution
state_analysis = customers["State"].value_counts()

print("\nCustomers by State:")
print(state_analysis)


# City distribution
city_analysis = customers["City"].value_counts().head(10)

print("\nTop 10 Cities by Customer Count:")
print(city_analysis)

# Step 21: Customer Age Groups

customers["Age_Group"] = pd.cut(
    customers["Age"],
    bins=[0, 25, 35, 45, 55, 100],
    labels=["18-25", "26-35", "36-45", "46-55", "56+"]
)

age_group_analysis = customers["Age_Group"].value_counts().sort_index()

print("\nCustomers by Age Group:")
print(age_group_analysis)

# Step 22: Customer Gender Percentage

gender_analysis = customers["Gender"].value_counts()

gender_percentage = (
    customers["Gender"]
    .value_counts(normalize=True)
    .mul(100)
    .round(2)
)

print("\nCustomer Gender Count:")
print(gender_analysis)

print("\nCustomer Gender Percentage:")
print(gender_percentage)

# Step 23: Sales by Product

sales_by_product = orders_products.sort_values(
    by="Sales",
    ascending=True
)

plt.figure(figsize=(10, 6))

plt.barh(
    sales_by_product["Product_Name"],
    sales_by_product["Sales"]
)

plt.xlabel("Sales")
plt.ylabel("Product")
plt.title("Sales by Product")

plt.tight_layout()
plt.show()


# Step 24: Profit by Product

profit_by_product = orders_products.sort_values(
    by="Profit",
    ascending=True
)

plt.figure(figsize=(10, 6))

plt.barh(
    profit_by_product["Product_Name"],
    profit_by_product["Profit"]
)

plt.xlabel("Profit")
plt.ylabel("Product")
plt.title("Profit by Product")

plt.tight_layout()
plt.show()


# Step 25: Profit Margin by Product

margin_by_product = orders_products.sort_values(
    by="Profit_Margin",
    ascending=True
)

plt.figure(figsize=(10, 6))

plt.barh(
    margin_by_product["Product_Name"],
    margin_by_product["Profit_Margin"]
)

plt.xlabel("Profit Margin (%)")
plt.ylabel("Product")
plt.title("Profit Margin by Product")

plt.tight_layout()
plt.show()

# Step 26: Sales vs Profit


plt.figure(figsize=(10, 6))

plt.scatter(
    orders_products["Sales"],
    orders_products["Profit"]
)

plt.xlabel("Sales")
plt.ylabel("Profit")
plt.title("Sales vs Profit")

plt.tight_layout()
plt.show()


# Step 27: Category-wise Sales and Profit

category_analysis = orders_products.groupby("Category").agg(
    Total_Sales=("Sales", "sum"),
    Total_Profit=("Profit", "sum")
).reset_index()

print("\nCategory-wise Sales and Profit:")
print(category_analysis)

# Sales by Category
plt.figure(figsize=(10, 6))

plt.bar(
    category_analysis["Category"],
    category_analysis["Total_Sales"]
)

plt.xlabel("Category")
plt.ylabel("Total Sales")
plt.title("Sales by Category")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# Profit by Category
plt.figure(figsize=(10, 6))

plt.bar(
    category_analysis["Category"],
    category_analysis["Total_Profit"]
)

plt.xlabel("Category")
plt.ylabel("Total Profit")
plt.title("Profit by Category")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# Step 28: Customer Age Group Analysis

age_group_analysis = customers["Age_Group"].value_counts().sort_index()

print("\nCustomers by Age Group:")
print(age_group_analysis)

plt.figure(figsize=(10, 6))

plt.bar(
    age_group_analysis.index.astype(str),
    age_group_analysis.values
)

plt.xlabel("Age Group")
plt.ylabel("Number of Customers")
plt.title("Customers by Age Group")

plt.tight_layout()
plt.show()

# Step 29: Customer Gender Analysis

gender_analysis = customers["Gender"].value_counts()

print("\nCustomer Gender Analysis:")
print(gender_analysis)

plt.figure(figsize=(8, 5))

plt.bar(
    gender_analysis.index,
    gender_analysis.values
)

plt.xlabel("Gender")
plt.ylabel("Number of Customers")
plt.title("Customer Distribution by Gender")

plt.tight_layout()
plt.show()


# Step 30: Export Analysis Data

orders_products.to_csv(
    "../output/orders_products_analysis.csv",
    index=False
)

category_analysis.to_csv(
    "../output/category_analysis.csv",
    index=False
)

age_group_analysis.to_csv(
    "../output/age_group_analysis.csv"
)

gender_analysis.to_csv(
    "../output/gender_analysis.csv"
)

print("\nStep 30 completed!")
print("Analysis files exported successfully.")
