import json
from mdutils.mdutils import MdUtils


# read json data
f = open('./data/cefi_list.json')
data = json.load(f)


# create markdown file
mdFile = MdUtils(file_name='README')

mdFile.new_header(level=1, title='CEFI related resource list')

mdFile.new_paragraph("This is a curated list for the 'CEFI related resource'"+
                     "on the information hub created for the NOAA Climate, Ecosystems, and Fisheries Initiative ("+
                     mdFile.new_inline_link(link='https://www.fisheries.noaa.gov/topic/climate-change/climate-ecosystems-and-fisheries', text='CEFI')+
                     "). The goal of the information hub is \n")

mdFile.new_line('> Build a comprehensive Climate, Ecosystems, and Fisheries Initiative Information Hub to provide easy access'+
                ' to regional ocean model outputs (high spatial resolution reanalysis, hindcasts, predictions, and projections'+
                ' optimized for management applications), ecosystem projections, and other information relevant to'+
                ' climate-informed resource management. \n')


mdFile.new_line('The complete list here is mirroring the '+
                mdFile.new_inline_link(link='https://psl.noaa.gov/data/fisheries/', text='CEFI related resource search tool')+
                '. Through the search tool, users can apply filter and search text to narrow down the list based on the related topics. \n')

mdFile.new_line('We welcome external contribution to this list. Please read the `CONTRIBUTION.md` before submitting suggestion. Thank you! \n')


# --- list start
mdFile.new_header(level=2, title='Mirroring list')

for list in data['lists']:
    mdFile.new_line(mdFile.new_inline_link(link=list['url'], text=list['title'])+' \n')
    mdFile.new_line('> '+list['desc'] +'\n')


mdFile.new_table_of_contents(table_title='Contents', depth=2)


mdFile.create_md_file()