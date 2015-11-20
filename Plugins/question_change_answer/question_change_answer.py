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

container = 'top'
priority_execute = '-question_answer'
acls = { 'Teacher': ('executable',), 'Grader': ('executable',),
         'Author': ('executable',) }

import time
import configuration

option_name = 'change-allowed-timeout'
option_help = '''"integer"
        Define the time in seconds allowed to modify an answer
        once it has be accepted.
        The plugin 'question_change_answer' must be activated.'''
option_default = "3600"
change_allowed_timeout = 3600

def option_set(dummy_plugin, value):
    global change_allowed_timeout
    change_allowed_timeout = int(value)

def allowed_to_change_answer(state):
    if not state.plugins_dict['question_change_answer'].current_acls['executable']:
        return False
    if state.question is None:
        return False
    if state.current_role in acls:
        return True # At any time
    if 'question_answer' in state.form:
        return False
    t = state.student.answer(state.question.name).answer_times[-1]
    if time.time() - t < change_allowed_timeout:
        return True

configuration.allowed_to_change_answer = allowed_to_change_answer

# def execute(state, dummy_plugin, dummy_argument):
#    pass

def add_a_link(state, question):
    """This function is called by 'answered' plugin."""
    if not configuration.allowed_to_change_answer(state):
        return '' # Not the right to reanswer
    if not state.student.answered_question(question.name):
        return '' # Not yet answered
    if (time.time() - state.student.answer(question.name).answer_times[-1]
        > change_allowed_timeout):
        return '' # Too late to change the answer
    return  '<A HREF="%s" CLASS="question_change_answer"></A>' % (
               question.url(),
               )
