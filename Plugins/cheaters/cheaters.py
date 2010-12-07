#!/usr/bin/env python
# -*- coding: latin1 -*-
#    QUENLIG: Questionnaire en ligne (Online interactive tutorial)
#    Copyright (C) 2008 Thierry EXCOFFIER, Universite Claude Bernard
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

import utilities
import statistics
import questions

container = 'analyse'
priority_execute = '-question_answer'
priority_display = 1000000
link_to_self = True
acls = { 'Teacher': ('executable',) }

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

    st = '<TABLE>'
    for s in stats.sorted_students:
        st += "<TR><TH>%s</TH>" % s.a_href()
        for ss in stats.sorted_students:
            try:
                n = ( 10 * s.nr_answer_same_time[ss.name]
                     / float(s.the_number_of_good_answers) )
            except KeyError:
                n = 0
                
            if n < 3 :
                color = ""
            elif n < 4 :
                if abs(s.the_number_of_good_answers
                       - ss.the_number_of_good_answers)<2:
                    color = styles[-1]
                else:
                    color = styles[1]
            else:
                if abs(s.the_number_of_good_answers
                       - ss.the_number_of_good_answers)<2:
                    color = styles[-2]
                else:
                    color = styles[2]
            st += "<TD %s>%d</TD>" % (color, n)
        st += "</TR>\n"
    st += "</TABLE>"
    plugin.heart_content = st
    state.question = None

    return ''




