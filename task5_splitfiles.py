import pandas as pd
import os

file_path = "merged_haunted_places_all_3.csv"
df = pd.read_csv(file_path)

total_parts = 6
rows_per_part = len(df) // total_parts
remainder = len(df) % total_parts

# ✅ Save splits to current folder
output_dir = os.getcwd()
split_files = []

start = 0
for part in range(1, total_parts + 1):
    extra = 1 if part <= remainder else 0
    end = start + rows_per_part + extra
    chunk = df.iloc[start:end]
    filename = f"team6_part_{part:02d}.csv"
    path = os.path.join(output_dir, filename)
    chunk.to_csv(path, index=False)
    split_files.append((part, filename, len(chunk)))
    start = end

print(" Done! All files saved in:", output_dir)
