"""
The script genearte the CSV file 
based on the raw input json file
"""

import json
import csv

# Path to the input JSON file and output CSV file
JSON_FILE = 'data/cefi_list.json'
CSV_FILE = 'data/cefi_list.csv'

# Read the JSON data from the file
with open(JSON_FILE, 'r', encoding='utf-8') as file:
    data = json.load(file)

# Extract the list of entries
entries = data.get('lists', [])

# Open the CSV file for writing
with open(CSV_FILE, 'w', newline='', encoding='utf-8') as file:
    # Define the CSV writer
    writer = csv.writer(file)

    # Write the header row
    writer.writerow(['Title', 'URL'])

    # Iterate over the entries and write each one to the CSV
    for entry in entries:
        title = entry.get('title', '')
        url = entry.get('url', '')
        writer.writerow([title, url])

print(f"CSV file '{CSV_FILE}' created successfully.")
