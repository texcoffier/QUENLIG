#!/usr/bin/env python3
# -*- coding: latin-1 -*-
#    QUENLIG: Questionnaire en ligne (Online interactive tutorial)
#    Copyright (C) 2008 Thierry EXCOFFIER, Universite Claude Bernard
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

"""Display all the questions definition."""

from QUENLIG import statistics
from QUENLIG import questions

container = 'action'
link_to_self = True
priority_execute = '-question_source'
acls = { 'Teacher': ('executable',), 'Author': ('executable',) }
css_attributes = ('TABLE { border: 1px solid black ; }',
                  )

def execute(state, plugin, argument):
    if argument:    
        s = []
        for question in sorted(list(questions.questions.values()),
                               key=lambda q: q.name):
            state.question = question
            state.student.init_seed(question.name)
            s.append('<strong>' + question.name + '</strong>')
            if question.maximum_time:
                s.append(' maximum_time:%d' % question.maximum_time)
            if question.maximum_bad_answer:
                s.append(' maximum_bad_answer:%d'%question.maximum_bad_answer)
            
            s.append('<br>' + question.question(state))
            s.append('<table class="information_table" style="clear:right">')
            for t in question.tests:
                s.append(t.html(state=state))
            s.append('</table><hr>')

        plugin.heart_content = '\n'.join(s)
        state.question = None
    return ''

