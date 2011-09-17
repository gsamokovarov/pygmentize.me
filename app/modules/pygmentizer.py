'''
app.modules.pygmentizer
~~~~~~~~~~~~~~~~~~~~~~~~~

The main pygmentizing widget for the site.
'''

import tornado


class PygmentizerModule(tornado.web.UIModule):
    '''
    The pygmentizer module is used as the main usage for code highlighting.
    '''

    def render(self):
        '''
        Renders the inined html code.
        '''

        return self.render_string('modules/pygmentizer.html')

