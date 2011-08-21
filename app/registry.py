'''
app.registry
~~~~~~~~~~~~

Provides a ``Registrable`` mixin and a ``Registry`` psuedo class.
'''

from abc import ABCMeta

__all__ = ['Registrable', 'Registry']


# Will I have any benefit of making this tread local?
_REGISTRABLE_INFO = {}


class Registrable(object):
    '''
    Mixin providing a registrable support for a base class.

    Every subclass can register itself by calling the 'register' method.
    '''

    @classmethod
    def register(cls):
        '''
        Registers the current class to it's own base class registry.
        '''

        if isinstance(cls, Registry):
            raise TypeError('Can not register a registry.')

        for base in cls.__bases__:
            if issubclass(base, Registry):
                _REGISTRABLE_INFO[base].append(cls)

                break
        else:
            raise TypeError('No registry ancsestor found!')

    @classmethod
    def make_registry(cls):
        '''
        Makes the current class a registry.
        '''

        #for base in cls.__mro__:
        #    if issubclass(base, Registry):
        #        raise TypeError(
        #            'Can not make multiple registries in one chain.')

        _REGISTRABLE_INFO[cls] = []


class Registry(object):
    '''
    Psuedo class used for registry subclass checking.

    A registry is every class including the ``Registrable`` mixin and being
    called the ``make_registry`` class method.
    '''

    __metaclass__ = ABCMeta

    @classmethod
    def __subclasshook__(cls, other_class):
        if cls is Registry:
            return other_class in _REGISTRABLE_INFO

        return NotImplemented

    @staticmethod
    def entries_for(cls):
        '''
        Returns the entries for the specified registry.

        Raises an ``TypeError`` when the specified class is not a registry.
        '''

        if not issubclass(cls, Registry):
            raise TypeError('Not a registry!')

        return _REGISTRABLE_INFO[cls]

    @staticmethod
    def clear(cls=None):
        '''
        Clears the specified registry of its entries or all of purges all fo
        the registries with their entries of no class is specified.
        '''

        if cls is not None:
            if issubclass(cls, Registry):
                _REGISTRABLE_INFO[cls] = []
            else:
                raise TypeError('Not a registry!')
        else:
            _REGISTRABLE_INFO.clear()

