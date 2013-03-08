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

"""Display the students grades for a question sorted by answer"""

import utilities
import statistics

priority_display = 'question_stat'
acls = { 'Author': ('executable',), 'Grader': ('executable',) }

def execute(state, plugin, argument):
    if not state.question:
        return
    stats = statistics.question_stats()
    columns = set()
    for s in stats.all_students:
        a = s.answer(state.question.name)
        if a.answered:
            for k in a.grades:
                if a.grades[k] != '0':
                    columns.add(k)
    columns = sorted(columns)

    table = []
    for s in stats.all_students:
        a = s.answer(state.question.name)
        if not a.answered:
            continue
        table.append([utilities.answer_format(a.answered)]
                     + [a.grades.get(c, '') for c in columns])

    return utilities.sortable_table(plugin.sort_column, table,
                                    url=plugin.plugin.css_name,
                                    titles=['X'] + columns
                                    )
