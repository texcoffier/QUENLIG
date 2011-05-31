# -*- coding: latin-1 -*-
# QUENLIG: Questionnaire en ligne (Online interactive tutorial)
# Copyright (C) 2011 Thierry EXCOFFIER, Eliane PERNA Universite Claude Bernard
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
#
# Contact: Thierry.EXCOFFIER@bat710.univ-lyon1.fr
#

"""
Les "dict" Python
"""

from questions import *
from check import *

add(name="création",
    required = ["table:création", "idem:chaine", "table:stocke élément"],
    before = """Un dictionnaire est un tableau dont les indices sont
    presque ce que vous voulez.
    Les indices des dictionnaires sont appelés des « clefs ».
    Généralement ce sont des chaines de caractères, mais pas seulement.
    <p>
    Le dictionnaire <tt>nombres = {'un':1, 'deux': 2}</tt>
    peut-être créé de la manière suivante&nbsp;:<pre>
nombres = {}          # Dictionnaire vide
nombres['un'] = 1     # La valeur de la clef 'un' est 1
nombres['deux'] = 2   # La valeur de la clef 'deux' est 2</pre>
    """,
    question="""Donnez l'écriture directe (avec les {clef: valeur...})
    du dictionnaire dont la valeur de la clef « nom » est
    la chaine de caractère « thierry »
    et la valeur de la clef « age » est l'entier « 21 ».
    <p>
    Les symboles '«' et '»' ne font bien sûr pas parti de votre réponse.
    """,

    tests = (
        Good(P(Equal('{"nom":"thierry", "age": 21}'))),
        P(expects(('nom', 'thierry', 'age', '21', ':', '{', '}', ',', '"',
                   '"nom":', '"age":', '"nom":"thierry"',
                   '"age": 21'))),
        ),

    good_answer = """Les clefs que l'on peut utiliser dans un dictionnaire
    sont&nbsp;:
    <ul>
    <li> Les entiers et flottants.
    <li> Les chaines de caractères.
    <li> Les tuples (ce sont des tableaux non modifiables)
    <li> D'autres choses, mais c'est rarement utile.
    </ul>""",
    )
