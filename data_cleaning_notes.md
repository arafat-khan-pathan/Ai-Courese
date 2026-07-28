# Data Cleaning & Processing Notes (CSV / Excel)

> Step-by-step approach + syntax, using Pandas.

---

## 0. Setup

```python
import pandas as pd
import numpy as np

df = pd.read_csv("file.csv")          # for CSV
df = pd.read_excel("file.xlsx")       # for Excel
```

---

## The General Workflow (follow in order)

```
1. Load data
2. First look (shape, info, head)
3. Fix column names
4. Handle missing values
5. Fix data types
6. Remove duplicates
7. Handle outliers
8. Fix inconsistent text/categories
9. Feature-level fixes (dates, units)
10. Final check + save clean file
```

---

## 1. First Look at the Data

```python
df.shape          # (rows, columns)
df.head()         # first 5 rows
df.tail()         # last 5 rows
df.info()         # types + missing count
df.describe()     # stats for numeric columns
df.columns        # list of column names
df.dtypes         # data type of each column
```

**Goal:** understand size, types, and spot obvious problems.

---

## 2. Fix Column Names

```python
df.columns = df.columns.str.strip()          # remove extra spaces
df.columns = df.columns.str.lower()          # lowercase
df.columns = df.columns.str.replace(" ", "_") # spaces -> underscore

# or rename specific ones
df.rename(columns={"Old Name": "new_name"}, inplace=True)
```

**Goal:** clean, consistent, easy-to-type column names.

---

## 3. Handle Missing Values

```python
df.isnull().sum()              # count missing per column
df.isnull().sum() / len(df)    # % missing per column
```

### Options to fix:

```python
df.dropna()                        # drop rows with ANY missing value
df.dropna(subset=["col"])          # drop rows missing in a specific column
df.dropna(thresh=5)                # keep rows with at least 5 non-null values

df.fillna(0)                        # fill with a fixed value
df["col"].fillna(df["col"].mean(), inplace=True)   # fill with mean
df["col"].fillna(df["col"].median(), inplace=True) # fill with median
df["col"].fillna(df["col"].mode()[0], inplace=True) # fill with most frequent (categorical)
df["col"].fillna(method="ffill", inplace=True)     # forward fill
df["col"].fillna(method="bfill", inplace=True)     # backward fill
```

> **Rule of thumb:** numeric column → mean/median. Categorical column → mode or `"Unknown"`.

---

## 4. Fix Data Types

```python
df["age"] = df["age"].astype(int)
df["price"] = df["price"].astype(float)
df["date"] = pd.to_datetime(df["date"])
df["category"] = df["category"].astype("category")
```

**Common issue:** numbers stored as text (e.g., `"1,200"` or `"$500"`).

```python
df["price"] = df["price"].str.replace(",", "").str.replace("$", "")
df["price"] = df["price"].astype(float)
```

---

## 5. Remove Duplicates

```python
df.duplicated().sum()          # count duplicate rows
df.drop_duplicates(inplace=True)
df.drop_duplicates(subset=["id"], inplace=True)   # based on specific column
```

---

## 6. Handle Outliers

```python
df["col"].describe()   # check min/max/quartiles first

# IQR method
Q1 = df["col"].quantile(0.25)
Q3 = df["col"].quantile(0.75)
IQR = Q3 - Q1
lower = Q1 - 1.5 * IQR
upper = Q3 + 1.5 * IQR

df_clean = df[(df["col"] >= lower) & (df["col"] <= upper)]
```

> Only remove outliers if they're genuinely errors — not all outliers are bad data.

---

## 7. Fix Inconsistent Text / Categories

```python
df["col"] = df["col"].str.strip()          # remove whitespace
df["col"] = df["col"].str.lower()          # normalize case
df["col"] = df["col"].str.title()          # "john doe" -> "John Doe"

df["col"].unique()                          # see all unique values
df["col"] = df["col"].replace({
    "Dhaka ": "Dhaka",
    "dhaka": "Dhaka"
})                                           # fix typos/inconsistent labels
```

---

## 8. Dates & Units

```python
df["date"] = pd.to_datetime(df["date"], errors="coerce")  # invalid dates -> NaT
df["year"] = df["date"].dt.year
df["month"] = df["date"].dt.month
df["weekday"] = df["date"].dt.day_name()
```

---

## 9. Detect & Handle Wrong/Invalid Values

```python
df[df["age"] < 0]              # find impossible values
df = df[df["age"] >= 0]        # filter them out

df["col"].value_counts()       # spot rare/weird categories
```

---

## 10. Final Check

```python
df.isnull().sum()      # should be 0 (or intentional)
df.duplicated().sum()  # should be 0
df.info()               # confirm correct dtypes
df.describe()            # confirm ranges make sense
```

---

## 11. Save Cleaned File

```python
df.to_csv("cleaned_data.csv", index=False)
df.to_excel("cleaned_data.xlsx", index=False)
```

---

## Quick Cheat Sheet Summary

```
Load     -> pd.read_csv() / pd.read_excel()
Inspect  -> .info(), .describe(), .isnull().sum()
Rename   -> df.columns.str.strip().str.lower()
Missing  -> .dropna() / .fillna(mean/median/mode)
Types    -> .astype(), pd.to_datetime()
Dupes    -> .drop_duplicates()
Outliers -> IQR method (Q1, Q3, IQR)
Text     -> .str.strip(), .str.lower(), .replace()
Save     -> df.to_csv() / df.to_excel()
```
