# -*- coding: utf-8 -*-
#
# StepScan doc

import sys, os

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#sys.path.append(os.path.abspath('.'))

# sys.path.append(os.path.abspath(os.path.join('..', 'lib')))
sys.path.insert(0, os.path.abspath(os.path.join('sphinx', 'ext')))
sys.path.insert(0, 'macros')


# -- General configuration -----------------------------------------------------
extensions = ['sphinx.ext.autodoc', 'sphinx.ext.mathjax',
              'sphinx.ext.napoleon', 'sphinxcontrib.video',
              'sphinx_copybutton']


templates_path = ['_templates']
source_suffix = {'.rst': 'restructuredtext'}

master_doc = 'index'
project = u'GSECARS Microprobe'
copyright = u'2025, Matthew Newville'

release = 'September 28, 2025'

exclude_trees = ['_build', 'sphinx']

exclude_trees = ['_build']
default_role = None
source_encoding = 'utf-8'

add_function_parentheses = True
add_module_names = True

pygments_style = 'sphinx'

# The theme to use for HTML and HTML Help pages.  Major themes that come with
# Sphinx are currently 'default' and 'sphinxdoc'.
html_theme_path = ['sphinx_theme']
html_theme = 'bizstyle'

html_static_path = ['_static']
html_sidebars = {
  'index': ["indexsidebar.html",  "sourcelink.html", "searchbox.html"],
  "*": [ "localtoc.html",  "relations.html", "sourcelink.html", "searchbox.html"]
}
html_title = 'GSECARS X-ray Microprobe Beamline, APS 13-ID-E'
html_short_title = 'GSECARS X-ray Microprobe'

html_domain_indices = False
html_use_index = True
html_show_sourcelink = True
