# Import essential libraries
import os
import requests
import csv
import time
import glob

print("Starting Task 6: Image Analysis for Haunted Places")


# Helper functions for finding files
def find_file(filename, start_dir='.'):
    """Find a file by name starting from start_dir"""
    matches = []
    for root, _, files in os.walk(start_dir):
        for file in files:
            if filename in file:
                matches.append(os.path.join(root, file))
    return matches


def find_image_dir(start_dir='.', min_images=5):
    """Find directories containing images"""
    image_dirs = []
    for root, _, files in os.walk(start_dir):
        image_files = [f for f in files if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
        if len(image_files) >= min_images:
            image_dirs.append((root, len(image_files)))

    # Sort by number of images (most images first)
    return sorted(image_dirs, key=lambda x: x[1], reverse=True)


# Function to get image caption from Tika
def get_image_caption(image_path):
    try:
        with open(image_path, 'rb') as img:
            response = requests.put(
                'http://localhost:8764/inception/v4/caption',
                files={'file': img},
                timeout=10  # Add timeout
            )
            if response.status_code == 200:
                return response.json().get('caption', 'No caption available')
            return f"Error {response.status_code}"
    except Exception as e:
        return f"Error: {str(e)}"


# Function to detect objects in the image
def detect_objects(image_path):
    try:
        with open(image_path, 'rb') as img:
            response = requests.put(
                'http://localhost:8765/inception/v3/detect',
                files={'file': img},
                timeout=10  # Add timeout
            )
            if response.status_code == 200:
                objects = response.json().get('objects', [])
                return ", ".join([obj['class'] for obj in objects])
            return f"Error {response.status_code}"
    except Exception as e:
        return f"Error: {str(e)}"


# Step 1: Find the dataset file
print("\nLooking for the haunted places dataset...")
possible_datasets = find_file('haunted_places_final.tsv')
possible_datasets += find_file('haunted_places.tsv')  # Try alternative name

if possible_datasets:
    print(f"Found {len(possible_datasets)} potential dataset files:")
    for i, path in enumerate(possible_datasets):
        print(f"  {i + 1}. {path}")

    # Auto-select first one or ask user
    if len(possible_datasets) == 1:
        dataset_path = possible_datasets[0]
        print(f"Using dataset: {dataset_path}")
    else:
        choice = input(f"Enter number 1-{len(possible_datasets)} to select dataset: ")
        try:
            dataset_path = possible_datasets[int(choice) - 1]
        except:
            dataset_path = possible_datasets[0]
            print(f"Invalid choice. Using: {dataset_path}")
else:
    # Look for any TSV files if specific names not found
    tsv_files = find_file('.tsv')
    if tsv_files:
        print(f"Found {len(tsv_files)} TSV files:")
        for i, path in enumerate(tsv_files):
            print(f"  {i + 1}. {path}")

        choice = input(f"Enter number 1-{len(tsv_files)} to select dataset (or press Enter for manual entry): ")
        try:
            dataset_path = tsv_files[int(choice) - 1]
        except:
            dataset_path = input("Enter full path to haunted places dataset TSV file: ")
    else:
        dataset_path = input("Enter full path to haunted places dataset TSV file: ")

# Step 2: Find image directory
print("\nLooking for image directories...")
image_dirs = find_image_dir()

if image_dirs:
    print(f"Found {len(image_dirs)} directories with images:")
    for i, (dir_path, count) in enumerate(image_dirs):
        print(f"  {i + 1}. {dir_path} ({count} images)")

    # Auto-select or ask user
    if len(image_dirs) == 1:
        images_dir = image_dirs[0][0]
        print(f"Using image directory: {images_dir}")
    else:
        choice = input(f"Enter number 1-{len(image_dirs)} to select image directory: ")
        try:
            images_dir = image_dirs[int(choice) - 1][0]
        except:
            images_dir = image_dirs[0][0]
            print(f"Invalid choice. Using: {images_dir}")
else:
    # Check if 'Output folder for images' exists (from task5)
    output_folder = "Output folder for images"
    if os.path.exists(output_folder) and os.path.isdir(output_folder):
        images_dir = output_folder
        print(f"Using task5's output folder: {images_dir}")
    else:
        images_dir = input("Enter path to image directory: ")

# Step 3: Load the dataset
print(f"\nLoading dataset from {dataset_path}")
try:
    data = []
    headers = []
    with open(dataset_path, 'r', encoding='utf-8') as file:
        tsv_reader = csv.reader(file, delimiter='\t')
        headers = next(tsv_reader)
        for row in tsv_reader:
            data.append(row)

    print(f"Successfully loaded dataset with {len(data)} rows and {len(headers)} columns")
    print(f"Headers: {', '.join(headers[:5])}...")
except Exception as e:
    print(f"Error loading dataset: {str(e)}")
    exit(1)

# Step 4: Add new columns if needed
print("\nUpdating dataset structure...")
if 'image_path' not in headers:
    headers.append('image_path')
    print("Added 'image_path' column")
if 'image_caption' not in headers:
    headers.append('image_caption')
    print("Added 'image_caption' column")
if 'detected_objects' not in headers:
    headers.append('detected_objects')
    print("Added 'detected_objects' column")

# Get column indices
image_path_idx = headers.index('image_path')
caption_idx = headers.index('image_caption')
objects_idx = headers.index('detected_objects')

# Ensure all rows have enough columns
for row in data:
    while len(row) < len(headers):
        row.append("")

# Step 5: Get list of image files
print(f"\nScanning for images in {images_dir}")
if os.path.exists(images_dir) and os.path.isdir(images_dir):
    image_files = [f for f in os.listdir(images_dir) if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
    print(f"Found {len(image_files)} images")

    if len(image_files) > 0:
        print(f"Sample image names: {', '.join(image_files[:3])}")
    else:
        print("No images found in directory.")
        exit(1)
else:
    print(f"Image directory not found: {images_dir}")
    exit(1)

# Step 6: Test with one image first
print("\n=== Testing Docker services with sample image ===")
test_image = os.path.join(images_dir, image_files[0])
print(f"Testing with: {test_image}")

caption = get_image_caption(test_image)
print(f"Caption: {caption}")

objects = detect_objects(test_image)
print(f"Detected objects: {objects}")

if caption.startswith("Error") or objects.startswith("Error"):
    print("\n⚠️ There might be issues with the Docker services.")
    print("Please make sure the Docker containers are running:")
    print("1. docker run -d -p 8764:8764 uscdatascience/im2txt-rest-tika")
    print("2. docker run -d -p 8765:8765 uscdatascience/inception-rest-tika")

    proceed = input("\nDo you want to continue anyway? (y/n): ")
    if proceed.lower() != 'y':
        exit(1)
else:
    print("\n✅ Docker services are working correctly!")

# Step 7: Process all images
print("\n=== Processing all images ===")
process = input(f"Do you want to process all {len(image_files)} images? (y/n): ")

if process.lower() == 'y':
    successful = 0
    failed = 0

    # Create a mapping between image filenames and dataset rows
    # This is a simple approach - you might need to adjust based on your naming convention
    print("Processing images...")

    for i, image_file in enumerate(image_files):
        if i < len(data):  # Only process if we have a corresponding data row
            image_path = os.path.join(images_dir, image_file)
            print(f"[{i + 1}/{len(image_files)}] Processing: {image_file}")

            try:
                # Update the dataset
                data[i][image_path_idx] = image_path

                # Get image caption
                caption = get_image_caption(image_path)
                data[i][caption_idx] = caption
                print(f"  Caption: {caption}")

                # Detect objects
                objects = detect_objects(image_path)
                data[i][objects_idx] = objects
                print(f"  Objects: {objects}")

                successful += 1

                # Add a small delay to avoid overwhelming the Docker services
                time.sleep(0.5)
            except Exception as e:
                print(f"  Error: {str(e)}")
                failed += 1

    print(f"\nProcessing complete: {successful} successful, {failed} failed")

    # Step 8: Save the updated dataset
    output_dir = os.path.dirname(dataset_path)
    output_filename = "haunted_places_with_images.tsv"
    output_path = os.path.join(output_dir, output_filename)

    try:
        with open(output_path, 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file, delimiter='\t')
            writer.writerow(headers)
            writer.writerows(data)
        print(f"\nUpdated dataset saved to: {output_path}")
    except Exception as e:
        print(f"Error saving dataset: {str(e)}")

        # Fallback - try saving to current directory
        try:
            backup_path = os.path.join('.', output_filename)
            with open(backup_path, 'w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file, delimiter='\t')
                writer.writerow(headers)
                writer.writerows(data)
            print(f"Backup saved to: {backup_path}")
        except:
            print("Failed to save backup file as well.")
else:
    print("Processing cancelled.")

print("\nTask 6 complete!")