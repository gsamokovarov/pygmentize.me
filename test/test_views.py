import json
import pickle

from plush.testing import case_for

from app import app


class TestHTML(case_for(app)):
    def test_content_type(self):
        response = self.post('/api/formatter/html', {
            'code': 'pass',
            'lexer': 'python'
        })

        self.assertTrue('text/html' in response.headers['Content-Type'])

    def test_simple_post_should_highlight_in_html(self):
        response = self.post('/api/formatter/html', {
            'code': '''
                    puts "Hello World!"
                    '''.strip(),
            'lexer': 'ruby',
        })

        self.assertEquals(response.body, u'<div class="highlight"><pre><span class="nb">puts</span> <span class="s2">&quot;Hello World!&quot;</span>\n</pre></div>\n')

    def test_erroneus_post_arguments(self):
        response = self.post('/api/formatter/html', {})

        self.assertEqual(response.code, 400)

    def test_post_options_should_apply_to_html_formatter(self):
        response = self.post('/api/formatter/html', {
            'code': '''
                    puts "Hello World!"
                    '''.strip(),
            'lexer': 'ruby',
            'options': json.dumps({
                'cssclass': 'syntax'
            }),
        })

        self.assertRegexpMatches(response.body, r'.*class="syntax".*')

    def test_get_style_defs_should_call_formatter_get_style_defs(self):
        response = self.post('/api/formatter/html', {
            'code': '''
                    puts "Hello World!"
                    '''.strip(),
            'lexer': 'ruby',
            'styles': json.dumps(['div.syntax pre', 'pre.syntax']),
        })

        self.assertRegexpMatches(response.body, r'.*div\.syntax pre.*pre\.syntax.*')


class TestLatex(case_for(app)):
    def test_content_type(self):
        response = self.post('/api/formatter/latex', {
            'code': 'pass',
            'lexer': 'python'
        })

        self.assertTrue('application/x-latex' in response.headers['Content-Type'])

    def test_simple_post_should_highlight_in_latex(self):
        response = self.post('/api/formatter/latex', {
            'code': '''
                    puts "Hello World!"
                    '''.strip(),
            'lexer': 'ruby',
        })

        self.assertEquals(response.body, u'\\begin{Verbatim}[commandchars=\\\\\\{\\}]\n\\PY{n+nb}{puts} \\PY{l+s+s2}{"}\\PY{l+s+s2}{Hello World!}\\PY{l+s+s2}{"}\n\\end{Verbatim}\n')


class TestRTFHandler(case_for(app)):
    def test_content_type(self):
        response = self.post('/api/formatter/rtf', {
            'code': 'pass',
            'lexer': 'python'
        })

        self.assertTrue('application/msword' in response.headers['Content-Type'])

    def test_simple_post_should_highlight_in_rtf(self):
        response = self.post('/api/formatter/rtf', {
            'code': '''
                    puts "Hello World!"
                    '''.strip(),
            'lexer': 'ruby',
        })

        self.assertEqual(response.body, u'{\\rtf1\\ansi\\deff0{\\fonttbl{\\f0\\fmodern\\fprq1\\fcharset0;}}{\\colortbl;\\red128\\green128\\blue128;\\red186\\green33\\blue33;\\red0\\green64\\blue208;\\red102\\green102\\blue102;\\red64\\green128\\blue128;\\red160\\green160\\blue0;\\red25\\green23\\blue124;\\red0\\green128\\blue0;\\red187\\green102\\blue136;\\red187\\green102\\blue34;\\red136\\green0\\blue0;\\red170\\green34\\blue255;\\red153\\green153\\blue153;\\red0\\green160\\blue0;\\red160\\green0\\blue0;\\red255\\green0\\blue0;\\red128\\green0\\blue128;\\red176\\green0\\blue64;\\red0\\green0\\blue255;\\red187\\green187\\blue187;\\red188\\green122\\blue0;\\red0\\green0\\blue128;\\red125\\green144\\blue41;\\red210\\green65\\blue58;}\\f0{\\cf8 puts} {\\cf2 "}{\\cf2 Hello World!}{\\cf2 "}\\par\n}')

    def test_rtf_formatter_should_ignore_get_style_defs(self):
        response = self.post('/api/formatter/rtf', {
            'code': '''
                    puts "Hello World!"
                    '''.strip(),
            'lexer': 'ruby',
            'styles': json.dumps(['div.syntax pre', 'pre.syntax']),
        })

        self.assertEqual(response.body, u'{\\rtf1\\ansi\\deff0{\\fonttbl{\\f0\\fmodern\\fprq1\\fcharset0;}}{\\colortbl;\\red128\\green128\\blue128;\\red186\\green33\\blue33;\\red0\\green64\\blue208;\\red102\\green102\\blue102;\\red64\\green128\\blue128;\\red160\\green160\\blue0;\\red25\\green23\\blue124;\\red0\\green128\\blue0;\\red187\\green102\\blue136;\\red187\\green102\\blue34;\\red136\\green0\\blue0;\\red170\\green34\\blue255;\\red153\\green153\\blue153;\\red0\\green160\\blue0;\\red160\\green0\\blue0;\\red255\\green0\\blue0;\\red128\\green0\\blue128;\\red176\\green0\\blue64;\\red0\\green0\\blue255;\\red187\\green187\\blue187;\\red188\\green122\\blue0;\\red0\\green0\\blue128;\\red125\\green144\\blue41;\\red210\\green65\\blue58;}\\f0{\\cf8 puts} {\\cf2 "}{\\cf2 Hello World!}{\\cf2 "}\\par\n}')


class TestTerminalHandler(case_for(app)):
    def test_simple_post_should_highlight_with_terminal_magic_chars(self):
        response = self.post('/api/formatter/terminal', {
            'code': '''
                    puts "Hello World!"
                    '''.strip(),
            'lexer': 'ruby',
        })

        self.assertEqual(response.body, u'\x1b[36mputs\x1b[39;49;00m \x1b[39;49;00m\x1b[33m"\x1b[39;49;00m\x1b[33mHello World!\x1b[39;49;00m\x1b[33m"\x1b[39;49;00m\n')
