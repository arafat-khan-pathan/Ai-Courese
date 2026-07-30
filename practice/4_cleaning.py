import numpy as np 
import pandas as pd


    
df = pd.read_csv("4_customer_feedback.csv")
df = df.reset_index(drop=True)
print(df.columns.to_list())
df.columns = df.columns.str.lower()
print(len(df))
df = df.drop_duplicates()
print(len(df))
null_tokens = ["N/A", "NA", "n/a", "NULL", "null", "None", "none", "-", "--", "?", ""]
df = df.replace(null_tokens, np.nan)
print(df.head())

df.columns = df.columns.str.strip()
df.columns = df.columns.str.replace(r'\s+', ' ', regex=True)

#rating
df['rating'] = df['rating'].astype(str).str.strip().str.replace(r'\s+', ' ', regex=True)
df["rating"] = df["rating"].astype(float)
df["rating"] = np.ceil(df["rating"]).clip(upper=5)
df["rating"] = df["rating"].fillna(df["rating"].mean()).round(2).astype(int)

#sentiment
df['sentiment'] = df['sentiment'].fillna(df["sentiment"].mode()[0] if not df["sentiment"].mode().empty else "Neutral")
df['sentiment'] = df['sentiment'].astype(str).str.strip().str.replace(r'\s+', ' ', regex=True).str.title()


# comment
df['comment'] = df['comment'].astype('string').str.strip().str.replace(r'\s+', ' ', regex=True).str.lower()
df['comment'] = df['comment'].fillna("no comment").str.lower()

#product_area
df['product_area'] = df['product_area'].astype(str).str.strip().str.replace(r'\s+', ' ', regex=True).str.title()
# df = df.dropna(subset=["product_area"])
df['product_area'] = df['product_area'].fillna(df['product_area'].mode()[0])



print(df.dtypes)
print(df.isnull().sum())


print(df['comment'].value_counts())
print(df['comment'].value_counts())


df.to_csv("4_cleaned_customer_feedback.csv", index=False)
# print(df.to_string())