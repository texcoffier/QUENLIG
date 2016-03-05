# -*- coding: latin-1 -*-
#    QUENLIG: Questionnaire en ligne (Online interactive tutorial)
#    Copyright (C) 2011 Thierry EXCOFFIER, Universite Claude Bernard
#
#    This program is free software; you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation; either version 2 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program; if not, write to the Free Software
#    Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
#
#    Contact: Thierry.EXCOFFIER@bat710.univ-lyon1.fr
#

from QUENLIG.questions import *
from .check import C

add(name = "entier",
    required = ['variable:casse variable'],
    question = """Quelle ligne tapez-vous pour déclarer un nombre
    entier signé nommé <tt>i</tt>&nbsp;?""",
    tests = (
        Good(C(Equal('int i'))),
        ),
    )

add(name = "deux entiers",
    required = ["entier"],
    question = """Quelle ligne tapez-vous pour déclarer les nombres
    entiers signés nommés <tt>i</tt> et <tt>j</tt>&nbsp;?""",
    tests = (
        Good(C(Equal('int i,j'))),
        Bad(C(Comment(Equal('int j,i'),
                      "Il faut déclarer <tt>i</tt> puis <tt>j</tt>"))),
        ),
    )

add(name = "flottant",
    required = ["entier"],
    question = """Quelle ligne tapez-vous pour déclarer
    un nombre flottant nommé <tt>f</tt>&nbsp;?""",
    tests = (
        Good(C(Equal('float f'))),
        ),
    )

add(name = "entier flottant",
    required = ["entier", "flottant"],
    question = """Qu'écrivez-vous pour déclarer
    un nombre flottant nommé <tt>x</tt> puis un nombre entier
    nommée <tt>n</tt>&nbsp;?""",
    nr_lines = 2,
    tests = (
        Good(C(Equal('float x;int n'))),
        ),
    )

add(name = "struct",
    required = ["entier flottant"],
    question = """Qu'écrivez-vous pour déclarer
    une structure nommée <tt>ef</tt> contenant :
    <ul>
    <li> un champ nommé <tt>x</tt> contenant un nombre flottant
    <li> un champ nommé <tt>n</tt> contenant un nombre entier
    </ul>""",
    nr_lines = 5,
    tests = (
        Good(C(Equal('struct ef{float x;int n;}'))),
        ),
    )

add(name = "table",
    required = ["entier"],
    question = """Qu'écrivez-vous pour déclarer
    un tableau nommé <tt>t</tt> contenant 4 entiers&nbsp;?""",
    tests = (
        Good(C(Equal('int t[4]'))),
        ),
    )
