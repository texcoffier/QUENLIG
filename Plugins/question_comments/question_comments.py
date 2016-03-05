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

"""Displays all the comments about the current question."""

from QUENLIG import utilities
from QUENLIG import statistics
import cgi

priority_display = 'question_required'
sort_column = 3
acls = { 'Teacher': ('executable',), 'Author': ('executable',),
         'Grader': ('executable',) }

def execute(state, plugin, argument):
    if state.question == None:
        return

    stats = statistics.question_stats()
    
    comments = []
    for s in stats.all_students:
        for a in s.answers.values():
            if a.question != state.question.name:
                continue
            for c in a.comments:
                comments.append( [cgi.escape(c[1]),
                                  s.mailto(body=str(a.question) + "  " + c[1]),
                                  utilities.date_format(c[0])])

    if len(comments) == 0:
        return None
    return utilities.sortable_table(plugin.sort_column, comments,
                                    url=plugin.plugin.css_name
                                    )






