#!/usr/bin/python3
# -*- coding: utf-8 -*-
import yaml

class YamlFile():

    @staticmethod
    def read(filename):

        with open(filename, 'r', encoding='utf-8') as f:
                filedata = yaml.load(f)

        return filedata
