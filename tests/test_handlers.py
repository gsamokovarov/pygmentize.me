import json

import tornado
from tornado.web import Application
from tornado.escape import url_escape
from tornado.httpclient import HTTPRequest
from tornado.testing import AsyncHTTPTestCase

from app.handlers.base import BaseHandler, APIHandler, FormatterHandler
from app.handlers.formatters import (
    HTMLHandler, LatexHandler, RTFHandler, TerminalHandler)


class PostRequest(HTTPRequest):
    '''
    HTTP request which accepts a dictionary as its body and converts it to the
    apropriate HTTP query.
    '''

    def __init__(self, url, body, **kwargs):
        kwargs['body'] = '&'.join('{0}={1}'.format(url_escape(k), url_escape(v))
                                  for (k, v) in body.iteritems())

        super(self.__class__, self).__init__(url, method='POST', **kwargs)


class BaseTest(AsyncHTTPTestCase):
    def post(self, path, body, **kwargs):
        self.http_client.fetch(PostRequest(self.get_url(path), body, **kwargs),
                               self.stop)
        return self.wait()


class TestBaseHandler(BaseTest):
    def get_app(self):
        class ArgumentHandler(BaseHandler):
            def post(self):
                get_integer = lambda: self.get_argument('integer', type=int)

                self.write(str(isinstance(get_integer(), int)))

        return Application([('/', ArgumentHandler)])

    def test_should_get_the_argument_as_the_given_type(self):
        response = self.post('/', {'integer': '24'})

        self.assertEquals('True', response.body)

    def test_should_raise_http_error_on_wrong_type(self):
        response = self.post('/', {'integer': 'abc'})

        self.assertRegexpMatches(response.body, r'.*Bad Request.*')


class TestAPIHandler(BaseTest):
    def get_app(self):
        class ErrorHandler(APIHandler):
            def post(self):
                self.send_api_error(Exception('Wrong!'))

        return Application([('/', ErrorHandler),])

    def test_send_api_error(self):
        response = self.post('/', {'argument': '1'})
        
        self.assertEquals(response.body, 'Wrong!')

#{ Formatter handlers tests...

class TestHTMLHandler(BaseTest):
    def get_app(self):
        return Application([('/', HTMLHandler),])

    def test_content_type(self):
        response = self.post('/', {'code': 'pass', 'lexer': 'python'})

        self.assertTrue(
            HTMLHandler.CONTENT_TYPE in response.headers['Content-Type']
        )

    def test_simple_post_should_highlight_in_html(self):
        response = self.post('/', {
            'code': '''
                    puts "Hello World!"
                    '''.strip(),
            'lexer': 'ruby',
        })

        self.assertEquals(
            response.body,
            u'<div class="highlight"><pre><span class="nb">puts</span> <span class="s2">&quot;Hello World!&quot;</span>\n</pre></div>\n'
        )

    def test_erroneus_post_arguments(self):
        response = self.post('/', {})

        self.assertEquals(
            response.body,
            r'Missing argument code'
        )

    def test_post_options_should_apply_to_html_formatter(self):
        response = self.post('/', {
            'code': '''
                    puts "Hello World!"
                    '''.strip(),
            'lexer': 'ruby',
            'options': json.dumps({
                'cssclass': 'syntax'
            }),
        })

        self.assertRegexpMatches(
            response.body,
            r'.*class="syntax".*'
        )

    def test_get_style_defs_should_call_formatter_get_style_defs(self):
        response = self.post('/', {
            'code': '''
                    puts "Hello World!"
                    '''.strip(),
            'lexer': 'ruby',
            'get_style_defs': json.dumps(['div.syntax pre', 'pre.syntax']),
        })

        self.assertRegexpMatches(
            response.body,
            r'.*div\.syntax pre.*pre\.syntax.*'
        )


class TestLatexHandler(BaseTest):
    def get_app(self):
        return Application([('/', LatexHandler),])

    def test_content_type(self):
        response = self.post('/', {'code': 'pass', 'lexer': 'python'})

        print response.headers

        self.assertTrue(
            LatexHandler.CONTENT_TYPE in response.headers['Content-Type'],
        )

    def test_simple_post_should_highlight_in_latex(self):
        response = self.post('/', {
            'code': '''
                    puts "Hello World!"
                    '''.strip(),
            'lexer': 'ruby',
        })

        self.assertEquals(
            response.body,
            u'\\begin{Verbatim}[commandchars=\\\\\\{\\}]\n\\PY{n+nb}{puts} \\PY{l+s+s2}{"}\\PY{l+s+s2}{Hello World!}\\PY{l+s+s2}{"}\n\\end{Verbatim}\n'
        )

    def test_lexer_formatter_should_ignore_get_style_defs(self):
        response = self.post('/', {
            'code': '''
                    puts "Hello World!"
                    '''.strip(),
            'lexer': 'ruby',
            'get_style_defs': json.dumps(['div.syntax pre', 'pre.syntax']),
        })

        self.assertEquals(
            response.body,
            u'\\begin{Verbatim}[commandchars=\\\\\\{\\}]\n\\PY{n+nb}{puts} \\PY{l+s+s2}{"}\\PY{l+s+s2}{Hello World!}\\PY{l+s+s2}{"}\n\\end{Verbatim}\n'
        )


