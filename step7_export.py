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
df["Archived"]        = df["Archived"].fillna(False)
# Standardize Grant? to Yes/No
df["Grant?"] = df["Grant?"].apply(
    lambda x: "Yes" if str(x).strip() in ["True", "TRUE", "Yes", "1"] else "No"
)
df["Final Items"]        = pd.to_numeric(df["Final Items"], errors="coerce").fillna(0)
df["Estimated Contents"] = pd.to_numeric(df["Estimated Contents"], errors="coerce").fillna(0)
df["Checklist Item Total Count"]     = pd.to_numeric(df["Checklist Item Total Count"], errors="coerce").fillna(0)
df["Checklist Item Completed Count"] = pd.to_numeric(df["Checklist Item Completed Count"], errors="coerce").fillna(0)
df["Attachment Count"] = pd.to_numeric(df["Attachment Count"], errors="coerce").fillna(0)
df["Vote Count"]       = pd.to_numeric(df["Vote Count"], errors="coerce").fillna(0)
df["Comment Count"]    = pd.to_numeric(df["Comment Count"], errors="coerce").fillna(0)

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

today = pd.Timestamp(datetime.today(), tz="UTC")
df["Days in Pipeline"] = (today - df["Start Date"]).dt.days.clip(lower=0)

df["Completion Rate %"] = np.where(
    df["Estimated Contents"] > 0,
    (df["Final Items"] / df["Estimated Contents"] * 100).round(1),
    0
)

df["Checklist Completion %"] = np.where(
    df["Checklist Item Total Count"] > 0,
    (df["Checklist Item Completed Count"] / df["Checklist Item Total Count"] * 100).round(1),
    0
)

df["Start Month Year"] = df["Start Date"].dt.to_period("M").astype(str)
df["Start Year"] = df["Start Date"].dt.year

def volume_bucket(n):
    if n == 0:      return "Unknown"
    if n <= 50:     return "Small (1-50)"
    if n <= 200:    return "Medium (51-200)"
    if n <= 1000:   return "Large (201-1000)"
    return "XL (1000+)"

df["Volume Bucket"] = df["Estimated Contents"].apply(volume_bucket)

# Strip timezone before exporting (Excel doesn't support timezone-aware dates)
for col in date_cols:
    df[col] = df[col].dt.tz_localize(None)

# Export
df.to_excel("unt_cleaned.xlsx", index=False)

print("=" * 50)
print("  ✅ DONE! Saved as unt_cleaned.xlsx")
print(f"  Shape: {df.shape[0]} rows × {df.shape[1]} columns")
print("=" * 50)
print("\nFinal columns:")
for col in df.columns:
    print(f"  {col}")