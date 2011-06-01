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
Les "list" Python
"""

from questions import *
from check import *

add(name="création",
    required = ["idem:affectation", "idem:chaine", "idem:flottant"],
    before = """Un tableau Python est défini par une liste de valeurs
    entre crochets. Voici quelques exemples&nbsp;:
    <ul>
    <li> Un tableau vide : <tt>[]</tt>
    <li> Un tableau contenant un entier : <tt>[5]</tt>
    <li> Un tableau des chaines de caractères : <tt>["oui", "non"]</tt>
    <li> Un tableau contenant des tableaux :
    <tt>[["zero", "zero"], ["one", "un"], ["two", "deux"]]</tt>
    </ul>
    """,
    question="""Contrairement au langage C, les tableaux Python
    peuvent contenir des choses de natures différentes.
    <p>
    Affectez dans la variable <tt>r</tt> un tableau contenant
    l'entier <tt>5</tt>, la chaine de caractères <tt>toto</tt>
    et le nombre flottant <tt>1 virgule 2</tt>.
    """,

    tests = (
        Good(P(Equal('r = [5,"toto",1.2]'))),
        Expect('r'),
        Expect('='),
        Expect('5'),
        Expect('1.2'),
        Expect('"toto"'),
        Expect('['),
        Expect(']'),
        ),

    good_answer = """N'ayez pas peur, il y a des moyens simples pour
    créer de grand tableaux vides sans avoir à tout écrire&nbsp;!""",
    )

add(name="accès",
    required = ["création", "idem:affectation"],
    before = """Comme en langage C, on désigne un élément d'un tableau
    en ajoutant <tt>[la position]</tt> après le tableau.
    <p>
    Comme en langage C, la position du premier élement est <tt>0</tt>
    """,
    question = """La variable <tt>t</tt> contient un tableau,
    comment stockez vous dans la variable <tt>i5</tt> le cinquième
    élement du tableau <tt>t</tt>&nbsp;?""",
    tests = (
        Good(P(Equal('i5 = t[4]'))),
        Bad(Comment(P(Equal('i5 = t[5]')),
                    """ATTENTION : la position du premier élement est
                    <tt>0</tt>. Vous avez donc pris le sixième élement
                    du tableau <tt>t</tt>""")),
        Expect('i5'),
        Expect('t'),
        Expect('['),
        Expect(']'),
        Expect('='),
        ),   
    good_answer = """Contrairement au langage C, si vous essayez de lire un
    élements en dehors du tableau, il y a une erreur.""",
    )

add(name="stocke élément",
    required = ["accès"],
    question = """Comment stocker la valeur <tt>10</tt> dans le centième
    élément du tableau <tt>x</tt>&nbsp;?""",
    tests = (
        Good(P(Equal('x[99] = 10'))),
        Bad(Comment(P(Equal('x[100] = 10')),
                    """ATTENTION : la position du premier élement est
                    <tt>0</tt>. Vous avez donc indiqué
                    le 101<sup>ème</sup> élément.""")),
        Expect('99'),
        Expect('10'),
        Expect('['),
        Expect(']'),
        Expect('='),
        Expect('x'),
        ),
    good_answer = """Contrairement au langage C, si vous essayez d'écrire
    dans un élement en dehors du tableau, il y a une erreur.""",
    )

add(name="range",
    required = ["création"],
    before = """La fonction <tt>range</tt> permet de créer des tableaux
    contenant des entiers successifs.""",
    question = """Tapez <tt>range(10)</tt> dans votre interpréteur Python.
    <p>
    Quel est le dernier nombre affiché dans le tableau&nbsp;?
    """,
    tests = (
        Good(Int(9)),
        ),
    good_answer = """<tt>range</tt> permet aussi de générer un tableau
    contenant les entiers entre 2 bornes : <tt>range(100, 200)</tt>""",
    )

add(name="len",
    required = ["création"],
    question = "Qu'affiche la commande Python : <tt>len([6, 7, 8, 9])</tt>",
    tests = (
        Good(Int(4)),
        ),
    good_answer = "Bien entendu, <tt>len(range(1000))</tt> affiche 1000",
    )

add(name="sum",
    required = ["création"],
    question = "Qu'affiche la commande Python : <tt>sum([2000, 11, -1])</tt>",
    tests = (
        Good(Int(2010)),
        ),
    good_answer = """Bien entendu, <tt>sum(range(4))</tt> affiche 6.
    <p>
    Et <tt>sum([])</tt> donne <tt>0</tt>.
    """,
    )

add(name="concaténation",
    required = ["création", "range"],
    before = """On peut concaténer des tables en utilisant
    l'opérateur <tt>+</tt>, les tables utilisées ne sont pas modifiées,
    une nouvelle table est créée.<p>
    <tt>[1, 2] + ["x", "y"]</tt> donne <tt>[1, 2, "x", "y"]</tt>
    """,
    question = """Proposez une commande qui crée la table&nbsp;:<br>
    <tt>[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9]</tt>""",
    tests = (
        Good(P(Equal('range(10)+range(10)'))),
        Good(P(Equal('range(10)*2')|Equal('2*range(10)'))),
        Reject('3', """Vous devez utilisez <tt>range</tt> pour créer la table
        des entiers de 0 à 9"""),
        P(expects(('range', '+', 'range(10)'))),
        ),
    good_answer = "À votre avis, que donne <tt>[5] + [] + [6]</tt>&nbsp;?",
    )

add(name="affectation",
    required = ["création", "sum"],
    before = """Contrairement au langage C, l'affectation n'est pas une recopie
    mais un nommage.
    Vous pouvez donc donner plusieurs noms à la même chose.""",
    question = "Que va afficher le programme suivant&nbsp;?" + python_html(
        """a = [1, 2]
