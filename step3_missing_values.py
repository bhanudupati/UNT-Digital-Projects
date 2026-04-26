import pandas as pd

df = pd.read_csv('K7kUaRU4 - projects-in-progress(K7kUaRU4 - projects-in-progress).csv', low_memory=False)

# Drop useless columns first
cols_to_drop = ["Notes","Status","Make PDF Downloadable (PDC Only)","Priority",
                "Final Tiffs","Card Description","Card URL","List ID","Board ID",
                "Board Name","Attachment Links"]
df = df.drop(columns=cols_to_drop)

# Handle missing values
df["Labels"]          = df["Labels"].fillna("Unknown")
df["Partner - Code"]  = df["Partner - Code"].fillna("No Partner")
df["Collection Code"] = df["Collection Code"].fillna("Unknown")
df["Model"]           = df["Model"].fillna("Unknown")
df["Due Reminder"]    = df["Due Reminder"].fillna("None")
df["Grant?"]          = df["Grant?"].fillna(False)
df["Archived"]        = df["Archived"].fillna(False)
df["Final Items"]         = pd.to_numeric(df["Final Items"], errors="coerce").fillna(0)
df["Estimated Contents"]  = pd.to_numeric(df["Estimated Contents"], errors="coerce").fillna(0)
df["Attachment Count"]    = pd.to_numeric(df["Attachment Count"], errors="coerce").fillna(0)
df["Vote Count"]          = pd.to_numeric(df["Vote Count"], errors="coerce").fillna(0)
df["Comment Count"]       = pd.to_numeric(df["Comment Count"], errors="coerce").fillna(0)
df["Checklist Item Total Count"]     = pd.to_numeric(df["Checklist Item Total Count"], errors="coerce").fillna(0)
df["Checklist Item Completed Count"] = pd.to_numeric(df["Checklist Item Completed Count"], errors="coerce").fillna(0)

print("Missing values handled!")
print("\nRemaining nulls per column:")
print(df.isnull().sum())