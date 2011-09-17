'''
app.application
~~~~~~~~~~~~~~~

This module contains the an extended tornado application.
'''

import os

import tornado

from app.conf import Settings
from app.routing import Autoroute, Route, Routings


class Application(tornado.web.Application):
    '''
    Extended tornado application to support our custom routings.
    '''

    SETTINGS_PATH = os.path.join(os.path.dirname(__file__), 'settings.yaml')

    def __init__(self, handlers=None, default_host="", transforms=None,
                 wsgi=False, **settings):

        already_routed = Routings.collect(Autoroute.routings,
                                          Route.routings)
        if handlers is not None:
            already_routed.add(*handlers)

        if os.path.exists(self.SETTINGS_PATH):
            settings = Settings.from_yaml(self.SETTINGS_PATH).update(settings)

        if 'handlers' in settings:
            already_routed.add(*settings['handlers'])
    
        tornado.web.Application.__init__(self, already_routed, default_host,
                                         transforms, wsgi, **settings)

