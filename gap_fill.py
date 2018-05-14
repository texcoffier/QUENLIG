import os
import re
import cgi
from QUENLIG.questions import TestUnary, Contain, Comment, Good, Bad, add
import QUENLIG.configuration
from QUENLIG import utilities


class NewlineIfy(TestUnary):
    """Add newlines before and after the anwser.

    This way, one can check Contain("\nfoo=bar\n") to check that
    foo=bar is given on a single line, whether it's at the beginning
    or at the end of the answer.
    """
    def canonize(self, string, dummy_state):
        string = re.sub(r'[\n\r]*$', '\n', string)
        string = re.sub(r'^[\n\r]*', '\n', string)
        return string


def process_template(template, prettifier, feedback):
    """Read a rich template (including expected answer and other meta-data
    within {{{...}}}) and produce a Quenlig gap-fill question.

    ``template`` is the text to fill-in.

    ``prettifier`` is a function called on each text portion (between
    {{{...}}}) that return a prettified version of this text.
    """
    splited = re.split("{{{([^}]*)}}}", template)
    tests = []
    i = 0
    new_template = ""
    while 2 * i + 1 < len(splited):
        def ans(a):
            return "\nA" + str(i) + "=" + a + "\n"
        code = splited[2 * i]
        # Content of the {{{...}}} splited according to |.
        # \ is the escape character.
        annotations = re.findall(r'(?:[^|\\]|\\.)+', splited[2 * i + 1])
        # Remove the escape character
        annotations = (re.sub(r'\\(.)', r'\1', a) for a in annotations)
        expected = []
        for a in annotations:
            if '=' not in a:
                # Accept {{{expected}}} or {{{OK1|OK2}}}
                expected.append(a)
                continue
            # Match strings like feedback[word]=sentence
            e = r'^(?P<key>[^=\[]*)(\[(?P<attr>[^\]]*)\])?=(?P<value>.*)'
            m = re.match(e, a)
            if not m:
                raise ValueError(
                    "Incorrect annotation in template: {}".format(a))
            k, attr, v = m.group('key'), m.group('attr'), m.group('value')
            # {{{expected=This is a correct answer}}}
            if k == "expected":
                expected.append(v)
            # {{{feedback[badanswer]=some feedback}}}:
            # reject badanswer and give feedback.
            if k == "feedback":
                if attr:
                    this_test = NewlineIfy(Contain(ans(attr)))
                    this_test = Comment(
                        this_test,
                        "<strike><i>{}</i></strike>: {}".format(
                            cgi.escape(attr), v)
                    )
                    this_test = Bad(this_test)
                    tests.append(this_test)
        new_template += prettifier(code) + "{{{$A" + str(i) + "}}}"

        this_test = Contain(ans(expected[0]))
        for e in expected[1:]:
            this_test = this_test | Contain(ans(e))
        this_test = NewlineIfy(~ this_test)
        if feedback:
            this_test = Comment(this_test,
                                'String "' +
                                cgi.escape(expected[0]) +
                                '" should appear in the answer.')
        this_test = Bad(this_test)
        tests.append(this_test)

        i += 1
    new_template += prettifier(splited[2 * i])
    return new_template, tests


def build_highlighter(lexer, formatter, template, template_file):
    try:
        import pygments
        from pygments.lexers import guess_lexer_for_filename, guess_lexer
        from pygments.formatters import HtmlFormatter
        # guess language on the template without {{{}}}:
        clean_template = re.sub('{{{[^}]*}}}', ' ', template)
        if lexer is None:
            if template_file is not None:
                lexer = guess_lexer_for_filename(template_file, clean_template)
            else:
                lexer = guess_lexer(clean_template)
        if formatter is None:
            formatter = HtmlFormatter(
                # inline formatting directives (avoid the need for a
                # separate style section):
                noclasses=True,
                # We'll wrap the whole thing ourselves:
                nowrap=True,
            )

        def pygments_highlight(code):
            return pygments.highlight(code, lexer, formatter)
    except ImportError:
        # Pygments is not available, just escape the code
        def pygments_highlight(code):
            return cgi.escape(code)

    def H(code):
        h = pygments_highlight(code)
        if not code.endswith('\n'):
            h = re.sub(r'[\n\r]+$', '', h)
        return h
    return H


def add_gap_fill(question, template=None, template_file=None,
                 feedback=False,
                 highlight=False, lexer=None, formatter=None, **kwargs):

    """Convenience wrapper around add() to add "fill-in the gaps" questions.

    ``question`` is the text of the question.

    ``template`` is the text to fill-in. It containts directives of
    the form {{{expected}}}, each of them will be replaced by a gap,
    and a test will be generated to check that the user answers with
    the expected string. Alternatively, one may provide a
    ``template_file`` argument and the file's content will be used.

    ``highlight`` is a Boolean saying whether the template should be
    highlighted. If so, it will use the lexer and formatter passed as
    argument, or guess the lexer and use its own formatter.

    ``feedback`` is a boolean saying whether to provide feedback on
    incorrect answers to student.

    Other arguments are forwarded to ``add``.

    Example:

        add_gap_fill(
            name="skel-lock2",
            question="Fill in the gaps:",
            template="void f({{{int}}}) {return {{{42}}};}",
            highlight=True,
            lexer=CppLexer()
        )

    """
    if template_file is None and template is None:
        raise ValueError(
            "Please provide either template or template_file keyword argument")
    if template_file is not None and template is not None:
        raise ValueError(
            "Please provide either template or template_file keyword argument,"
            " but not both")
    if template_file is not None:
        path = os.path.join(QUENLIG.configuration.questions, template_file)
        if not os.path.exists(path):
            raise ValueError(
                "Could not find template file '{}' in question '{}'.".format(
                    path, kwargs['name']))
        template = utilities.read(path)

    if highlight:
        H = build_highlighter(lexer, formatter, template, template_file)
    else:
        def H(x): return x
    new_template, tests = process_template(template, H, feedback)

    question += ("{{{$}}}" +  # Start the answer part.
                 """<div class="source"><pre style="background: white">""" +
                 new_template +
                 """</pre></div>""")
    tests.append(Good())  # Always True
    add(question=question, tests=tests, function_name='add_gap_fill', **kwargs)
