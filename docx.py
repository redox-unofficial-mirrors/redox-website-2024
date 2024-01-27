#!/usr/bin/python3

import subprocess
import tempfile
import argparse
import pathlib
import sys
import os

from template import template_file

tmp_fd, tmp_path = tempfile.mkstemp()

parser = argparse.ArgumentParser(description="DocX Filetype Support")

parser.add_argument('--source', metavar="source", help="The document to be templated")
parser.add_argument('--build', metavar="build", help="The directory where all build resources are stored")
parser.add_argument('--out', metavar="out", help="The complete path of the final resource")
parser.add_argument('--root', metavar="root", help="The complete path of the page root")
parser.add_argument('--languages', metavar="languages", help="Which languages are emitted")
parser.add_argument('--lang', metavar="lang", help="Which language is currently being compiled")

args = parser.parse_args(sys.argv[1:])

subprocess.run(['pandoc', args.source, '--from', 'docx', '--to', 'html', '--embed-resources', '--reference-doc', './reference.docx', '--section-divs'], stdout=tmp_fd)

os.makedirs(pathlib.Path(args.out).parent, exist_ok=True)

with open(args.out, 'w+') as out:
    out.write(template_file(tmp_path, 'article', { 
        'out': args.out,
        'source': args.source,
        'build': args.build,
        'root': args.root,
        'languages': args.languages.split(','),
        'lang': args.lang,
    }, {}))
