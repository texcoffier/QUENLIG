#!/usr/bin/env python
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

"""This plugin add links in the 'work done' page in order to
allow students to change an old good answer
"""

container = 'page'
priority_execute = '-question_answer'
acls = { 'Teacher': ('executable',) }

import time

change_allowed_timeout = 3600

def execute(state, plugin, argument):

    state.student.allowed_to_change_answer = True
    if state.student.current_role == 'Teacher':
        state.student.allowed_to_change_answer = True
        return ''
    if state.question is None:
        return ''
    t = state.student.answer(state.question.name).last_time
    if 'question_answer' in state.form:
        return ''        
    if time.time() - t < change_allowed_timeout:
        state.student.allowed_to_change_answer = True

    return ''

def add_a_link(state, question):
    if not hasattr(state.student, 'allowed_to_change_answer'):
        return '' # Not the right to reanswer
    if not state.student.answered_question(question.name):
        return '' # Not yet answered
    if (time.time() - state.student.answer(question.name).last_time
        > change_allowed_timeout):
        return '' # Too late to change the answer
    return  '<A HREF="%s" CLASS="question_change_answer"></A>' % (
               question.url(),
               )
