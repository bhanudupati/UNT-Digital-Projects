import pandas as pd
import re

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
df["Final Items"]         = pd.to_numeric(df["Final Items"], errors="coerce").fillna(0)
df["Estimated Contents"]  = pd.to_numeric(df["Estimated Contents"], errors="coerce").fillna(0)

# Clean Labels — remove color codes like "(sky_light)", "(green)"
def clean_label(val):
    if pd.isna(val) or val == "Unknown":
        return "Unknown"
    cleaned = re.sub(r"\s*\(.*?\)", "", str(val)).strip()
    return cleaned if cleaned else "Unknown"

df["Collection Type"] = df["Labels"].apply(clean_label)

# Standardize List Name into clean pipeline stages
def clean_stage(val):
    if pd.isna(val):        return "Unknown"
    val = str(val).strip()
    if "Scanning" in val:   return "Scanning"
    if "Processing" in val: return "Processing"
    if "Waiting" in val:    return "Waiting on Partner"
    if "Physical" in val:   return "Physical to Digital"
    if "Complete" in val:   return "Complete"
    if "Hold" in val:       return "On Hold"
    return val

df["Pipeline Stage"] = df["List Name"].apply(clean_stage)

# Has Partner flag
df["Has Partner"] = df["Partner - Code"] != "No Partner"

print("Categorical columns cleaned!")
print("\nCollection Type unique values:")
print(df["Collection Type"].value_counts())
print("\nPipeline Stage unique values:")
print(df["Pipeline Stage"].value_counts())
print("\nHas Partner:")
print(df["Has Partner"].value_counts())