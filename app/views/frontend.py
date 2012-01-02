from __future__ import absolute_import

from .. import app

@app.get(r'/')
def index(request):
    request.render('index.html')
