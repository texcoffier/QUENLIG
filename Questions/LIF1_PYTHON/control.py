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
Les structures de contrôle Python
"""

from questions import *
from check import *

add(name="for",
    required = ["table:range", "idem:flottant", "io:print"],
    before = """La boucle <tt>for</tt> de Python est plus simple
    que celle du C. C'est une boucle permettant de parcourir des ensembles.
    Par exemple&nbsp;:""" + python_html("""
    >>> for element in [45, -5, "coucou", 3.40000000, [7,8]]:
    ...    print(element)
    ...
    45
    -5
    coucou
    3.4
    [7, 8]
    >>> """) + """
    Quelques remarques :
    <ul>
    <li> Affiché en rouge, ce sont les choses à ne pas oublier.
    <li> Pour indiquer que l'on a terminé la boucle, on tape sur
    la touche « Entrée » sur une ligne vide.
    <li> On peut utiliser n'importe quelle variable comme indice
    de boucle, par forcément <tt>element</tt>.
    """,
    question="""Faites un boucle avec <tt>i</tt> comme indice de boucle,
    qui parcourt l'ensemble des nombre entiers de 0 à 9 inclus et
    qui affiche chacun des nombre.
    <p>
    Ne recopiez pas les <tt>&gt;&gt;&gt;</tt> et <tt>...</tt>,
    mais seulement ce que <b>vous</b> avez tapé.
    N'oubliez pas les espaces pour décaler à droite.
    """,
    nr_lines = 3,
    tests = (
        Good(P(Equal('for i in range(10):\n   print(i)'))),
        Expect("for",
               "On utilise le mot-clef <tt>for</tt> pour faire un boucle"),
        Expect(' i ',
               """Vous devez appeler <tt>i</tt> la variable qui
               est l'indice de boucle"""),
        Expect('range',
               """Vous devez utiliser la fonction <tt>range</tt> pour
               créer les nombres entiers de 0 à 9 inclus."""),
        P(Expect('range(10)',
               """Vous devez utiliser <tt>range(10)</tt> pour
               créer les nombres entiers de 0 à 9 inclus.""", canonize=False)),
        Expect(':', """Le langage Python impose le « : » qui indique
        le début du corps de la boucle"""),
        Expect('print', """Vous devez utiliser la fonction <tt>print</tt>
        pour afficher la valeur de l'indice."""),
        P(Expect('print(i)',
                 """Vous devez simplement afficher la variable <tt>i</tt>.
                 Donc c'est <tt>print(i)</tt>""", canonize=False)),
        Expect(' in ', """Le langage Python est très littéraire,
        il manque le <tt>in</tt> qui veut dire <b>dans</b> en français."""),
        ),

    good_answer = """Si l'on veut faire plusieurs actions dans le corps
    de la boucle, il suffit d'écrire plusieurs lignes d'instructions.
    <p>
    ATTENTION :  Et les lignes qui sont dans le corps de la boucle
    ne peuvent pas être plus à gauche que la première ligne de la boucle.   
    """,
    )

add(name="for 2",
    required = ["for", "io:print"],
    question = """La réponse est le programme qui affiche&nbsp;:
    <pre>0 0
1 1
2 4
3 9
4 16
5 25
6 36
7 49
8 64
9 81</pre>
Vous utiliserez <tt>i</tt> comme indice de boucle.""",
    nr_lines = 3,
    tests = (
        Good(P(Equal('for i in range(10):\n   print(i, i*i)'))),
        expects(('for', ' i ', ' in ', 'range', 'range(10)', ':', 'print')),
        Expect('*', """Pour calculer le carré de <tt>i</tt> vous devez
        utiliser une multiplication"""),
        expects(('(', ')', ','),
                """Pour afficher <tt>i</tt> et son carré, vous devez utiliser
                la fonction <tt>print</tt> (n'oubliez pas les parenthèses)
                avec deux arguments qui sont <tt>i</tt> et <tt>i*i</tt>.
                (n'oubliez pas la virgule entre les deux arguments."""),
        ),
    good_answer = """Quand il n'y a qu'une seule instruction dans le corps
    de la boucle, on peut tout mettre sur une seule ligne&nbsp;:
    <pre>for i in range(10): print(i, i*i)</pre>
    Mais ceci n'est pas recommandé car c'est moins lisible.""",
    )

