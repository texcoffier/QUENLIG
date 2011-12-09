#!/usr/bin/env python
# -*- coding: latin-1 -*-
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

container = 'questions'
priority_display = '-questions_next'
priority_execute = '-questions'
acls = { 'Teacher': ('executable',) }
tip_preformated = True

types = ('normal', 'all')

def execute(state, plugin, argument):

    if 'the_value' not in plugin.__dict__:
        plugin.the_value = types[0]

    if argument:
        if argument == types[0]:
            state.student.answerable_any = False
        elif argument == types[1]:
            state.student.answerable_any = True
        else:
            return 'BUG'
        plugin.the_value = argument

    s = '<select onChange="window.location = \'%s?%s=\' + value ;">\n' % (
        state.url_base_full,
        plugin.plugin.css_name)
    for i in types:
        if plugin.the_value == i:
            selected = " selected"
        else:
            selected = ""
        s += '<option%s VALUE="%s">%s</option>\n' % (selected,
                                                     i,
                                                     plugin.translations[i])
    s += '</select>\n'

    return s

