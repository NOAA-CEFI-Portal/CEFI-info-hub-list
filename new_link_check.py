import json
import sys
import requests

def check_duplicate_url(json_url, new_url):
    # Fetch the JSON file from the provided URL
    response = requests.get(json_url)

    # Check if the response was successful
    if response.status_code != 200:
        print(f"Failed to fetch the JSON file. Status code: {response.status_code}")
        print(f"Response content: {response.content}")
        return False

    try:
        data = response.json()
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")
        print(f"Response content: {response.content}")
        return False
    
    # Assuming the URLs are stored under a key named 'urls'
    existing_urls = set(data.get('urls', []))  # Update 'urls' to the correct key if different
    
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
    
    # Replace this with the actual path to your JSON file on GitHub (raw link)
    json_url = 'https://github.com/seventh-hokage/CEFI-info-hub-list/blob/312e5c94e14a96a42326df8deb4d0e0384ccf0ad/data/cefi_list.json'  # Replace with actual file name

    check_duplicate_url(json_url, new_url)
