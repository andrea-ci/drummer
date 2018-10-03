#!/usr/bin/python3
# -*- coding: utf-8 -*-
from os import path

class ClassLoaderException(Exception):
    pass

class ClassLoader():
    """ loads and returns a class given its full path """

    def load(self, classpath, classname):

        try:
            # import the class
            mod_to_import = path.join(classpath, classname.lower()).replace('/','.')
            
            mod = __import__(mod_to_import, fromlist=[classname])
            LoadedClass = getattr(mod, classname)

        except:
            raise ClassLoaderException('unable to load class')

        return LoadedClass
