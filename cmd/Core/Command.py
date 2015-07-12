#!/usr/bin/env python
# PYTHON_ARGCOMPLETE_OK
import os, json, argparse

from cmd.Base.Config import *

class Command() :
  def __init__(self, command_name, parser) :
    # Set initial variable for Command Class
    self.setCommandName(command_name)
    subparser = parser.add_parser(self.getCommandName(), formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    self.setCommandParser(subparser)

    # Set Function by reference call
    self.addCommandOption = self.getCommandParser().add_argument

  def setCommandName(self, command_name) :
    self.CommandName = command_name

  def getCommandName(self) :
    return self.CommandName

  def setExecFilePath(self, exec_path) :
    self.command_info['exec_path'] = exec_path

  def getExecFilePath(self) :
    return self.command_info['exec_path']

  def setCommandInfo(self, command_info) :
    self.command_info = command_info

  def getCommandInfo(self) :
    return self.command_info

  def setCommandParser(self, parser) :
    self.CommandParser = parser

  def getCommandParser(self) :
    return self.CommandParser

  def setCommandFunction(self, function) :
    self.getCommandParser().set_defaults(func=function)

    if hasattr(self, 'command_info') and not self.command_info['option'] is None :
      for opt in self.command_info['option'] :
        if type(opt) is unicode :
          self.getCommandParser().add_argument('--'+opt, action='store_true')
        elif type(opt) is dict :
          for item in opt :
            self.getCommandParser().add_argument('--'+item, choices=opt[item])
    self.getCommandParser().add_argument('argv', nargs='*')

  def execCommandFunction(self, args) :
    # todo :
    # ['']+args.argv,
    # Because execve cannot recognize the first argument of "args.argv"
    opt_list = ['']
    for k, v in args.__dict__.iteritems() :
      if v == True :
        opt_list.append(k)
      elif not k is 'func' and not k is 'argv' and not v is None:
        opt_list.append(v)

    os.execve(self.getExecFilePath(), opt_list+args.argv, {})

class CommandManager(Config) :
  def __init__(self, parser, base_dir) :
    Config.__init__(self, base_dir)

    self.loadCommandConfig()
    self.setCommandManagerParser(parser)

    # set Control Command such as add, del, edit...
    self.setControlCommands()

    # load Commands
    self.loadCommands()

  def getCommandsDir(self) :
    return os.path.join(self.getBaseDir(), 'commands')

  def getCommandsConfig(self) :
    return self.CommandsConfig

  def getCommandsList(self) :
    return self.commandsList

  def setCommandsList(self, config) :
    self.commandsList = []
    for command in config['commands'] :
      self.commandsList.append(command)

  def setCommandManagerParser(self, parser) :
    self.CommandManagerParser = parser

  def getCommandManagerParser(self) :
    return self.CommandManagerParser

  def loadCommandConfig(self) :
    config = self.getConfigInfo()
    if 'commands' not in config :
      config = self.setCommandDataAsDefault()

    if not os.path.isdir(self.getCommandsDir()) :
      os.mkdir(self.getCommandsDir())

    self.CommandsConfig = config['commands']
    self.setCommandsList(config)

  def updateCommandConfig(self, commandConfig) :
    config = self.getConfigInfo()
    config['commands'] = commandConfig
    self.setConfigInfo(config)
    

  def setCommandDataAsDefault(self) :
    with open(self.getConfigPath(), 'rw') as config_handler :
      config = json.load(config_handler)
      if 'commands' not in config :
        config['commands'] = {}

      self.setConfigInfo(config)

    return config

  def createCommandFile(self, commandInfo) :
    f = open(commandInfo['exec_path'], 'a+')

    if commandInfo['type'] == 'sh' :
      f.write('#!/bin/bash\n\n')
      f.write('echo %s' % commandInfo['name'])
    elif commandInfo['type'] == 'py' :
      f.write('#!/usr/bin/env python\n\n')
      f.write('print \'%s\'' % commandInfo['name'])

    f.close()
    os.chmod(commandInfo['exec_path'], 0775)

  def setControlCommands(self) :
    addHandler = Command('add', self.getCommandManagerParser())
    addHandler.addCommandOption('-t', '--type', nargs = 1,
                                choices=('sh','py','core'), default=['sh'])
    addHandler.addCommandOption('-o', '--option', nargs = '*')
    addHandler.addCommandOption('commandName', nargs = 1)
    addHandler.setCommandFunction(self.addCommandFunction)

    delHandler = Command('del', self.getCommandManagerParser())
    delHandler.addCommandOption('commandName', nargs = 1,
                                choices=tuple(self.getCommandsList()))
    delHandler.setCommandFunction(self.delCommandFunction)

    editHandler = Command('edit', self.getCommandManagerParser())
    editHandler.addCommandOption('commandName', nargs = 1,
                                 choices=tuple(self.getCommandsList()))
    editHandler.setCommandFunction(self.editCommandFunction)

    confHandler = Command('conf', self.getCommandManagerParser())
    confHandler.addCommandOption('args', nargs = '?')
    confHandler.setCommandFunction(self.confCommandFunction)

  def loadCommands(self) :
    commandsConfig = self.getCommandsConfig()
    for command in commandsConfig :
      commandHandler = Command(commandsConfig[command]['name'], self.getCommandManagerParser())
      commandHandler.setCommandInfo(commandsConfig[command])
      commandHandler.setCommandFunction(commandHandler.execCommandFunction)


  def addCommandFunction(self, argument) :
    commandName = argument.commandName[0]
    commandType = argument.type[0]
    commandOption = argument.option

    if commandName in self.getCommandsList() or commandName in ('add', 'del', 'edit') :
      print 'Error : command %s is already existed' % commandName
      return

    if commandType == 'core' :
      exec_path = None
    else :
      exec_path = os.path.join(self.getCommandsDir(),
                               commandName+'.'+commandType)

    newCommandInfo = { 'name' : commandName,
                       'type' : commandType,
                       'option' : commandOption,
                       'exec_path' : exec_path }

    self.createCommandFile(newCommandInfo)

    CommandConfig = self.getCommandsConfig()
    CommandConfig[commandName] = newCommandInfo

    self.updateCommandConfig(CommandConfig)
    print 'Add Command : %s is created' % commandName

  def delCommandFunction(self, argument) :
    commandName = argument.commandName[0]
    CommandConfig = self.getCommandsConfig()
    self.moveOldDir(CommandConfig[commandName])
    del CommandConfig[commandName]
    self.updateCommandConfig(CommandConfig)

  def editCommandFunction(self, argument) :
    commandName = argument.commandName[0]
    config = self.getCommandsConfig()
    os.system('vim %s' % config[commandName]['exec_path'])

  def confCommandFunction(self, argument) :
    os.system('vim %s' % self.getConfigPath())

  def moveOldDir(self, commandInfo) :
    oldDirPath = os.path.join(self.getCommandsDir(), '__olddir__')
    if not os.path.isdir(oldDirPath) :
      os.mkdir(oldDirPath)
    os.rename(commandInfo['exec_path'], os.path.join(oldDirPath, commandInfo['name']) + '.' + commandInfo['type'])

