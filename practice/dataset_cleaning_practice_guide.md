# Dataset Cleaning Practice Guide

> 5 practice CSV files (already generated for you) + step-by-step cleaning
> instructions for each + 5 real-world dataset links for extra practice.

---

## Your 5 Practice CSV Files

| # | File | Problems Inside |
|---|---|---|
| 1 | `1_ecommerce_sales.csv` | Missing values, price with `$` symbol, inconsistent city names, duplicates |
| 2 | `2_student_scores.csv` | Invalid scores (negative/>100), missing values, inconsistent gender/grade labels, duplicates |
| 3 | `3_employee_hr.csv` | Mixed date formats, salary with commas, inconsistent department names, invalid age |
| 4 | `4_customer_feedback.csv` | Invalid rating (out of range), missing comments, inconsistent sentiment case, duplicates |
| 5 | `5_weather_sensor.csv` | Sensor error values (extreme outliers), missing values, `"NA"` as string instead of null |

> These were generated to mimic **real messy data** so you can practice every cleaning skill.

---

# General Approach (apply to ANY dataset)

```
1. Load & look          -> df.shape, df.info(), df.head()
2. Understand columns    -> what should each column contain?
3. Check missing values  -> df.isnull().sum()
4. Check duplicates      -> df.duplicated().sum()
5. Check data types      -> df.dtypes
6. Check for invalid/out-of-range values
7. Fix text inconsistencies (case, spacing, typos)
8. Fix date/number formats
9. Handle outliers
10. Re-check everything, then save cleaned file
```

Always ask: **"What should this column look like when it's correct?"** — that answer drives every fix.

---

## 1. `1_ecommerce_sales.csv` — E-commerce Sales

### Step-by-step

```python
import pandas as pd
df = pd.read_csv("1_ecommerce_sales.csv")

# 1. First look
df.info()
df.isnull().sum()
df.duplicated().sum()

# 2. Remove exact duplicate rows
df = df.drop_duplicates()

# 3. Fix price column (remove $ sign, convert to float)
df["price"] = df["price"].astype(str).str.replace("$", "", regex=False)
df["price"] = pd.to_numeric(df["price"], errors="coerce")

# 4. Fill missing price with column median
df["price"] = df["price"].fillna(df["price"].median())

# 5. Fill missing quantity with 1 (reasonable default) or drop
df["quantity"] = df["quantity"].fillna(df["quantity"].median())

# 6. Fix city names (strip spaces, standardize case)
df["city"] = df["city"].str.strip().str.title()
df["city"] = df["city"].fillna("Unknown")

# 7. Fix date column (handle two formats)
df["order_date"] = pd.to_datetime(df["order_date"], errors="coerce", dayfirst=True)

# 8. Fill missing product name
df["product"] = df["product"].fillna("Unknown Product")

# 9. Final check
df.isnull().sum()
df.info()

df.to_csv("1_ecommerce_sales_cleaned.csv", index=False)
```

**Key skill practiced:** currency string cleaning, mixed date formats, text standardization.

---

## 2. `2_student_scores.csv` — Student Exam Scores

### Step-by-step

```python
df = pd.read_csv("2_student_scores.csv")

# 1. Remove duplicates
df = df.drop_duplicates()

# 2. Fix invalid scores (must be 0–100)
df.loc[(df["math_score"] < 0) | (df["math_score"] > 100), "math_score"] = None
df["math_score"] = df["math_score"].fillna(df["math_score"].median())

# 3. Fill missing english_score
df["english_score"] = df["english_score"].fillna(df["english_score"].mean())

# 4. Standardize gender column
df["gender"] = df["gender"].str.strip().str.upper()
df["gender"] = df["gender"].replace({"MALE": "M", "FEMALE": "F"})

# 5. Standardize grade column
df["grade"] = df["grade"].str.strip().str.upper()

# 6. Check final unique values
df["gender"].unique()
df["grade"].unique()

df.to_csv("2_student_scores_cleaned.csv", index=False)
```

**Key skill practiced:** range validation, category standardization (`M`/`Male`/`m` → one label).

---

## 3. `3_employee_hr.csv` — Employee HR Data

### Step-by-step

```python
df = pd.read_csv("3_employee_hr.csv")

# 1. Remove duplicates
df = df.drop_duplicates()

# 2. Fix salary (remove commas, convert to numeric)
df["salary"] = df["salary"].astype(str).str.replace(",", "", regex=False)
df["salary"] = pd.to_numeric(df["salary"], errors="coerce")

# 3. Fix department names (strip + standardize case)
df["department"] = df["department"].str.strip().str.title()

# 4. Fix join_date — multiple formats in the same column
df["join_date"] = pd.to_datetime(df["join_date"], errors="coerce")
# if many fail, try format-by-format:
# df["join_date"] = pd.to_datetime(df["join_date"], format="%d-%m-%Y", errors="coerce")

# 5. Fix invalid age (negative or missing)
df.loc[df["age"] < 0, "age"] = None
df["age"] = df["age"].fillna(df["age"].median())

# 6. Final check
df.isnull().sum()
df.dtypes

df.to_csv("3_employee_hr_cleaned.csv", index=False)
```

