import os
import time
import pandas as pd
import requests
from io import BytesIO

HUGGINGFACE_TOKEN = "YOUR_TOKEN"
CSV_FILE = "team6_part_01.csv"
OUTPUT_CSV = "output_part1_sd.csv"
IMAGE_DIR = r"Output folder for images"
DELAY_SECONDS = 10

os.makedirs(IMAGE_DIR, exist_ok=True)

API_URL = "https://api-inference.huggingface.co/models/CompVis/stable-diffusion-v1-4"
HEADERS = {"Authorization": f"Bearer {HUGGINGFACE_TOKEN}"}

def generate_image(prompt):
    payload = {"inputs": prompt}
    response = requests.post(API_URL, headers=HEADERS, json=payload)
    if response.status_code == 200:
        return response.content
    else:
        print(f"[API Error] {response.status_code}: {response.text}")
        return None

def make_prompt(description):
    return f"Haunted ghost scene: {description[:300]}"

def make_safe_filename(text, max_length=50):
    safe_text = ''.join(c if c.isalnum() or c in (' ', '_') else '_' for c in text)
    return safe_text[:max_length].strip().replace(' ', '_') + ".png"

df = pd.read_csv(CSV_FILE)
if 'image_path' not in df.columns:
    df['image_path'] = ""

for idx, row in df.iterrows():
    desc = row.get('description', '')
    if pd.isna(desc) or not desc.strip():
        continue

    prompt = make_prompt(desc)
    filename = make_safe_filename(desc)
    save_path = os.path.join(IMAGE_DIR, filename)

    if os.path.exists(save_path):
        df.at[idx, 'image_path'] = save_path
        continue

    print(f"[{idx+1}/{len(df)}] Generating: {filename}")
    image_data = generate_image(prompt)
    if image_data:
        with open(save_path, 'wb') as f:
            f.write(image_data)
        df.at[idx, 'image_path'] = save_path
    else:
        print(f"[Warning] Failed at index {idx}")

    time.sleep(DELAY_SECONDS)

df.to_csv(OUTPUT_CSV, index=False)
print("All images saved to:", IMAGE_DIR)


