#!/usr/bin/env python3
# -*- coding: latin-1 -*-
#    QUENLIG: Questionnaire en ligne (Online interactive tutorial)
#    Copyright (C) 2007 Thierry EXCOFFIER, Universite Claude Bernard
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

"""Display the question text."""

priority_display = 'question_before'
acls = { 'Default': ('executable',) }

def option_set(plugin, value):
    from QUENLIG import configuration
    import ast
    (configuration.nr_bad_answers_allowed,
     configuration.multiply_time,
     configuration.max_suspended_time) = ast.literal_eval(value)

option_name = 'suspend'
option_help = '''"(nr_bad_answers, multiply, max_suspend)"
        After 'nr_bad_answers': the student must wait 1 minute
        before answering again.
        After each new bad answer, the wait time is multiplied by 'multiply'.
        The maximum wait time is 'max_suspend' minutes.'''
option_default = "(5, 2, 60)"

def execute(state, dummy_plugin, dummy_argument):
    q = state.question

    if q == None:
        return
    if state.yes_it_is_good:
        return None

    state.student.tell_question(q.name)

    return '<p>' + q.get_question(state).split('{{{')[0]






    

