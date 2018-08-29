#!/usr/bin/python3
# -*- coding: utf-8 -*-
from console.loader import CommandLoader
from console.parsing import Tokenizer, TokenTree

# load patterns from file
patterns = CommandLoader.load()

tokens = {}
tokenizer = Tokenizer()
token_tree = TokenTree()

for p in patterns:

    print(p)

    # tokenize
    tokens, locs = tokenizer.from_source(p, tokens)

    token_tree.build(tokens, locs)




"""
# build pattern tree
for p in patterns:

    pattern_tree = {}

    positions = []
    for idx, tok in tokens.items():
        #print(tok.content)

        pos = p.find(tok.content)

        if pos>0:
            positions.append(pos)

    sorted_positions = sorted(range(len(positions)), key=positions.__getitem__)

    for ii,jj in enumerate(sorted_positions[:-1]):
        pattern_tree[jj] = sorted_positions[ii+1]

    print(sorted_positions)
    print(pattern_tree)


for ii,t in tokens.items():
    print(t.content)
"""
