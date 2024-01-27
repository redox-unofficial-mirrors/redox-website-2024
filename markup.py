#!/usr/bin/python3

import sys
import argparse

from template import template


parser = argparse.ArgumentParser(description="HTML Filetype Support")

parser.add_argument('--source', metavar="source", help="The document to be templated")
parser.add_argument('--build', metavar="build", help="The directory where all build resources are stored")
parser.add_argument('--out', metavar="out", help="The complete path of the final resource")
parser.add_argument('--root', metavar="root", help="The complete path of the page root")
parser.add_argument('--languages', metavar="languages", help="Which languages are emitted")
parser.add_argument('--lang', metavar="lang", help="Which language is currently being compiled")
                    
args = parser.parse_args(sys.argv[1:])

with open(args.source, 'r') as source, open(args.out, 'w+') as dest:
    dest.write(template(source.read(), 'article', { 
        'out': args.out,
        'source': args.source,
        'build': args.build,
        'root': args.root,
        'languages': args.languages.split(','),
        'lang': args.lang,
    }, {}))
