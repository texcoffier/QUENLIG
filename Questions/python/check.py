# -*- coding: latin-1 -*-
#    QUENLIG: Questionnaire en ligne (Online interactive tutorial)
#    Copyright (C) 2005-2006 Thierry EXCOFFIER, Universite Claude Bernard
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
#    Contact: Thierry.EXCOFFIER@univ-lyon1.fr

import os
import sys
from QUENLIG.questions import *
from QUENLIG import questions
import html
import subprocess

preamble = subprocess.check_output(['pypy-sandbox', '--', '-c', '0'],
                                   stderr=subprocess.STDOUT)

global_evals = {}

def python_eval(v):
    """Eval a python with a cache"""
    if v in global_evals:
        return global_evals[v]

    if not os.path.isdir('XXX-PYPY'):
        os.mkdir('XXX-PYPY')
    f = open("XXX-PYPY/xxx.py", "w")
    f.write("""# -*- coding: latin-1 -*-\n""")
    f.write(v)
    f.close()
    # sudo :                              exco ALL=(nobody) NOPASSWD: ALL
    f = os.popen('ulimit -t 1 ; ulimit -v 100000 ; pypy-sandbox --tmp XXX-PYPY xxx.py 2>&1',
                 'r')
    displayed = f.read().replace(preamble, '')
    f.close()

    global_evals[v] = displayed

    return displayed

def answer_cleaning(v, remove_spaces=False, remove_newline=False):
    if remove_spaces:
        v = v.replace(' ', '')
    if remove_newline:
        v = v.replace('\n', '')
    return v

def python_answer(v, comment=''):
    if comment:
        comment = comment + "</p><p>"
    else:
        comment += '<br>'
    return comment + "Le Python r�pond : <pre>" + html.escape(v).replace('\n', '&nbsp;\n') + '</pre>'

# With this the Python answer good or bad is always displayed.
questions.current_eval_after = lambda answer, state: python_answer(python_eval(answer))


class TestPython(Test):
    def __init__(self, strings=None, comment=None,
                 replacement=None, dumb_replace=None,
                 remove_spaces=False, remove_newline=False):
        Test.__init__(self, strings, comment=comment, replace=dumb_replace,
                      replacement=replacement)
        self.remove_spaces = remove_spaces
        self.remove_newline = remove_newline
        self.strings_parsed = [answer_cleaning(v,remove_spaces,remove_newline)
                               for v in self.strings]

    def answer_processing(self, answer):
        return answer_cleaning(python_eval(answer),
                               self.remove_spaces, self.remove_newline)

class python_answer_good(TestPython, good):
    html_class = "test_python test_good test_is"
class python_answer_bad(TestPython, bad):
    html_class = "test_python test_bad test_is"
class python_answer_reject(TestPython, reject):
    html_class = "test_python test_bad test_reject"
class python_display(TestPython):
    html_class = "test_python test_bad test_reject"



print_required = require(
    "print",
    """Il faut utiliser le mot <tt>print</tt> pour lui dire
    <em>dis-moi</em> sinon il ne te dira rien""")

apostrophe_required = require(
    "'",
    """Il faut mettre des apostrophes autour de ce que tu veux faire
    r�p�ter au Python""")

apostrophe_rejected = reject(
    "'",
    """Il ne faut pas mettre des apostrophes autour des nombres
    et des op�rations, sinon Python ne les comprend pas""")

space_required = require(
    " ",
    """Le Python est comme toi, pour qu'il comprenne une phrase
    form�e de mot, il pr�f�re que les mots soient s�par�s les
    uns de autres par un espace.""")

plus_required = require(
    '+',
    "Tu as oubli� le '+' pour faire l'addition")

minus_required = require(
    '-',
    "Tu as oubli� le '-' pour faire la soustraction")

multiply_required = require(
    '*',
    "Tu as oubli� le '*' pour faire la multiplication")

comma_required = require(
    ',',
    "Tu as oubli� la virgule qui veut dire �<em>et</em>�")

comma_rejected = reject(
    ',',
    "On a pas besoin de la virgule pour r�pondre � cet exercice.")

lf_required = require(
    '\\n',
    "Tu as oubli� un <tt>\\n</tt> pour lui dire de revenir � la ligne.")

bracket_required = require(
    ('(', ')'),
    """Tu as oubli� de mettre des parenth�ses pour que
    le Python calcule dans le bon ordre.""")

square_bracket_required = require(
    ('[', ']'),
    """Tu as oubli� de mettre des crochets <tt>[</tt>
    et <tt>]</tt> pour indiquer le devant et l'arri�re de
    la couverture du classeur.""")

for_required = require(
    ('for ', 'in', ':'),
    """Pour feuilleter un classeur, il faut respecter la phrase&nbsp;:<br>
    <tt>for page in classeur:</tt>
    """)

if_required = require(
    ('if ', ':'),
    """Pour faire un <em>si</em> il faut utiliser le mot <tt>if</tt>
    et mettre un <tt>:</tt> apr�s la condition.
    """)

else_required = require(
    ('else', ':'),
    """Pour faire un <em>sinon</em> il faut utiliser le mot <tt>else</tt>
    suivi d'un <tt>:</tt>""")

egality_required = require(
    '==',
    """Pour tester si deux choses sont �gales,
    il faut utiliser <tt>==</tt> (oui, il faut 2 =)""")

in_required = require(
    'in',
    """Pour savoir si quelque chose est dans un classeur
    on utilise le mot Python <tt>in</tt>.
    <p>
    <tt>5 in [4,6,7]</tt> r�pond <tt>False</tt>""")

not_required = require(
    'not',
    """C'est le mot <tt>not</tt> qui indique la n�gation.
    Pour faire l'exercice, tu en as besoin.
    """)

less_than_required = require(
    '<',
    """Pour tester si une chose est plus petite qu'une autre,
    il faut utiliser <tt>&lt;</tt>""")

def range_required(value=None):
    if value == None:
        return require('range', "On doit utiliser <tt>range</tt>")
    return require(('range', str(value)),
                   """Utilise <tt>range</tt> pour faire une classeur
                   contenant les nombres de 0 � %d""" % (value-1))


def do_not_cheat(rejected=None, required=None):
    cheat_message = """C'est Python qui doit trouver la r�ponse, pas toi.
    Il doit faire les calculs tout seul sans que tu l'aides.
    """
    if rejected != None:
        return reject(rejected, cheat_message)
    if required != None:
        cheat_message += """On doit trouver dans la phrase Python
        les �l�ments suivants&nbsp;:""" + str(required)
        return require(required, cheat_message)

replace_required = require(
    ('.', 'replace', '('),
    """Il faut utiliser <tt>.replace(</tt> pour faire le remplacement."""
    )
