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
    self.commandManager = CommandManager(self.getAutoCommandParser(), self.getBaseDir())

    # Initialize Category Controller
    self.categoryManager = CategoryManager(self.getAutoCommandParser(), self.getBaseDir(), self.commandManager.getCommandsList())

    # Applied Auto Complete
    argcomplete.autocomplete(parser)
    self.options = parser.parse_args()

  def setAutoCommandParser(self, parser) :
    self.AutoCommandParser = parser

  def getAutoCommandParser(self) :
    return self.AutoCommandParser

  def getAutoCommandDir(self) :
    return self.getBaseDir()

  def loadAutoCommandInfo(self) :
    self.AutoCommandConfig = self.getConfigInfo()

if __name__ == "__main__":
  autoCmd = AutoCommand()
  autoCmd.options.func(autoCmd.options) 
