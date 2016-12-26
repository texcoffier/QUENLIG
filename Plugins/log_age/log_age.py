#!/usr/bin/env python3
# -*- coding: latin-1 -*-
#    QUENLIG: Questionnaire en ligne (Online interactive tutorial)
#    Copyright (C) 2016 Thierry EXCOFFIER, Universite Claude Bernard
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

"""Destroy all the students with 0 or 1 good answer."""

from QUENLIG import configuration
from QUENLIG import student

container = 'action'
link_to_self = True
priority_execute = 'competences' # Need configuration.erasable_after


acls = { 'Admin': ('executable',), 'Grader': ('executable',) }

def option_set(plugin, value):
    configuration.log_age = float(value)
    # student.students = {} # Not possible because it breaks many things
    student.all_students()

option_name = 'log_age'
option_help = '''"#days"
        Students who have not worked the last #days are not loaded
        on startup and so not used to compute statistics or export grades.'''
option_default = "365"

def execute(state, plugin, argument):
    if not argument:
        return ''
    save = configuration.log_age
    option_set(plugin, "9999")
    configuration.log_age = save
    return ''














