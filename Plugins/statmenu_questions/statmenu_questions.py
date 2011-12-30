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

"""Displays session statistics about the questions."""

import utilities
import statistics
import questions

priority_display = 'statmenu_students'
priority_execute = '-question_answer'
link_to_self = True
acls = { 'Teacher': ('executable',) }

def execute(state, plugin, argument):
    if argument == None:
        return ''

    stats = statistics.question_stats()
    nr_students = float(len(stats.all_students))

    s = []
    for question in questions.questions.values():
        norme = float(question.student_given)
        if question.student_given == 0:
            continue
        s.append([
            question.a_href(),
            "%6.3f" % (question.student_given  / nr_students),
            "%6.3f" % (question.student_view   / norme),
            "%6.3f" % (question.student_good   / norme),
            "%6.3f" % (question.student_bad    / norme),
            "%6.3f" % (question.student_indice / norme),
            utilities.time_format(question.student_time  / norme),
            "%6.3f" % (question.student_nr_comment/ norme),
            ])

    if s:
        plugin.heart_content = \
               utilities.sortable_table(plugin.sort_column, s,
                                  url = "%s&%s=1" % (plugin.plugin.css_name, plugin.plugin.css_name))
        state.question = None

    return ''





