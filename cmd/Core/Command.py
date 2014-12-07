#!/usr/bin/env python
# PYTHON_ARGCOMPLETE_OK
import os, json

from cmd.Base.Config import *

class Command(Config) :
  def __init__(self, 
               command_name, 
               parser) :
    # Set initial variable for Command Class
    self.setCommandName(command_name)
    subparser = parser.add_parser(self.getCommandName(), add_help=False)
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

  def saveCommandInfo(self, json) :
    pass

  def delCommandOption(self, _option) :
    pass

  def setCommandFunction(self, function) :
    self.getCommandParser().set_defaults(func=function)

  def execCommandFunction(self, args) :
    os.execve(self.getExecFilePath(), (), {})

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
    print argument

  def editCommandFunction(self, argument) :
    commandName = argument.commandName[0]
    config = self.getCommandsConfig()
    os.system('vim %s' % config[commandName]['exec_path'])


