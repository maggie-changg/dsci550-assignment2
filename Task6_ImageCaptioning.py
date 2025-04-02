import os
import requests
import csv

DIR = "part2_images"  # Change this to your image directory
API_URL = "http://localhost:8764/inception/v3/caption/image"
OUTPUT_CSV = "captions_output.csv"  # CSV file to store results

# Open CSV file in write mode
with open(OUTPUT_CSV, mode="w", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(["Filename", "Caption"])  # Write header row

    for filename in os.listdir(DIR):
        if filename.lower().endswith((".jpg", ".jpeg", ".png")):
            filepath = os.path.join(DIR, filename)
            with open(filepath, "rb") as img_file:
                response = requests.post(API_URL, data=img_file)

                if response.status_code == 200:
                    try:
                        data = response.json()

                        # Debugging: Print raw response
                        print(f"Raw API Response for {filename}:", data)

                        # Extract first caption if available
                        captions_list = data.get("captions", [])
                        if captions_list and isinstance(captions_list, list):
                            first_caption = captions_list[0].get("sentence", "No caption found")
                            print(f"Caption for {filename}: {first_caption}")

                            # Write filename and caption to CSV
                            writer.writerow([filename, first_caption])
                        else:
                            print(f"No valid caption received for {filename}")
                            writer.writerow([filename, "No valid caption"])
                    except requests.exceptions.JSONDecodeError:
                        print(f"Error decoding JSON response for {filename}")
                        writer.writerow([filename, "Error decoding JSON"])
                else:
                    print(f"Failed to get caption for {filename}: HTTP {response.status_code}")
                    writer.writerow([filename, f"HTTP {response.status_code} error"])

            print("---------------------------")

print(f"\nCaptions saved to {OUTPUT_CSV} ✅")
import os
import requests
import csv

DIR = "part2_images"  # Change this to your image directory
API_URL = "http://localhost:8764/inception/v3/caption/image"
OUTPUT_CSV = "captions_output.csv"  # CSV file to store results

# Open CSV file in write mode
with open(OUTPUT_CSV, mode="w", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(["Filename", "Caption"])  # Write header row

    for filename in os.listdir(DIR):
        if filename.lower().endswith((".jpg", ".jpeg", ".png")):
            filepath = os.path.join(DIR, filename)
            with open(filepath, "rb") as img_file:
                response = requests.post(API_URL, data=img_file)

                if response.status_code == 200:
                    try:
                        data = response.json()

                        # Debugging: Print raw response
                        print(f"Raw API Response for {filename}:", data)

                        # Extract first caption if available
                        captions_list = data.get("captions", [])
                        if captions_list and isinstance(captions_list, list):
                            first_caption = captions_list[0].get("sentence", "No caption found")
                            print(f"Caption for {filename}: {first_caption}")

                            # Write filename and caption to CSV
                            writer.writerow([filename, first_caption])
                        else:
                            print(f"No valid caption received for {filename}")
                            writer.writerow([filename, "No valid caption"])
                    except requests.exceptions.JSONDecodeError:
                        print(f"Error decoding JSON response for {filename}")
                        writer.writerow([filename, "Error decoding JSON"])
                else:
                    print(f"Failed to get caption for {filename}: HTTP {response.status_code}")
                    writer.writerow([filename, f"HTTP {response.status_code} error"])

            print("---------------------------")

print(f"\nCaptions saved to {OUTPUT_CSV} ✅")
