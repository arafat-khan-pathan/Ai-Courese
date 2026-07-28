# Pandas Notes (Quick Syntax Reference)

> Beginner-friendly notes — focus on syntax you'll actually use.

---

## 1. Import

```python
import pandas as pd
```

---

## 2. Core Data Structures

| Structure | Meaning | Create |
|---|---|---|
| `Series` | 1D labeled array | `pd.Series([1,2,3])` |
| `DataFrame` | 2D labeled table | `pd.DataFrame(data)` |

```python
# From a dictionary
df = pd.DataFrame({
    "name": ["Rafi", "Nadia"],
    "age": [22, 21]
})
```

---

## 3. Reading & Writing Files

```python
pd.read_csv("file.csv")
pd.read_excel("file.xlsx")
pd.read_json("file.json")

df.to_csv("out.csv", index=False)
df.to_excel("out.xlsx", index=False)
```

---

## 4. Exploring Data

```python
df.head()        # first 5 rows
df.tail()        # last 5 rows
df.shape         # (rows, columns)
df.info()        # column types, nulls
df.describe()    # stats summary (numeric columns)
df.columns       # column names
df.dtypes        # data type of each column
```

---

## 5. Selecting Data

```python
df["age"]              # select one column (Series)
df[["name","age"]]     # select multiple columns
df.loc[0]               # select row by label/index
df.iloc[0]               # select row by position
df.loc[0, "name"]        # specific cell (label-based)
df.iloc[0, 1]             # specific cell (position-based)
df[df["age"] > 21]       # conditional filtering
```

---

## 6. Adding / Modifying / Dropping

```python
df["new_col"] = df["age"] * 2         # add new column
df.rename(columns={"age":"years"})    # rename column
df.drop("age", axis=1)                # drop column
df.drop(0, axis=0)                    # drop row by index
df.drop_duplicates()                  # remove duplicate rows
```

> Most of these return a **new** DataFrame unless you pass `inplace=True`.

---

## 7. Handling Missing Data

```python
df.isnull()             # True/False for missing values
df.isnull().sum()       # count missing values per column
df.dropna()              # drop rows with any missing value
df.fillna(0)              # replace missing values with 0
```

---

## 8. Sorting & Grouping

```python
df.sort_values("age")                  # sort by column (ascending)
df.sort_values("age", ascending=False) # descending

df.groupby("dept")["salary"].mean()    # group + aggregate
df.groupby("dept").agg({"salary":"sum","age":"mean"})
```

---

## 9. Merging & Joining

```python
pd.concat([df1, df2])                     # stack DataFrames
pd.merge(df1, df2, on="id")               # SQL-style join
pd.merge(df1, df2, on="id", how="left")   # left/right/outer/inner
```

---

## 10. Useful Functions

| Function | Meaning |
|---|---|
| `df["col"].unique()` | Unique values in a column |
| `df["col"].nunique()` | Count of unique values |
| `df["col"].value_counts()` | Frequency of each value |
| `df.apply(func)` | Apply a function across rows/columns |
| `df["col"].map(func)` | Apply function element-wise (Series) |
| `df.reset_index()` | Reset row index |
| `df.set_index("col")` | Set a column as index |

---

## 11. Basic Stats

```python
df["age"].mean()
df["age"].median()
df["age"].std()
df["age"].min() / df["age"].max()
df["age"].sum()
```

---

## Quick Cheat Sheet Summary

```
Read     -> pd.read_csv(), pd.read_excel()
Explore  -> .head(), .info(), .describe(), .shape
Select   -> df["col"], df.loc[], df.iloc[], filtering
Clean    -> .dropna(), .fillna(), .drop_duplicates()
Group    -> df.groupby("col").agg()
Combine  -> pd.concat(), pd.merge()
```
