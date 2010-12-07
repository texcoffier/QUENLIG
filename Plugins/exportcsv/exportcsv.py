#!/usr/bin/env python
# -*- coding: latin1 -*-
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

import statistics

allow_out_of_sequence_execution = True
container = 'analyse'
link_to_self = True
tip_preformated = True
acls = { 'Teacher': ('executable',) }

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

    for s in stats.all_students:
        content.append(
            (
                s.filename,
                s.the_number_of_good_answers  / max_good_answers ,
                s.the_number_of_bad_answers   / max_bad_answers  ,
                s.the_number_of_given_indices / max_given_indices,
                (s.the_time_searching + s.the_time_after)/3600.,
                s.points()
            ))
    content.sort()

    header = plugin.tip.split('\\A')

    t = [header[6]]
    t.append(','.join(header[1:6]))
    for c in content:
        t.append("%s, %4.2f, %4.2f, %4.2f, %4.1f, %4.1f" % c)
        
    return 'text/comma-separated-values', '\n'.join(t)




