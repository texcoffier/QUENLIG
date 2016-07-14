#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#    QUENLIG: Questionnaire en ligne (Online interactive tutorial)
#    Copyright (C) 2016 Thierry EXCOFFIER, Universite Claude Bernard
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

"""Add the REDO button after the student answer."""

priority_execute = '-question_answer'
priority_display = 'question_answer'
acls = {}

def execute(state, plugin, argument):
    if state.question == None:
        return
    if state.question.tests == ():
        return
    if not state.student.answer(state.question.name).answered:
        return
    if state.question.get_nr_versions() <= 1:
        return
    if state.form.get('erase', False):
        return
    return '''<button onclick="window.location+='&erase=1'"><var></var></button>'''


    




    

