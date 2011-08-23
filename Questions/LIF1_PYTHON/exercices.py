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
    fonction donne le bon résultat dans l'interpréteur Python.
    <p>
    Que donne <tt>somme([0.5, 1.3, 0.1])</tt>&nbsp;?""",
    )

add(name="ajoute complexe",
    required = ["control:def", "structure:attributs"],
    before = """En Python il n'y a pas de procédures, seulement des fonctions.
    <p>
    Si il n'y a pas de <tt>return<tt> dans une fonction alors
    la valeur <tt>None</tt> est automatiquement retournée
    <p>
    On peut considérer qu'une procédure est une fonction sans <tt>return<tt>
    """,
    question = """Définissez la procédure <tt>ajoute_au_premier</tt>
    qui a comme paramètres <tt>a</tt> et <tt>b</tt> qui sont des complexes
    et qui ajoute <tt>a</tt> et <tt>b</tt> et stocke le
    résultat dans <tt>a</tt>""",
    default_answer = """def ajoute_au_premier(a, b):
    """,
    nr_lines = 4,
    tests = (
        Good(P(Replace((
            ('b.imaginaire+a.imaginaire', 'a.imaginaire+b.imaginaire'),
            ('b.reel+a.reel', 'a.reel+b.reel'),
            ('a.reel=a.reel+', 'a.reel+='),
            ('a.imaginaire=a.imaginaire+', 'a.imaginaire+='),
            ),
                       Equal('def ajoute_au_premier(a,b):\n a.reel+=b.reel\n a.imaginaire+=b.imaginaire')
                        | Equal('def ajoute_au_premier(a,b):\n a.imaginaire+=b.imaginaire\n a.reel+=b.reel')
                       ))),
        Bad(Comment(~ NumberOfIs('\n', 2),
                    """La réponse est en 3 lignes : le <tt>def</tt>
                    et les deux affections (parties réel et imaginaire)""")),
        expects(('def', ':', '=', '+', 'imaginaire', 'reel',
                'a.imaginaire', 'a.reel', 'b.imaginaire', 'b.reel')),
        ),
    good_answer = """Il est tout à fait possible d'écrire
    <tt>a += b</tt> au lieu de <tt>ajoute_au_premier(a, b)</tt>.
    <p>
    Mais pour cela on définit une <em>methode</em> et cela dépasse
    l'objectif de ce cours.""",
    )
    

# XXX a finir ? (structure:instance paramétrée n'est pas fini non plus)
# add(name="ajoute complexe",
#     required = ["control:def", "structure:instance paramétrée",
#                 "structure:attributs"],
#     question = """Définissez la fonction <tt>sum_c</tt>
#     qui a comme paramètres <tt>a</tt> et <tt>b</tt> qui sont des complexes
#     et qui retourne le complexe égal à la somme des deux.
#     <p>
#     Cette fonction ne doit pas modifier ses paramètres.
#     """,
#     default_answer = """def sum_c(a, b):
#     """,
#     tests = (
#         Good(P('def sum_c(a,b):return Complexe(a.reel+b.reel,a.imaginaire+b.imaginaire)')),
#         ),
#     good_answer = """On peut bien sûr faire en sorte d'utiliser <tt>+</tt>
#     pour additionner les complexes.
#     Mais pour cela on définit une <em>methode</em> mais cela dépasse
#     l'objectif de ce cours.""",
#     )
#     
