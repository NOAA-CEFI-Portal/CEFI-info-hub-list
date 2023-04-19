# This script run once creates a catalog landing page based on the *_config.json file
# reference when called. E.g., python create_catalog_landing_page.py EcoSys_config.json
from jinja2 import Environment, FileSystemLoader
# import argparse
import json
import os
import shutil
import sys
#basic templating
# use conda web_templating. .. source activate web_templating

def write_html_index(template, configs, org_config, cat_defs):
    root = os.path.dirname(os.path.abspath(__file__))
    #root = path to output directory
    filename = os.path.join(root, 'deploy', 'browse.html')
    with open(filename, 'w') as fh:
        fh.write(template.render(configs = configs, org_config = org_config, cat_defs = cat_defs))

def load_template():
    root = os.path.dirname(os.path.abspath(__file__))
    templates_dir = os.path.join(root, 'templates')
    env = Environment( loader = FileSystemLoader(templates_dir) )
    template = env.get_template('catalog_landing_page.html')
    return template

# def parse_args():
#     parser = argparse.ArgumentParser()
#     parser.add_argument('files')
#     args = parser.parse_args()
#     filename = args.files;
#     return filename

def write_templates(configs, org_config, cat_defs):
    # filename = parse_args()
    template = load_template()
    write_html_index(template, configs, org_config, cat_defs)

def main(org_config, cat_defs):
    allthemodels =  {}
    json_file = open(org_config['source_file'], encoding="utf-8")
    org_config = json.load(json_file)
    for f in org_config['lists']:
    #    old_name = f +'.json'
#        print(os.getcwd())
        allthemodels[f['title']] = f
        #print(allthemodels,'\n\n')
    #    filename = os.path.join(org_config['location_of_model_list'], old_name)
    #    with open(filename) as ff:
     #       allthemodels[f] = json.load(ff)
     #       print(allthemodels[f])
    write_templates(allthemodels, org_config, cat_defs)

if __name__ == '__main__':
    org_config_file = 'Browse_config.json'
#    org_config_file = '../data/cefi_list.json'
    json_file = open(org_config_file, encoding="utf-8")
    #org_config_file = sys.argv[1]; # use this approach if we need to generate multiple files
    org_config = json.load(json_file)

    json_file = open(org_config['source_file'], encoding="utf-8")
    categories = json.load(json_file)
    cat_defs = categories['categories_definition']
    #with open(org_config_file) as f:
    #        org_config =  json.load(f)
    main(org_config, cat_defs)