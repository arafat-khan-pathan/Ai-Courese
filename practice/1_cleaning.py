import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('1_ecommerce_sales.csv')

null_tokens = ["N/A", "NA", "n/a", "NULL", "null", "None", "none", "-", "--", "?", ""]
df = df.replace(null_tokens, np.nan)

print(len(df))
df.columns = df.columns.str.strip()
df.columns = df.columns.str.replace(' ', '_')
df.columns = df.columns.str.lower()
print(df.columns.to_list())
print(df.dtypes)
print(df.head(10))

df["order_id"] = df["order_id"].astype(str)


df["price"] = df["price"].astype(str)
df["price"] = df["price"].str.replace(r"[^0-9.]", "", regex=True)
df["price"] = pd.to_numeric(df["price"], errors="coerce")
df["price"] = df["price"].fillna(df["price"].mean())
df['price'] = df['price'].round(2)
df["price"] = df["price"].map("{:.2f}".format)
df["price"] = df["price"].astype(float)



df["quantity"] = df["quantity"].astype(str)
df["quantity"] = df["quantity"].str.replace(r"[^0-9.]", "", regex=True)
df["quantity"] = pd.to_numeric(df["quantity"], errors="coerce")
df["quantity"] = df["quantity"].fillna(df["quantity"].mean())
df["quantity"] = df["quantity"].astype(int)
df["quantity"] = df["quantity"].fillna(df["quantity"].mean()).round().astype(int)


df["city"] = df["city"].str.strip()
df["city"] = df["city"].str.replace(r"[^a-zA-Z]", "", regex=True)
df['city'] = df['city'].fillna(df["city"].mode()[0])
df['city'] = df['city'].str.title()

#['order_id', 'product', 'category', 'price', 'quantity', 'order_date', 'city']


df = df.dropna(subset=["city", "category", "product"], how="any")
df = df.drop_duplicates(subset=["order_id", "product", "category", "price", "quantity", "order_date", "city"], keep="first")
df = df.reset_index(drop=True)

columns = ["city", "category", "product"]
for col in columns:
    df[col] = df[col].str.strip().str.lower()
    
    
    
df = df.dropna(subset=["order_date"])    
# df["order_date"] = df["order_date"].fillna("Unknown")

# df["order_date"] = pd.to_datetime(
#     df["order_date"], errors="coerce"
# )
# df["order_date"] = pd.to_datetime(df["order_date"])




# print(df.isnull().sum())

print(df.head(10))
print(len(df))
print(df.to_string())






# print(df.dtypes)
# print(df.head(10))
# print(df.isnull().sum())
# df = df['']
print(df["order_date"].dtype)

df["order_date"] = pd.to_datetime(
    df["order_date"],
    format="mixed",
    dayfirst=True
)
df["order_date"] = df["order_date"].dt.strftime("%d-%m-%Y")
print(df["order_date"].dtype)
print(df.to_string())
df["order_date"] = pd.to_datetime(
    df["order_date"],
    format="mixed",
    dayfirst=True
)
today = pd.Timestamp.today()
df = df[df["order_date"] <= today]
df = df.reset_index(drop=True)

df = df.drop_duplicates(subset=["order_id", "product", "category", "price", "quantity", "order_date", "city"], keep="first")    
df = df.reset_index(drop=True)
 
df["order_id"] = df["order_id"].astype(str)
df["order_id"] = df["order_id"].str.strip()
df["order_id"] = df["order_id"].astype(int)


print("=" * 80)
print("=" * 50)
print("DATA VALIDATION REPORT")
print("=" * 50)

print("\nShape:")
print(df.shape)

print("\nMissing Values:")
print(df.isnull().sum())

print("\nDuplicate Rows:")
print(df.duplicated().sum())

print("\nData Types:")
print(df.dtypes)

print("\nSummary:")
print(df.describe(include="all"))


# df.loc[df["price"] <= 0, "price"] = np.nan   # condition false then nan not delet row
# df = df[df["price"] > 0]   #delet entire row

