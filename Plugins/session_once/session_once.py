#!/usr/bin/env python3
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

"""If 15% of the questions are answered
and there is 4 hours without answers.
Then no more answers are allowed.
The student may see there answers.
"""

import time
from QUENLIG import questions

percent = 0.15
timeout = 4*3600

priority_execute = "-question_answer"
container = 'identity'
acls = { }

def execute(state, dummy_plugin, dummy_argument):
    if state.student.number_of_good_answers()<len(questions.questions)*percent:
        return
    if time.time() - state.student.time_last() < timeout:
        return
    state.question = None
    for p in ('question', 'questions', 'questions_shuffle', 'question_answer'):
        state.plugins_dict[p].current_acls.update(['!executable'])
    return '<p class="session_stopped"></p>'
        

