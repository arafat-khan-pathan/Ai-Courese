import numpy as np
import pandas as pd

df = pd.read_csv("5_weather_sensor.csv")
print(df.columns.tolist())
print(df.shape)
df = df.drop_duplicates()

#time
df["timestamp"] = pd.to_datetime(df["timestamp"])
df["date"] = df["timestamp"].dt.date
df["time"] = df["timestamp"].dt.time
df["date"] = df["timestamp"].dt.strftime("%Y-%m-%d")
df["time"] = df["timestamp"].dt.strftime("%H:%M")

cols = df.columns.tolist()
cols.remove("date")
cols.remove("time")
cols.insert(1, "date")   # 2nd column
cols.insert(2, "time")   # 3rd column

df = df[cols]
df = df.drop(columns=["timestamp"])
df = df.reset_index(drop=True)
# df = df.drop(index=0)   # Remove the first row

#date
df["date"] = pd.to_datetime(df["date"], errors="coerce")
today = pd.Timestamp.today().normalize()
df = df[df["date"] <= today]


cols = ["temperature_c", "humidity_pct", "rainfall_mm"]
df[cols] = df[cols].astype(float).abs()


for col in cols:
    df[col] = df[col].fillna(df.groupby("date")[col].transform("mean")).round(1)




df = df.sort_values(
    by=[ "date", "time", "temperature_c", "humidity_pct", "rainfall_mm"],
    ascending=[True, True, False, False, False]
)

df["humidity_pct"] = (df["humidity_pct"].fillna(df.groupby("date")["humidity_pct"].transform("mean")).ffill().bfill()).round(1)


print(df.isnull().sum())
df.to_csv("5_weather_sensor_cleaned.csv", index=False)