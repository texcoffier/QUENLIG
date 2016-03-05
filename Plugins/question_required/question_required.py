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

"""Display the informations about the required questions."""

from QUENLIG import utilities
from QUENLIG import questions

priority_display = 'question_indices'
priority_execute = 'question_answer' # We need to know if the answer was answered
acls = { 'Default': ('executable',) }

css_attributes = (
    "/DIV.an_answer { }",
    ".answer { background: #FFF ; margin-bottom: 1em; border-bottom: 1px solid black}",
    ".course { opacity:0.3 ; width: 50% }"
    "DIV.question_required .course:hover { opacity:1 }"
    )

def execute(state, dummy_plugin, dummy_argument):
    if state.question == None:
        return
    if state.student.answered_question(state.question.name):
        return
        
    s = []
    for p in state.question.required:
        if p.hidden:
            continue
        if p.hide:
            return
        q = questions.questions[p.name]
        question = q.question(state)
        try:
            answer = utilities.answer_format(
                state.student.answers[p.name].answered,
                question=question)
        except (KeyError, AttributeError):
            answer = ''
        question = question.split("{{{")[0]
        answer = '<div class="answer">' + answer + '</div>'
        if (q.courses  or  p.before) and q.before:
            before = q.before(state)
        else:
            before = ""
        if before and question:
            s.append('<table><tr><td width="50%">')
            s.append(question)
            s.append('<td class="course">' + before + "</tr></table>")
            s.append(answer)
        else:
            s.append(before + question +  answer)
    if s:
        return ''.join(s)





