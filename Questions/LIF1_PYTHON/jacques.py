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
Quelques questions
"""

from questions import *
from check import *

add(name="liste",
    required = ["table:création", "idem:chaine", "idem:flottant", ],
    question = """Définissez une liste contenant dans l'ordre les éléments :
               <TT>1, "a", 2, "b", 3.5</TT>""",
    tests = ( Good(P(End('[1,"a",2,"b",3.5]') ) ),
            ),
    good_answer = "Évidemment, une liste peut contenir des listes",
 )

add(name="concatenation",
    required = ["liste", "table:concaténation"],
    question = "Quel est l'opérateur permettant de concaténer 2 listes&nbsp;?",
    tests = ( Good(Equal("+")),
              ),
    good_answer = "Une nouvelle liste est créée par recopie des éléments.",
)

add(name="sous-liste",
    required = ["liste", "concatenation", "table:accès négatif"],
    question = """Donner le résultat de l'expression
               <TT>[l[0]]+l[2:-2]+[l[-1]]</TT> appliquée à la liste
               <TT>l=[1,2,3,4,5,6]</TT>""",
    tests = ( Good(P(Equal("[1,3,4,6]"))),
              ) ,
    good_answer = """Effectivement,
   l'expression permet de retirer le deuxième et
   l'avant dernier élément de toute liste <TT>l</TT> de longueur supérieure
   ou égale à 3.""",
)

add(name="rotation gauche",
    required = ["liste", "concatenation", "sous-liste"],
    question = """Ecrire l'expression, qui, quelle que soit une liste nommée
    <tt>l</tt> de la forme <tt>[a, b..., c, d]</tt>,
    crée une nouvelle liste de la forme <tt>[d, a, b..., c]</tt>.
""",
    tests = (
        Reject('=', """On veux seulement le résultat, vous n'avez pas
               besoin de le stocker"""),
        Reject('[0:',
               """On n'écrit pas <tt>t[0:4]</tt> mais <tt>t[:4]</tt>
                  car c'est plus court."""),
        Reject('len',
               """Vous n'avez pas besoin de calculer la longueur de la liste
               car en Python les indices négatifs partent de la fin du
              tableau&nbsp;: l[-1] est le dernier élément."""),
        Good(P(Equal("[l[-1]]+l[:-1]"))),
        Bad(Comment(
                P(Equal("l[-1]+l[:-1]")),
                """Vous ajoutez un élément à une liste alors que vous
                 devez ajouter deux listes""")
            ),
        ),
    good_answer = """On peut bien sûr faire une fonction,
                     mais dans ce cas, attention à la liste vide.""",
   )
    
