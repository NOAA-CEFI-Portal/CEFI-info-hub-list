# This script run once creates a catalog landing page based on the *_config.json file
# reference when called. E.g., python create_catalog_landing_page.py EcoSys_config.json
from jinja2 import Environment, FileSystemLoader
import json
import os


def load_template(template_file):
    root = os.path.dirname(os.path.abspath(__file__))
    templates_dir = os.path.join(root, 'templates')
    env = Environment( loader = FileSystemLoader(templates_dir) )
    template = env.get_template(template_file)
    return template

def write_html_index(template, configs, org_config, cat_defs):
    root = os.path.dirname(os.path.abspath(__file__))
    filename = os.path.join(root, 'deploy', 'browse.html')
    with open(filename, 'w') as fh:
        fh.write(template.render(configs = configs, org_config = org_config, cat_defs = cat_defs))


if __name__ == '__main__':
    # load the website config json
    config_dir = os.path.dirname(os.path.abspath(__file__))
    org_config_file = os.path.join(config_dir,'Browse_config.json')
    json_file = open(org_config_file, encoding="utf-8")
    org_config = json.load(json_file)

    # load the CEFI list json file
    json_file = open(os.path.join(config_dir,org_config['source_file']), encoding="utf-8")
    cefi_json = json.load(json_file)

    # use CEFI list categories_definition to get tags and filter
    cat_defs = cefi_json['categories_definition']

    # use CEFI listed resources
    resources = cefi_json['lists']

    # parse the resource and store in a dictionary
    #  data title (key) : data info dictionary (value)
    resource_list =  {}
    for resource in resources:
        resource_list[resource['title']] = resource

    # load template file
    template = load_template('catalog_landing_page.html')

    # write to template file
    write_html_index(template, resource_list, org_config, cat_defs)