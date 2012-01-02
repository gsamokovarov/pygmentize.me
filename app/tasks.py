'''
app.tasks
~~~~~~~~~

Collection of tasks.
'''

from pygments import highlight

from .helpers import lexer_by_name, formatter_by_name


def colorize(code, lexer, formatter, **options):
    '''
    Colorises `code` from a `lexer` and `formatter` names with optional
    `options` from keyword arguments.
    '''

    return highlight(code, lexer_by_name(lexer),
                     formatter_by_name(formatter, **options))


def get_style_defs(formatter, *options):
    '''
    Gets the style definitions for a `formatter` with optinal `options` from
    extra arguments.
    '''

    return formatter_by_name(formatter).get_style_defs(*options)
