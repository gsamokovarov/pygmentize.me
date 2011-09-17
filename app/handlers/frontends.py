'''
app.handlers.frontends
~~~~~~~~~~~~~~~~~~~~~~

The handlers responsible for the fronted of the services.
'''

import tornado

from app.routing import route


@route(r'/')
class IndexHandler(tornado.web.RequestHandler):
    '''
    The handler responsible for the index page of the service.
    '''

    def get(self):
        return self.render('index.html')

