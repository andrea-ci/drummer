#!/usr/bin/python3
# -*- coding: utf-8 -*-
import argparse

parser = argparse.ArgumentParser(description='Process some integers.')

parser.add_argument(    'echo',
                        help='echo the string you use here')

parser.add_argument(    '-v', '--verbose',
                        help='increase output verbosity',
                        action='count',
                        default=0)

#parser.add_argument('integers', metavar='N', type=int, nargs='+', help='an integer for the accumulator')

#parser.add_argument('--sum', dest='accumulate', action='store_const', const=sum, default=max, help='sum the integers (default: find the max)')


args = parser.parse_args()
print(args)
#print(args.accumulate(args.integers))
