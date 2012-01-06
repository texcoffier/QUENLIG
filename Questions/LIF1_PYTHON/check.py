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
import ast

def P_clean(txt):
    if isinstance(txt, str):
        # Replace tabulations with space
        txt = txt.strip(' \n\t').replace('\t',' ').replace('\n\n', '\n').replace('\n',';')
        # A run of spaces if replaced by one space
        txt = re.sub('  +', ' ', txt)
        # A run of ; if replaced by one space
        txt = re.sub(';;+', ';', txt)
        # Spaces around not a normal letter are removed
        txt = re.sub(' *([^a-zA-Z0-9_]) *', r'\1', txt)
        return txt
    else:
        return [P_clean(i) for i in txt]


class P(TestUnary):
    """This test class is easy to use because it removes unecessary white
    space. Be it lose indentation. Bad code can be accepted"""
    
    def canonize(self, student_answer, state=None):
        if re.match('.*;[ \t]*$', student_answer):
            return (False,
                    'On ne met pas de <tt>;</tt> en fin de ligne en Python')
        if '...' in student_answer:
            return (False,
                    "Enlevez les «...» en début de ligne, ils ne font pas parti du langage. C'est l'invite de commande de l'interpréteur")
        try:
            compiler.parse(student_answer)
        except SyntaxError, e:
            return (False,
                    'Message de Python : <b>' + cgi.escape(str(e)) + '</b><br>'
                    )
        return P_clean(student_answer)

class P_AST(TestUnary):
    """Translate the Python code into the abstract Syntax Tree.
    Use this class for multiline Python code.
    With this test, unecessary parenthesis are not taken into account.
    But Replace, Contain, Start... operators are complicated to use,
    the canonize argument must be set to False and the string is the AST one.
    To see it :

    import ast
    ast.dump(ast.parse('def f(x): return x**2'))
    """
    def canonize(self, student_answer, state=None):
        if re.match('.*;[ \t]*$', student_answer):
            return (False,
                    'On ne met pas de <tt>;</tt> en fin de ligne en Python')
        if '...' in student_answer:
            return (False,
                    "Enlevez les «...» en début de ligne, ils ne font pas parti du langage. C'est l'invite de commande de l'interpréteur")
        try:
            ast_tree = ast.parse(student_answer)
        except SyntaxError, e:
            return (False,
                    'Message de Python : <b>' + cgi.escape(str(e)) + '</b><br>'
                    )
        print ast.dump(ast_tree)
        return ast.dump(ast_tree)
        
    
def python_color(txt):
    txt = cgi.escape(txt)
    if txt[-1] == ':':
        txt = txt[:-1] + '<span style="background:#F88">:</span>'
    txt = re.sub("^( +)", r'<span style="background:#F88">\1</span>', txt)
    txt = re.sub(" in ", r' <span style="background:#FF8">in</span> ', txt)

    txt = re.sub(r"\b(if|else|for|def|return|class|while|import)\b",
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

    return '<div style="font-family: monospace; background: #FFE;padding:2px;border: 1px solid black;white-space: pre">' + '<br>'.join(s) + '</div>'



def expects(expected, comment=None):
    a = Expect(expected[0], comment, canonize=False)
    for e in expected[1:]:
        a = a & Expect(e, comment, canonize=False)
    return a