add(name="for 3",
    required = ["for 2"],
    question = """La réponse est le programme qui affiche&nbsp;:
    <pre>i= 0
i*i= 0
i= 1
i*i= 1
i= 2
i*i= 4
i= 3
i*i= 9
i= 4
i*i= 16</pre>
Vous utiliserez <tt>i</tt> comme indice de boucle.
<p>
Comme il y a 2 lignes à afficher pour chaque valeur prise par
la variable <tt>i</tt>, vous utiliserez deux fois la fonction <tt>print</tt>.
""",
    nr_lines = 4,
    tests = (
        Good(P(Equal('for i in range(5):\n   print("i=",i)\n   print("i*i=",i*i)'))),
        P(expects(('for', ' i ', ' in ', 'range', 'range(5)', ':', 'print',
                   'i=', 'i*i='))),
        Expect('*', """Pour calculer le carré de <tt>i</tt> vous devez
        utiliser une multiplication"""),
        expects(('(', ')', ','),
                "Où sont les paramètres des fonctions <tt>print</tt>&nbsp;?"),
        Bad(Comment(~NumberOfIs('print', 2),
                    """Vous devez <b>impérativement</b> utiliser <b>deux</b>
                    fois la fonction <tt>print</tt> pour cet exercice.""")),
        Bad(Comment(~NumberOfIs('"', 4),
                    """Vous devez afficher deux chaines de caractères
                    qui sont « i = » et « i*i= »,
                    il doit donc y avoir 4 guillemets dans votre réponse""")),
        Bad(Comment(~NumberOfIs('(', 3) | ~NumberOfIs(')', 3),
                    """Vous avez 3 appels de fonctions dans ce programme.
                    Il y en a un pour <tt>range</tt> et 2 pour <tt>print</tt>.
                    Il doit donc y avoir 3 parenthèses ouvrantes
                    et 3 parenthèses fermantes.""")),
        Bad(Comment(~NumberOfIs(',', 2),
                    """Il n'y a pas le bon nombre de virgules
                    dans votre réponse""")),
        ),
    good_answer = r"""On aurait pu faire un seul <tt>print</tt> :
    <pre>for i in range(5):
            print("i=", i, "\ni*i=", i*i)</pre>
    Comme en langage C, le <tt>\n</tt> indique qu'il faut passer
    à la ligne suivante.""",
    )


add(name="def",
    required = ["idem:incrémenter", "idem:multiplication", "idem:soustraction",
                "idem:division entière"],
    before = """Une fonction en Python calcule un résultat dépendant
    de ses paramètres. Voici un exemple de fonction&nbsp;:""" + python_html("""
    def modulo(a, b):
       quotient = a // b
       return a - b * quotient""") + """
   Cette fonction à deux paramètres et retourne un entier si on lui
   à passé deux entiers en paramètre. <tt>modulo(20, 7)</tt>
   affiche <tt>6</tt>
   <p>
   Il faut bien penser à ce qui est en rouge.
   <p>
   Les lignes qui sont dans la fonction ne peuvent pas être plus
   à gauche que la première ligne de la fonction.
   """,
    question = """La réponse à cette question est la définition de la fonction
   <tt>carre</tt> qui retourne le carré du nombre <tt>x</tt> passé en paramètre.
   """,
    tests = (
        Good(P(Equal('def carre(x):\n return x*x'))),
        Good(P(Equal('def carre(x):\n return x**2'))),
        expects(('def ', 'carre', 'x', 'return')),
        expects(('(', ')'),
                "Les paramètres de la fonction sont entre parenthèses"),
        Expect('*',
               """Pour calculer le carré, vous multipliez le nombre
   par lui-même"""),
        ),
    nr_lines = 3,
    good_answer = """Cette fonction <tt>carre</tt> va donner le bon
   résultat pour toutes les variables qui contiennent quelque chose
   qui peut être multiplié (entier, flottant, imaginaires...)""",
    )

