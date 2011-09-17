'''
app.routing
~~~~~~~~~~~

Optional routing utilities.

Can be used from custom tornado applications for explicit or implicit routing.
The explicit routing is achieved through the ``Route`` mainly from the usage of
the ``route`` class decorator. The implicit routing is achieved through the
usage of the ``Autoroute`` class. The ``Autoroute`` instances acts like class
decorators, so you can specify you routing rule (you convention) and decorate
the handlers with it afterwards. You are not limited to just one autoroute, you
can do as many as you need.
'''

from itertools import chain

import tornado


class Routings(list):
    '''
    Collection for routings.
    '''

    @classmethod
    def collect(cls, *routings):
        '''
        Collects multiple routings by their precedence.
        '''

        return Routings().add(*chain.from_iterable(routings))

    @property
    def urls(self):
        '''
        Returns the already routed urls.
        '''

        return [r[0] for r in self]

    @property
    def handlers(self):
        '''
        Returns the already routed handlers.
        '''

        return [r[1] for r in self]

    @property
    def kwargs(self):
        '''
        Returns all of the given extra kwargs, if any.
        '''

        return [r[2] for r in self if len(r) > 2]

    @property
    def empty(self):
        '''
        Return ``True`` when the routings are empty.
        '''

        return not bool(len(self))

    def add(self, *routings):
        '''
        Safetly inserts a handler into the current list.

        If there is already a url routed to a handler, we will reroute it.
        '''

        already_routed = dict((r[0], i) for i, r in enumerate(self))

        for route in routings:
            url, handler = route[0:2]

            if url in already_routed:
                self[already_routed[url]] = route
            else:
                self.append(route)
                already_routed[url] = len(self) - 1

        return self

    def clear(self):
        '''
        Clears the current content.
        '''

        self[:] = []


class RouteMeta(type):
    '''
    The meta class for the ``Route`` object.

    Inserts a lazy ``routings`` property.
    '''

    @property
    def routings(cls):
        '''
        Non thread safe lazy property.
        '''

        attr_name = '_routings'

        if not hasattr(cls, attr_name):
            setattr(cls, attr_name, Routings())

        return getattr(cls, attr_name)


class Route(object):
    '''
    Explicitly routes a handler to a url.

    Explicitly routed handlers have higher precedence then the automatically
    routed ones.
    '''

    __metaclass__ = RouteMeta

    def __init__(self, handler, url, **kwargs):
        if not issubclass(handler, tornado.web.RequestHandler):
            raise TypeError('Expected a RequestHandler; got: {0}'.\
                            format(handler))

        routing = [url, handler]
        if kwargs:
            routing.append(kwargs)

        Route.routings.add(tuple(routing))


class Autoroute(object):
    '''
    Implicitly routes a handler to a url generated from a rule, used to make
    your own routing conventions.

    Automatically routed handlers have lower precedence then the expicitly
    routed ones.
    '''

    __metaclass__ = RouteMeta

    class Rules(object):
        '''
        Collection of common rules used for autorouting.
        '''

        @staticmethod
        def lowered_name(handler):
            if hasattr(handler, 'name'):
                name = getattr(handler, 'name')
            else:
                # Simply replaces the last occurence of Handler in the handler
                # name.
                name = handler.__name__[::-1].replace('reldnaH', '', 1)[::-1]

            return name.lower()

    @property
    def prefixed(self):
        '''
        Returns ``True`` when a prefix is specified, ``False`` otherwise.
        '''

        return bool(self.prefix)

    @property
    def suffixed(self):
        '''
        Returns ``True`` when suffix is specified, ``False`` otherwise.
        '''

        return bool(self.suffix)

    def __init__(self, prefix=None, rule=None, suffix=None):
        if rule is None:
            raise TypeError('Must specify the rule keyword argument.')

        if not callable(rule):
            raise TypeError('The rule must be callable.')

        self.prefix = prefix if prefix is not None else ''
        self.rule = rule
        self.suffix = suffix if suffix is not None else ''

    def __call__(self, handler=None, **kwargs):
        if kwargs and handler is None: # and it should be...
            def decorated_route(cls):
                return self.route(cls, **kwargs)

            return decorated_route

        return self.route(handler, **kwargs)

    def route(self, handler, **kwargs):
        '''
        Routes a handler with the already specified rule.
        '''

        if not issubclass(handler, tornado.web.RequestHandler):
            raise TypeError('Expected a RequestHandler; got: {0}'.\
                            format(handler))

        url = '{0}{1}{2}'.format(self.prefix, self.rule(handler), self.suffix)

        routing = [url, handler]
        if kwargs:
            routing.append(kwargs)

        Autoroute.routings.add(tuple(routing))

        return handler


def route(url, **kwargs):
    '''
    Class decorator for routing handlers to specified urls.

    Helper providing prettier syntax to ``Route``.
    '''

    def wrapper(cls):
        Route(cls, url, **kwargs)

        return cls

    return wrapper

