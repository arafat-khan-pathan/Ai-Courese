# Data Cleaning — Master Reference (Pandas + NumPy)

One ordered file. Follow top to bottom — order matters (e.g. you can't fix duplicates
before fixing text case, or you'll miss hidden duplicates).
Replace `df`, `col`, `price` etc. with YOUR real column names.

```
1.  Load data
2.  First inspection
3.  Fix column names
4.  Standardize missing-value tokens
5.  Handle missing values (drop/fill)
6.  Fix data types (numbers-as-text, currency, dates)
7.  Remove duplicates (exact + hidden)
8.  Fix inconsistent text/categories
9.  Validate IDs
10. Validate emails/phones
11. Standardize booleans
12. Handle outliers/impossible values
13. Cross-field logic checks
14. Feature creation
15. Final checks
16. Export
```

---

## 1. Load Data

```python
import pandas as pd
import numpy as np

df = pd.read_csv("file.csv")                  # CSV
df = pd.read_excel("file.xlsx")               # Excel
df = pd.read_csv("file.csv", dtype=str)       # SAFER first pass: everything as text
# WHY dtype=str: stops pandas guessing types early and silently dropping leading zeros
# (e.g. an ID "00123" becomes 123). Convert real numeric columns deliberately later (step 6).
```

---

## 2. First Inspection

```python
pd.set_option('display.max_columns', None)    # show all columns, not truncated
pd.set_option('display.max_colwidth', None)   # show full text, catch hidden \t \n

df.shape                # (rows, cols)
df.shape[0]             # row count
df.shape[1]             # column count
len(df)                 # row count (alt)
df.head()               # first 5 rows
df.tail()               # last 5 rows
df.sample(20)           # RANDOM rows — better than head(), surfaces more problems
df.info()               # dtypes + non-null counts
df.describe()           # numeric summary stats
df.describe(include='all')   # stats for ALL columns, incl. categorical
df.columns             # column names
df.dtypes              # dtype per column
df.count()             # non-null count per column
df.isnull().sum()      # missing count per column
df.isnull().sum() / len(df) * 100   # % missing per column
df['col'].value_counts(dropna=False)   # run per column — reveals every messy variant
df['col'].unique()     # all distinct values in a column
```

**Goal:** understand size, types, and spot obvious problems before touching anything.

---

## 3. Fix Column Names

```python
df.columns = df.columns.str.strip()             # remove extra spaces
df.columns = df.columns.str.lower()             # lowercase
df.columns = df.columns.str.replace(" ", "_")   # spaces -> underscore

# rename specific columns — dict must have commas between pairs:
df = df.rename(columns={
    "Old Name": "new_name",
    "rating": "rating_score",
    "fullName": "full_name",
})
```
> WHY here, early: every later snippet references column names — fix them once, up front,
> so `df['Order Date']` and `df['order_date']` don't both float around your notebook.

---

## 4. Standardize Missing-Value Tokens

```python
null_tokens = ["N/A", "NA", "n/a", "NULL", "null", "None", "none", "-", "--", "?", ""]
df = df.replace(null_tokens, np.nan)
# WHY: "N/A" is currently a valid-looking STRING, not a real NaN.
# isnull(), dropna(), fillna(), numeric conversion — none of them catch it until this runs.
# WHEN: do this BEFORE dtype conversion and BEFORE duplicate detection.
```

---

## 5. Handle Missing Values

```python
df.isnull().sum()                    # recheck AFTER step 4 — this is the real picture

# --- DROP strategies ---
df.dropna()                          # drop rows with ANY missing value (aggressive — use sparingly)
df.dropna(subset=["price"])          # drop rows missing in one specific column
df.dropna(subset=["price", "quantity"])   # drop rows missing in either of several columns
df.dropna(how="all")                 # drop rows only if ALL values are missing
df.dropna(thresh=5)                  # keep rows with at least 5 non-null values
df.dropna(axis=1, how="all")         # drop COLUMNS that are entirely missing

# --- FILL strategies ---
df.fillna(0)                                              # fixed value (use carefully — 0 can distort stats)
df["col"].fillna(df["col"].mean(), inplace=True)          # numeric: mean
df["col"].fillna(df["col"].median(), inplace=True)        # numeric: median (safer if outliers exist)
df["col"].fillna(df["col"].mode()[0], inplace=True)       # categorical: most frequent value
df["col"] = df["col"].fillna("Unknown")                   # categorical: explicit placeholder
df["col"].fillna(method="ffill", inplace=True)            # forward fill (time-ordered data only)
df["col"].fillna(method="bfill", inplace=True)            # backward fill

# group-aware fill — better than a flat mean when categories differ a lot
df["price"] = df.groupby("category")["price"].transform(lambda x: x.fillna(x.median()))
# WHY: a missing Electronics price shouldn't be filled using the whole dataset's average
# (which is dragged down/up by cheap/expensive unrelated categories like Books or Furniture)
```
> **Rule of thumb:** numeric → mean/median (median if outliers present). Categorical → mode or `"Unknown"`.
> **Never** fill an identifier column (e.g. CustomerID) — a missing ID is a row to flag, not guess.

---

## 6. Fix Data Types

### 6a. Numbers stored as text / currency symbols
```python
df["price"] = df["price"].str.replace("$", "", regex=False)
df["price"] = df["price"].str.replace(",", "", regex=False)
df["price"] = df["price"].str.replace(r'[^0-9.]', '', regex=True)   # strip everything except digits/decimal
df["price"] = df["price"].str.replace(" pcs", "", regex=False)      # strip unit labels

# European-style decimal comma vs thousands separator — ONLY if you've confirmed this pattern exists:
df["price"] = df["price"].str.replace(".", "", regex=False).str.replace(",", ".", regex=False)

df["price"] = pd.to_numeric(df["price"], errors="coerce")   # bad values -> NaN, doesn't crash
# df["price"] = pd.to_numeric(df["price"], errors="raise")  # use instead when you WANT it to crash on bad data

Phone must contain exactly 11 digits.
df.loc[
    ~df["phone"].str.fullmatch(r"\d{11}"),
    "phone"
] = np.nan
```
```python
# ALWAYS check before/after — a big jump means you destroyed real data, not just garbage:
before = df["price"].isna().sum()
# ... run your conversion ...
after = df["price"].isna().sum()
print(before, "->", after)
```

### 6b. Simple type casts
```python
df["age"] = df["age"].astype(int)
df["price"] = df["price"].astype(float)
df["category"] = df["category"].astype("category")   # memory-efficient for low-cardinality columns
```

### 6c. Dates (mixed formats)
```python
df["order_date"] = pd.to_datetime(df["order_date"], errors="coerce", dayfirst=True)
# errors="coerce": unparseable/invalid dates (Feb 30, "0000-00-00") become NaT instead of crashing

# when ONE format guess fails across a mixed-format column, combine multiple explicit passes:
fmt1 = pd.to_datetime(df["order_date"], format="%d/%m/%Y", errors="coerce")
fmt2 = pd.to_datetime(df["order_date"], format="%Y-%m-%d", errors="coerce")
df["order_date"] = fmt1.fillna(fmt2)

df["order_date"].isna().sum()   # count parsing failures (NaT) — investigate if high
```

---

## 7. Remove Duplicates

```python
df.duplicated().sum()                                     # count exact full-row duplicates
df[df.duplicated(keep=False)]                             # show ALL copies (not just the "extra" one)
df = df.drop_duplicates()                                 # remove exact duplicates, keep first by default
df = df.drop_duplicates(subset=["id"])                    # dedupe by one key column
df = df.drop_duplicates(subset=["product", "price", "quantity"])   # dedupe by a combination of columns
df = df.drop_duplicates(keep="first")   # document WHY 'first' not 'last' in your notes
```

### Hidden duplicates (same real record, different formatting)
```python
# only works reliably AFTER step 8 (text cleaning) — build a temporary normalized key:
key = (
    df["customer_name"].str.lower().str.strip() + "_" +
    df["order_date"].astype(str) + "_" +
    df["product"].str.lower().str.strip()
)
df[key.duplicated(keep=False)]
# WHY: catches "John Smith" vs " john smith" as the same order — plain .duplicated() misses this
# because the raw text isn't identical even though it means the same thing.
```

---

## 8. Fix Inconsistent Text / Categories

```python
df["col"] = df["col"].str.strip()                            # remove leading/trailing spaces
df["col"] = df["col"].str.replace(r'\s+', ' ', regex=True)   # collapse internal multiple spaces/tabs/newlines
df["col"] = df["col"].str.lower()                            # or .str.title() / .str.upper() — pick ONE standard
df["col"] = df["col"].str.replace(" ", "_")                  # spaces -> underscore (for slug-style values)
df["col"] = df["col"].str.replace("_", " ")                  # underscore -> spaces (reverse)

df["col"].unique()          # see every distinct value BEFORE deciding a mapping

# fix inconsistent spellings with an explicit mapping — safer than fuzzy matching:
df["country"] = df["country"].replace({
    "usa": "United States", "u.s.a": "United States", "america": "United States",
    "uk": "United Kingdom", "england": "United Kingdom",
    "dhaka ": "Dhaka", "dhaka": "Dhaka",
})
```
```python
# diagnostic: find hidden whitespace before fixing it
mask = df["col"].str.len() != df["col"].str.strip().str.len()
df.loc[mask, "col"]
```
> WHEN: run this BEFORE duplicate detection (step 7's hidden-duplicate check) and BEFORE
> category validation — "Dhaka" vs " dhaka" vs "DHAKA" must become one value first.

---

## 9. Validate IDs

```python
# one CustomerID should map to exactly ONE customer name
id_check = df.groupby("customer_id")["customer_name"].nunique()
bad_ids = id_check[id_check > 1].index
df[df["customer_id"].isin(bad_ids)]     # inspect manually — don't guess which name is "right"

# format validation with regex — define what a VALID id looks like first
df["valid_id_format"] = df["customer_id"].str.fullmatch(r"C\d{4}")
df[~df["valid_id_format"]]              # rows with malformed IDs
```

---

## 10. Validate Emails / Phones

```python
email_pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
df["valid_email"] = df["email"].str.match(email_pattern, na=False)
# na=False: missing emails count as "not valid" instead of raising an error

df["valid_phone"] = df["phone"].str.replace(r'\D', '', regex=True).str.len().between(7, 15)
# strip non-digit formatting chars (-, (), +) first so they don't count against length
```

---

## 11. Standardize Boolean Columns

```python
bool_map = {
    "yes": True, "y": True, "1": True, "true": True,
    "no": False, "n": False, "0": False, "false": False,
}
df["is_returned"] = df["is_returned"].astype(str).str.lower().str.strip().map(bool_map)
# WHY .map() not .replace(): any UNMAPPED value ("Nope", "Ya") becomes NaN automatically —
# forces you to notice and decide, instead of silently misclassifying it.
```

---

## 12. Handle Outliers / Impossible Values

```python
df["col"].describe()          # check min/max/quartiles first — look before you filter

# impossible values — business-logic check, not statistics
df[df["age"] < 0]                          # find impossible values
df = df[df["age"] >= 0]                     # filter them out (only after you've reviewed them)
invalid_age = df[(df["age"] < 0) | (df["age"] > 100)]

# statistical outliers — IQR method
Q1 = df["price"].quantile(0.25)
Q3 = df["price"].quantile(0.75)
IQR = Q3 - Q1
lower = Q1 - 1.5 * IQR
upper = Q3 + 1.5 * IQR
outliers = df[(df["price"] < lower) | (df["price"] > upper)]
df_clean = df[(df["price"] >= lower) & (df["price"] <= upper)]
```
> Only remove outliers you've actually looked at — a rare $5,000 order might be real,
> not an error. Impossible values (negative age) are always wrong; statistical outliers
> need judgment, not an automatic rule.

---

## 13. Cross-Field Logic Checks

```python
df["order_date"] = pd.to_datetime(df["order_date"])
df["year"] = df["order_date"].dt.year
df["month"] = df["order_date"].dt.month
df["day"] = df["order_date"].dt.day
df["weekday"] = df["order_date"].dt.day_name()

# ship date can't be before order date
bad_dates = df[df["ship_date"] < df["order_date"]]

# future dates
bad_future = df[df["order_date"] > pd.Timestamp.now()]

# calculated total vs stored total — use tolerance, NEVER == for floats
expected = df["quantity"] * df["price_each"] * (1 - df["discount"])
mismatch = df[~np.isclose(expected, df["total"], atol=0.5, equal_nan=False)]
# np.isclose, not ==: floating-point rounding causes false mismatches with exact equality
```

---

## 14. Feature Creation (after types are fixed, not before)

```python
df["quantity"] = df["quantity"].astype(int)
df["price_each"] = df["price_each"].astype(float)

df["total"] = df["quantity"] * df["price_each"]     # base amount
df["discount"] = df["total"] * 0.10                 # example discount rule
df["net"] = df["total"] - df["discount"]            # final amount after discount
```
> Only derive new columns from ALREADY-cleaned inputs — a "Total" calculated from a
> still-messy price column just propagates the mess into a new place.

---

## 15. Final Checks

```python
df.isnull().sum()            # should be 0, or intentionally left (document why)
df.duplicated().sum()        # should be 0
df.info()                    # confirm every dtype is what you expect
df.describe()                # confirm ranges make sense (no negative prices, no age of 300)

# assertions — pipeline fails LOUDLY if you rerun this later and something regresses
assert df.duplicated().sum() == 0
assert (df["price"] >= 0).all()
assert df["customer_id"].notna().all()
```

---

## 16. Export

```python
df.to_csv("cleaned_data.csv", index=False)     # index=False: don't add a meaningless index column
df.to_excel("cleaned_data.xlsx", index=False)

check = pd.read_csv("cleaned_data.csv")
check.info()   # re-read your own export and confirm dtypes actually stuck
```

---

## Quick Cheat Sheet

```
Load      -> pd.read_csv() / pd.read_excel()
Inspect   -> .info(), .describe(), .isnull().sum(), .sample(20)
Columns   -> .str.strip().str.lower().str.replace(" ", "_")
Nulls     -> .replace(null_tokens, np.nan)  BEFORE anything else
Missing   -> .dropna() / .fillna(mean/median/mode/"Unknown")
Types     -> .str.replace() -> pd.to_numeric(errors="coerce") / pd.to_datetime(errors="coerce")
Dupes     -> .drop_duplicates()  (+ normalized-key check for hidden dupes)
Text      -> .str.strip(), .str.lower()/.title(), .replace({mapping})
IDs       -> groupby(id)[name].nunique() > 1  -> inconsistent ID
Contact   -> .str.match(regex, na=False)
Booleans  -> .map({...})  not .replace()
Outliers  -> IQR method (Q1, Q3, IQR) + business-logic range checks
Cross-check -> np.isclose() for float comparisons, never ==
Final     -> assert checks, then .to_csv(index=False)
```

---


