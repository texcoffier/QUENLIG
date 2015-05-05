#!/usr/bin/env python
# -*- coding: latin-1 -*-
#    QUENLIG: Questionnaire en ligne (Online interactive tutorial)
#    Copyright (C) 2007,2012 Thierry EXCOFFIER, Universite Claude Bernard
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

"""Display the student work time."""

import utilities

priority_display = 'statmenu_nr_questions'
priority_execute = 'question_answer' # Verify answer before
priority_execute = '-question' # Check before displaying question
acls = { 'Student': ('executable',) }

option_name = 'max-thinking-time'
option_help = """"{'':60, 'student1': 90}"
        A Python dictionnary with the maximum number of minutes
 	of work time per student. The key is the student ID.
	The '' key indicates the default time."""
option_default = "{'':100*60, 'guest_john_doe': 60}"
def option_set(plugin, value):
    value = eval(value)
    plugin.max_time = value.get(plugin.state.student.filename,
                                value.get('', 999999))


def execute(state, plugin, argument):
    t = state.student.time_after() + state.student.time_searching()
    if t > plugin.max_time*60:
        state.session_stop_ok = False
        state.question = None
        plugin.heart_content = '<p class="no_more_time"></p>'
    
    return utilities.time_format(int(t))

