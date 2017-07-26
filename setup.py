#-*- coding:utf-8 -*-
from distutils.core import setup
import py2exe

setup(name='BMAssistant',
      version='1.3',
      description='A bookmark assistant',
      author='vetains',
      author_email='vetains@163.com',
      py_modules=['BMAssistant'],
      console=['BMAssistant.py'],
      windows=["BMAssistant.py"],options = { "py2exe":{"dll_excludes":["MSVCP90.dll"]}})
