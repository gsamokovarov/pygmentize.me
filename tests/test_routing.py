import unittest

from tornado.web import RequestHandler

from app.routing import route, Route, Autoroute, Routings


class RoutingsTest(unittest.TestCase):
    def test_basic_add(self):
        OtherHandler = type('OtherHandler', (RequestHandler,), {})

        routings = Routings([(r'/', RequestHandler)])
        routings.add((r'/', OtherHandler))

        self.assertTrue(OtherHandler in routings.handlers)
        self.assertFalse(RequestHandler in routings.handlers)

    def test_collect(self):
        OtherHandler = type('OtherHandler', (RequestHandler,), {})

        routings1 = Routings([(r'/', RequestHandler)])
        routings2 = Routings([(r'/', OtherHandler),
                              (r'/home', RequestHandler)])

        routings = Routings.collect(routings1, routings2)

        self.assertTrue(OtherHandler in routings.handlers)
        self.assertTrue(RequestHandler in routings.handlers)

        self.assertTrue(r'/' in routings.urls)
        self.assertTrue(r'/home' in routings.urls)


    def test_clear(self):
        routings = Routings([(r'/', RequestHandler)])
        routings.clear()

        self.assertTrue(routings.empty)
        
        
class RouteTest(unittest.TestCase):
    def tearDown(self):
        Route.routings.clear()

    def test_contains_class_level_routings(self):
        self.assertTrue(hasattr(Route, 'routings'))

    def test_route_decorator(self):
        @route(r'/')
        class DummyHandler(RequestHandler): pass

        self.assertTrue(r'/' in Route.routings.urls)
        self.assertTrue(DummyHandler in Route.routings.handlers)
        

class AutorouteTest(unittest.TestCase):
    def tearDown(self):
        Autoroute.routings.clear()

    def test_contains_class_level_routings(self):
        self.assertTrue(hasattr(Autoroute, 'routings'))

    def test_autorouting_from_prefix(self):
        autoroute = Autoroute(prefix='/api/', 
                              rule=Autoroute.Rules.lowered_name)

        @autoroute
        class MethodHandler(RequestHandler): pass

        self.assertTrue(MethodHandler in Autoroute.routings.handlers)
        self.assertTrue('/api/method' in Autoroute.routings.urls)

    def test_autorouting_with_kwargs(self):
        autoroute = Autoroute(prefix='/api/', 
                              rule=Autoroute.Rules.lowered_name)

        @autoroute(custom='settings')
        class KwargsHandler(RequestHandler):
            def __init__(self, *args, **kwargs):
                self.kwargs = kwargs
                RequestHandler.__init__(self, *args, **kwargs)

        self.assertTrue(KwargsHandler in Autoroute.routings.handlers)
        self.assertTrue('/api/kwargs' in Autoroute.routings.urls)
        self.assertTrue({'custom': 'settings'} in Autoroute.routings.kwargs)


class AutorouteRulesTest(unittest.TestCase):
    def test_lowered_name(self):
        rule = Autoroute.Rules.lowered_name

        NamedHandler = type('NamedHandler', (), {
                           'name': 'NAME'
                       })
        UnnamedHandler = type('UnnamedHandler', (), {})
        
        self.assertEquals('name', rule(NamedHandler))
        self.assertEquals('unnamed', rule(UnnamedHandler))

