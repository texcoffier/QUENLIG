#!/usr/bin/env python
# -*- coding: latin-1 -*-
#    QUENLIG: Questionnaire en ligne (Online interactive tutorial)
#    Copyright (C) 2010 Thierry EXCOFFIER, Universite Claude Bernard
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

import questions
import statistics

priority_execute = '-question_before'

container = 'action'

link_to_self = True

acls = { 'Teacher': ('executable',) }

def execute(state, plugin, argument):
    if state.question is None:
        return
    if argument:
        # Remove old questions
        module_name = state.question.world
        q = {}
        for i in questions.questions.values():
            if i.world != module_name:
                q[i.name] = i
        questions.questions = q
        questions.previous_question = ""
        # Reload !
        reload(questions.modules[module_name])
        state.question = questions.questions[state.question.name]
        statistics.forget_stats()
        state.student.answerables_cache = None
        questions.sort_questions()

    return ''


