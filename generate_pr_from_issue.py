"""
This is a python script designed to add a PR
based on the created issues of adding new resources

1. include the image to the image folder
2. modified the cefi_list.json file with the new entry

"""
import subprocess
import json
import requests
import generate_readme


def parse_issue(body):
    """
    The function parse the body of the github issue
    """
    # read source json file (data type definition)
    ori_cefi_data = generate_readme.get_cefi_list()

    # loop over all categories (variable is skipped at the moment)
    cat_list = []
    for cat in ori_cefi_data['categories_definition'].keys():
        cat_list.append(ori_cefi_data['categories_definition'][cat]['name'])

    # Split the text by '\n\n' to separate paragraphs
    paragraphs = body.split('\n\n')

    # Initialize lists to store the headings and their content
    head_list = []
    cont_list = []

    for paragraph in paragraphs:
        # Check if the paragraph is a Markdown heading
        if "###" in paragraph:
            head_list.append(paragraph.strip()[3:])
        else:
            cont_list.append(paragraph.strip())

    return head_list, cont_list


if __name__ == '__main__' :
    # cefi list repo location
    ORGNAME = "NOAA-PSL"
    REPO_NAME = "CEFI-info-hub-list"

    # A token is automatically provided by GitHub Actions
    # ACCESS_TOKEN = "${{ secrets.GITHUB_TOKEN }}"
    # Using the GitHub api to get the issue info
    ISSUE_NUM = "${{ github.event.issue.number }}"
    # ISSUE_NUM = "47"
    url = f"https://api.github.com/repos/{ORGNAME}/{REPO_NAME}/issues/{ISSUE_NUM}"

    response = requests.get(url)
    issue = response.json()

    # parsing issue
    headings, contents = parse_issue(issue['body'])

    if len(headings) != len(contents) :
        print("Error : there might be mismatching heading and content from issue parsing.")

    # read source json file (data type definition)
    cefi_data = generate_readme.get_cefi_list()
    type_list = list(cefi_data['categories_definition'].keys())

    # download the image file and include in the directory
    img_url = contents[4].split('(')[1][:-1]

    img_filename = ""
    for string in contents[0].lower().split():
        img_filename += string + "_"
    img_filename = img_filename[:-1]

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

    # add new entry related to category type
    add_dict = {}
    headings = [heading.strip() for heading in headings]
    for nt, ctype in enumerate(type_list):
        type_name = cefi_data['categories_definition'][ctype]['name']
        if type_name in headings:
            heading_ind = headings.index(type_name)
            option_list = contents[heading_ind].split(',')
            option_num_list = [int(option.split('-')[0]) for option in option_list]
            add_dict[ctype] = option_num_list

    # add new entry related to title, desc, and url etc.
    new_entry = {
        "url" : contents[1],
        "title" : contents[0],
        "desc" : contents[3],
        "thumbnail" : f"/data/gridded/images/{img_filename}.png",	
    }
    new_entry = {**new_entry, **add_dict}
    cefi_data['lists'].append(new_entry)

    # Save the dictionary as JSON in the file
    with open('data/cefi_list.json', "w", encoding="utf-8") as output_json:
        json.dump(cefi_data, output_json, indent=4)
