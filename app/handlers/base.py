'''
app.handlers
~~~~~~~~~~~~

Collection of base handlers, not used directly into the application.
'''

import json

import tornado
import pygments.lexers

from app.registry import Registrable


class BaseHandler(tornado.web.RequestHandler):
    '''
    Defines type aware ``get_argument`` and respects ``set_default_headers``
    definitions.
    '''

    def initialize(self):
        if hasattr(self, 'set_default_headers'):
            self.set_default_headers()

    _ID_TYPE = lambda _: _
    _ARG_DEFAULT = tornado.web.RequestHandler._ARG_DEFAULT
    def get_argument(self, name, default=_ARG_DEFAULT, strip=True,
            type=_ID_TYPE):
        '''
        Returns the value of the argument with the given name, converting it to
        type if specified.

        The contact for `type` is that you have to take one argument and raise
        `ValueError` on bad input.
        '''

        try:
            return type(tornado.web.RequestHandler.
                        get_argument(self, name, default, strip))
        except ValueError, message:
            raise tornado.web.HTTPError(400, str(message))


class APIHandler(BaseHandler):
    '''
    This class provides the most common operations found in any API handler.

    Takes care of the common parameters processing.
    '''

    def get_common_arguments(self):
        '''
        Returns (code, lexer, options) which are the current common arguments
        shared across all of the API requests.
        '''

        code = self.get_argument('code')
        lexer = pygments.lexers.get_lexer_by_name(self.get_argument('lexer'))

        options = self.get_argument('options', '{}', type=json.loads)

        return (code, lexer, options)

    def send_api_error(self, exception, status_code=404):
        '''
        Sends an API error to the client.

        By default any status code different than 200 on a POST request
        indicates an API error. An API error is raised whenever Pygments
        chokes for the given input.
        '''

        self.set_status(status_code)

        self.finish(str(exception))


class FormatterHandler(APIHandler, Registrable):
    '''
    Encapsulates a basic RESTful API for the pygments formatters.

    Arguments
    ~~~~~~~~~

    * ``code`` - The code to highlight.
                                                                    [Required]
    * ``lexer`` - The name of the lexer to use for the highlight.
                                                                    [Required]
    * ``options`` - A JSON object of the options to pass to the formatter.
                                                                    [Optional]
    * ``get_style_defs`` - A JSON array of options to the formatters
                           get_style_defs method. Does nothing if not
                           supported by the formatter.
                                                                    [Optional]
    '''

    SUPPORTS_STYLE_DEFS = False
    FORMATTER = lambda *args, **kwargs: NotImplemented

    def set_default_headers(self):
        '''
        Provides the default headers for the formatter.

        See: `RequestHandler.set_default_headers`
        '''

        if hasattr(self, 'CONTENT_TYPE'):
            self.set_header('Content-Type', getattr(self, 'CONTENT_TYPE'))

    def pre_highlight(self, code, lexer, formatter):
        '''
        Hook called before writing out the highlight.

        Returns a tuple of (code, lexer, formatter).
        '''

        return (code, lexer, formatter)

    def post_highlight(self, highlight):
        '''
        Hook called _after_ the writing of the highlight.

        Returns the highlight.
        '''

        return highlight

    def pre_get_style_defs(self, defs):
        '''
        Hook called _before_ the call to `get_style_defs`.

        Returns the definitions.
        '''

        return defs

    def post_get_style_defs(self, highlight):
        '''
        Hook called after the call to `get_style_defs`.

        Returns the highlight.
        '''

        return highlight

    @tornado.web.asynchronous
    def post(self):
        try:
            code, lexer, options = self.get_common_arguments()
            formatter = self.FORMATTER(**options)
        except tornado.web.HTTPError, e:
            if e.status_code == 400:
                self.send_api_error(e.log_message, 400)
            else:
                self.send_api_error(e.log_message)

            return

        # Helps us to catch broken handlers earlier.
        if formatter is NotImplemented:
            raise NotImplementedError

        code, lexer, formatter = self.pre_highlight(code, lexer, formatter)

        try:
            highlighted = pygments.highlight(code, lexer, formatter)
        except Exception, e:
            self.send_api_error(e)

            return

        highlighted = self.post_highlight(highlighted)

        self.write(highlighted)

        if self.SUPPORTS_STYLE_DEFS:
            with_options = self.pre_get_style_defs(
                self.get_argument('get_style_defs', None))

            if with_options is not None:
                try:
                    style_defs = formatter.get_style_defs(with_options)
                except Exception, e:
                    self.send_api_error(e)

                    return

                style_defs = self.post_get_style_defs(style_defs)

                self.write(style_defs)

        self.finish()

FormatterHandler.make_registry()

