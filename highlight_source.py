import os
import cgi

import QUENLIG.configuration
from QUENLIG import utilities


def highlight_file(path, lexer=None, formatter=None):
    """Return a syntax-highlighted string corresponding to the program
    contained in a file.

    * path is the name of the file (relative to the questions directory)

    * lexer (optional) is a Pygmentize lexer. By default, the lexer is
      guessed from the filename and content.

    * formatter (optional) is a Pygmentize formatter. By default, the
      code will be formatted in HTML on a white background.
    """
    path = os.path.join(QUENLIG.configuration.questions, path)
    if not os.path.exists(path):
        raise ValueError("Could not find template file '{}'.".format(path))
    code = utilities.read(path)

    try:
        import pygments
        from pygments.lexers import guess_lexer_for_filename
        from pygments.formatters import HtmlFormatter
    except ImportError:
        # Pygments is not available, just surround the code with <pre>
        return '<pre style="background: white">{}</pre>'.format(
            cgi.escape(code))

    if lexer is None:
        lexer = guess_lexer_for_filename(path, code)
    if formatter is None:
        formatter = HtmlFormatter(
            # inline formatting directives (avoid the need for a
            # separate style section):
            noclasses=True,
            prestyles="background: white",
            cssclass="source"
        )

    return pygments.highlight(code, lexer, formatter)
