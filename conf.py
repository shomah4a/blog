# -*- coding: utf-8 -*-

import os

import tinkerer
import tinkerer.paths

# **************************************************************
# TODO: Edit the lines below
# **************************************************************

# Change this to the name of your blog
project = u'プログラマのネタ帳 二冊目'

# Change this to the tagline of your blog
tagline = u'暇な人がなんかメモするところ'

# Change this to your name
author = '@shomah4a'

# Change this to your copyright string
copyright = '2013, ' + author

# Change this to your blog root URL (required for RSS feed)
website = 'http://blog.shomah4a.net/'

# **************************************************************
# More tweaks you can do
# **************************************************************

# Add your Disqus shortname to enable comments powered by Disqus
disqus_shortname = None

# Change your favicon (new favicon goes in _static directory)
html_favicon = 'tinkerer.ico'

# Pick another Tinkerer theme or use your own
html_theme = "modern"
html_theme = "boilerplate"
html_theme = "minimal"
html_theme = "responsive"
html_theme = "tinkerbase"
html_theme = "modern5"

html_theme = "custom_minimal"

# Theme-specific options, see docs
html_theme_options = { }

# Link to RSS service like FeedBurner if any, otherwise feed is
# linked directly
rss_service = None

# Number of blog posts per page
posts_per_page = 2

# **************************************************************
# Edit lines below to further customize Sphinx build
# **************************************************************

# Add other Sphinx extensions here
extensions = ['tinkerer.ext.blog',
              'tinkerer.ext.disqus',
              'sphinxcontrib.blockdiag',
              'sphinxcontrib.gist',
              'sphinxcontrib.twitter',
              'sphinx_amazonjp_embed']

# Add other template paths here
templates_path = ['_templates']

# Add other static paths here
html_static_path = ['_static', tinkerer.paths.static]

# Add other theme paths here
html_theme_path = [tinkerer.paths.themes, os.path.join(os.path.dirname(__file__), 'themes')]

print html_theme_path

# Add file patterns to exclude from build
exclude_patterns = ["drafts/*"]

# Add templates to be rendered in sidebar here
html_sidebars = {
    "**": ["author.html", "recent.html", "searchbox.html", 'tags.html', 'advertise.html']
}

# **************************************************************
# Do not modify below lines as the values are required by
# Tinkerer to play nice with Sphinx
# **************************************************************

source_suffix = tinkerer.source_suffix
master_doc = tinkerer.master_doc
version = tinkerer.__version__
release = tinkerer.__version__
html_title = project
html_use_index = False
html_show_sourcelink = False
html_add_permalinks = None

amazonjp_affiliate_id = 'shomah4a-22'
