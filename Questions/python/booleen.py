# -*- coding: latin-1 -*-
#    QUENLIG: Questionnaire en ligne (Online interactive tutorial)
#    Copyright (C) 2006 Thierry EXCOFFIER, Universite Claude Bernard
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

from questions import *
from check import *

add(name='intro',
    required=['nombre:addition multiple', 'classeur:multiplication',
              'texte:remplace multiple', 'pour:compter de 2 en 2'],
    before="""Quand quelque chose est vrai, Python l'écrit
    <tt>True</tt> et si c'est faux, il écrit <tt>False</tt>""",
    question="""Fait écrire <tt>True</tt> à Python""",
    tests=(
    print_required,
    space_required,
    apostrophe_rejected,
    require("True", "Je ne vois pas le <tt>True</tt>"),
    python_answer_good('True\n'),
    ),
    )

add(name='égalité nombres',
    required=['intro', 'nombre:multiplication'],
    before="""Pour demander à Python si deux choses sont égales,
    on met l'opération <tt>==</tt> entre les deux choses.
    Par exemple <tt>print 5 == 7</tt> affiche <tt>False</tt>""",
    question="""Fait afficher à Python si <tt>123*456</tt>
    est égale à <tt>56088</tt>.""",
    tests=(
    print_required,
    space_required,
    apostrophe_rejected,
    multiply_required,
    do_not_cheat(rejected='True'),
    require(('123', '*', '456'), "Tu dois faire calculer <tt>123*456</tt>"),
    egality_required,
    comment("""Les parenthèses ne sont pas utiles car le Python
    calcule d'abord les multiplications, puis les additions et enfin
    il fait les comparaisons (<tt>==</tt> et les autres)""",
            require=(')','(')),
    python_answer_good('True\n'),
    ),
    )

add(name='égalité textes',
    required=['égalité nombres', 'texte:chien'],
    question="""Fais afficher à Python si <tt>'Bonjour'</tt>
    est égale à <tt>'bonjour'</tt>.""",
    tests=(
    print_required,
    space_required,
    apostrophe_required,
    do_not_cheat(rejected='False'),
    require(("'Bonjour'", "'bonjour'"),
            "Tu dois comparer les textes <tt>Bonjour</tt> et <tt>bonjour</tt>"
            ),
    egality_required,
    python_answer_good('False\n'),
    ),
    )

add(name='égalité classeurs',
    required=['égalité textes', 'classeur:dans classeur',
              'classeur:les entiers'],
    before = """2 classeurs sont égaux si chacune de leurs pages sont égales.
    <table class="invisible">
    <tr>
    <td align="right"><tt>[1,2,3]</tt></td>
    <td><tt>==</tt></td>
    <td><tt>[1,2,3]</tt></td>
    <td> donne <tt>True</tt> car ils sont identiques.</td>
    </tr>
    <tr>
    <td align="right"><tt>[1,2,3]</tt></td>
    <td><tt>==</tt></td>
    <td><tt>[1,1+1,1+1+1]</tt></td>
    <td> donne <tt>True</tt> car c'est vrai.</td>
    </tr>
    <tr>
    <td align="right"><tt>[1,2,3,4]</tt></td>
    <td><tt>==</tt></td>
    <td><tt>[1,2]+[3,4]</tt></td>
    <td> donne <tt>True</tt></td>
    </tr>
    <tr>
    <td align="right"><tt>[1,2,3]</tt></td>
    <td><tt>==</tt></td>
    <td><tt>[1,2]</tt></td>
    <td> donne <tt>False</tt> car ils n'ont pas le même nombre de pages.</td>
    </tr>
    <tr>
    <td align="right"><tt>[1,2,3]</tt></td>
    <td><tt>==</tt></td>
    <td><tt>[1,2,'3']</tt></td>
    <td> donne <tt>False</tt> car <tt>3</tt> est différent de <tt>'3'</tt></td>
    </tr>
    <tr>
    <td align="right"><tt>[1,2,3]</tt></td>
    <td><tt>==</tt></td>
    <td><tt>[1,3,2]</tt></td>
    <td> donne <tt>False</tt> car l'ordre est différent</td>
    </tr>
    </table>
    """,    
    question="""Fais afficher à Python si <tt>[0,1,2,1+2]</tt>
    est égale à <tt>range(4)</tt>.""",
    tests=(
    print_required,
    space_required,
    apostrophe_rejected,
    square_bracket_required,
    egality_required,
    do_not_cheat(rejected='True'),
    do_not_cheat(rejected='3'),
    range_required(4),
    python_answer_good('True\n'),
    ),
    )

good_search = """0 * 8 == 72 : False
1 * 8 == 72 : False
2 * 8 == 72 : False
3 * 8 == 72 : False
4 * 8 == 72 : False
5 * 8 == 72 : False
6 * 8 == 72 : False
7 * 8 == 72 : False
8 * 8 == 72 : False
9 * 8 == 72 : True
10 * 8 == 72 : False
11 * 8 == 72 : False
12 * 8 == 72 : False
13 * 8 == 72 : False
14 * 8 == 72 : False
"""

good_search2 = good_search.replace(' ','')

