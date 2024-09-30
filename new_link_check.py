"""
Testing if the submitted resource overlapping
with the resource that is currently in the
database
"""
import os
import json
import requests
from generate_readme import get_cefi_list
from generate_pr_from_issue import parse_issue, check_link_availability


def check_duplicate_url(new_url):
    """Test root url similarity

    Parameters
    ----------
    new_url : str
        new url in string for checking is there 
        is same root url in the database

    Raises
    ------
    LookupError
        show error when possible duplication happened
    """

    # get the JSON file from the provided URL
    data = get_cefi_list()

    # linear search the list (unordered)
    new_url_list = new_url.split('/')
    for cefi_list in data['lists']:
        ori_url_list = cefi_list['url'].split('/')
        if ori_url_list[2] == new_url_list[2]:
            print('Same root URL detected. Possible duplicate/overlapping resources!')
            print(f'New resource URL : {new_url}')
            print(f'Database resource URL : {cefi_list["url"]}')
            GetGitHubIssue().add_label('possible duplicate')
            # raise LookupError('Possible duplicate/overlapping resources!')

class GetGitHubIssue:
    """Get and Parse GitHub Issue
    """
    def __init__(self):
        # cefi list repo location
        self.org_name = "NOAA-CEFI-Portal"
        self.repo_name = "CEFI-info-hub-list"

    def add_label(self, label):
        """add label to event triggered issue

        Parameters
        ----------
        label : str
            label name to add to the issue
        """
        # get the issue number
        event_path = os.environ['GITHUB_EVENT_PATH']
        with open(event_path, 'r', encoding='utf-8') as event_file:
            event_data = json.load(event_file)
        # Access the issue number from the event payload
        issue_number = event_data['issue']['number']

        url = (
            "https://api.github.com/repos/"+
            f"{self.org_name}/{self.repo_name}/issues/{issue_number}/labels"
        )

        GITHUB_TOKEN = os.environ['GITHUB_TOKEN']

        headers = {
            "Authorization": f"token {GITHUB_TOKEN}",
            "Accept": "application/vnd.github.v3+json"
        }
        response = requests.post(url, json=[label], headers=headers, timeout=1000)
        response.raise_for_status()  # Raise an error for bad responses

    def get_github_issue(self,debug=False,issue_num=123)-> dict:
        """Getting github issue content

        Parameters
        ----------
        debug : bool, optional
            activate debug mode or not, by default False
        issue_num : int, optional
            only work when debug set to True, by default 123

        Returns
        -------
        dict
            issue_headings : heading infos
            issue_contents : contents

        Raises
        ------
        ValueError
            when parsing failed (usually related to the issue title format)
        """

        # A token is automatically provided by GitHub Actions
        # ACCESS_TOKEN = "${{ secrets.GITHUB_TOKEN }}"
        # Using the GitHub api to get the issue info
        # Load the contents of the event payload from GITHUB_EVENT_PATH
        if debug :
            issue_number = issue_num
        else :
            event_path = os.environ['GITHUB_EVENT_PATH']
            with open(event_path, 'r', encoding='utf-8') as event_file:
                event_data = json.load(event_file)
            # Access the issue number from the event payload
            issue_number = event_data['issue']['number']

        print(f'issue number: {issue_number}' )
        url = (
            "https://api.github.com/repos/"+
            f"{self.org_name}/{self.repo_name}/issues/{issue_number}"
        )

        response = requests.get(url, timeout=1000)
        issue = response.json()

        # parsing issue
        headings, contents = parse_issue(issue['body'])

        if len(headings) != len(contents) :
            raise ValueError(
                'error in issue parsing (new_link_check.py).'
            )

        return {
            "issue_headings":headings,
            "issue_contents": contents
        }

    def get_issue_info(self,**kwargs)-> dict:
        """parsing the github issue content

        Returns
        -------
        dict
            dictionary contain the parsed issue content
        """
        dict_issue = self.get_github_issue(**kwargs)

        headings = dict_issue['issue_headings']
        contents = dict_issue['issue_contents']

        # read source json file (data type definition)
        cefi_data = get_cefi_list()
        type_list = list(cefi_data['categories_definition'].keys())

        # add category type of new entry
        add_dict = {}
        headings = [heading.strip() for heading in headings]
        for ctype in type_list:
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
            "desc" : contents[3]
        }

        return {**new_entry, **add_dict}

if __name__ == "__main__":

    # get parsed issue content in dict
    dict_issue_parsed = GetGitHubIssue().get_issue_info(debug=False, issue_num=136)

    # check the url for duplication in the data base
    check_duplicate_url(dict_issue_parsed['url'])
