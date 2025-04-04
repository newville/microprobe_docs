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

extensions = ['sphinx.ext.autodoc',
              'sphinx.ext.mathjax',
              'sphinx.ext.ifconfig',
              'sphinx.ext.linkcode',
              'sphinx.ext.napoleon']

def linkcode_resolve(domain, info):
    print("Linke Code ", domain, info)
    if domain != 'py':
        return None
    mname = info.get('module', '')
    if mname in (None, '', 'None'):
        return None
    link = 'file:///U:/xas_user/config/13ide/escan_macros'
    return '%s/%s.py' % (link, mname)


templates_path = ['_templates']
source_suffix = '.rst'

master_doc = 'index'
project = u'GSECARS Microprobe'
copyright = u'2025, Matthew Newville'

release = 'March 2025'

exclude_trees = ['_build', 'sphinx']

add_function_parentheses = True
add_module_names = False

pygments_style = 'sphinx'

# A list of ignored prefixes for module index sorting.
#modindex_common_prefix = []


# -- Options for HTML output ---------------------------------------------------

# The theme to use for HTML and HTML Help pages.  Major themes that come with
# Sphinx are currently 'default' and 'sphinxdoc'.
html_theme_path = ['sphinx/theme']
html_theme = 'default'
# html_theme = 'sphinxdoc'

html_theme = 'bizstyle'

# Add any paths that contain custom themes here, relative to this directory.
#html_theme_path = []

# The name for this set of Sphinx documents.  If None, it defaults to
# "<project> v<release> documentation".
#html_title = None
html_title = 'GSECARS X-ray Microprobe Beamline, APS 13-ID-E'

# A shorter title for the navigation bar.  Default is the same as html_title.
html_short_title = 'GSECARS X-ray Microprobe'

# The name of an image file (relative to this directory) to place at the top
# of the sidebar.
#html_logo = None

# The name of an image file (within the static path) to use as favicon of the
# docs.  This file should be a Windows icon file (.ico) being 16x16 or 32x32
# pixels large.
#html_favicon = None

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']

# If not '', a 'Last updated on:' timestamp is inserted at every page bottom,
# using the given strftime format.
#html_last_updated_fmt = '%b %d, %Y'

# If true, SmartyPants will be used to convert quotes and dashes to
# typographically correct entities.
html_use_smartypants = False # True

# Custom sidebar templates, maps document names to template names.
html_sidebars = {'index': ['indexsidebar.html','searchbox.html']}

# Additional templates that should be rendered to pages, maps page names to
# template names.
#html_additional_pages = {}

# If false, no module index is generated.
html_use_modindex = False

# If false, no index is generated.
#html_use_index = True

# If true, the index is split into individual pages for each letter.
#html_split_index = False

# If true, links to the reST sources are added to the pages.
html_show_sourcelink = True

# If true, an OpenSearch description file will be output, and all pages will
# contain a <link> tag referring to it.  The value of this option must be the
# base URL from which the finished HTML is served.
#html_use_opensearch = ''

# If nonempty, this is the file name suffix for HTML files (e.g. ".xhtml").
#html_file_suffix = ''

# Output file base name for HTML help builder.
htmlhelp_basename = 'GSEXRM'
