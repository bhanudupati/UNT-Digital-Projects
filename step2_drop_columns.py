import pandas as pd

df = pd.read_csv('K7kUaRU4 - projects-in-progress(K7kUaRU4 - projects-in-progress).csv', low_memory=False)

# Drop columns that are 90%+ empty or not useful for analysis
cols_to_drop = [
    "Notes",
    "Status",
    "Make PDF Downloadable (PDC Only)",
    "Priority",
    "Final Tiffs",
    "Card Description",
    "Card URL",
    "List ID",
    "Board ID",
    "Board Name",
    "Attachment Links",
]

df = df.drop(columns=cols_to_drop)

print("Columns dropped successfully!")
print("Remaining shape:", df.shape)
print("Remaining columns:", df.columns.tolist())