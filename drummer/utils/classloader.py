#!/usr/bin/python3
# -*- coding: utf-8 -*-

class ClassLoaderException(Exception):
    pass

class ClassLoader():
    """ loads class from the given module path """

    def load(self, filename, classname):

        try:
            # import the class
            #mod_to_import = path.join(filename, classname.lower()).replace('/','.')
            mod_to_import = filename.replace('/','.')

            mod = __import__(mod_to_import, fromlist=[classname])

            LoadedClass = getattr(mod, classname)

        except:
            raise ClassLoaderException('Unable to load class')

        return LoadedClass
