# **pygmentize.me** - _your friendly syntax highlighting service_

## Overview

[pygmentize.me](http://pygmentize.me) is a web service providing syntax highlighting through the wonderful Python pygments library.

## API

Note that there are no trailing slashes at the end of the URL's.

**/api/formatter/:name**

Colorizes a chunk of code with the formatter specified by `name`. Every one argument is a regular *HTTP POST* query parameter.

*Arguments*

- `code` _[Required]_ - The code to highlight.
- `lexer` _[Default: text]_ - The name of the lexer to use for the highlight.
- `options` _[Default: None]_ - A JSON object of the options to pass to the formatter.
- `styles` _[Default: None]_  - A JSON array of options to the formatters `get_style_defs` method. Does nothing if not supported by the formatter.

*Returns*

The colorized code in the formatter markup language. The `Content-Type` header is set to the appropriate type for the markup.

**/api/supported/formatters**

*Returns*

The supported formatters and theirs metadata in a *JSON* object.

*Example*

    {'text':
      {'also_known_as': ['plain']},
      {'supports_style_defs': false},
      {'content_type': 'text/plain'}}

## Clients

**node.js**

- [Cobalt](https://github.com/gsamokovarov/cobalt) - A [node.js](http://nodejs.org) client written in CoffeeScript.

## License

Copyright (c) 2012, Genadi Samokovarov

This module is free software, and you may redistribute it and/or modify
it under the same terms as Python itself, so long as this copyright message
and disclaimer are retained in their original form.
 
IN NO EVENT SHALL THE AUTHOR BE LIABLE TO ANY PARTY FOR DIRECT, INDIRECT,
SPECIAL, INCIDENTAL, OR CONSEQUENTIAL DAMAGES ARISING OUT OF THE USE OF
THIS CODE, EVEN IF THE AUTHOR HAS BEEN ADVISED OF THE POSSIBILITY OF SUCH
DAMAGE.
 
THE AUTHOR SPECIFICALLY DISCLAIMS ANY WARRANTIES, INCLUDING, BUT NOT
LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A
PARTICULAR PURPOSE.  THE CODE PROVIDED HEREUNDER IS ON AN "AS IS" BASIS,
AND THERE IS NO OBLIGATION WHATSOEVER TO PROVIDE MAINTENANCE,
SUPPORT, UPDATES, ENHANCEMENTS, OR MODIFICATIONS.
