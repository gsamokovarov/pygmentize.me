'''
pygmentize.me
~~~~~~~~~~~~~

This application runs the backend of the site. Provides all the fuctionallity
needed to keep it up and running.
'''

import os

import tornado.web
from tornado.options import define, options

from app.handlers import HTMLHandler


define('port', 8080, type=int,
        help='The port to run the server on')


class Application(tornado.web.Application):
    def __init__(self):
        settings = dict(
            static_path=os.path.join(os.path.dirname(__file__), 'static'),
            template_path=os.path.join(os.path.dirname(__file__), 'templates'),
        )

        super(self.__class__, self).__init__(self.handlers, settings)


application = Application(handlers=[
    (r'^/html', HTMLHandler),
])

