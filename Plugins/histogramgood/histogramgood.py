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

container = 'analyse'
link_to_self = True
priority_execute = '-question_answer'
acls = { 'Teacher': ('executable',) }

def histogram_good(state):
    stats = statistics.question_stats()

    div = int(state.form.get("value", "10"))

    histo = [0] * (1 + stats.max_good_answers/div)
    for s in stats.all_students:
        histo[ s.the_number_of_good_answers/div ] += 1
    t = "<pre>"
    for h in range(len(histo)):
        t += ("%3d-%3d : " % (h*div, (h+1)*div-1))  +  "*" * histo[h] + "\n"
    t += '</pre>'

    t += '<p class="histobad"></p>'
    histo = [0] * (1 + stats.max_bad_answers/div)
    for s in stats.all_students:
        histo[ s.the_number_of_bad_answers/div ] += 1
    t += "<pre>"
    for h in range(len(histo)):
        t += ("%3d-%3d : " % (h*div, (h+1)*div-1))  +  "*" * histo[h] + "\n"
    t += '</pre>'

    return t

def execute(state, plugin, argument):
    if argument:
        plugin.heart_content = '<p class="histogram"></p>' + \
                                     histogram_good(state)
        state.question = None
    return ''


    




    

