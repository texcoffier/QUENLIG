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

"""The output of this plugin is a CSV file containing for each student
the normalized number of good/bad answers and indices.
There is also the work time in hours."""

import statistics
import configuration

container = 'statmenu'
link_to_self = True
acls = { 'Grader': ('executable',) }

def execute(state, plugin, argument):
    if not argument:
        return ''

    stats = statistics.question_stats()
    content = []

    if stats.max_good_answers == 0:
        max_good_answers = 1.
    else:
        max_good_answers = float(stats.max_good_answers)

    if stats.max_bad_answers == 0:
        max_bad_answers = 1.
    else:
        max_bad_answers = float(stats.max_bad_answers)

    if stats.max_given_indices == 0:
        max_given_indices = 1.
    else:
        max_given_indices = float(stats.max_given_indices)

    teachers = set()
    for s in stats.all_students:
        teachers.update(s.grading_teachers())

    for s in stats.all_students:
        grades = s.grades()
        content.append(
            (
                s.filename,
                s.the_number_of_good_answers  / max_good_answers ,
                s.the_number_of_bad_answers   / max_bad_answers  ,
                s.the_number_of_given_indices / max_given_indices,
                (s.the_time_searching + s.the_time_after)/3600.,
                s.points(),
                ) +
            tuple(grades.get(teacher, 0)  for teacher in teachers)
            )
    content.sort()

    header = plugin.tip.split('\\A')[1:-1]
    header.append('Points')
    header += list(teachers)
    formater = "%s" + ", %5.3f" * (len(header)-1)

    t = [','.join(header),
         ','.join(configuration.explain_grade.get(i,'') for i in header)
         ]
    for c in content:
        t.append(formater % c)
        
    return 'text/csv; charset=UTF-8', '\n'.join(t).encode('utf-8')




