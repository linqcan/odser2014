#!/usr/bin/env python
"""
This module handles exposes a method for retrieving
configuration settings from 'config.json'.
"""
import json

CONFIG_FILE = "../config.json"
JSON_OBJ = None

def get(config_type, config_attr):
  """
  Returns the value of attribute 'config_attr' for
  configuration type 'config_type'.
  """
  return_type = None
  return_value = None

  try:
    return_type = JSON_OBJ[config_type]
  except KeyError:
    print "No such config type '%s'" % config_type
    raise

  try:
    return_value = return_type[config_attr]
  except KeyError:
    print "No such attribute '%s' for config type '%s'" % (config_attr, config_type)
    raise

  return return_value


file_handle = open(CONFIG_FILE, "r")
JSON_OBJ = json.load(file_handle)
