#!/usr/bin/env python3
# -*- coding: latin-1 -*-
#    QUENLIG: Questionnaire en ligne (Online interactive tutorial)
#    Copyright (C) 2007-2014 Thierry EXCOFFIER, Universite Claude Bernard
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

"""displays all the comments about all the questions."""

from QUENLIG import utilities
from QUENLIG import statistics
from QUENLIG import questions
import cgi

container = 'analyse'
link_to_self = True
priority_execute = '-question_source'
acls = { 'Author': ('executable',), 'Grader': ('executable',) }

def execute(state, plugin, argument):
    if argument == None:
        return ''

    stats = statistics.question_stats()
    
    comments = []
    for s in stats.all_students:
        for a in s.answers.values():
            q = questions.a_href(a.question).replace(' ','&nbsp;')
            for c in a.comments:
                comments.append( [
                    q,
                    cgi.escape(c[1]),
                    s.a_href(body=c[1]),
                    utilities.date_format(c[0]).replace(' ','&nbsp;')])


    plugin.heart_content = \
             utilities.sortable_table(plugin.sort_column,
                                      comments,
                                      url = "%s&%s=1" % (plugin.plugin.css_name, plugin.plugin.css_name)
                                      )
    state.question = None

    return ''

