#!/usr/bin/env python3
# -*- coding: latin-1 -*-
#    QUENLIG: Questionnaire en ligne (Online interactive tutorial)
#    Copyright (C) 2010-2014 Thierry EXCOFFIER, Universite Claude Bernard
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

"""Display the questions and answers of any student.
This plugin link is not visible on the web page.
To use it, you must click on a student name on the student statistics page.
"""

import Plugins.answered.answered
from QUENLIG import student

prototype = 'answered' # Same plugin
priority_execute = '-question_answer'
acls = { 'Teacher': ('executable',), 'Grader': ('executable',),
         'Admin': ('executable',), 'Author': ('executable',)}
link_to_self = False

def execute(state, plugin, argument):
    if argument not in student.students:
        return

    for dummy in state.steal_identity([student.students[argument]]):
        saved_role = state.current_role
        try:
            Plugins.answered.answered.execute(state, plugin, argument)
        finally:
            state.current_role = saved_role
    
