import os
import sys
from pathlib import Path

def include(file):
    with open(os.path.abspath(file), 'r') as file:
        return file.read()

def map_source_to_dest(page_root, build_dir, full_path):
    build_dir = os.path.abspath(build_dir)
    page_root = os.path.abspath(page_root)
    
    if not full_path.startswith(page_root):
        return None
    
    relative_path = full_path[len(page_root) + 1:]
    
    split = relative_path.split('.')
    matcher = split[-1]
    language = split[-2]
    
    if len(split) <= 2:
        print("Invalid filename: {}".format(full_path), file=sys.stderr)
        return None
    
    return (os.path.join(build_dir, language, '.'.join(split[:-2]) + '.html'), matcher, language)

def map_source_to_http(page_root, build_dir, full_path):
    build_dir = os.path.abspath(build_dir)
    page_root = os.path.abspath(page_root)
    
    if not full_path.startswith(page_root):
        return None
    
    relative_path = full_path[len(page_root) + 1:]
    
    split = relative_path.split('.')
    matcher = split[-1]
    language = split[-2]
    
    if len(split) <= 2:
        print("Invalid filename: {}".format(full_path), file=sys.stderr)
        return None
    
    return (os.path.join('/', language, '.'.join(split[:-2]) + '.html'), matcher, language)