add(name="if",
    required = ["idem:inférieur", "idem:égalité", "def"],
    before = "La syntaxe du « si » en Python est : " + python_html("""
    if condition:
       Les lignes de commande qui sont écrites ici
       sont exécutées si la condition est vérifiée.
       Ces lignes ne peuvent pas être à gauche de la première.
    else:
       Le bloc de « sinon » est optionnel.
       Ces lignes doivent être indentées sur
       la même colonne que le premier bloc."""),
   question = """Donnez la définition de la fonction <tt>signe</tt>,
   qui a comme paramètre <tt>a</tt> et qui retourne&nbsp;:
   <ul>
   <li> -1 si <tt>a</tt> est négatif
   <li> 0 s'il est nul.
   <li> 1 s'il est positif
   </ul>
   N'utilisez pas de <tt>else</tt> dans cette fonction, ce n'est
   pas la peine car il y a des <tt>return</tt>.
   <p>
   Retournez les valeurs dans l'ordre indiqués sinon votre
   réponse sera injustement refusée même si elle est correcte.
   """,
   nr_lines = 7,
   tests = (
   Good(P(Replace((('a<=-1', 'a<0'), ('return a', 'return 0'),
                 ),
                 Equal('def signe(a):\n if a<0:\n  return -1\n if a==0:\n  return 0\n return 1')))),
   expects(('def', 'signe', 'a', 'if', 'return', '0', '1', '-1', ':')),
   Bad(Comment(~NumberOfIs('if', 2),
       """Il faut deux « si » (pas un ni trois).
       Il y en a un pour savoir si c'est négatif et un pour savoir
        si c'est nul.
        Si un nombre n'est ni négatif, ni nul, on peut supposer
        qu'il est positif.""")),
        ),
   )

add(name="while",
    required = ["if", "idem:division", "idem:incrémenter", "idem:inégalité"],
    before = "La syntaxe du « while » en Python est : " + python_html("""
    while condition:
       Les lignes de commande qui sont écrites ici
       sont exécutées tant que la la condition est vérifiée."""),
    question = """Donnez la définition de la fonction <tt>log2</tt>,
    qui a comme paramètre <tt>a</tt> un entier et qui retourne
    le nombre de bits nécessaires pour écrire cet entier.
    <p>
    L'agorithme consiste à initialiser <tt>i</tt> à zéro,
    puis tant que <tt>a</tt> n'est pas nul,
    on le divise par 2 et on ajoute 1 à <tt>i</tt>
    """,
    nr_lines = 7,
    tests = (
        expects(('def', 'log2', 'while', 'return', 'a', '/', '2', '1', '0')),
        Good(P(Replace((('//', '/'),
                        ('a=a/2', 'a/=2'),
                        ('a!=0', 'a'),
                        ('i+=1;a/=2', 'a/=2;i+=1'),
                        ),
                       Equal("""def log2(a):
 i = 0
 while a:
    a /= 2
    i += 1
 return i""")
                       )
               )
             ),
        ),
    good_answer = """Contrairement au langage C, il n'y a PAS
    de <tt>do ... while(...)</tt> en langage Python.<p>
    <p>
    La boucle est très lente pour calculer le logarithme,
    Il est bien sûr plus rapide de faire&nbsp;:""" + python_html("""
    import math
    log_de_2 = math.log(2)
    def log2(a):
       return math.log(a) / log_de_2"""),
    )
