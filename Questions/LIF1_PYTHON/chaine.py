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
Tout sur les chaines de caractères
"""

from questions import *
from check import *

add(name="conversion",
    required = ["table:chaine", "idem:flottant", "idem:chaine",
                "idem:affectation"],
    before = """En Python on n'ajoute pas des choux et des carottes.
    Il faut que ce que l'on ajoute soit un minimum compatible,
    par exemple un entier et un nombre flottant.
    On ne peut pas ajouter une chaine de caractères et un nombre.
    <p>
    Pour convertir quelque chose en une chaine de caractères,
    il suffit d'utiliser la fonction <tt>str</tt> retourne une chaine
    de caractères calculée à partir de son unique paramètre
    (qui n'est pas modifié).""",
    question="""Stockez dans la variable <tt>a</tt> l'entier désigné
    par la variable <tt>b</tt> entre parenthèses.
    <p>
    Si <tt>b=76</tt> alors <tt>a</tt> contiendra la chaine de caractères
    <tt>(76)</tt>""",

    tests = (
        Good(P(Equal('a="("+str(b)+")"'))),
        Bad(Comment(Contain('76'),
                    """La valeur 76 était un exemple, il faut que cela
                    fonctionne pour toutes les valeurs de <tt>b</tt>""")),
        Bad(Comment(P(Equal('a=(b)')),
                    """Ici les parenthèses n'ont aucun effet,
                    c'est comme si vous aviez écrit <tt>a=b</tt>""")),
        Bad(Comment(P(Equal('a="("+b+")"')),
                    """Python ne va pas vouloir ajouter une chaine
                    de caractère et un entier.""")),
        Expect("str", """Vous devez utiliser la fonction <tt>str</tt>
        pour traduire <tt>b</tt> en chaine de caractères"""),
        Expect('+', """Vous avez besoin de concaténer les chaines de
        caractère contenant <tt>(</tt>, la valeur de <tt>b</tt> en chaine
        de caractère ainsi que <tt>)</tt>.
        Pour concaténer les chaines vous avez besoin de l'opérateur <tt>+</tt>.
        """),
        Bad(Comment(~NumberOfIs('"',4),
                    """Vous avez besoin d'indiquer une chaine de caractères
                    contenant <tt>(</tt> et une contenant <tt>)</tt>
                    vous avez donc besoin d'écrire 4 guillemets.""")),
        expects(("a", "=", "b", "(", ")", '"("', '")"')),
        ),

    good_answer = """Bien évidemment, si vous passez une chaine
    de caractères en paramètre de la fonction <tt>str</tt> cette
    chaine sera retournée inchangée.""",
    )

add(name="strip",
    required = ["idem:chaine", "structure:attributs"],
    before = """Toutes les chaines de caractères ont un attribut
    nommé <tt>strip</tt> qui est une fonction qui retourne la même
    chaine de caractère mais sans les espaces qui sont au début
    et à la fin de la chaine.
    <p>
    Si <tt>a</tt> contient <tt>" x "</tt> alors <tt>a.strip()</tt> est
    la chaine de caractère <tt>"x"</tt>.
    <p>
    <tt>" a  b  c    ".strip()</tt> retourne <tt>"a  b  c"</tt>
    en laissant les espaces à l'intérieur.
    """,
    question = """Si <tt>a</tt> est une chaine de caractère quelconque,
    quelle est la valeur de l'expression suivante&nbsp;:
    <tt>a.strip() == a.strip().strip()</tt>""",
    tests = (
        Good(Equal("True")),
        Bad(Comment(UpperCase(Equal("True")),
                    """Attention les minuscules et les majuscules sont
                    différentes.""")),
        ),
    good_answer = """La fonction <tt>strip</tt> est fondamentale dès que
    l'on pose des questions à un utilisateur.
    Il a en effet toujours la tendance à mettre des espaces en trop en début
    et fin de saisie""",
    )

add(name="entier",
    required = ["io:lire ligne", "conversion"],
    before = """Pour convertir quelque chose en entier,
    on utilise la fonction <tt>int</tt>.
    Elle prend un paramètre de type quelconque et retourne,
    si c'est possible, l'entier correspondant.
    <p>
    <tt>int(5.4)</tt> donne l'entier <tt>5</tt><br>
    <tt>int(5)</tt> donne l'entier <tt>5</tt><br>
    <tt>int("5")</tt> donne l'entier <tt>5</tt>
    """,
    question = """Écrivez la fonction <tt>lire_entier</tt>
    qui lit une ligne au clavier et retourne un entier.
    <p>
    Ce n'est pas la peine d'indiquer le <tt>import sys</tt>
    """,
    nr_lines = 3,
    tests = (
        Good(P(Equal("def lire_entier():\n return int(sys.stdin.readline())"))),
        expects(('def', 'lire_entier', ':', 'return', 'sys', 'stdin',
                 'readline', 'int', '.')),
        Bad(Comment(~NumberOfIs('(',3) | ~NumberOfIs(')',3),
                    """Dans votre réponse il y a un appel à la fonction
                    <tt>readline</tt>, un appel à <tt>int</tt> et la
                    déclaration des paramètres de <tt>lire_entier</tt>.
                    Il doit donc y avoir 3 fois <tt>()</tt> dans votre réponse.
                    """)),
        Bad(Comment(~NumberOfIs('.',2),
                    """Dans <tt>sys.stdin.readline</tt> il y a deux fois
                    le caractère '<tt>.</tt>'
                    <p>
                    Il doit donc y avoir 2 '<tt>.</tt>' dans votre
                    réponse""")),
        ),
    good_answer = """Avec cette fonction on ne peut pas taper deux
    entiers sur la même ligne...""",
    )
        


