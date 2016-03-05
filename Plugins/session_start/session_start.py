#!/usr/bin/env python3
# -*- coding: latin-1 -*-
#    QUENLIG: Questionnaire en ligne (Online interactive tutorial)
#    Copyright (C) 2007-2012 Thierry EXCOFFIER, Universite Claude Bernard
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

"""It rejects any work before the session start."""

from QUENLIG import utilities
import time

font_size = "70%"
container = 'identity'
color = "#999"
acls = { 'Student': ('executable',) }
priority_execute = "-question_answer"

date_format = "%H:%M %d/%m/%Y"

def parse_date(value, student, default):
    value = value.strip().replace('\n', ' ').replace('\r',' ')
    if value.startswith('{'):
        value = eval(value)
    else:
        value = {"": value}

    value = value.get(student, value.get("", default)).strip()
    return time.mktime(time.strptime(value, date_format) )

def option_set(plugin, value):
    plugin.state.start_date = parse_date(value, plugin.state.student.filename,
                                         option_default )

option_name = 'begin-date'
option_help = '''"HH:MM DD/MM/YYYY"
        Set the examination start date.
	The value can be a Python dictionnary with student id as keys,
	the default value is defined by the empty ("") key.'''
option_default = "09:00 1/1/2005" 


def execute(state, plugin, argument):
    state.session_start_ok = state.start > state.start_date
    if not state.session_start_ok:
        state.question = None
        plugin.heart_content = '<p class="session_not_started"></p>'
        return utilities.user_date(state.start_date)
