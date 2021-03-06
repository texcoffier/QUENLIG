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

"""This plugin display a box with the information about the bad answer."""

priority_display = 'question_answer'
priority_execute = 'question_answer'
background = '#FCC'
title_background = '#F88'
acls = { 'Default': ('executable',) }

def execute(state, plugin, argument):
    if state.question == None:
        return
    if state.question.tests == ():
        return
    if state.student.answered_question(state.question.name):
        return
    
    s = state.student.last_answer(state.question.name)
    if not s:
        return

    dummy_number, message = state.student.check_answer(s, state)

    if state.question.bad_answer:
        if message:
            message += '<hr>'
        message += state.question.bad_answer

    return message
