# -*- coding: utf-8 -*-
"""
Created on 2020 Dec 17 13:06

@author: guyn

get sources from the Fritz marshal, 
run custom analysis on each, 
assign some values and post them back to Fritz
as Annotations on those sources

INSTRUCTIONS:
    You must create a "config.yaml" file and define:
    [] the URL of the instance of SkyPortal / fritz you want to leech. 
    [] the name of the annotation origin you want to apply to each source. 
    [] the date when your analysis code was last updated (for re-calculating 
       older versions of the annotation data). 
    [] the date, or relative time (in days) after which you want to load 
       sources. Any sources before that time are ignored. 
    
    You must also create a file named "token" and copy your token from Fritz 
    into this file. 
    Both config.yaml and token should be ignored by git, so you can customize 
    and put your token in there without it being published. 

"""

import os
import glob
import yaml
import importlib
import requests
import json
import arrow

import custom_functions


def load_config():
    # load the config YAML file

    try:
        with open(os.path.dirname(__file__)+'/config.yaml') as file:
            config = yaml.full_load(file)
    except FileNotFoundError:
        with open(os.path.dirname(__file__) + '/config.default.yaml') as file:
            config = yaml.full_load(file)

    # get the SkyPortal token from file
    with open(os.path.dirname(__file__)+"/token", "r") as file:
        token = file.readline()

    config['token'] = token.strip()  # add the token into the config object

    return config


def parse_start_date(date):
    if date is None or date.strip() in ["", "null", "undefined"]:
        return ''

    if isinstance(date, (int, float)) and date < 0:
        return str(arrow.utcnow().shift(days=date))

    return date


def load_objects(config):  # call the API to get the relevant objects
    head = {"Authorization": f"token {config['token']}", "content_type": "application/json"}
    params = {
        'filterIDs': config.get('filters', None),
        'startDate': parse_start_date(config.get('start_date', None)),
        'includePhotometry': config.get('needs_photometry', False),
        'includeSpectra': config.get('needs_spectroscopy', False),
        'annotationExcludeOrigin': config.get('origin'),
        'annotationExcludeDate': config.get('annotation_date', None),
      }
    r = requests.get(f"{config['url']}/api/candidates", headers=head, params=params)

    j = r.json()

    if r.status_code == 200:
        objects = j['data']
        return objects['candidates']
    else:
        print(j['message'])
        return []


def run_all_functions(obj, results, config):

    for module_path in glob.glob(os.path.dirname(__file__)+'/custom_functions/*.py'):
        module_name = os.path.splitext(os.path.basename(module_path))[0]
        print(f"running module '{module_name}' on object '{obj['id']}'")

        # module must have a function with the same name as module itself
        module = importlib.import_module("custom_functions." + module_name)
        importlib.reload(module)

        # run the function!
        getattr(module, module_name)(obj, results, config)


def post_annotation(obj, results, config):
    head = {"Authorization": f"token {config['token']}", "content_type": "application/json"}
    data = json.dumps({"obj_id": obj['id'], "origin": config['origin'], "data": results})

    # check if an annotation exists
    annotation_id = [a['id'] for a in obj['annotations'] if a['origin'] == config['origin']]

    if annotation_id:
        r = requests.put(f"{config['url']}/api/annotation/{annotation_id[0]}", headers=head, data=data)
    else:
        r = requests.post(f"{config['url']}/api/annotation", headers=head, data=data)

    if r.status_code != 200:
        raise(f"Could not post the annotation to obj_id= {obj['id']}")

if __name__ == "__main__":

    config = load_config()

    objects = load_objects(config)

    for obj in objects:
        results = {}  # this will be uploaded as an annotation
        run_all_functions(obj, results, config)

        if config.get('upload', False):  # only push results if upload is true
            post_annotation(obj, results, config)

