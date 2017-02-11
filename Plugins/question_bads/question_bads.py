#!/usr/bin/env python3
# -*- coding: latin-1 -*-
#    QUENLIG: Questionnaire en ligne (Online interactive tutorial)
#    Copyright (C) 2007-2016 Thierry EXCOFFIER, Universite Claude Bernard
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

"""Displays all the bad answers given for a question."""

import collections
from QUENLIG import utilities
from QUENLIG import statistics
from QUENLIG import questions

priority_display = 'question_comments'
acls = { 'Author': ('executable',) }
css_attributes = (
    "DIV.uncommented { background: #FAA; display: inline-block }",
    "DIV.uncommented PRE { background-color: #FAA ; }",
    )

sort_column = 0

def execute(state, plugin, argument):
    if state.question == None:
        return
    if not state.threaded_run:
        return # To be fast

    stats = statistics.question_stats()
    
    bads = collections.defaultdict(list)
    for s in stats.all_students:
        for a in s.answers.values():
            if a.question != state.question.name:
                continue
            for rand, answer in a.full_bad_answers:
                for dummy in state.steal_identity([s], a, rand):
                    commented = s.answer_commented(a.question, answer, state)
                    rand = state.question.question(state)
                    break
                else:
                    continue # The student is locked
                c = utilities.answer_format(answer)
                if not commented:
                    # Uppercase in order to display them first when sorted
                    c = '<div class="uncommented">' + c + "</div>"
                elif commented == '*':
                    c = "***!!!" + c + "!!!***"
                else:
                    c = '<a class="tips"><SPAN style="white-space: normal">%s</SPAN>%s</a>' %(commented,c)
                name = s.a_href(body='\n\n' + rand + '\n\n' + answer)
                if not a.answered:
                    name = "<b>" + name + "</b>"
                if a.indice != -1:
                    name = "<em>" + name + "</em>"
                bads[rand].append(
                    [state.question.canonize(answer,state), c, name, answer] )

    if len(bads) == 0:
        return

    new_ba = []
    for rand, ba in bads.items():
        # Fusion of bad answers with identical canonization
        ba.sort(key=lambda x: (x[0], len(x[3])))
        last = False
        for x in ba:
            if (x[0],x[1]) == last:
                if x[3] != last_orig:
                    x[2] += '<a class="tips"><SPAN style="white-space: normal">' +  utilities.answer_format(x[3], space=True) + '</SPAN>+</a>'
                new_ba[-1][2] += ", " + x[2]
            else:
                new_ba.append([rand, x[1], x[2]])
                last = (x[0], x[1])
                last_orig = x[3]

    return utilities.sortable_table(plugin.sort_column, new_ba,
                                    url=plugin.plugin.css_name,
                                    merge=True
                                    )
