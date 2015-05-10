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

"""Display the informations about the required questions."""

import cgi
import questions

priority_display = 'question_indices'
priority_execute = 'question_answer' # We need to know if the answer was answered
acls = { 'Default': ('executable',) }

css_attributes = (
    "/DIV.answeruser { white-space: pre; margin-left: 2em; background: #FFE; overflow:auto }",
    ".answer { font-weight: bold ; }",
    )

def execute(state, plugin, argument):
    if state.question == None:
        return    
    if state.student.answered_question(state.question.name):
        return
        
    s = []
    for p in state.question.required.names(only_visible=True):
        s.append( questions.questions[p].question(state).split("{{{")[0] )
        try:
            s[-1] += '<br><span class="answer"></span><div class="answeruser">%s</div>' % \
                     cgi.escape(state.student.answers[p].answered.strip())
                     
        except (KeyError, AttributeError):
            pass
    if s:
        return '<hr>'.join(s)





