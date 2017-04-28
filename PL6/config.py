
import argparse
import json

def read_config(file):
	config = (json.load(file) if file else None)
	return config

def get_config(config, keys, default):
    if not keys: return config
    if not config: return default
    
    if isinstance(config,dict):
        if keys[0] in config: 
            return get_config(config[keys[0]], keys[1:], default)
    if isinstance(config,list):
        if len(config) >= keys[0]:
            return get_config(config[keys[0]], keys[1:], default)

    return default
