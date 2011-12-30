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

"""Top level plugin. It defines the 3 columns of the page:
the left menu, the heart of the page and the administrator menu.
"""

css_attributes = (
    "> DIV > TABLE { width: 100% ; }",
    )
priority_execute = -10 # Before the other
horizontal = True
acls = { 'Default': ('executable',) }

def execute(state, plugin, argument):
    if state.question:
        if state.question not in state.student.answerables():
            if not hasattr(state.student, 'allowed_to_change_answer'):
                state.question = None

    return ''
