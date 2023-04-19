# This script run once creates tool landing pages from a model_list_dir/*.json file.

# import argparse
import json
import os
import shutil
import sys

from jinja2 import Environment, FileSystemLoader


# basic templating
# use conda web_templating. .. source activate web_templating

def write_html(template, configs, new_dir, modelname):
    # root = os.path.dirname(os.path.abspath(__file__))
    # docsdir = os.path.join(new_dir, 'deploy')
    htmlname = modelname + '.html'
    filename = os.path.join(new_dir, htmlname)
    # if not os.path.exists(docsdir):
    #    os.mkdir(docsdir)
    with open(filename, 'w') as fh:
        fh.write(template.render(**configs))


def load_template():
    root = os.path.dirname(os.path.abspath(__file__))
    templates_dir = os.path.join(root, 'templates')
    env = Environment(loader=FileSystemLoader(templates_dir))
    template = env.get_template('tool_landing_page.html')
    return template


# def parse_args():
#     parser = argparse.ArgumentParser()
#     parser.add_argument('files')
#     args = parser.parse_args()
#     filename = args.files;
#     return filename

def write_templates(configs, new_dir, modelname):
    # filename = parse_args()
    template = load_template()
    write_html(template, configs, new_dir, modelname)


def run_all_files(list_of_models, folder_out, configdir):
    for modelname in list_of_models:
        print(modelname)
        old_name = modelname + '.json'
        configfile = os.path.join(configdir, old_name)
        with open(configfile, "r") as read_file:
            configjson = json.load(read_file)
        new_dir = os.path.join(folder_out)
        # Create target Directory if don't exist
        if not os.path.exists(new_dir):
            os.mkdir(new_dir)
        write_templates(configjson, new_dir, modelname)


def main():
    with open("Browse_config.json", "r") as read_file:
        modellist_configjson = json.load(read_file)
    list_of_models = modellist_configjson['list_of_models']
    folder_out = 'deploy'
    configdir = 'model_list_dir'
    run_all_files(list_of_models, folder_out, configdir)


if __name__ == '__main__':
    main()