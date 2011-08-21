'''
app.handlers.formatters
~~~~~~~~~~~~~~~~~~~~~~~

The formatter handlers live here.
'''

__author__ = 'Genadi Samokovarov'

import pygments.formatters

from app.handlers.base import FormatterHandler


class HTMLHandler(FormatterHandler):
    '''
    RESTful API for HTML output.
    '''

    SUPPORTS_STYLE_DEFS = True
    FORMATTER = pygments.formatters.HtmlFormatter
    CONTENT_TYPE = 'text/html'

HTMLHandler.register()


class LatexHandler(FormatterHandler):
    '''
    RESTful API for Latex output.
    '''

    SUPPORTS_STYLE_DEFS = False
    FORMATTER = pygments.formatters.LatexFormatter
    CONTENT_TYPE = 'application/x-latex'

LatexHandler.register()


class RTFHandler(FormatterHandler):
    '''
    RESTful API for RTF output.
    '''

    SUPPORTS_STYLE_DEFS = False
    FORMATTER = pygments.formatters.RtfFormatter
    CONTENT_TYPE = 'application/msword'

RTFHandler.register()


class TerminalHandler(FormatterHandler):
    '''
    RESTFul API for Terminal output.
    '''

    SUPPORTS_STYLE_DEFS = False
    FORMATTER = pygments.formatters.TerminalFormatter

TerminalHandler.register()

