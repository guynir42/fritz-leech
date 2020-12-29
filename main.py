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
import inspect
import importlib

import custom_functions

def run_all_functions(obj):

    for module_name in custom_functions.__all__:  # go over all files in "custom_functions" folder
        module = importlib.import_module("custom_functions."+module_name)  # module must have a function with the same name as module itself
        getattr(module, module_name)(obj)

def load_config():
    

if __name__ == "__main__": 
    obj = {id: 'sample_id'}
    run_all_functions(obj)