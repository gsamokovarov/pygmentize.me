from plush.command import define, parse_command_line

from app import app


define('port', default=8000, type=int,
        help='The port to run the server on')
define('debug', default=True, type=bool,
        help='Run with debug information')


app.settings.from_module('settings')
app.run(**parse_command_line())
