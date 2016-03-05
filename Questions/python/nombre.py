# -*- coding: latin-1 -*-
#    QUENLIG: Questionnaire en ligne (Online interactive tutorial)
#    Copyright (C) 2005-2006 Thierry EXCOFFIER, Universite Claude Bernard
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

from QUENLIG.questions import *
from .check import *

add(name='nombre',
    required=['texte:un chat'],
    before="""Le Python comprend les nombres comme tu les écris habituellement,
    mais attention si tu met des apostrophes autour du nombre pour
    lui cela ne sera pas un nombre.
    <p>
    <em>1+1 donne 2, mais '1'+'1' donne '11'</em>
    """,
    question="""Fais écrire <em>18</em> à Python""",
    tests=(
    print_required,
    require("18",
            """Tu veux qu'il écrive <em>18</em>,
            il faut donc que tu lui dises d'écrire <em>18</em>."""),
    space_required,
    apostrophe_rejected,
    python_answer_good('18\n'),
    ),
    )

before_operation = """Le Python sait faire les 4 opérations sur les entiers.
Il suffit d'écrire ce que tu veux lui faire calculer et il le fait."""

add(name='addition',
    required=['nombre:nombre'],
    before=before_operation,
    question="""Fais afficher à Python le résultat de l'opération 2 + 3,
    c'est lui qui doit faire le calcul, pas toi.""",
    tests=(
    print_required,
    space_required,
    apostrophe_rejected,
    plus_required,
    require(('2', '3'),
            """Comment lui faire calculer 2 + 3 si dans la phrase que
            tu lui dis il n'y a pas 2 et 3&nbsp;?"""),
    python_answer_good('5\n'),
    ),
    )

add(name='addition énorme',
    required=['nombre:addition'],
    question="""Fais écrire à Python le résultat de l'addition
    de 123456789 et 987654321""",
    tests=(
    print_required,
    space_required,
    apostrophe_rejected,
    plus_required,
    python_answer_good('1111111110\n'),
    ),
    )

add(name='addition multiple',
    required=['nombre:addition'],
    question="Fais écrire à Python le résultat de l'addition de 1 et 2 et 3",
    tests=(
    print_required,
    space_required,
    plus_required,
    apostrophe_rejected,
    python_answer_good('6\n'),
    ),
    indices=(
    "Tu dois lui faire écrire le résultat de 1 + 2 + 3",
    ),
    )

add(name='soustraction',
    required=['nombre:nombre'],
    before=before_operation,
    question="""Fais écrire à Python le résultat de l'opération 3 - 2""",
    tests=(
    print_required,
    space_required,
    apostrophe_rejected,
    require(('-', '2', '3'),
            """Comment lui faire calculer 3 - 2 si dans la phrase que
            tu lui dis il n'y a pas 3 et - et 2&nbsp;?"""),
    python_answer_good('1\n'),
    ),
    )

add(name='soustraction énorme',
    required=['nombre:soustraction'],
    before="""J'ai un sac de 1000 bonbons, j'en donne 1.
    Combien m'en reste-t-il&nbsp;?
    """,
    question="""Fais afficher à Python le résultat de la soustraction
    1000 moins 1.""",
    tests=(
    print_required,
    space_required,
    apostrophe_rejected,
    require(('-', '1000', '1'),
            """Comment lui faire calculer 1000 - 1 si dans la phrase que
            tu lui dis il n'y a pas 1000 et - et 1&nbsp;?"""),
    python_answer_good('999\n'),
    ),
    )

add(name='multiplication',
    required=['nombre:nombre'],
    before=before_operation,
    question="""Fais écrire à Python le résultat de l'opération 2 * 3""",
    tests=(
    print_required,
    space_required,
    apostrophe_rejected,
    require(('*', '2', '3'),
            """Comment lui faire calculer 3 * 2 si dans la phrase que
            tu lui dis il n'y a pas 3 et * et 2&nbsp;?"""),
    python_answer_good('6\n'),
    ),
    )

