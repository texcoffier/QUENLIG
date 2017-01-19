#!/usr/bin/env python3
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

"""Add smileys to the statistics of good/bad/tip/..."""

from QUENLIG import utilities

priority_execute = 'statmenu_indice'
container = 'statmenu'
acls = { 'Student': ('executable',) }

style = {
    -2: "<img align=\"top\" src=\"../../very_bad.png\">",
    -1: "<img align=\"top\" src=\"../../bad.png\">",
    0: "",
    1: "<img align=\"top\" src=\"../../good.png\">",
    2: "<img align=\"top\" src=\"../../very_good.png\">",
    }

def execute(state, plugin, argument):

    me = state.student
    if not hasattr(me, 'warning_nr_good_answers'):
        return ''

    where = {
        'statmenu_good':(
        me.warning_nr_good_answers, me.number_of_good_answers()),
        'statmenu_bad':(
        me.warning_nr_bad_answers, me.number_of_bad_answers()),
        'statmenu_indice':(
        me.warning_nr_given_indices, me.number_of_given_indices()),
        'statmenu_time':(
        -abs(me.warning_time_after),
        utilities.time_format(int(me.time_searching()))),
      }

    for item, (warning, value) in where.items():
        state.plugins_dict[item].value = (
            '<em class="tips"><span class="%s%d"></span>' % (item, warning) +
            style[warning] +
            '</em>'  + state.plugins_dict[item].value )

    return ''




