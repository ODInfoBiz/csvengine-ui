'''
Created on Dec 16, 2015

@author: jumbrich
'''
import os
import csvengine
import yaml

import structlog
log =structlog.get_logger()


def assure_path_exists(path):
    
    d = os.path.abspath(path)
    if not os.path.exists(d):
        log.info("Creating directory", path=d)
        os.makedirs(d)
    else:
        log.info("Directory exists", path=d)
    return d

def default_conf():
    config={}
    confFile = os.path.join(csvengine.__path__[0], 'resources', 'base.yaml')
    log.info("Loading default conf", config=confFile)
    with open(confFile) as f_conf:
            conf = yaml.load(f_conf)
            for key, values in conf.items():
                config[key]={}
                for k, v in values.items():
                    config[key][k]=v
    
    return config

def load_config(confFile):
    config = default_conf()
    if confFile:
        log.info("Loading user config", config=confFile)
        with open(confFile) as f_conf:
            conf = yaml.load(f_conf)
            
            for key in config:
                if key in conf:
                    for k, v in config[key].items(): 
                        if len(conf[key].get(k,''))>0:
                            config[key][k] = conf[key].get(k,v)
            for key in conf:
                if key not in config:
                    config[key]={}
                    for k, v in conf[key].items(): 
                        config[key][k] = conf[key].get(k,v)
                    
    return config