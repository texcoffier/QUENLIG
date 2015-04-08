#!/usr/bin/env python
# -*- coding: latin-1 -*-
#    QUENLIG: Questionnaire en ligne (Online interactive tutorial)
#    Copyright (C) 2007,2014 Thierry EXCOFFIER, Universite Claude Bernard
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

"""Display all the questions and answer given by the connected student."""

container = 'action'
link_to_self = True
priority_execute = "-question_before"
acls = { 'Default': ('executable',), 'Admin': ('!executable',) }

css_attributes = (
#    'TABLE        { border: 1px solid black ; }',
    'TABLE.good_answer .an_answer { background: #DFD ; }',
    'TABLE.bad_answer  .an_answer { background: #FDD ; }',
    '.comment     { background: #DDD ; }',
    'TT.an_answer, PRE.an_answer { font-weight: bold ; }',
    )

def execute(state, plugin, argument):
    if argument and state.student:
        if argument != '1':
            mail = state.student.informations.get('mail')
            if mail:
                argument += ' <small><a href="mailto:%s">%s</a></small>' % (
                    mail, mail)
            s = '<h2 class="answered_by">%s</h2>' % argument
        else:
            s = ''
        plugin.heart_content = s + state.student.answered_page(state)
        state.question = None
    return ''