add(name="recherche 72",
    required=['égalité nombres', 'dis:formule et résultat',
              'pour:compter de 2 en 2'],
    question="""Fais afficher à Python :<pre>%s</pre>""" % good_search,
    tests=(
    print_required,
    space_required,
    apostrophe_required,
    egality_required,
    for_required,
    range_required(15),
    do_not_cheat(rejected=('False', '10')),
    python_answer_good(good_search2, remove_spaces=True),
    ),
    indices=(
    """Commence par faire une boucle affichant les nombres de 0 à 15,
    puis ajoute la formule, puis ajoute le test d'égalité pour
    que Python affiche <tt>True</tt> ou <tt>False</tt>""",
    )
    )

add(name='égalité étrange',
    required=['égalité textes'],
    question="""Fait afficher à Python si <tt>'True'</tt>
    et égale à <tt>True</tt>""",
    tests=(
    print_required,
    space_required,
    apostrophe_required,
    egality_required,
    require('True',
            """Je ne trouve pas la texte <tt>'True'</tt> dans
             la phrase Python&nbsp;!"""
            ),
    do_not_cheat(rejected='False'),
    python_answer_good('False\n'),
    ),
    good_answer="""Pour Python le texte <tt>'True'</tt>
    et <tt>True</tt> ne sont pas égaux car le deuxième n'est pas un texte
    mais un booléen qui indique si quelque chose est vrai ou faux.""",
    )

    
add(name='inférieur nombre',
    required=['égalité nombres'],
    before="""La phrase <tt>a &lt; b</tt> est vraie
    si <tt>a</tt> est plus petit que <tt>b</tt>.
    <p>
    <tt>a</tt> et <tt>b</tt> peuvent être des nombres, des textes, ...""",
    question="""Fais afficher si <tt>2*3</tt> est inférieur à <tt>6</tt>""",
    tests=(
    print_required,
    space_required,
    apostrophe_rejected,
    do_not_cheat(rejected='False'),
    require(('2','3','6','<','*'),
            "Dans la phrase Python on doit trouver&nbsp;: 2, 3, 6, *, &lt; et 6"
            ),
    less_than_required,
    python_answer_good('False\n'),
    ),
    good_answer = """Et oui, c'est faux car 6 n'est pas inférieur à 6....""",
    )

add(name='inférieur texte',
    required=['inférieur nombre', 'égalité textes'],
    before="""Un texte est inférieur (&lt;) à un autre s'il
    est avant lui dans le dictionnaire.""",
    question="""Fais afficher si <tt>'après'</tt> est inférieur à <tt>'avant'</tt>""",
    tests=(
    print_required,
    space_required,
    apostrophe_required,
    do_not_cheat(rejected='True'),
    require(("'après'","'avant'", '<'),
            "Dans la phrase Python on doit trouver&nbsp;: 'après', 'avant' et &lt;"
            ),
    less_than_required,
    python_answer_good('True\n'),
    ),
    )

add(name='dans',
    required=['si:cherche', 'égalité nombres'],
    before="""On a souvent besoin de savoir si quelque chose est
    dans un classeur. En français, on dirait
    <em>truc est-il dans machin&nbsp;?</em>
    en Python on dit <tt>truc in machin</tt>
    On a pas besoin du point d'interrogation.
    <pre>5 in [7,6,5,7]</pre>
    L'expression est vrai car <tt>5</tt> est dnas le classeur.    
    """,
    question="""Fais écrire à Python s'il trouve <tt>'a'</tt>
    dans le classeur <tt>'un grand chat'</tt>""",
    tests=(
    print_required,
    space_required,
    apostrophe_required,
    in_required,
    do_not_cheat(rejected='True'),
    reject('for', """Il faut faire cet exercice sans boucle <tt>for</tt>"""),
    require(("'un grand chat'","'a'"),
            """Dans la phrase Python on doit trouver&nbsp;: 'un grand chat'
            et 'a'"""
            ),
    python_answer_good('True\n'),
    ),
    )
    
add(name='classeur dedans',
    required=['dans', 'égalité classeurs'],
    question = """Fais afficher à Python s'il trouve
    <tt>[1,2]</tt> dans <tt>[ range(3), [2,1], [1,1+1], [1,2,3] ]</tt>""",
    default_answer = '[ range(3), [2,1], [1,1+1], [1,2,3] ]',
    tests=(
    print_required,
    space_required,
    in_required,
    square_bracket_required,
    number_of_is('[', 5),
    number_of_is(']', 5),
    range_required(3),
    do_not_cheat(rejected='True'),
    reject('for', """Il faut faire cet exercice sans boucle <tt>for</tt>"""),
    python_answer_good('True\n'),
    ),
    )


add(name='pas dans',
    required=['dans', 'histoire:enlève voyelles'],
    before="""En anglais, <tt>not</tt> veut dire <em>non</em> ou <em>pas</em>.
    L'expression Python <tt>5 not in [4,6]</tt> est <em>vrai</em>
    car <tt>5</tt> n'est pas dans <tt>[4,6]</tt>
    """,
    question="""Fais écrire à Python <tt>'un grand chat'</tt>
    en enlevant les voyelles (<tt>'aeiou'</tt>).
    """,
    nr_lines = 4,
    tests=(
    print_required,
    space_required,
    apostrophe_required,
    in_required,
    not_required,
    for_required,
    do_not_cheat(rejected='ngrndch'),
    require(("'un grand chat'","'aeiou'"),
            """Dans la phrase Python on doit trouver&nbsp;: 'un grand chat'
            et 'aeiou'"""
            ),
    python_answer_good('ngrndcht', remove_spaces=True, remove_newline=True),
    ),
    )
