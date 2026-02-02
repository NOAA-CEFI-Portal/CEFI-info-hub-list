import re
import requests
import json



# Function to find and return all URLs in a text file
def find_url(file_path):
    # Define a regular expression pattern to match URLs
    url_pattern = r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
    with open(file_path, 'r') as file:
        text = file.read()
        urls = re.findall(url_pattern, text)
        urls = [url for url in urls]
        return urls
    
def find_url_json(file_path,exclude=[]):
    # Open the JSON file for reading
    with open(file_path, 'r') as file:
        # Load the JSON data from the file into a Python data structure
        data = json.load(file)
        urls = []
        for res_list in data['lists']:
            if res_list['url'] not in exclude:
                urls.append(res_list['url'])
    return urls

    
# Function to check URLs
def check_urls(url_list):
    bad_list = []
    for url in url_list:
        try:
            response = requests.get(url,timeout=5)
            if response.status_code == 200:
                print(f"{url} valid with 200 response.")
            else:
                print(f"{url} valid returned {response.status_code} response.")
        except requests.exceptions.RequestException as e:
            try:
                response = requests.get(url,timeout=5,verify=False)
                if response.status_code == 200:
                    print(f"{url} valid with 200 response.")
                else:
                    print(f"{url} valid returned {response.status_code} response.")
            except requests.exceptions.RequestException as e:
                print(f"{url} is not a valid URL. Error: {e}")
                bad_list.append(url)
    return bad_list

class URLNotValidError(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)

if __name__=="__main__":
    # exception list of bad url (wrong reponse with ok website access)
    ex_list = [
        "https://nodc.id/oceanography",
        "https://oceanadapt.rutgers.edu/",
    ]

    # Provide the path to your text file
    file_path = './data/cefi_list.json'

    # Call the function to find URLs in the file
    # found_urls = find_url(file_path)
    found_urls = find_url_json(file_path,exclude=ex_list)

    bad_url = check_urls(found_urls)

    if len(bad_url) != 0:
        print("summary of bad URL")
        print("--------------------")
        for url in bad_url:
            print(url)
        print("--------------------")
        raise URLNotValidError("Please check the bad URLs.")