class TestRTFHandler(BaseTest):
    def get_app(self):
        return Application([('/', RTFHandler),])

    def test_content_type(self):
        response = self.post('/', {'code': 'pass', 'lexer': 'python'})

        self.assertTrue(
            RTFHandler.CONTENT_TYPE in response.headers['Content-Type']
        )

    def test_simple_post_should_highlight_in_rtf(self):
        response = self.post('/', {
            'code': '''
                    puts "Hello World!"
                    '''.strip(),
            'lexer': 'ruby',
        })

        self.assertEquals(
            response.body,
            u'{\\rtf1\\ansi\\deff0{\\fonttbl{\\f0\\fmodern\\fprq1\\fcharset0;}}{\\colortbl;\\red128\\green128\\blue128;\\red186\\green33\\blue33;\\red0\\green64\\blue208;\\red102\\green102\\blue102;\\red64\\green128\\blue128;\\red160\\green160\\blue0;\\red25\\green23\\blue124;\\red0\\green128\\blue0;\\red187\\green102\\blue136;\\red187\\green102\\blue34;\\red136\\green0\\blue0;\\red170\\green34\\blue255;\\red153\\green153\\blue153;\\red0\\green160\\blue0;\\red160\\green0\\blue0;\\red255\\green0\\blue0;\\red128\\green0\\blue128;\\red176\\green0\\blue64;\\red0\\green0\\blue255;\\red187\\green187\\blue187;\\red188\\green122\\blue0;\\red0\\green0\\blue128;\\red125\\green144\\blue41;\\red210\\green65\\blue58;}\\f0{\\cf8 puts} {\\cf2 "}{\\cf2 Hello World!}{\\cf2 "}\\par\n}'
        )

    def test_rtf_formatter_should_ignore_get_style_defs(self):
        response = self.post('/', {
            'code': '''
                    puts "Hello World!"
                    '''.strip(),
            'lexer': 'ruby',
            'get_style_defs': json.dumps(['div.syntax pre', 'pre.syntax']),
        })

        self.assertEquals(
            response.body,
            u'{\\rtf1\\ansi\\deff0{\\fonttbl{\\f0\\fmodern\\fprq1\\fcharset0;}}{\\colortbl;\\red128\\green128\\blue128;\\red186\\green33\\blue33;\\red0\\green64\\blue208;\\red102\\green102\\blue102;\\red64\\green128\\blue128;\\red160\\green160\\blue0;\\red25\\green23\\blue124;\\red0\\green128\\blue0;\\red187\\green102\\blue136;\\red187\\green102\\blue34;\\red136\\green0\\blue0;\\red170\\green34\\blue255;\\red153\\green153\\blue153;\\red0\\green160\\blue0;\\red160\\green0\\blue0;\\red255\\green0\\blue0;\\red128\\green0\\blue128;\\red176\\green0\\blue64;\\red0\\green0\\blue255;\\red187\\green187\\blue187;\\red188\\green122\\blue0;\\red0\\green0\\blue128;\\red125\\green144\\blue41;\\red210\\green65\\blue58;}\\f0{\\cf8 puts} {\\cf2 "}{\\cf2 Hello World!}{\\cf2 "}\\par\n}'
        )


class TestTerminalHandler(BaseTest):
    def get_app(self):
        return Application([('/', TerminalHandler),])

    def test_simple_post_should_highlight_with_terminal_magic_chars(self):
        response = self.post('/', {
            'code': '''
                    puts "Hello World!"
                    '''.strip(),
            'lexer': 'ruby',
        })

        self.assertEquals(
            response.body,
            u'\x1b[36mputs\x1b[39;49;00m \x1b[39;49;00m\x1b[33m"\x1b[39;49;00m\x1b[33mHello World!\x1b[39;49;00m\x1b[33m"\x1b[39;49;00m\n'
        )

#}
