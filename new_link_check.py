import json
import sys
import requests

def check_duplicate_url(json_url, new_url):
    # get the JSON file from the provided URL
    response = requests.get(json_url)
    data = response.json()
    
    # Update 'urls' to the correct key if different
    existing_urls = set(data['urls'])  
    
    # Check if the new URL is a duplicate
    if new_url in existing_urls:
        print(f"Duplicate URL found: {new_url}")
        return True
    else:
        print("No duplicate found.")
        return False

if __name__ == "__main__":
    # The new URL will be passed as a command-line argument
    new_url = sys.argv[1]
    # Correct the URL to point to the specific JSON file on GitHub
    json_url = 'https://github.com/seventh-hokage/CEFI-info-hub-list/blob/bf273bcddc15f8e2e281b26cd47b36069619f158/data/cefi_list.json'

    check_duplicate_url(json_url, new_url)
