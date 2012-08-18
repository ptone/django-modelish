#!/usr/bin/env python

import os
import sys

import args
from yaml import load

from modelish.generate import generate_source, DEFAULT_GRAMMARISH

HELP = "usage:  modelish <source.yml> [--grammar=<grammar.yml> --extra-grammar=<grammar.yml>]"

def simple_error(m):
    sys.stderr.write(m + '\n')
    sys.stderr.write(HELP + '\n')
    sys.exit(1)

def main():
    if not args.files:
        simple_error('no source yaml file provided')
    if len(args.files) > 1:
        simple_error('more than one file provided')
    f = args.files[0]
    if not os.path.exists(f):
        simple_error('no such file: {}'.format(f))

    model_source = load(open(f))
    grammar = DEFAULT_GRAMMARISH
    if '--grammar' in args.assignments:
        f = args.assignments['--grammar']
        if not os.path.exists(f):
            simple_error('no such file: {}'.format(f))
        grammar = load(open(f))
    extra_grammar = {}
    if '--extra-grammar' in args.assignments:
        f = args.assignments['--extra-grammar']
        if not os.path.exists(f):
            simple_error('no such file: {}'.format(f))
        extra_grammar = load(open(f))
        grammar.update(extra_grammar)
    python_source = generate_source(model_source, grammar)
    print python_source

if __name__ == '__main__':
    main()
