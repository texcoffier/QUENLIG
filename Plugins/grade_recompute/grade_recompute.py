#!/usr/bin/env python
# -*- coding: latin-1 -*-
#    QUENLIG: Questionnaire en ligne (Online interactive tutorial)
#    Copyright (C) 2013 Thierry EXCOFFIER, Universite Claude Bernard
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

"""

"""

acls = { 'Author': ('executable',),  }
container = 'analyse'
priority_execute = '-question_answer'
link_to_self = True
css_attributes = (
    "A { color: red }",
    )

import statistics
import questions

def execute(state, plugin, argument):
    if not argument:
        return ''

    stats = statistics.question_stats()

    me = state.student
    for s in stats.all_students:
        for a in s.answers.values():
            if a.answered and a.question in questions.questions:
                state.student = s
                state.question = questions.questions[a.question]
                s.check_answer(a.answered, state)
    state.student = me
    state.question = None
    plugin.heart_content = '<p class="grade_recompute"></p>'
    return ''