b = a
b[0] = 3
print(sum(a) + sum(b))"""),
    tests = (
        Int(10),
        ),
    good_answer = """Cela donne ce résultat car la variable <tt>a</tt>
    et <tt>b</tt> représentent le même tableau.
    Si vous modifiez le tableau cela modifie les deux variables.
    <p>
    Vous n'avez pas ce problème avec les nombres et les chaines de caractères
    car <b>on ne peut pas les modifier</b> une fois qu'ils ont été utilisés.
    On appelle cela des <em>immutables</em>.
    """,
    )

add(name="matrice",
    required = ["création", "stocke élément"],
    before = """Une table peut contenir des tables :
    <tt>matrice = [ [1,2], [3,4] ]</tt>
    <p>
    Pour identifier une case de la matrice on va d'abord indiquer
    un élement du premier tableau (c'est élément est un tableau)
    et un élement de cet élément.
    <p>
    <tt>matrice[0][1]</tt> donne <tt>2</tt>
    """,
    question = """Que tapez-vous pour remplacer dans la matrice donnée
    en exemple le <tt>3</tt> par <tt>5</tt>&nbsp;?""",
    tests = (
        Good(P(Equal('matrice[1][0] = 5'))),
        P(expects(('matrice', '[', ']', '5', '=',
                   'matrice[1]', 'matrice[1][0]'))),
        ),
    good_answer = """On peut bien sûr faire des matrices de matrices&nbsp;!""",
    )

add(name="multiplication",
    required = ["concaténation", "idem:multiplication", "matrice"],
    before = "<tt>3 * [5, 7]</tt> donne <tt>[5, 7, 5, 7, 5, 7]</tt>",
    question = "Créez une table contenant 1000 zéros (l'entier 0)&nbsp;?",
    tests = (
        Good(P(Equal("1000*[0]") | Equal('[0]*1000'))),
        P(expects(('1000', '*', '[', ']', '[0]'))),
        ),
    good_answer = """ATTENTION au piège : le contenu de la tableau
    n'est pas recopié, les éléments sont tous les mêmes.
    <p>
    Regardez bien le programme suivant&nbsp;:""" + python_html(
        """
        t = [[1,2]] * 3
        print(t)             # Cela affiche [[1, 2], [1, 2], [1, 2]]
        t[0][0] = 5
        print(t)             # Cela affiche [[5, 2], [5, 2], [5, 2]]
        """),
    )
        
    
    
    
    
    
    