**Key skill practiced:** multi-format date parsing, comma-separated numbers, invalid numeric values.

---

## 4. `4_customer_feedback.csv` — Customer Feedback / Survey

### Step-by-step

```python
df = pd.read_csv("4_customer_feedback.csv")

# 1. Remove duplicates
df = df.drop_duplicates()

# 2. Fix rating (valid range 1–5)
df.loc[(df["rating"] < 1) | (df["rating"] > 5), "rating"] = None
df["rating"] = df["rating"].fillna(df["rating"].median())

# 3. Standardize sentiment text
df["sentiment"] = df["sentiment"].str.strip().str.title()

# 4. Standardize product_area text
df["product_area"] = df["product_area"].str.strip().str.title()

# 5. Handle missing/placeholder comments
df["comment"] = df["comment"].replace("N/A", None)
df["comment"] = df["comment"].fillna("No comment")
df["comment"] = df["comment"].str.strip()

df.to_csv("4_customer_feedback_cleaned.csv", index=False)
```

**Key skill practiced:** placeholder-value detection (`"N/A"` isn't `NaN` by default), text trimming.

---

## 5. `5_weather_sensor.csv` — Weather / Sensor Data

### Step-by-step

```python
df = pd.read_csv("5_weather_sensor.csv")

# 1. Remove duplicates
df = df.drop_duplicates()

# 2. Convert timestamp
df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce")

# 3. Fix sensor errors in temperature (realistic range: -10 to 50 °C)
df.loc[(df["temperature_c"] < -10) | (df["temperature_c"] > 50), "temperature_c"] = None
df["temperature_c"] = df["temperature_c"].fillna(df["temperature_c"].mean())

# 4. Fill missing humidity
df["humidity_pct"] = df["humidity_pct"].fillna(df["humidity_pct"].median())

# 5. Fix rainfall column ("NA" string -> real NaN -> fill)
df["rainfall_mm"] = pd.to_numeric(df["rainfall_mm"], errors="coerce")
df["rainfall_mm"] = df["rainfall_mm"].fillna(0)

# 6. Final check
df.describe()

df.to_csv("5_weather_sensor_cleaned.csv", index=False)
```

**Key skill practiced:** sensor/outlier detection using realistic domain ranges, `"NA"` string trap.

---

# Extra Practice: 5 Real-World Messy Datasets (Kaggle)

| # | Dataset | Link |
|---|---|---|
| 1 | Dirty dataset — concert tours (irregular formatting, missing entries) | https://www.kaggle.com/datasets/amruthayenikonda/dirty-dataset-to-practice-data-cleaning |
| 2 | Movies dataset (inconsistent ratings, mixed genres, nulls) | https://www.kaggle.com/datasets/bharatnatrayn/movies-dataset-for-feature-extracion-prediction |
| 3 | Food choices survey (coded responses, missing nutrition data) | https://www.kaggle.com/datasets/borapajo/food-choices |
| 4 | Data Science jobs on Glassdoor (salary in text, duplicates) | https://www.kaggle.com/datasets/rashikrahmanpritom/data-science-job-posting-on-glassdoor |
| 5 | Audible dataset (scraped, uncleaned) | https://www.kaggle.com/datasets/snehangsude/audible-dataset |

> You'll need a free Kaggle account to download. Click **Download** on each page, or use the Kaggle API (`kaggle datasets download -d <owner/dataset>`).

---

# Cleaning Checklist (use for every new dataset)

```
[ ] Loaded data and checked shape/info
[ ] Checked and removed duplicate rows
[ ] Checked missing values per column
[ ] Decided fill strategy per column (mean/median/mode/drop)
[ ] Fixed data types (numbers stored as text, dates as text)
[ ] Standardized text columns (case, whitespace, typos)
[ ] Checked for invalid/impossible values (negative age, rating > 5, etc.)
[ ] Checked for outliers using domain knowledge or IQR
[ ] Renamed columns to be clean and consistent
[ ] Re-verified with .info() / .isnull().sum() / .describe()
[ ] Saved cleaned file separately (never overwrite raw data)
```

> **Golden rule:** never overwrite your raw/original file. Always save cleaned data as a new file (`_cleaned.csv`) so you can compare or redo steps if something goes wrong.
