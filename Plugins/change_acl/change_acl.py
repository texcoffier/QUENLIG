#!/usr/bin/env python
# -*- coding: latin-1 -*-
#    QUENLIG: Questionnaire en ligne (Online interactive tutorial)
#    Copyright (C) 2012 Thierry EXCOFFIER, Universite Claude Bernard
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

"""
Allow to change the ACL of users and roles.
"""

import student
import re
import plugins
import utilities
import Plugins.acls.acls

priority_execute = 'statmenu_students'

container = 'administration'

sort_column = 0

acls = { 'Teacher': ('executable',) }

css_attributes = (
    '/tt.roles { font-size: 70%; font-weight: normal ; }',
    '/.doc { font-size: 70%; }',
    )

def acl_page(plugin, user):
    # Plugins.acls.acls.update_student_acls(student.students[user])
    acls = []
    roles = [user]
    stop = False
    while not stop:
        stop = True
        for role in student.students[roles[-1]].roles[::-1]:
            if role not in roles:
                roles.append(role)
                stop = False
              
    
    t = []
    for plugin_name, a_plugin in plugins.Plugin.plugins_dict.items():
        line = [plugin_name, a_plugin.default_container(),
                ('class="doc"', a_plugin.plugin.__doc__)
                ]
        for role in roles:
            a = student.students[role].acls.get_an_acl(plugin_name, 'executable')
            if a is None:
                a = ''
            if 'executable' in a_plugin.plugin.acls.get(role, ()):
                b = 'True'
            else:
                b = ''
            line.append('<b>' + str(a) + '</b>/' + str(b))
        t.append(line)

    titles = ['Plugin', 'Container', 'Documentation']
    for role in roles:
        titles.append(role + '<br><tt class="roles">'
                      + ' '.join(student.students[role].roles)
                      + '</tt>')
    
    return utilities.sortable_table(plugin.sort_column,
                                    t,
                                    url = "%s&%s=%s" % (plugin.plugin.css_name,
                                                        plugin.plugin.css_name,
                                                        user),
                                    titles = titles)


def execute(state, plugin, argument):
    if argument:
        plugin.heart_content = acl_page(plugin, argument)
        return

    p = state.plugins_dict['answered_other']

    if not p.heart_content:
        return

    p.heart_content = ('<a href="?change_acl='
                       + state.form['answered_other'] + '">ACL</a>'
                       + p.heart_content
                       )
