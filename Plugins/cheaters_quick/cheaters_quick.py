#!/usr/bin/env python
# -*- coding: latin-1 -*-
#    QUENLIG: Questionnaire en ligne (Online interactive tutorial)
#    Copyright (C) 2008,2012 Thierry EXCOFFIER, Universite Claude Bernard
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

"""Detection of students answering too quickly."""

import utilities
import statistics
import questions
import collections

container = 'analyse'
priority_execute = '-question_answer'
priority_display = 1000000
link_to_self = True
acls = { 'Teacher': ('executable',), 'Grader': ('executable',) }
sort_column = -2

def execute(state, plugin, argument):
    if argument == None:
        return ''

    stats = statistics.question_stats()

    too_quick = collections.defaultdict(int)
    too_quick2 = collections.defaultdict(int)
    too_quick4 = collections.defaultdict(int)
    for s in stats.sorted_students:
        for question_name, answer in s.answers.items():
            if not answer.answered:
                continue
            question = questions.questions[question_name]
            average_time = question.student_time / question.student_given
            if answer.time_searching < average_time / 10:
                too_quick[s] += 1
            if answer.time_searching < average_time / 20:
                too_quick2[s] += 1
            if answer.time_searching < average_time / 40:
                too_quick4[s] += 1
        
    plugin.heart_content = utilities.sortable_table(
        plugin.sort_column,
        [[s.a_href(), nb, too_quick2[s], too_quick4[s]]
         for s, nb in too_quick.items()],
        url = "%s&%s=1" % (plugin.plugin.css_name, plugin.plugin.css_name))
    
    state.question = None

    return ''




