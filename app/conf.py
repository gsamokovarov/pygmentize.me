'''
app.conf
~~~~~~~~

Appication settings helper.
'''

import yaml


class Settings(dict):
    '''
    The `settings` container object.

    Supports `dot notation`, meaning that you can get elements like attributes
    and creation from a YAML markup.
    '''

    @classmethod
    def from_yaml(cls, markup, filename=False):
        '''
        Creates a ``Settings`` object from YAML `markup` or YAML file name if
        `filename` is truthful.
        '''

        if filename:
            with open(markup) as yaml_file:
                return cls(yaml.load(yaml_file))

        return cls(yaml.load(markup))

    def have(self, *options):
        '''
        Checks wheter the settings include all of the specified options.
        '''

        return all(opt in self for opt in options)
    has = have

    def __getattr__(self, attr):
        try:
            return self[attr]
        except KeyError, e:
            raise AttributeError(e)

