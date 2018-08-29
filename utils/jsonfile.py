#!/usr/bin/python3
# -*- coding: utf-8 -*-
import json

class JsonFile():

    @staticmethod
    def write(filename, data):

        # save file
        with open(filename,'w') as f:
            json.dump(data, f, sort_keys=True, indent=4, ensure_ascii=False)

        return True


    @staticmethod
    def read(filename):

        # read file
        with open(filename,'r',encoding='utf-8') as fp:
            data = json.load(fp)

        return data
