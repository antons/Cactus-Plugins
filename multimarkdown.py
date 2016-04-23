"""
MultiMarkdown plugin. Options may be provided in config.
"multimarkdown-options": [ 
    "--random" 
]
"""

import subprocess
import tempfile

from cactus.template_tags import register

from django.utils.encoding import force_text
from django.utils.safestring import mark_safe

MMD_OPTIONS=[]

def multimarkdown(value, arg=''):
    with tempfile.NamedTemporaryFile() as temp:
        temp.write(force_text(value).encode('utf8'))
        temp.flush()
        command = ['multimarkdown']
        command.extend(MMD_OPTIONS)
        command.append(temp.name)
        html = subprocess.check_output(command)
        return mark_safe(html)

def preBuild(site):
    global MMD_OPTIONS
    MMD_OPTIONS = site.config.get('multimarkdown-options', [])
    register.filter('multimarkdown', multimarkdown, isSafe=True)
    register.filter('mmd', multimarkdown, isSafe=True)
