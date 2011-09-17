'''
pygmentize.me
~~~~~~~~~~~~~

This application runs the backend of the site. Provides all the fuctionallity
needed to keep it up and running.
'''

__author__ = 'Genadi Samokovarov'

import os

import tornado
import tornado.web
import tornado.httpserver
from tornado.options import define, options

# We _must_ import the handlers or else they don't get populated by the routing
# mechanism set in place.
import app.handlers.formatters
import app.handlers.frontends
from app.application import Application


# Define the application command line options.
define('port', 8080, type=int,
        help='The port to run the server on')

define('debug', True, type=bool,
        help='Wheter to support autoreloading or not.')


def main():
    # Parse command line options.
    tornado.options.parse_command_line()

    # Set up the application.
    application = Application(
        static_path=os.path.join(os.path.dirname(__file__), 'static'),
        template_path=os.path.join(os.path.dirname(__file__), 'templates'),
        debug=options.debug,
    )

    # Run the server.
    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()


if __name__ == '__main__':
    main()

