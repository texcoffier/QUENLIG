#!/usr/bin/env python
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

import utilities

priority_display = 'question_good'
priority_execute = 'question_answer' # We need to know if the answer was answered
boxed = True
acls = { 'Default': ('executable',) }

def execute(state, plugin, argument):
    if state.question == None:
        return

    if len(state.question.indices) == 0:
        return

    if state.student.answered_question(state.question.name):
        # No indices if the question is yet answered
        return

    if argument:
        state.student.tell_indice(state.question.name, int(argument))

    indice = state.student.get_indice(state.question.name) + 1
    indice = min(indice, len(state.question.indices))
    s = ""
    if indice > 0:
        indices = [ ind for ind in state.question.indices[:indice] ]
        s += utilities.list_format(indices)
    if indice < len(state.question.indices):
        if indice == 0:
            html_class = 'first_indice'
        else:
            html_class = 'next_indice'
        s += '<A CLASS="%s" HREF="?%s=%d"></A>'% (html_class,
                                                  plugin.plugin.css_name,
                                                  indice+1)
    return s


    




    

