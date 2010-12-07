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
#    Contact: Thierry.EXCOFFIER@bat710.univ-lyon1.fr

import os
import sys
from questions import *
import questions
import cgi

f = os.popen('sudo -u nobody echo ok', 'r')
if f.read() != 'ok\n':
    sys.stderr.write("""Please use the command 'visudo' to add the line:
    
login_name_of_the_user_running_the_server   ALL=(nobody)   NOPASSWD: ALL

This allow the server to use 'sudo nobody'
""")
    sys.exit(1)
f.close()


global_evals = {}

def python_eval(v):
    """Eval a python with a cache"""
    if global_evals.has_key(v):
        return global_evals[v]
    
    f = open("xxx.py", "w")
    f.write("""# -*- coding: latin-1 -*-\n""")
    f.write(v)
    f.close()
    # sudo :                              exco ALL=(nobody) NOPASSWD: ALL
    f = os.popen('ulimit -t 1 ; ulimit -v 10000 ; sudo -u nobody python xxx.py 2>&1', 'r')
    displayed = f.read()
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
    return comment + "Le Python répond : <pre>" + cgi.escape(v).replace('\n', '&nbsp;\n') + '</pre>'

# With this the Python answer good or bad is always displayed.
questions.current_evaluate_answer = lambda answer, state: python_answer(python_eval(answer))


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
    répéter au Python""")

apostrophe_rejected = reject(
    "'",
    """Il ne faut pas mettre des apostrophes autour des nombres
    et des opérations, sinon Python ne les comprend pas""")

space_required = require(
    " ",
    """Le Python est comme toi, pour qu'il comprenne une phrase
    formée de mot, il préfère que les mots soient séparés les
    uns de autres par un espace.""")

plus_required = require(
    '+',
    "Tu as oublié le '+' pour faire l'addition")

minus_required = require(
    '-',
    "Tu as oublié le '-' pour faire la soustraction")

multiply_required = require(
    '*',
    "Tu as oublié le '*' pour faire la multiplication")

comma_required = require(
    ',',
    "Tu as oublié la virgule qui veut dire <em>et</em>")

comma_rejected = reject(
    ',',
    "On a pas besoin de la virgule pour répondre à cet exercice.")

lf_required = require(
    '\\n',
    "Tu as oublié un <tt>\\n</tt> pour lui dire de revenir à la ligne.")

bracket_required = require(
    ('(', ')'),
    """Tu as oublié de mettre des parenthèses pour que
    le Python calcule dans le bon ordre.""")

square_bracket_required = require(
    ('[', ']'),
    """Tu as oublié de mettre des crochets <tt>[</tt>
    et <tt>]</tt> pour indiquer le devant et l'arrière de
    la couverture du classeur.""")

for_required = require(
    ('for ', 'in', ':'),
    """Pour feuilleter un classeur, il faut respecter la phrase&nbsp;:<br>
    <tt>for page in classeur:</tt>
    """)

if_required = require(
    ('if ', ':'),
    """Pour faire un <em>si</em> il faut utiliser le mot <tt>if</tt>
    et mettre un <tt>:</tt> après la condition.
    """)

else_required = require(
    ('else', ':'),
    """Pour faire un <em>sinon</em> il faut utiliser le mot <tt>else</tt>
    suivi d'un <tt>:</tt>""")

egality_required = require(
    '==',
    """Pour tester si deux choses sont égales,
    il faut utiliser <tt>==</tt> (oui, il faut 2 =)""")

in_required = require(
    'in',
    """Pour savoir si quelque chose est dans un classeur
    on utilise le mot Python <tt>in</tt>.
    <p>
    <tt>5 in [4,6,7]</tt> répond <tt>False</tt>""")

not_required = require(
    'not',
    """C'est le mot <tt>not</tt> qui indique la négation.
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
                   contenant les nombres de 0 à %d""" % (value-1))


def do_not_cheat(rejected=None, required=None):
    cheat_message = """C'est Python qui doit trouver la réponse, pas toi.
    Il doit faire les calculs tout seul sans que tu l'aides.
    """
    if rejected != None:
        return reject(rejected, cheat_message)
    if required != None:
        cheat_message += """On doit trouver dans la phrase Python
        les éléments suivants&nbsp;:""" + str(required)
        return require(required, cheat_message)

replace_required = require(
    ('.', 'replace', '('),
    """Il faut utiliser <tt>.replace(</tt> pour faire le remplacement."""
    )
