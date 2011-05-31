# -*- coding: latin-1 -*-
#    QUENLIG: Questionnaire en ligne (Online interactive tutorial)
#    Copyright (C) 2011 Thierry EXCOFFIER, Universite Claude Bernard
#
#    This program is free software; you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation; either version 2 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program; if not, write to the Free Software
#    Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
#
#    Contact: Thierry.EXCOFFIER@bat710.univ-lyon1.fr
#

from questions import *
import re
import cgi
import compiler

def P_clean(txt):
    if isinstance(txt, str):
        # Replace tabulations with space
        txt = txt.strip(' \n\t').replace('\t',' ').replace('\n',' ')
        # A run of spaces if replaced by one space
        txt = re.sub('  +', ' ', txt)
        # Spaces around not a normal letter are removed
        txt = re.sub(' *([^a-zA-Z0-9_]) *', r'\1', txt)
        return txt
    else:
        return [P_clean(i) for i in txt]


class P(TestUnary):
    def __call__(self, student_answer, state=None, parser=no_parse):
        if re.match('.*;[ \t]*$', student_answer):
            return (False,
                    'On ne met pas de <tt>;</tt> en fin de ligne en Python')
        try:
            compiler.parse(student_answer)
        except SyntaxError as e:
            return False, 'Message de Python : <b>' + cgi.escape(str(e))+'</b>'
        return self.children[0](
            P_clean(student_answer), state,
            lambda string, state, test: parser(P_clean(string), state, test)
            )

def python_color(txt):
    txt = cgi.escape(txt)
    if txt[-1] == ':':
        txt = txt[:-1] + '<span style="background:#F88">:</span>'
    txt = re.sub("^( *)", r'<span style="background:#F88">\1</span>', txt)
    txt = re.sub(" in ", r' <span style="background:#FF8">in</span> ', txt)

    txt = re.sub(r"\b(if|else|for|def|return)\b",
                 r'<span style="background:#FF8">\1</span>',
                 txt)
    return txt

def python_html(txt):
    s = []
    if '>>>' in txt:
        for line in txt.strip().split('\n'):
            line = line.strip()
            if line.startswith('>>> '):
                s.append('&gt;&gt;&gt; <b>' + python_color(line[4:]) + '</b>')
            elif line.startswith('... '):
                s.append('... <b>' + python_color(line[4:]) + '</b>')
            else:
                s.append('<em>' + cgi.escape(line) + '</em>')
    else:
        txt = txt.strip('\n').split('\n')
        indent = len(txt[0]) - len(txt[0].lstrip(' '))
        for line in txt:
            if line.strip():
                s.append(python_color(line[indent:]))

    return '<div style="font-family: monospace; background: #FFE;padding:2px;border: 1px solid black;white-space: pre">' + '\n'.join(s) + '</div>'



def expects(expected, comment=None):
    a = Expect(expected[0], comment)
    for e in expected[1:]:
        a = a & Expect(e, comment)
    return a
