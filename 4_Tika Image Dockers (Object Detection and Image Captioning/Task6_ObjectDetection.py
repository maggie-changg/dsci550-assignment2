import os
import requests
import csv

DIR = "part2_images"  # Change this to your image directory
API_URL = "http://localhost:8764/inception/v4/classify/image"
OUTPUT_CSV = "object_detection_output.csv"  # Output CSV file

# Open CSV file for writing
with open(OUTPUT_CSV, mode="w", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(["Filename", "Detected Objects"])  # CSV Header

    for filename in os.listdir(DIR):
        if filename.lower().endswith((".jpg", ".jpeg", ".png")):
            filepath = os.path.join(DIR, filename)
            with open(filepath, "rb") as img_file:
                response = requests.post(API_URL, data=img_file)

                if response.status_code == 200:
                    try:
                        data = response.json()
                        
                        # Debugging: Print raw API response
                        print(f"Raw API Response for {filename}:", data)

                        # Extract detected objects and confidence scores
                        classnames = data.get("classnames", [])
                        confidences = data.get("confidence", [])

                        # Ensure both lists are non-empty and of the same length
                        if classnames and confidences and len(classnames) == len(confidences):
                            detected_objects = [
                                f"{classnames[i]} ({confidences[i]:.2f})"
                                for i in range(len(classnames))
                            ]
                            detected_objects_str = ", ".join(detected_objects)
                        else:
                            detected_objects_str = "No objects detected"

                        print(f"Detected Objects for {filename}: {detected_objects_str}")

                        # Write to CSV
                        writer.writerow([filename, detected_objects_str])
                    except requests.exceptions.JSONDecodeError:
                        print(f"Error decoding JSON response for {filename}")
                        writer.writerow([filename, "Error decoding JSON"])
                else:
                    print(f"Failed to detect objects for {filename}: HTTP {response.status_code}")
                    writer.writerow([filename, f"HTTP {response.status_code} error"])

            print("---------------------------")

print(f"\nObject detection results saved to {OUTPUT_CSV} ✅")
