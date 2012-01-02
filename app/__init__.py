'''
pygmentize.me
~~~~~~~~~~~~~

pygmentize.me is a highlighting service based on the awesome pygments library.
'''

from __future__ import absolute_import

from os.path import join, abspath, dirname
import yaml

from plush import Plush
from plush.decorators import asynchronous


with open(join(abspath(dirname(__file__)), 'formatters.yaml')) as file:
    FORMATTERS = yaml.load(file)

del file

app = Plush(__name__)
app.use('decorator', asynchronous)

# Import time side effect. Populates the app with routes.
from . import views
