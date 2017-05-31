"""
config.py
Goncalo Pereira, May 2017

The read_file function supports the load of json files like so:

	{
	    "a": false,
	    "b": {
	        "b1": 1,
	        "b2": "something",

	    	"b3": {
	    		"b1x": 0.25,
	    		"b2y": 1.01,
	    	},
	    },
	    "c": [1, 2, 3]
	}

The configurations can then be queried using the get_config function:

	get_config(configs, ['a']) # would return the boolean value False
	get_config(configs, ['b']) # would return a dictionary
	get_config(configs, ['b', 'b1']) # would return the number 1
	get_config(configs, ['b', 'b2']) # would return the string "something"
	get_config(configs, ['c', 0]) # would return the number 1
	get_config(configs, ['c', 1]) # would return the number 2

The configurations can also be accessed directly:

	configs['b']['b3']['b1x'] would return the number 0.25

Default values can be used when the configuration is not defined:

	get_config(configs, ['d'], True) # would return the default boolean value True

Or if no default is provided the None value will be returned:

	get_config(configs, ['d']) # would return the default value None	

"""

import argparse
import json

def read_config(file):
	if file:
		config = json.load(file)
	else:
		print("Warning: No configuration was provided, default values will be used!")
		config = None

	return config

def get_config(config, keys, default=None):
	if not keys: return config
	if not config: return default
	
	if isinstance(config,dict):
		if keys[0] in config: 
			return get_config(config[keys[0]], keys[1:], default)
	if isinstance(config,list):
		if len(config) >= keys[0]:
			return get_config(config[keys[0]], keys[1:], default)

	print("Warning: default value of {} used for configuration {}".format(default, keys))
	return default
	