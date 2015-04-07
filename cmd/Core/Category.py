#!/usr/bin/env python
# PYTHON_ARGCOMPLETE_OK
import os, json

from cmd.Base.Config import *
from cmd.Core.Command import *

class Category() :
  def __init__(self, category_name, parser) :
    # Set initial variable for Category Class
    self.setCategoryName(category_name)
    category_parser = parser.add_parser(self.getCategoryName(), add_help=False)
    self.setCategoryParser(category_parser.add_subparsers())

    #self.loadCategoryInfo()

  def setCategoryName(self, category_name) :
    self.CategoryName = category_name

  def getCategoryName(self) :
    return self.CategoryName

  def getCategoryPath(self) :
    return self.getBaseDir()

  def setCategoryParser(self, parser) :
    self.CategoryParser = parser

  def getCategoryParser(self) :
    return self.CategoryParser


class CategoryManager(Config) :
  def __init__(self, parser, base_dir, commandList = []) :
    Config.__init__(self, base_dir)

    self.loadCategoriesConfig()
    self.setCategoryManagerParser(parser)

    # To avoid multiple name with commands
    self.commandList = commandList

    # set category controller
    self.setCategoryController()

    # load Categories
    self.loadCategories()

  def setCategoryController(self) :
    cHandler = Category('category', self.getCategoryManagerParser())
    
    addHandler = Command('add', cHandler.getCategoryParser())
    addHandler.addCommandOption('categoryName', nargs = 1)
    addHandler.setCommandFunction(self.addCategoryFunction)

    delHandler = Command('del', cHandler.getCategoryParser())
    delHandler.addCommandOption('categoryName', nargs = 1,
                                choices=tuple(self.getCategoryList()))
    delHandler.setCommandFunction(self.delCategoryFunction)

    renameHandler = Command('rename', cHandler.getCategoryParser())
    renameHandler.addCommandOption('categoryName', nargs = 2,
                                choices=tuple(self.getCategoryList()))
    renameHandler.setCommandFunction(self.renameCategoryFunction)

  def addCategoryFunction(self, argument) :
    categoryName = argument.categoryName[0]

    if categoryName in self.getCategoryList() or categoryName in self.commandList or categoryName in ('add', 'del', 'rename') :
      print 'Error : %s is already existed in command name' % categoryName
      return

    newCategoryInfo = { 'name' : categoryName, 
                                'base_dir' : os.path.join(self.getCategoriesDir(), categoryName)}
    self.createCategoryDir(newCategoryInfo)

    CategoryConfig = self.getCategoriesConfig()
    CategoryConfig[categoryName] = newCategoryInfo

    self.updateCategoryConfig(CategoryConfig)
    print 'Add Category : %s is created' % categoryName

  def delCategoryFunction(self, argument) :
    categoryName = argument.categoryName[0]
    CategoryConfig = self.getCategoriesConfig()
    self.moveOldDir(CategoryConfig[categoryName])
    del CategoryConfig[categoryName]
    self.updateCategoryConfig(CategoryConfig)

  def renameCategoryFunction(self, argument) :
    categoryName = argument.categoryName[0]
    newCategoryName = argument.categoryName[1]
    CategoryConfig = self.getCategoriesConfig()
    temp = CategoryConfig[categoryName]
    del CategoryConfig[categoryName]
    temp['name'] = newCategoryName
    CategoryConfig[newCategoryName] = temp
    self.updateCategoryConfig(CategoryConfig)
    os.rename(os.path.join(self.getCategoriesDir(), categoryName),
                  os.path.join(self.getCategoriesDir(), newCategoryName))

  def setCategoryManagerParser(self, parser) :
    self.CategoryManagerParser = parser

  def getCategoryManagerParser(self) :
    return self.CategoryManagerParser

  def moveOldDir(self, categoryInfo) :
    oldDirPath = os.path.join(self.getCategoriesDir(), '__olddir__')
    if not os.path.isdir(oldDirPath) :
      os.mkdir(oldDirPath)
    os.rename(categoryInfo['base_dir'], os.path.join(oldDirPath, categoryInfo['name']))

  def createCategoryDir(self, categoryInfo) :
    if categoryInfo['name'] in os.listdir(self.getCategoriesDir()) :
      print 'Error : %s is already existed in category name ' % categoryInfo['name']
      return

    os.mkdir(categoryInfo['base_dir'])

  def getCategoriesDir(self) :
    return os.path.join(self.getBaseDir(), 'categories')

  def getCategoriesConfig(self) :
    return self.CategoriesConfig

  def getCategoryList(self) :
    return self.categoriesList

  def setCategoriesList(self, config) :
    self.categoriesList = []
    for category in config['categories'] :
      self.categoriesList.append(category)

  def loadCategoriesConfig(self) :
    config = self.getConfigInfo()
    if 'categories' not in config :
      config = self.setCategoryDataAsDefault()

    if not os.path.isdir(self.getCategoriesDir()) :
      os.mkdir(self.getCategoriesDir())

    self.CategoriesConfig = config['categories']
    self.setCategoriesList(config)

  def setCategoryDataAsDefault(self) :
    with open(self.getConfigPath(), 'rw') as config_handler :
      config = json.load(config_handler)
      if 'categories' not in config :
        config['categories'] = {}

      self.setConfigInfo(config)

    return config

  def loadCategories(self) :
    categoriesConfig = self.getCategoriesConfig()
    for category in categoriesConfig :
      categoryInfo = categoriesConfig[category]
      categoryHandler = Category(categoryInfo['name'], self.getCategoryManagerParser())
      CommandManager(categoryHandler.getCategoryParser(), categoryInfo['base_dir'])

  def updateCategoryConfig(self, categoryConfig) :
    config = self.getConfigInfo()
    config['categories'] = categoryConfig
    self.setConfigInfo(config)
