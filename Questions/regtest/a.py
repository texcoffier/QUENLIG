# -*- coding: latin-1 -*-
#    QUENLIG: Questionnaire en ligne (Online interactive tutorial)
#    Copyright (C) 2005-2011 Thierry EXCOFFIER, Universite Claude Bernard
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

add(name="a",
    question="question_a",
    tests=(
    good("a", "good_answer__a"),
    Good(Equal("unlockCHOICES")),
    bad("a0", "bad_answer__a0"),
    bad("a1", "bad_a1"),
    bad(("a2", "a3"), "bad_a3"),
    ),
    bad_answer = "bad_answer_comment",
    good_answer = "good_answer_comment",
    indices=("Indice X", "Indice Y"),
    )

add(name="b",
    question="question_b",
    tests=(
    good("b", 'good_b'),
    good(("B", 'xbx')),
    ),
    indices=("Indice A", "Indice B"),
    )

add(name="c",
    required = ['a'],
    question="question_c",
    tests=(
    good("c"),
    ),
    bad_answer = "bad_c",
    good_answer = "good_c",
    )
