#!/usr/bin/python3
# -*- coding: utf-8 -*-
from console.argparsing import Pattern

class Runner:

    @staticmethod
    def execute(args):

        # evaluate user input
        truth_table = Pattern().compare_with(args)

        # execute proper command
        print(truth_table)
