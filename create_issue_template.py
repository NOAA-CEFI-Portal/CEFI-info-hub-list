import yaml
import generate_readme

cefi_data = generate_readme.get_cefi_list()

issue_temp = ".github/ISSUE_TEMPLATE/add_resource.yml"

with open(issue_temp) as f:
    issue_data = yaml.load(f,Loader=yaml.loader.SafeLoader)


issue_data['name'] = 'Add a new resource'

# loop over all categories
for cat in cefi_data['categories_definition'].keys():
    if cat != 'cvar':
        issue_data['body'].append(
            {'type': 'dropdown',
            'id': cat,
             'attributes': {'label': cefi_data['categories_definition'][cat]['name'],
                            'multiple': True,
                            'options': list(cefi_data['categories_definition'][cat].values())[1:]
                            }
            }
        )

out_fname = '.github/ISSUE_TEMPLATE/test.yml'
with open(out_fname, 'w') as f:
    data = yaml.dump(issue_data, f, sort_keys=False, default_flow_style=False)