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
    before = """En Python on ajoute pas des choux et des carottes.
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
    Si <tt>b=76</tt> alors <tt>a</tt> contiendra <tt>(76)</tt>""",

    tests = (
        Good(P(Equal('a="("+str(b)+")"'))),
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
    chaine de caractère mais en sans les espaces qui sont au début
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
