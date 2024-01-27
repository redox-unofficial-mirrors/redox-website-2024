import os
import re
import importlib
import template_utils

def template_file(file, wrapper, env = {}, glob = {}):
    with open(file, 'r') as html:
        data = html.read()
        html.close()
        return template(data, wrapper, env, glob)

def template(data, wrapper, env = {}, glob = {}):
    title = re.search(r"<h[1-6]>([^<]*)</h[1-6]>", data)
    
    if title is not None:
        title = title.group(1).capitalize()
    else:
        title = ' '.join(env['out'].split('/')[-1].split('.')[:-1]).capitalize()
    
    if isinstance(wrapper, str):
        data = "<{tag}>{body}</{tag}>".format(tag=wrapper, body=data)

    with open(os.path.abspath('./template.html'), 'r') as file:
        template = file.read()
        file.close()
        
    template_vars = {
        'file': file,
        'body': data,
        'glob': glob,
        'final_path': env['out'][len(env['build']):] if env['out'].startswith(env['build']) else env['out'],
        'title': title
    } | env
    
    global_modules = {
        k: getattr(template_utils, k) for k in dir(template_utils) if not k.startswith('_')
    } | { 'mod': importlib.import_module }

    while '<?py(' in template:
        block = template.index('<?py(')
        end = template.index(')?>', block)

        python = template[block + 5:end]

        template = template[:block] + str(eval(python, global_modules, template_vars)) + template[end + 3:]

    while '<?py{' in template:
        block = template.index('<?py{')
        end = template.index('}?>')

        python = template[block + 5:end]

        exec(python, global_modules, template_vars)

        template = template[:block] + template[end + 3:]
    
    return template
             
def escape(text):
    return text.replace('<', '&lt;').replace('>', '&gt;')
