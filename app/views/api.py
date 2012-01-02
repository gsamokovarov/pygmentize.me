from __future__ import absolute_import

import json

from plush.response import BadRequest
from plush.util.lang import tap

from .. import app, FORMATTERS
from ..tasks import colorize, get_style_defs


@app.get(r'/api/supported/formatters')
def api_supported_formatters(request):
    '''
    Renders the supported formatters and metadata about them in JSON.

    Example::

      {'text':
        {'also_known_as': ['plain']},
        {'supports_style_defs': false},
        {'content_type': 'text/plain'}}
    '''

    with request.finishing():
        request.json(FORMATTERS)


@app.post(r'/api/formatter/(\w+)')
def api_formatter(request, formatter):
    '''
    Arguments
    ~~~~~~~~~

    * `code`    - The code to highlight.
                                                                    [Required]
    * `lexer`   - The name of the lexer to use for the highlight.
                                                                    [Optional]
    * `options` - A JSON object of the options to pass to the formatter.
                                                                    [Optional]
    * `styles`  - A JSON array of options to the formatters get_style_defs
                  method. Does nothing if not supported by the formatter.
                                                                    [Optional]
    '''

    if formatter not in FORMATTERS:
        for proper_name, formatter_info in FORMATTERS.items():
            if formatter in formatter_info['also_known_as']:
                formatter = proper_name
                break
        else:
            return request.send(BadRequest("Unsupported formatter"))
    else:
        formatter_info = FORMATTERS[formatter]

    code = request.param('code')
    lexer = request.param('lexer', default=None)
    options = request.param('options', default='{}', type=json.loads, ensure=dict)
    styles = request.param('styles', default='null', type=json.loads)

    styles_given = formatter_info['supports_style_defs'] and styles

    with request.finishing():
        try:
            colorized_code = colorize(code, lexer, formatter, **options)
            if styles_given:
                style_defs = get_style_defs(formatter, styles)
        except Exception, error:
            return request.send(BadRequest(error))

        request.content_type = formatter_info['content_type']

        request.write(colorized_code)
        if styles_given:
            request.write(style_defs)
