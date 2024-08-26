import json
import csv

# Path to the input JSON file and output CSV file
json_file_loc = r'data/input.json'
csv_file_loc = r'data/output.csv'

# Read the JSON data from the file
with open(input_file_path, 'r') as json_file:
    data = json.load(json_file)

# Extract the list of entries
entries = data.get('lists', [])

# Open the CSV file for writing
with open(output_file_path, 'w', newline='', encoding='utf-8') as csv_file:
    # Define the CSV writer
    writer = csv.writer(csv_file)
    
    # Write the header row
    writer.writerow(['Title', 'URL'])
    
    # Iterate over the entries and write each one to the CSV
    for entry in entries:
        title = entry.get('title', '')
        url = entry.get('url', '')
        writer.writerow([title, url])

print(f"CSV file '{csv_file_loc}' created successfully.")