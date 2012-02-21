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

"""Displays a statistics table about all the students."""

import utilities
import statistics
import questions

container = 'statmenu'
priority_execute = '-question_answer'
priority_display = 1000000
link_to_self = True
acls = { 'Teacher': ('executable',),  'Grader': ('executable',),
         'Admin': ('executable',),}

styles = {
    -2: "style='background-color:#FF0000;'",
    -1: "style='background-color:#FFA0A0;'",
    0: "",
    1: "style='background-color:#A0FFA0;'",
    2: "style='background-color:#00FF00;'",
    }

def execute(state, plugin, argument):
    if argument == None:
        return ''

    stats = statistics.question_stats()

    content = []
    for s in stats.all_students:
        nr_good_answers = (styles[s.warning_nr_good_answers],
                           s.the_number_of_good_answers)
        nr_bad_answers = (styles[s.warning_nr_bad_answers],
                          s.the_number_of_bad_answers)
        nr_given_indices = (styles[s.warning_nr_given_indices],
                            s.the_number_of_given_indices)
        time_after = (styles[s.warning_time_after],
                      utilities.time_format(s.the_time_after))

        line = [
            s.a_href(),
            nr_good_answers,
            s.the_number_of_given_questions,
            nr_bad_answers,
            nr_given_indices,
            s.the_number_of_comment,
            utilities.time_format(s.the_time_searching),
            time_after,
            utilities.date_format(s.the_time_first),
            utilities.date_format(s.the_time_last),
            "%3.1f" % s.nr_of_same_time_normed,
            int(s.the_time_variance),
            ]

        # line.append('<img src="?action=question_pixel_map_see_other&student=%s">' % s.filename)

        content.append(line)
        
    plugin.heart_content = \
         utilities.sortable_table(plugin.sort_column,
                                  content,
                                  url = "%s&%s=1" % (plugin.plugin.css_name,
                                                     plugin.plugin.css_name))
    state.question = None

    return ''





