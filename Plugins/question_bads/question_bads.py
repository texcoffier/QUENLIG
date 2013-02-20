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

"""Displays all the bad answers given for a question."""

import utilities
import statistics
import questions

priority_display = 'question_comments'
acls = { 'Author': ('executable',) }
css_attributes = (
    "SPAN.uncommented { background: #FAA; }",
    "SPAN.uncommented PRE { background-color: #FAA ; }",
    )

def execute(state, plugin, argument):
    if state.question == None:
        return

    stats = statistics.question_stats()
    
    ba = []
    for s in stats.all_students:
        for a in s.answers.values():
            if a.question != state.question.name:
                continue
            for answer in a.bad_answers:
                commented = s.answer_commented(a.question, answer)
                c = utilities.answer_format(answer)
                if not commented:
                    # Uppercase in order to display them first when sorted
                    c = "<SPAN class=\"uncommented\">" + c + "</span>"
                elif commented == '*':
                    c = "***!!!" + c + "!!!***"
                else:
                    c = '<a class="tips"><SPAN style="white-space: normal">%s</SPAN>%s</a>' %(commented,c)
                    
                name = s.a_href()
                if not a.answered:
                    name = "<b>" + name + "</b>"
                if a.indice != -1:
                    name = "<em>" + name + "</em>"
                ba.append( [state.question.canonize(answer,state), c, name,
                            answer] )

    if len(ba) == 0:
        return
                
    # Fusion of bad answers with identical canonization
    ba.sort(key=lambda x: (x[0], len(x[3])))
    new_ba = []
    last = False
    for x in ba:
        if x[0] == last:
            if x[3] != last_orig:
                x[2] += '<a class="tips"><SPAN style="white-space: normal">' +  utilities.answer_format(x[3], space=True) + '</SPAN>+</a>'
            new_ba[-1][1] += ", " + x[2]
        else:
            new_ba.append([x[1], x[2]])
            last = x[0]
            last_orig = x[3]

    return utilities.sortable_table(plugin.sort_column, new_ba,
                                    url=plugin.plugin.css_name
                                    )
