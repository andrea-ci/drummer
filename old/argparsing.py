#!/usr/bin/python3
# -*- coding: utf-8 -*-
import re
from sys import exit as sys_exit

# token detection
RE_CMD = re.compile(r'\w+')
RE_NAME = RE_CMD
RE_REQ_GROUP = re.compile(r'\(.+\)')
RE_OPT_GROUP = re.compile(r'\[.+\]')
RE_ARG = re.compile(r'<\w+>')
RE_LOPT = re.compile(r'--\w+')
RE_SOPT = re.compile(r'-\w+')

ARGUMENT = 'argument'
COMMAND = 'command'
L_OPTION = 'long_option'
S_OPTION = 'short_option'
REQ_GROUP = 'req_group'
OPT_GROUP = 'opt_group'


class UsageException(Exception):
    pass


class Token():

    def __init__(self, category, content):
        self.category = category
        self.content = content


class TokenGroup(Token):
    pass


class Tokenizer():

    def from_source(self, source, tokens):

        locs = []

        # token groups
        source, tokens, locs = self.get_groups(source, tokens, locs)

        # arguments
        source, tokens, locs = self.get_tokens(source, tokens, locs)

        # token ids of usage pattern
        usage_pattern = self.prepare_pattern(locs)

        return tokens, usage_pattern


    def get_tokens(self, source, tokens, locs):

        for category in [ARGUMENT, L_OPTION, S_OPTION, COMMAND]:
            source, tokens, locs = self.get_token_by_category(category, source, tokens, locs)

        return source, tokens, locs


    def get_groups(self, source, tokens, locs):

        for category in [REQ_GROUP, OPT_GROUP]:
            source, tokens, locs = self.get_group_by_category(category, source, tokens, locs)

        return source, tokens, locs


    def get_group_by_category(self, category, source, tokens, locs):

        if category == REQ_GROUP:
            regex = RE_REQ_GROUP
        elif category == OPT_GROUP:
            regex = RE_OPT_GROUP
        else:
            regex = None

        for m in regex.finditer(source):

            # parse group content
            _, tokens, tmp_locs = self.get_tokens(source[m.start()+1:m.end()-1], tokens, [])

            # token ids in group token
            group_elements = [loc[0] for loc in tmp_locs]

            # add group token
            num_tokens = len(tokens)

            tidx = m.start()

            tid = self.exists(category, group_elements, tokens)

            # if not existing, add token
            if not tid:
                tid = num_tokens
                tokens[tid] = TokenGroup( category, group_elements )

            # add token location
            locs.append( (tid, tidx) )

            # clean source
            n = len(m.group())
            source = source.replace(m.group(), (' '*n))

        return source, tokens, locs


    def get_token_by_category(self, category, source, tokens, locs):

        # regex selection
        if category == ARGUMENT:
            regex = RE_ARG
        elif category == L_OPTION:
            regex = RE_LOPT
        elif category == S_OPTION:
            regex = RE_SOPT
        elif category == COMMAND:
            regex = RE_CMD
        else:
            regex = None

        # token search
        for m in regex.finditer(source):

            num_tokens = len(tokens)

            content = m.group()
            tidx = m.start()

            tid = self.exists(category, content, tokens)

            # if not existing, add token
            if not tid:
                tid = num_tokens
                tokens[tid] = Token( category, content )

            # add token location
            locs.append( (tid, tidx) )

            # clean source
            n = len(m.group())
            source = source.replace(m.group(), (' '*n))

        return source, tokens, locs


    def exists(self, category, content, tokens):

        tid = None
        for idx, tok in tokens.items():

            if (tok.category == category and tok.content == content):

                tid = idx
                break

        return tid


    def prepare_pattern(self, locs):

        token_positions = [ll[1] for ll in locs]

        token_idxs = sorted(range(len(token_positions)), key=token_positions.__getitem__)

        sorted_tids = [locs[ii][0] for ii in token_idxs]

        return sorted_tids


class User():

    @staticmethod
    def create_from(arg_list):

        tokens = []

        if len(arg_list)>1:

            for arg in arg_list[1:]:

                if RE_LOPT.match(arg):
                    m = RE_LOPT.match(arg)
                    tokens.append(m.group())

                elif RE_SOPT.match(arg):
                    m = RE_SOPT.match(arg)
                    tokens.append(m.group())

                elif RE_NAME.match(arg):
                    m = RE_NAME.match(arg)
                    tokens.append(m.group())

        return tokens


class Help():

    @staticmethod
    def get(usage_lines):

        help = '\n  Usage:\n'
        for line in usage_lines:
            help += '    {0}\n'.format(line)

        return help


class Pattern():

    def __init__(self, usage_lines):

        # command patterns
        self.usage_lines = usage_lines


    def compare_with(self, user_line):

        pattern_match = False

        # parse input line
        user_pattern = User.create_from(user_line)

        # pattern tokenizer
        tokenizer = Tokenizer()
        tokens = {}

        for ul in self.usage_lines:

            # tokenize usage pattern
            tokens, usage_pattern = tokenizer.from_source(ul, tokens)

            # compare with user input
            pattern_match, truth_table = self.user_matches(tokens, usage_pattern, user_pattern)

            if pattern_match:
                break

        if not pattern_match:

            # gracefully exit
            print(Help.get(self.usage_lines))
            sys_exit()

        return truth_table


    def user_matches(self, tokens, usage_pattern, user_pattern):

        # truth table
        truth_table = {}

        ii = 0
        jj = 0
        matching = True

        while matching and ii<len(usage_pattern) and jj<len(user_pattern):

            # usage token
            usage_id = usage_pattern[ii]
            usage_token = tokens[usage_id]

            # user token
            user_token = user_pattern[jj]

            if usage_token.category == COMMAND:

                matching = usage_token.content == user_token

                if matching:
                    truth_table[usage_token.content] = True
                else:
                    truth_table[usage_token.content] = False

                jj += 1

            elif usage_token.category == ARGUMENT:

                m = RE_NAME.match(user_token)
                if m:
                    matching = True
                else:
                    matching = False

                truth_table[usage_token.content] = user_token

                jj += 1

            elif usage_token.category in [L_OPTION, S_OPTION]:

                if usage_token.content == user_token:

                    truth_table[usage_token.content] = True

                    jj += 1

                else:
                    truth_table[usage_token.content] = False

            elif usage_token.category == REQ_GROUP:

                mutex_elements = usage_token.content

                matching = False
                for mid in mutex_elements:

                    mutex_token = tokens[mid]

                    if mutex_token.content == user_token:

                        truth_table[mutex_token.content] = True
                        matching = True

                        jj += 1

                        break

                    else:
                        truth_table[mutex_token.content] = False

            elif usage_token.category == OPT_GROUP:

                mutex_elements = usage_token.content

                matching = False
                for mid in mutex_elements:

                    mutex_token = tokens[mid]

                    if mutex_token.content == user_token:

                        truth_table[mutex_token.content] = True
                        matching = True

                        jj += 1

                        break

                    else:
                        truth_table[mutex_token.content] = False

                if not matching:
                    matching = True

            else:
                raise UsageException('token not supported')

            ii += 1

        # check for user tokens left and not supported
        if len(user_pattern[jj:])>0:
            matching = False

        # check for required tokens left in pattern and not matched
        if len(usage_pattern[ii:])>0:
            left_tokens = [idx for idx in usage_pattern[ii:] if (tokens[idx].category not in (L_OPTION, S_OPTION, OPT_GROUP))]
            if len(left_tokens)>0:
                matching = False

        return matching, truth_table
