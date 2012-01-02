import pygments.util
import pygments.lexers
import pygments.formatters

__all__ = "lexer_by_name formatter_by_name".split()

FALLBACK_LEXER = FALLBACK_FORMATTER = 'text'


def lexer_by_name(name, fallback=FALLBACK_LEXER, **options):
    '''
    Tries to get a lexer by name and if it doesn't exists it falls back to the
    `fallback` one.
    '''
    
    try:
        return pygments.lexers.get_lexer_by_name(name, **options)
    except pygments.util.ClassNotFound:
        return pygments.lexers.get_lexer_by_name(fallback, **options)


def formatter_by_name(name, fallback=FALLBACK_FORMATTER, **options):
    '''
    Tries to get a formatter by name and if it doesn't exists it falls back to
    the `fallback` one.
    '''

    try:
        return pygments.formatters.get_formatter_by_name(name, **options)
    except pygments.util.ClassNotFound:
        return pygments.formatters.get_formatter_by_name(fallback, **options)
