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
Exercices simples
"""

from questions import *
from check import *

add(name="len",
    required = ["control:def", "control:for", "table:len"],
    question = """La réponse à cette question est la définition de la fonction
   <tt>longueur</tt> qui retourne la longueur du tableau passé en paramètre.
   <p>
   La définition de la fonction est la suivante~:
   <ul>
   <li>On déclare <tt>longueur</tt> comme une fonction avec un paramètre
        <tt>table</tt>
   <li>On met 0 dans la variable <tt>nb_elements</tt>.
   <li>Pour chaque élément <tt>i</tt> du tableau <tt>table</tt> :
       <ul>
       <li> On ajoute 1 à la variable <tt>nb_elements</tt>
       </ul>
   <li> On retourne la valeur de <tt>nb_elements</tt>
   </ul>
   """,
    nr_lines = 5,
    tests = (
        Good(P(Replace((('nb_elements=nb_elements+1', 'nb_elements+=1'),
                        ('nb_elements=1+nb_elements', 'nb_elements+=1'),
                        ),
                       Equal('def longueur(table):\n nb_elements = 0\n for i in table:\n  nb_elements += 1\n return nb_elements')))),
        expects(('for', 'nb_elements', '1', 'return', '=', ' in ', 'def ',
                 'longueur', ':')),
        Expect(' i ', "L'indice de boucle doit être <tt>i</tt>"),
        ),
    good_answer = """La fonction <tt>len</tt> ne fait pas de boucle,
    elle est donc beaucoup plus rapide que votre version.""",
    )

add(name="sum",
    required = ["control:def", "control:for", "table:sum"],
    question = """La réponse à cette question est la définition de la fonction
   <tt>somme</tt> qui retourne la somme des éléments d'un tableau
   passé en paramètre.
   <p>
   La définition de la fonction est la suivante~:
   <ul>
   <li>On déclare <tt>somme</tt> comme une fonction avec un paramètre
        <tt>table</tt>
   <li>On met 0 dans la variable <tt>la_somme</tt>.
   <li>Pour chaque élément <tt>i</tt> du tableau <tt>table</tt> :
       <ul>
       <li> On ajoute <tt>i</tt> à la variable <tt>la_somme</tt>
       </ul>
   <li> On retourne la valeur de <tt>la_somme</tt>
   </ul>
   """,
    nr_lines = 5,
    tests = (
        Good(P(Replace((('la_somme=la_somme+i', 'la_somme+=i'),
                        ('la_somme=i+la_somme', 'la_somme+=i'),
                        ),
                       Equal('def somme(table):\n la_somme = 0\n for i in table:\n  la_somme += i\n return la_somme')))),
        expects(('for', 'la_somme', 'return', '=', ' in ', 'def ',
                 'somme', ':')),
        Expect(' i ', "L'indice de boucle doit être <tt>i</tt>"),
        ),
    good_answer = """Si vous ne l'avez pas fait : vérifier que votre
    fonction donne le bon résultat dans l'interpréteur Python.""",
    )

