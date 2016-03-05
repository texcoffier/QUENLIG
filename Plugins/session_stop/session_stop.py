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

"""It rejects any work after the session stop."""

from QUENLIG import utilities
import Plugins.session_start.session_start

priority_display = 'session_start'
priority_execute = "-question_answer"
acls = { 'Student': ('executable',) }
font_size = "70%"
color = "#999"

def option_set(plugin, value):
    plugin.state.stop_date = Plugins.session_start.session_start.parse_date(
        value, plugin.state.student.filename, option_default )

option_name = 'end-date'
option_help = '''"HH:MM DD/MM/YYYY"
        Set the examination termination date.'''
option_default = "19:00 1/1/2035" 

def execute(state, plugin, argument):
    state.session_stop_ok = state.start < state.stop_date
    if not state.session_stop_ok:
        state.question = None
        plugin.heart_content = '<p class="session_stopped"></p>'
        return utilities.user_date(state.stop_date)

