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

add(name="accès négatif",
    required = ["accès", "control:for", "chaine"],
    before = """Quand on indique une position dans un tableau à partir
    de la fin on utilise un nombre négatif.
    <tt>a[-1]</tt> est le dernier élément et
    <tt>a[-2]</tt> est l'avant-dernier.""",
    question = """Faites afficher les 10 derniers éléments
    du tableau <tt>a</tt>
    <p>
    Vous utiliserez <tt>i</tt> comme variable de boucle.
    """,
    nr_lines = 3,
    tests = (
        Reject("len", "Sans utiliser <tt>len</tt> bien sûr"),
        Reject("*", "Sans utiliser <tt>*</tt> s'il vous plaît."),
        Good(P(Equal('for i in range(10):\n print(a[-i-1])'))),
        Good(P(Equal('for i in range(10):\n print(a[-1-i])'))),
        Good(P(Equal('for i in range(10):\n print(a[-(1+i)])'))),
        Good(P(Equal('for i in range(10):\n print(a[-(i+1)])'))),
        Good(P(Equal('for i in range(1,11):\n print(a[-i])'))),
        Good(P(Equal('for i in range(-1,-11,-1):\n print(a[i])'))),
        ),
    bad_answer = """Le plus simple est de compléter le code suivant&nbsp;:
    <pre>for i in range(10):
    print()</pre>""",
    good_answer = """Cela marche aussi sur les chaines de caractères.
    <p><tt>"QWERTY"[-1]</tt> c'est tout simplement <tt>Y</tt>""",
    ),
    
    

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
    question = """Tapez <tt>range(10)[0]</tt> dans votre interpréteur Python.
    <p>
    Quel est le nombre affiché&nbsp;?
    """,
    tests = (
        Good(Int(0)),
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
    required = ["création", "range"],
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
    required = ["création", "idem:addition"],
    before = """On peut concaténer des tables en utilisant
    l'opérateur <tt>+</tt>, les tables utilisées ne sont pas modifiées,
    une nouvelle table est créée.<p>
    <tt>[1, 2] + ["x", "y"]</tt> donne <tt>[1, 2, "x", "y"]</tt>
    """,
    question = """Proposez une commande qui crée la table&nbsp;:<br>
    <tt>[7, 3, 8, 9, 1]</tt><br>
    En utilisant les variables suivantes (pas forcément toutes):
    <ul>
    <li> <tt>a = [7, 3 ,8]</tt>
    <li> <tt>b = [8, 9, 1]</tt>
    <li> <tt>c = [9]</tt>
    <li> <tt>d = [1]</tt>
    </ul>
    """,
    tests = (
        Good(P(Equal('a+c+d'))),
        Bad(Comment(P(Equal('a+b')),
                     """Vous obtenez <tt>[7, 3 ,8 ,8 ,9 ,1]</tt>,
                     ce n'est pas la valeur attendue."""
                     )),
        Reject('[',
               "Vous n'avez pas besoin d'accéder aux éléments des tables"),
        Reject('1', "Vous devez utiliser les variables, pas les valeurs"),
        P(expects(('+', 'a', 'c', 'd'))),
        ),
    good_answer = "À votre avis, que donne <tt>[5] + [] + [6]</tt>&nbsp;?",
    )


add(name="empiler",
    required=["concaténation", "control:for"],
    before = """Toutes les tables contiennent un attribut qui est une fonction
                permettant d'ajouter un élément à la fin de la table.
                C'est la fonction <tt>append</tt> qui a pour paramètre
                l'élément à ajouter&nbsp;:
                <tt>t.append(6)</tt> ajoute 6 à la fin de <tt>t</tt> qui
                contiendra donc un élément de plus.
             """,
    question = """Écrivez une boucle ajoutant tous les éléments contenus
                  dans la table <tt>a</tt> pour les mettre
                  dans la table <tt>b</tt>
               <p>Utilisez <tt>element_de_a</tt> comme indice de boucle.
               """,
    nr_lines = 3,
    tests = (
        P(expects(('for', 'element_de_a', ':', 'append', 'b.append',
                   'b.append(element_de_a)'))),
        Bad(Comment(~NumberOfIs('element_de_a', 2),
                     """<tt>element_de_a</tt> doit apparaître deux fois
                        dans votre réponse&nbsp;: une fois comme indice
                        de boucle et une fois comme argument de
                        la fonction <tt>append</tt>""")),
        Good(P(Equal("for element_de_a in a:\n b.append(element_de_a)"))),
        ),
    good_answer = """Il est évidemment beaucoup plus rapide d'écrire
                     <tt>b = b + a</tt>""",
    )

add(name="chaine",
    required = ["idem:chaine", "control:for", "concaténation", "accès",
                "idem:affectation"],
    before = """On peut utiliser une chaine de caractères exactement
    comme un tableau&nbsp;!""" + python_html("""
    for i in "coucou":
       print(i)          # Affiche chacune des lettres du texte sur une ligne
    print('*'*10)        # Affiche **********
    a = "Le"
    b = "chaton"
    c = a + " beau " + c # On peut les concaténer
    print(a[1])          # Affiche la lettre 'e'"""),
    question = """Stockez dans la variable <tt>a</tt> : la première
    et la cinquième lettre de la valeur contenue dans <tt>b</tt>.
    <p>
    <tt>a</tt> contiendra donc une chaine de 2 lettres.""",
    tests = (
        Good(P(Equal('a=b[0]+b[4]'))),
        Bad(Comment(P(Equal('a=b[1]+b[5]')),
                    "Attention les indices commencent à 0 !")),
        Expect('+', """On utilise <tt>+</tt> pour concaténer les chaines
        de caractères"""),
        P(expects(('a', 'b', '=', '0', '4', '[0]', '[4]'))),
        ),
    good_answer = """ATTENTION : contrairement aux tableaux, on ne peut
    pas modifier une chaine de caractères.
    Essayez de taper&nbsp;:
    <pre>a = "coucou"
a[0] = "C"</pre>
    Cela déclenchera une erreur.""",
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
        
    
    
    
    
    
    
