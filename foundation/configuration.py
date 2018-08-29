#!/usr/bin/python3
# -*- coding: utf-8 -*-
from utils.yamlfile import YamlFile
from os import path

class ConfigurationException(Exception):
    pass


class Configuration():

    @staticmethod
    def get():

        filename = path.join('config', 'sledge-config.yaml')

        configuration = YamlFile.read(filename)

        return configuration
