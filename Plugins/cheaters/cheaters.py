#!/usr/bin/env python3
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

"""Detection of the student always giving the same answer at the same time."""

from QUENLIG import utilities
from QUENLIG import statistics

container = 'analyse'
priority_execute = '-question_answer'
priority_display = 1000000
link_to_self = True
acls = { 'Teacher': ('executable',), 'Grader': ('executable',) }
sort_column = -3

def execute(state, plugin, argument):
    if argument == None:
        return ''

    stats = statistics.question_stats()

    pairs = []
    for s in stats.sorted_students:
        for ss in stats.sorted_students:
            if id(s) > id(ss):
                try:
                    if ss.name not in s.nr_answer_same_time:
                        continue
                    after, before = s.nr_answer_same_time[ss.name]
                    pairs.append((after, before,
                                  (100 * after)
                                  / s.the_number_of_good_answers,
                                  (100 * before)
                                  / ss.the_number_of_good_answers,
                                  s, ss))
                except KeyError:
                    pass
    if len(pairs) == 0:
         plugin.heart_content = '<p class="no_pairs_found"></p>'
         return ''
    pairs.sort(key=lambda x: x[0] + x[1])
    pairs.reverse()
    average = (sum(list(zip(*pairs))[1]) + sum(list(zip(*pairs))[2])) / len(pairs)
    average2 = sum((i[1]+i[2])**2 for i in pairs) / len(pairs)
    stddev = (average2 - average*average) ** 0.5
    
    st = []
    for after, before, nn1, nn2, s1, s2 in pairs:
        st.append([s1.a_href(), s2.a_href(),
                   after, before, '%.2f' % nn1,  '%.2f' % nn2])
        if max(nn1, nn2) < average + stddev/2: # not interesting
            break
        
    plugin.heart_content = utilities.sortable_table(
        plugin.sort_column,
        st,
        url = "%s&%s=1" % (plugin.plugin.css_name, plugin.plugin.css_name))

    state.question = None

    return ''




