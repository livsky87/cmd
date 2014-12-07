#!/usr/bin/env python
# PYTHON_ARGCOMPLETE_OK
import argcomplete, argparse, requests, pprint
from argcomplete import *
import os, sys, subprocess, json, types

from cmd.Base.Config import *
from cmd.Core.Command import *
from cmd.Core.Category import *

def github_org_members(prefix, parsed_args, **kwargs):
  resource = "https://api.github.com/orgs/{org}/members".format(org=parsed_args.organization)
  return (member['login'] for member in requests.get(resource).json() if member['login'].startswith(prefix))
def updateCmd () :
  os.system('register-python-argcomplete cmd.py')

class AutoCommand(Config) :
  def __init__(self, root_dir='~/.cmd') :
    Config.__init__(self, root_dir)

    # For Auto Command Implementation
    parser = argparse.ArgumentParser(prog='cmd', add_help=False)
    sub = parser.add_subparsers()
    self.setAutoCommandParser(sub)

    self.loadAutoCommandInfo()

    # Initialize Core Commands
    CommandManager(self.getAutoCommandParser(), self.getBaseDir())
    #self.initializeCoreCommands()

    # Applied Auto Complete
    argcomplete.autocomplete(parser)
    self.options = parser.parse_args()

  def setAutoCommandParser(self, parser) :
    self.AutoCommandParser = parser

  def getAutoCommandParser(self) :
    return self.AutoCommandParser

  def getAutoCommandDir(self) :
    return self.getBaseDir()

  def setCoreCommands(self) :
    pass

  def loadAutoCommandInfo(self) :
    self.AutoCommandConfig = self.getConfigInfo()

#    for category in self.AutoCommandConfig['categories'] :
#      Category(category,
#               self.getAutoCommandParser(), 
#               os.path.join(self.getAutoCommandDir(), 'categories', category))

  def initializeCoreCommands(self) :
    # initialize Core Commands
    addCommandHandler = Command('add', self.getAutoCommandParser(), self.getBaseDir(), 'core')
    delCommandHandler = Command('del', self.getAutoCommandParser(), self.getBaseDir(), 'core')
    editCommandHandler = Command('edit', self.getAutoCommandParser(), self.getBaseDir(), 'core')

    addCommandHandler.addCommandOption('-C','--category')
    addCommandHandler.addCommandOption('commandName')
    addCommandHandler.setCommandFunction(self.addCategory)

    delCommandHandler.addCommandOption('--category')
    delCommandHandler.addCommandOption('commandName')
    delCommandHandler.setCommandFunction(self.addCategory)

    editCommandHandler.addCommandOption('--category')
    editCommandHandler.addCommandOption('commandName')
    editCommandHandler.setCommandFunction(self.addCategory)


  def addCategory(self, arg) :
    print arg.commandName
    print arg.category

    #    if arg.category != None :
    #      print "Not None"
    #      print "Add Category!!!"
    #      if arg.commandName != None :
    #        commandName = arg.commandName.strip()
    #      elif arg.commandName == "" :
    #        commandName = None
    #      else :
    #        commandName = arg.commandName
    #
    #      print commandName
    #
    #      if len(arg.category) != 0 and commandName != None :
    #        print "too much arguments..."
    #        categoryName = None
    #      elif len(arg.category) == 0 :
    #        if commandName != None :
    #          categoryName = commandName
    #        else :
    #          categoryName = None
    #      elif commandName == None :
    #        if len(arg.category) != 0 :
    #          CategoryName = arg.category[0]
    #        else :
    #          categoryName = None
    #      else :
    #        categoryName = None
    #
    #      if categoryName != None :
    #        print categoryName
    #      else :
    #        print "Add Category failed..."
    #  
    #    else :
    #      print "None"
    #      print "Add Command"
    #



  def delCategory(self, category_name) :
    pass

  def editCategory(self, arg) :
    pass

"""

    ######################################################
    with open(os.path.join(self.root_dir, 'config'), 'rw') as config_handler :
      self.config = json.load(config_handler)

    #with open(os.path.join(self.root_dir, 'config'), 'w') as outfile :
    #  json.dump(js, outfile, indent=4, sort_keys=True)


    # For Auto Command Implementation
    self.parser = argparse.ArgumentParser(add_help=False)
    self.sub = self.parser.add_subparsers()

    # Initialize Core Commands
    self.categoryCommand = Category('category', self.sub, self.root_dir, 'core')
    addCategoryCommandHandler = Command('add', self.categoryCommand.getParser(), self.root_dir, self.addCategory)
    addCategoryCommandHandler.addOption('category_name', nargs='*')
    addCategoryCommandHandler.addOption('--type', choices=('normal', 'core'))
    
    Command('del', self.categoryCommand.getParser(), self.root_dir, self.delCategory)
    #coreCommand = Category('core', self.sub, self.root_dir)

    # Initialize User Commands
    for category in self.config['categories'] :
      self.categories[category] = Category(category,
                                           self.sub, 
                                           os.path.join(self.categories_dir, category),
                                           category_type='core')

    # Applied Auto Complete
    argcomplete.autocomplete(self.parser)
    self.options = self.parser.parse_args()

  def addCategory(self, args):
    print "addCategory in AutoCommand"
    category_name = args.category_name[0]
    if type(args.type) == types.NoneType :
      category_type = args.type
    else :
      category_type = args.type[0]

    print category_type
    if category_name not in self.config['categories'] :
      self.config['categories'][category_name] = {'type':category_type}
      self.updateConfig()

      category_handler = Category(category_name,
                                  self.sub,
                                  os.path.join(self.categories_dir, category_name),
                                  category_type)
      updateCmd()
    else :
      print '[Error] %s is already exist...' % (category_name)

  def delCategory(self, category_name):
    print "delCategory in AutoCommand"

  def updateConfig(self) :
    with open(os.path.join(self.root_dir, 'config'), 'w') as json_handler :
      json.dump(self.config, json_handler, indent=4, sort_keys=True)
"""

if __name__ == "__main__":
  autoCmd = AutoCommand()
  autoCmd.options.func(autoCmd.options) 
