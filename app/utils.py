'''
app.utils
~~~~~~~~~

Utilities classes and functions used throughout the project.
'''


class classonlymethod(classmethod):
    '''
    Descriptor for making class only methods.

    A class only method is a class method, which can be called only from the
    class itself and not from instances. If called from an instance will
    raise ``AttributeError``.
    '''

    def __get__(self, instance, owner):
        if instance is not None:
            raise AttributeError(
                "Class only methods can not be called from an instance")

        return classmethod.__get__(self, instance, owner)

