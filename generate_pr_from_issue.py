"""
This is a python script designed to add a PR
based on the created issues of adding new resources

1. include the image to the image folder
2. modified the cefi_list.json file with the new entry

"""
import os
import sys
import subprocess
import json
import requests
import generate_readme

def check_link_availability(test_url):
    """
    check url validity
    """
    try:
        resp = requests.get(test_url)
        if resp.status_code >= 200 and resp.status_code < 300:
            print(f"The link '{test_url}' is available.")
        else:
            print(f"The link '{test_url}' returned a status code: {resp.status_code}")
            sys.exit('Error : URL need check')
    except requests.exceptions.RequestException as error_msg:
        print(f"An error occurred while checking the link '{test_url}': {error_msg}")
        sys.exit('Error : URL not valid')

def parse_issue(body):
    """
    The function parse the body of the github issue
    """
    # # read source json file (data type definition)
    # ori_cefi_data = generate_readme.get_cefi_list()

    # # loop over all categories (variable is skipped at the moment)
    # cat_list = []
    # for cat in ori_cefi_data['categories_definition'].keys():
    #     cat_list.append(ori_cefi_data['categories_definition'][cat]['name'])

    # Split the text by '###' to separate headings and their content
    sections = body.split('###')
    
    # Initialize lists to store the headings and their content
    head_list = []
    cont_list = []

    for section in sections:
        if section.strip():
            # Split the section into heading and content
            parts = section.split('\n\n', 1)
            heading = parts[0].strip()
            content = parts[1].strip() if len(parts) > 1 else ""
            head_list.append(heading)
            cont_list.append(content)

    # Remove empty elements from the lists
    head_list = [heading for heading in head_list if heading]
    cont_list = [content for content in cont_list if content]

    return head_list, cont_list


if __name__ == '__main__' :
    # cefi list repo location
    ORGNAME = "NOAA-CEFI-Portal"
    REPO_NAME = "CEFI-info-hub-list"
    DEBUG = False

    # A token is automatically provided by GitHub Actions
    # ACCESS_TOKEN = "${{ secrets.GITHUB_TOKEN }}"
    # Using the GitHub api to get the issue info
    # Load the contents of the event payload from GITHUB_EVENT_PATH
    if DEBUG :
        ISSUE_NUM = 128
        # ISSUE_NUM = 59
    else :
        event_path = os.environ['GITHUB_EVENT_PATH']
        with open(event_path, 'r') as event_file:
            event_data = json.load(event_file)
        # Access the issue number from the event payload
        ISSUE_NUM = event_data['issue']['number']

    print(f'issue number: {ISSUE_NUM}' )
    url = f"https://api.github.com/repos/{ORGNAME}/{REPO_NAME}/issues/{ISSUE_NUM}"

    response = requests.get(url)
    print(response)
    issue = response.json()
    print(issue)

    # parsing issue
    headings, contents = parse_issue(issue['body'])

    if len(headings) != len(contents) :
        raise ValueError('Error : there might be mismatching heading and content from issue parsing.')

    # read source json file (data type definition)
    cefi_data = generate_readme.get_cefi_list()
    type_list = list(cefi_data['categories_definition'].keys())

    # download the image file and include in the directory
    try:
        img_url = contents[4].split('(')[1][:-1]
    except IndexError:
        print('Image name included')
        src_link = list(filter(lambda item: "src=" in item, contents[4].split()))
        img_url = src_link[0].split('"')[-2]


    img_filename = ""
    for string in issue['title'].split(']:')[1].strip().lower().split():
        img_filename += string + "_"
    img_filename = img_filename[:-1]
    
    if img_filename == '':
        img_filename = f'issue_number_{issue["number"]}'


    if not DEBUG :
        wget = subprocess.call(
            f'wget -O {img_filename}.png {img_url}',
            shell=True,
            executable="/usr/bin/bash"
        )

        mv = subprocess.call(
            f'mv {img_filename}.png images/{img_filename}.png',
            shell=True,
            executable="/usr/bin/bash"
        )

    # add category type of new entry
    add_dict = {}
    headings = [heading.strip() for heading in headings]
    for nt, ctype in enumerate(type_list):
        type_name = cefi_data['categories_definition'][ctype]['name']
        if type_name in headings:
            heading_ind = headings.index(type_name)
            option_list = contents[heading_ind].split(',')
            option_num_list = [int(option.split('-')[0]) for option in option_list]
            add_dict[ctype] = option_num_list
        # always adding 0-Any to all category if not specify by user
        if 0 not in add_dict[ctype]:
            add_dict[ctype] = [0]+add_dict[ctype]

    # add new entry related to title, desc, and url etc.
    check_link_availability(contents[1])
    new_entry = {
        "url" : contents[1],
        "title" : contents[0],
        "desc" : contents[3],
        "thumbnail" : f"images/{img_filename}.png",	
    }
    new_entry = {**new_entry, **add_dict}
    cefi_data['lists'].append(new_entry)

    # Save the dictionary as JSON in the file
    if not DEBUG :
        with open('data/cefi_list.json', "w", encoding="utf-8") as output_json:
            json.dump(cefi_data, output_json, indent=4)
