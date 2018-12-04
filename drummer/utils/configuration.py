#!/usr/bin/python3
# -*- coding: utf-8 -*-
from utils.files import YamlFile
from os import path

class ConfigurationException(Exception):
    pass


class Configuration():

    @staticmethod
    def load():

        config_filename = path.join('..', *('config','drummer-config.yml'))
        tasks_filename = path.join('..', *('config','drummer-tasks.yml'))

        try:
            configuration = YamlFile.read(config_filename)

        except:
            raise ConfigurationException('Configuration file not found')

        try:
            tasks = YamlFile.read(tasks_filename)
            configuration['tasks'] = tasks

        except:
            raise ConfigurationException('Task file not found')

        return configuration
