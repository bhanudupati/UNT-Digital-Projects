import pandas as pd
import numpy as np
import re
from datetime import datetime

df = pd.read_csv('K7kUaRU4 - projects-in-progress(K7kUaRU4 - projects-in-progress).csv', low_memory=False)

cols_to_drop = ["Notes","Status","Make PDF Downloadable (PDC Only)","Priority",
                "Final Tiffs","Card Description","Card URL","List ID","Board ID",
                "Board Name","Attachment Links"]
df = df.drop(columns=cols_to_drop)

df["Labels"]          = df["Labels"].fillna("Unknown")
df["Partner - Code"]  = df["Partner - Code"].fillna("No Partner")
df["Collection Code"] = df["Collection Code"].fillna("Unknown")
df["Model"]           = df["Model"].fillna("Unknown")
df["Due Reminder"]    = df["Due Reminder"].fillna("None")
df["Grant?"]          = df["Grant?"].fillna(False)
df["Archived"]        = df["Archived"].fillna(False)
df["Final Items"]        = pd.to_numeric(df["Final Items"], errors="coerce").fillna(0)
df["Estimated Contents"] = pd.to_numeric(df["Estimated Contents"], errors="coerce").fillna(0)
df["Checklist Item Total Count"]     = pd.to_numeric(df["Checklist Item Total Count"], errors="coerce").fillna(0)
df["Checklist Item Completed Count"] = pd.to_numeric(df["Checklist Item Completed Count"], errors="coerce").fillna(0)

date_cols = ["Due Date", "Last Activity Date", "Start Date", "Due Complete", "Anticipated Arrival"]
for col in date_cols:
    df[col] = pd.to_datetime(df[col], errors="coerce", utc=True)

def clean_label(val):
    if pd.isna(val) or val == "Unknown":
        return "Unknown"
    cleaned = re.sub(r"\s*\(.*?\)", "", str(val)).strip()
    return cleaned if cleaned else "Unknown"

df["Collection Type"] = df["Labels"].apply(clean_label)
df["Has Partner"] = df["Partner - Code"] != "No Partner"
df["Pipeline Stage"] = df["List Name"]

# Feature 1: Days in pipeline (Start Date → today)
today = pd.Timestamp(datetime.today(), tz="UTC")
df["Days in Pipeline"] = (today - df["Start Date"]).dt.days.clip(lower=0)

# Feature 2: Completion Rate
df["Completion Rate %"] = np.where(
    df["Estimated Contents"] > 0,
    (df["Final Items"] / df["Estimated Contents"] * 100).round(1),
    0
)

# Feature 3: Checklist Completion %
df["Checklist Completion %"] = np.where(
    df["Checklist Item Total Count"] > 0,
    (df["Checklist Item Completed Count"] / df["Checklist Item Total Count"] * 100).round(1),
    0
)

# Feature 4: Start Month Year for time series
df["Start Month Year"] = df["Start Date"].dt.to_period("M").astype(str)
df["Start Year"] = df["Start Date"].dt.year

# Feature 5: Volume bucket
def volume_bucket(n):
    if n == 0:      return "Unknown"
    if n <= 50:     return "Small (1-50)"
    if n <= 200:    return "Medium (51-200)"
    if n <= 1000:   return "Large (201-1000)"
    return "XL (1000+)"

df["Volume Bucket"] = df["Estimated Contents"].apply(volume_bucket)

print("Features engineered!")
print("\nNew columns added:")
print("  Days in Pipeline:", df["Days in Pipeline"].describe())
print("\n  Completion Rate %:", df["Completion Rate %"].describe())
print("\n  Checklist Completion %:", df["Checklist Completion %"].describe())
print("\n  Volume Bucket:")
print(df["Volume Bucket"].value_counts())
print("\n  Start Month Year sample:", df["Start Month Year"].dropna().unique()[:10])