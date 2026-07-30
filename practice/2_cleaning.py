import numpy as np
import pandas as pd

df = pd.read_csv('2_student_scores.csv')

print(len(df))
df = df.drop_duplicates()
print(df.columns.to_list())
print(df.head())

for col in df.columns:
    df[col] = df[col].astype(str)
    df[col] = df[col].str.strip().str.lower()
    df[col] = df[col].str.replace(r'\s+', ' ', regex=True)

print(df['grade'].unique())

df['grade'] = df['grade'].str.strip().str.upper()

df['english_score'] = df['english_score'].astype(float).round(2)
df = df[(df['english_score'] >= 0) & (df['english_score'] <= 100)]
df['english_score'] = df['english_score'].fillna(df['english_score'].mean()).round(2)
df["english_score"] = np.ceil(df["english_score"]).clip(lower=0, upper=100).astype(int)
    
df['math_score'] = df['math_score'].astype(float).round(2)
df = df[df['english_score'].between(0, 100)]
df['math_score'] = df['math_score'].fillna(df['math_score'].mean()).round(2)
df["math_score"] = np.ceil(df["math_score"]).clip(lower=0, upper=100).astype(int)

df['student_id'] = df['student_id'].astype(int)

df['name'] = df['name'].str.strip().str.title()
df['name'] = df['name'].str.replace(r'\s+', ' ', regex=True)
df['name'] = df['name'].str.replace(r'[^a-zA-Z\s]', '', regex=True)

bool_map = {
    "male": "Male",
    "m": "Male",
    "female": "Female",
    "f": "Female"
}
df["gender"] = df["gender"].astype(str).str.lower().str.strip().map(bool_map)    

print("=" * 50)
print("DATA VALIDATION REPORT")
print("=" * 50)

print("\nShape:", end = "  ")
print(df.shape)
print("\nDuplicate Rows:", end = "  ")
print(df.duplicated().sum())
print("\nUnique Values:")
print(df.nunique())
print("\nMissing Values:",)
print(df.isnull().sum())




print("\nData Types:")
print(df.dtypes)

print(df.head())

# print("\nSummary:")
# print(df.describe(include="all"))

print(df.to_string(index=False))

# output = df.to_csv('2_student_scores_cleaned.csv', index=False)
# print(output)