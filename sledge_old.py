#!/usr/bin/python3
# -*- coding: utf-8 -*-
from sys import argv as sys_argv
from utils.argparsing import Pattern
from utils.yamlfile import YamlFile

class CommandException(Exception):
    pass


class CommandLoader():

    @staticmethod
    def load():

        try:
            filedata = YamlFile.read('config/sledge-commands.yml')
            commands = filedata['commands']

        except:
            raise CommandException('cannot load commands from file')

        return commands


usage_lines = CommandLoader.load()

pattern = Pattern(usage_lines)
truth_table = pattern.compare_with(sys_argv)

print(truth_table)
