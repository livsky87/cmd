#!/usr/bin/env python
# PYTHON_ARGCOMPLETE_OK
import os, json

class Config :
  def __init__(self, base_dir) :
    self.base_dir = os.path.expanduser(base_dir)
    self.loadConfigInfo()

  def setBaseDir (self, base_dir) :
    self.base_dir = base_dir

  def getBaseDir(self) :
    return self.base_dir

  def getCommandsDir(self) :
    return os.path.join(self.base_dir, 'commands')

  def getConfigPath(self) :
    return os.path.join(self.base_dir, 'config')

  def getConfigInfo(self) :
    return self.config

  def setConfigInfo(self, json) :
    self.config = json
    self.updateConfig()

  def updateConfig(self) :
    try :
      with open(self.getConfigPath(), 'w') as json_handler :
        json.dump(self.config, json_handler, indent=4, sort_keys=True)
    except :
      print 'Permission dinied...'

  def setConfigDataAsDefault(self) :
    try :
      with open(self.getConfigPath(), 'w') as json_handler :
        json.dump({}, json_handler, indent=4)
    except :
      print('Permission denied...')

  def loadConfigInfo(self) :
    if not os.path.isdir(self.getBaseDir()) :
      os.mkdir(self.getBaseDir())

    if not os.path.isfile(self.getConfigPath()) :
      self.setConfigDataAsDefault()

    try :
      with open(self.getConfigPath(), 'r') as config_handler :
        self.config = json.load(config_handler)
    except :
      print('Permission denied...')
