#!/usr/bin/python3
# -*- coding: utf-8 -*-
from utils.yamlfile import YamlFile
from os import path

class ConfigurationException(Exception):
    pass


class Configuration():

    @staticmethod
    def load():

        filename = path.join('config','sledge-config.yml')

        try:
            configuration = YamlFile.read(filename)
        except:
            raise ConfigurationException('configuration not found')

        return configuration
