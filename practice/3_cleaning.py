import numpy as np 
import pandas as pd

df = pd.read_csv("3_employee_hr.csv")

df = df.reset_index(drop=True)
df = df.drop_duplicates()

null_tokens = ["N/A", "NA", "n/a", "NULL", "null", "None", "none", "-", "--", "?", ""]

df.columns = df.columns.str.lower()
print(df.columns.to_list())

df = df.replace(null_tokens, np.nan)
print(df.head())


### Age

df["age"] = df["age"].fillna(df["age"].mean()).round().astype(int).abs()
# df.loc[df["age"] < 18, "age"] = 0
# df.loc[df["age"] > 100, "age"] = 0
df.loc[df["age"] < 18, "age"] = df["age"] + 18
df.loc[df["age"] > 100, "age"] = df["age"] - 100

# df["age"] = df["age"].fillna(df["age"].mean()).round().astype(int).abs()

### department

df["department"] = df["department"].str.replace(r"[^a-zA-Z]", "", regex=True)
df['department'] = df['department'].str.title()
df['department'] = df['department'].str.strip()
df['department'] = df['department'].fillna(df['department'].mode()[0])


### salary

df["salary"] = df["salary"].str.replace(r"[^0-9]", "", regex=True)
#df["salary"] = df["salary"].str.replace(r"\D", "", regex=True)
df['salary'] = df['salary'].str.strip()
df['salary'] = np.ceil(df['salary'].astype(float)).astype(int)
df["salary"] = df["salary"].fillna(df["salary"].mean()).round().astype(int)
# df["salary"] = df["salary"].astype(str) + "$"
# df["salary"] = df["salary"].map("{:,.0f}$".format)
# df.rename(columns={"salary": "salary_$"}, inplace=True)


### join_date

df["join_date"] = pd.to_datetime(
    df["join_date"],
    format="mixed",
    dayfirst=True,
    errors="coerce"

)


today = pd.Timestamp.today().normalize()
df.loc[df["join_date"] > today, "join_date"] = pd.NaT
df = df.dropna(subset=["join_date"])

# df["join_date"] = pd.to_datetime(df["join_date"], format="%d-%m-%Y", errors="coerce")




### emp_code

df.loc[
    ~df["emp_code"].str.match(r"^EMP\d+$", na=False),
    "emp_code"
] = np.nan
df = df.dropna(subset=["emp_code"])




print("=" * 50)
print("DATA VALIDATION REPORT")
print("=" * 50)

print("\nShape:")
print(df.shape)

print("\nMissing Values:", )
print(df.isnull().sum())

print("\nDuplicate Rows:" , end = " ")
print(df.duplicated().sum())

print("\nData Types:")
print(df.dtypes)
# print (df['emp_code'].to_string())

df.to_csv("3_employee_hr_cleaned.csv", index=False)
print(df.to_string())
