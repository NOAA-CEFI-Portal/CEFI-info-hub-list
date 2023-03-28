"""
The script is to generate the YAML file 
which helps GitHub to generate a issue template 
for CEFI resource contribution.
"""
import yaml
import generate_readme

# read source json file (data type definition)
cefi_data = generate_readme.get_cefi_list()

# read the title part of the issue template
ISSUE_TEMP = ".github/ISSUE_TEMPLATE/header_file/add_cefi_resource_head.yml"
with open(ISSUE_TEMP,'r',encoding='utf8') as f:
    issue_temp_head = yaml.load(f,Loader=yaml.loader.SafeLoader)

# solve the unique name issue in ISSUE_TEMPLATE
issue_temp_head['name'] = 'Contribute to the CEFI resource list'

# loop over all categories (variable is skipped at the moment)
for cat in cefi_data['categories_definition'].keys():
    if cat != 'cvar':
        options = [f"{nt}-{text}" for nt,text in enumerate(cefi_data['categories_definition'][cat].values())]

        issue_temp_head['body'].append({
            'type': 'dropdown',
            'id': cat,
            'attributes': {
                'label': cefi_data['categories_definition'][cat]['name'],
                'multiple': True,
                'options': options[1:]
            },
            'validations': {
                'required': True
            }
        })

# output yml file
OUT_FNAME = '.github/ISSUE_TEMPLATE/add_cefi_resource.yml'
with open(OUT_FNAME, 'w',encoding='utf8') as f:
    data = yaml.dump(issue_temp_head, f, sort_keys=False, default_flow_style=False)
