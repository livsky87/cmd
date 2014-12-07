#!/usr/bin/env python
# PYTHON_ARGCOMPLETE_OK
import os, json

from cmd.Base.Config import *

class Category(Config) :
  def __init__(self,
               category_name,
               parser,
               base_dir,
               category_type='normal') :
    Config.__init__(self, base_dir)

    # Set initial variable for Category Class
    self.setCategoryName(category_name)
    category_parser = parser.add_parser(category_name, add_help=False)
    subparser = category_parser.add_subparsers()
    self.setCategoryParser(subparser)

    self.loadCategoryInfo()

  def setCategoryName(self, category_name) :
    self.CategoryName = category_name

  def getCategoryName(self) :
    return self.CategoryName

  def getCategoryPath(self) :
    return self.getBaseDir()

  def setCategoryParser(self, parser) :
    self.CategoryParser = parser
#    if getCommandType() == 'core' :
#      self.CommandParser.set_defaults(command=getCommandName(),
#                                      base_path=self.getBaseDir())
#    else :
#      self.CommandParser.set_defaults(command=getCommandName(),
#                                      base_path=self.getBaseDir(),
#                                      func=self.defaultFunction)

  def getCategoryParser(self) :
    return self.CategoryParser

  def loadCategoryInfo(self) :
    if not os.path.isdir(self.getCategoryPath()) :
      self.setConfigDataAsDefault()

    self.CategoryConfig = self.getConfigInfo()

  def setCategoryDataAsDefault(self) :
    if not os.path.isdir(self.getCategoryPath()) :
      os.mkdir(self.getCategoryPath())

  def saveCategoryInfo(self, json) :
    pass

  def addCategoryOption(self, _option, nargs='+', choices=()) :
    if len(choices) == 0 :
      self.getCategoryParser().add_argument(_option, nargs=nargs)
    else :
      self.getCategoryParser().add_argument(_option, nargs=nargs, choices=choices)

  def delCategoryOption(self, _option) :
    pass

  def addCommand(self, args):
    print 'BASE PATH :: ' + args.base_path
    print 'New Command :: ' + args.command_name[0]
    base_path = args.base_path.encode('utf-8')
    command_name = args.command_name[0]
    os.system('touch ' + os.path.join(base_path, 'commands', command_name))
    f = open(os.path.join(base_path, 'commands', command_name), 'w')
    f.write('#!/bin/bash\n\n')
    f.write('echo %s' % command_name)
    self.config['commands'][command_name] = {}
    Command(command_name, self.subparser, self.commands_dir)
    self.updateConfig()
    updateCmd()

  def delCommand(self, args):
    print 'BASE PATH :: ' + args.base_path
    print "delCommand in Category"
    os.system('rm ' + os.path.join(args.base_path, 'commands', args.var))
    updateCmd()
    #os.system('rm ' + os.path.join(args.base_path, args.var))
    #argcomplete.autocomplete(self.parser)
    #self.options = self.parser.parse_args()

  def editCommand(self, args):
    print 'BASE PATH :: ' + args.base_path
    print "editCommand in Category"


"""
    self.category_name = category_name
    self.category_type = category_type
    self.commands_dir = os.path.join(self.base_dir, 'commands')

    # Parser of this Category
    category_parser = parser.add_parser(self.category_name, add_help=False)
    self.subparser = category_parser.add_subparsers()
    #if self.category_type == 'core' :
    #  self.setCoreCommand(parser, self.base_dir)
    #else :
    self.config = self.loadCategoryInfo()
    self.setUserCommand(self.config)

    print self.category_type
    print "::::" + self.category_type
    if self.category_type != 'core' :
      print "::::" + self.category_type

      self.setUserCommand(self.config)

    self.setCoreCommand()
  def setCoreCommand(self) :
    addCommandHandler=Command('add', self.subparser, self.base_dir, self.addCommand)
    addCommandHandler.addOption('command_name', nargs='*')
    Command('rm', self.subparser, self.base_dir, self.delCommand)
    Command('edit', self.subparser, self.base_dir, self.editCommand)

  def setUserCommand(self, config) :
    for command in config["commands"] :
      print 'command ::: '+ command
      Command(command, self.subparser, self.base_dir)

  def loadCategoryInfo(self) :
    if not os.path.isdir(self.base_dir) :
      os.mkdir(self.base_dir)
      os.mkdir(os.path.join(self.base_dir,'commands'))

      with open(os.path.join(self.base_dir, 'config'), 'w') as json_handler :
        json.dump({ 
                    u'commands':{},
                    u'category_type':self.category_type
                  }, 
                  json_handler, indent=4)
      
    with open(os.path.join(self.base_dir, 'config'), 'rw') as config_handler :
      config = json.load(config_handler)

    return config

  def updateConfig(self) :
    with open(os.path.join(self.base_dir, 'config'), 'w') as json_handler :
      json.dump(self.config, json_handler, indent=4, sort_keys=True)

  def addCommand(self, args):
    print 'BASE PATH :: ' + args.base_path
    print 'New Command :: ' + args.command_name[0]
    base_path = args.base_path.encode('utf-8')
    command_name = args.command_name[0]
    os.system('touch ' + os.path.join(base_path, 'commands', command_name))
    f = open(os.path.join(base_path, 'commands', command_name), 'w')
    f.write('#!/bin/bash\n\n')
    f.write('echo %s' % command_name)
    self.config['commands'][command_name] = {}
    Command(command_name, self.subparser, self.commands_dir)
    self.updateConfig()
    updateCmd()

  def delCommand(self, args):
    print 'BASE PATH :: ' + args.base_path
    print "delCommand in Category"
    os.system('rm ' + os.path.join(args.base_path, 'commands', args.var))
    updateCmd()
    #os.system('rm ' + os.path.join(args.base_path, args.var))
    #argcomplete.autocomplete(self.parser)
    #self.options = self.parser.parse_args()

  def editCommand(self, args):
    print 'BASE PATH :: ' + args.base_path
    print "editCommand in Category"

  def setBaseDir(self, base_dir) :
    self.base_dir = base_dir

  def loadCategoryInfo(self) :
    config = self.getConfigInfo()
    if 'categories' not in config or getCategoryName() not in config['categories'] :
      config = self.setCategoryDataAsDefault()

    self.CategoryConfig = config['categories'][getCategoryName()]

  def setCategoryDataAsDefault(self) :
    print self.getConfigPath()
    with open(self.getConfigPath(), 'rw') as config_handler :
      config = json.load(config_handler)
      if 'categories' not in config :
        config['categories'] = {}
      if not os.path.isdir(self.getCategoryPath()) :
        os.mkdir(self.getCategoryPath())

      config['categories'][self.getCategoryName()] = {}

      print config
      json.dump(config, config_handler, indent=4)
      return json.load(config_handler)
"""
