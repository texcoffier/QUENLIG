# -*- coding: utf-8 -*-
#    QUENLIG: Questionnaire en ligne (Online interactive tutorial)
#    Copyright (C) 2020 Thierry EXCOFFIER, Universite Claude Bernard
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
#    Contact: Thierry.EXCOFFIER@univ-lyon1.fr
#
"""
Check ORing requireds
"""
from QUENLIG.questions import *

add(name="Q1",
    required=["a:a(unlockC)"],
    question="Q1",
    tests=(Good(),),
    )

add(name="Q2.1",
    required=["Q1(answer1)"],
    question="Q2.1",
    tests=(Good(),),
    )

add(name="Q2.2",
    required=["Q1(answer2)"],
    question="Q2.2",
    tests=(Good(),),
    )

add(name="Q3",
    required=["Q2.1{hide}{|}Q2.2"],
    question="Q3",
    tests=(Good(),),
    )