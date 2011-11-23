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
    question = """ Definissez une liste contenant dans l'ordre les elements <TT> 1, 'a', 2, 'b', 3 </TT> """,
    tests = ( Good(Equal("[ 1, 'a', 2, 'b', 3 ]") ) ) ,
    good_answer = """ Evidemment, une liste aussi etre un element d'une liste """,
 )

add(name="concatenation",
    required = [ "liste" ],
    question = """ Quel est l'operateur permettant de concatener 2 listes """,
    tests = ( Good(Equal("+"))) ,
    good_answer = """ Une nouvelle liste est creee par recopie des elements """,
)

add(name="sous-liste",
    required = [ "liste" ],
    question = """ Donner le resultat de l'expression <TT>[l[0]]+l[2:-2]+[l[-1]]</TT> appliquee a la liste <TT> l=[1,2,3,4,5,6] </TT> """,
    tests = ( Good(Equal("[1,3,4,6]")) ) ,
    good_answer = """ Effectivement, l'expression permet de retirer le deuxiemre et l'avant dernier element de toute liste <TT>l</TT> de longueur superieure ou egale a 3 """,
)

add(name="rotation circulaire gauche",
    required = ["liste","concatenation", "sous-liste"],
    question = """Ecrire l'expression, qui quelle que soit une liste nommee <tt> l </tt> <bf>non vide</bf>, retire le dernier element et l'insere en tete""",
    tests = (
        Good(Equal("[l[-1]]+l[:-1]")| Equal("[l[len(l)-1]]+l[:len(l)-1]")) ),
    good_answer = """On peut bien sur faire une fonction, mais dans ce cas, attention a la liste vide""",
   )
    
