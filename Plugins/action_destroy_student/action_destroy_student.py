#!/usr/bin/env python3
# -*- coding: latin-1 -*-
#    QUENLIG: Questionnaire en ligne (Online interactive tutorial)
#    Copyright (C) 2007-2017 Thierry EXCOFFIER, Universite Claude Bernard
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

"""Destroy all the students with 0 or 1 good answer."""

from QUENLIG import statistics
from QUENLIG import utilities
from QUENLIG import student

container = 'action'
link_to_self = True
priority_execute = 'statmenu_students'

acls = { 'Admin': ('executable',) }

def execute(state, plugin, argument):
    if not argument:
        p = state.plugins_dict['answered_other']
        if p.heart_content is not None:
            p.heart_content = (
                '<p><a class="delete_one" href="?action_destroy_student='
                + state.form['answered_other'] + '">&nbsp;</a>'
                + p.heart_content
            )
        return ''
    
    stats = statistics.question_stats()

    roles = set()
    for e in stats.all_students:
        try:
            for role in eval(utilities.read(e.roles_filename)):
                roles.add(role)
        except:
            pass

    if argument == '1':
        students = [e
                    for e in stats.all_students
                    if e.the_number_of_good_answers < 2
                    ]
    else:
        students = [student.student(argument)]
    s = []
    for e in students:
        if e == state.student:
            continue
        if e.filename in roles:
            continue
        s.append('%s(%s)' %(e.name, e.the_number_of_good_answers))
        e.destroy()
            
    plugin.heart_content = ('<p class="deleted"><br>' +
                                  '<br>\n'.join(s)
                                 )
    state.question = None

    return ''














