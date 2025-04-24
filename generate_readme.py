"""
The script is to generate the CEFI resource list README.md

The resource list is mirroring the https://psl.noaa.gov/data/fisheries/
search tool which provide a quick way to view the entire list and provide 
a alternative platform for contributing the resource to be included in the 
search tool.

Package used:
- mdutils (creating the markdown file from python)

Conda env:
- cefilist (only mdutils is installed)

"""
import json
from mdutils.mdutils import MdUtils

def get_cefi_list():
    """
    Read json data (soft link to the original source file)
    """

    json_file = open('data/cefi_list.json', encoding="utf-8")

    return json.load(json_file)

if __name__ == '__main__':

    data = get_cefi_list()

    # create markdown file
    mdFile = MdUtils(file_name='README')

    # start markdown structure
    mdFile.new_header(level=1, title='CEFI related resource list')

    mdFile.new_paragraph(
        "This is a curated list for the 'CEFI related resource'"+
        "on the information hub created for the NOAA Changing, Ecosystems, and Fisheries Initiative ("+
        mdFile.new_inline_link(
            link='https://www.fisheries.noaa.gov/resource/document/noaa-climate-ecosystems-and-fisheries-initiative-fact-sheet',
            text='CEFI'
            )+
        "). The goal of the information hub is \n"
        )

    mdFile.new_line(
        '> Build a comprehensive Changing, Ecosystems, and Fisheries Initiative Information Hub to provide easy access'+
        ' to regional ocean model outputs (high spatial resolution reanalysis, hindcasts, predictions, and projections'+
        ' optimized for management applications), ecosystem projections, and other information relevant to'+
        ' resource management. \n'
        )


    mdFile.new_line(
        'The complete list here is mirroring the '+
        mdFile.new_inline_link(
            link='https://psl.noaa.gov/data/fisheries/',
            text='CEFI related resource search tool'
            )+
        '. Through the search tool, users can apply filter and search text to narrow down the list based on the related topics. \n')

    mdFile.new_line('We welcome external contribution to this list. Please read the `CONTRIBUTION.md` before submitting suggestion. Thank you! \n')


    # include the list
    mdFile.new_header(level=2, title='Mirroring list')

    for cefi_list in data['lists']:
        mdFile.new_line(mdFile.new_inline_link(link=cefi_list['url'], text=cefi_list['title'])+' \n')
        mdFile.new_line('> '+cefi_list['desc'] +'\n')

    # include the table of content at the top of the file
    mdFile.new_table_of_contents(table_title='Contents', depth=2)

    # finalize the markdown file and output
    mdFile.create_md_file()

    ###### adding link check badge
    # Read the existing content of readme.md
    with open('README.md', 'r', encoding='utf-8') as file:
        existing_content = file.read()

    # New line of text to add at the top
    badge = "![Resource Link Checked](https://github.com/NOAA-CEFI-Portal/CEFI-info-hub-list/actions/workflows/gha_check_link_daily.yml/badge.svg)\n"

    # Combine the new line and existing content
    updated_content = badge + existing_content

    # Write the updated content back to readme.md
    with open('README.md', 'w', encoding='utf-8') as file:
        file.write(updated_content)
