#!/usr/bin/python3
# -*- coding: utf-8 -*-
from sys import argv as sys_argv
from console.argparsing import Pattern

pattern = Pattern()
truth_table = pattern.compare_with(sys_argv)

print(truth_table)
