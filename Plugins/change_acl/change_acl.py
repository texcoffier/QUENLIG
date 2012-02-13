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

container = 'action'

sort_column = 0

acls = { 'Admin': ('executable',) }

javascript = """
function change_acls(user)
{
  var f = document.getElementById('acls_form') ;
  var selects = f.getElementsByTagName('SELECT') ;
  var s = [user] ;
  for(var i=0; i<selects.length; i++)
    s.push( selects[i].name + '=' + selects[i].selectedIndex ) ;

  window.location = '?change_acl=' + s.join(',') ;
}
"""

def acl_page(plugin, user):
    # Plugins.acls.acls.update_student_acls(student.students[user])
    acls = []
    roles = [user]
    stop = False
    while not stop:
        stop = True
        for role in student.students[roles[-1]].roles[::-1]:
            if role != 'Wired' and role not in roles:
                roles.append(role)
                stop = False
              
    
    t = []
    for plugin_name, a_plugin in plugins.Plugin.plugins_dict.items():
        line = [plugin_name, a_plugin.default_container(),
                ('class="doc"', a_plugin.plugin.__doc__)
                ]
        if 'executable' in a_plugin.plugin.acls.get('Wired', ()):
            for role in roles:
                line.append('')
        else:
            for role in roles:
                a = student.students[role].acls.get_an_acl(plugin_name,
                                                           'executable')
                if role == roles[0]:
                    aa = '<select name="' + plugin_name + '"><option'
                    if a is None:
                        aa += ' selected'
                    aa += '></option><option'
                    if a is False:
                        aa += ' selected'
                    aa += '>Reject</option><option'
                    if a is True:
                        aa += ' selected'
                    aa += '>Allow</option></select>'
                else:
                    aa = {None: '', False: 'Reject', True: 'Allow'}[a]
                    aa = '<b>' + aa + '</b>'
                acl = a_plugin.plugin.acls.get(role, ())
                if 'executable' in acl:
                    b = 'Allow'
                elif '!executable' in acl:
                    b = 'Reject'
                else:
                    b = ''
                line.append((' class="nowrap"', aa + '/' + b))
        t.append(line)

    titles = ['Plugin', 'Container', 'Documentation']
    for role in roles:
        titles.append(role + '<br><tt class="roles">'
                      + ' '.join(student.students[role].roles)
                      + '</tt>')

    return (
        '<form id="acls_form" action="javascript:change_acls(\'' +
        user + '\')">' +
        '<button type="submit" class="change_acl_save" value=""></button>' +
        utilities.sortable_table(plugin.sort_column,
                                 t,
                                 url = "%s&%s=%s" % (plugin.plugin.css_name,
                                                     plugin.plugin.css_name,
                                                     user),
                                 titles = titles) +
        '<button type="submit" class="change_acl_save" value="x"></button>' +
        '</form>')


def execute(state, plugin, argument):
    if argument:
        arguments = argument.split(',')
        argument = arguments[0]
        if len(arguments) > 1:
            for i in arguments[1:]:
                i = i.split('=')
                if i[0] not in plugins.Plugin.plugins_dict:
                    continue
                print argument, i
                acls = student.students[argument].acls
                if i[1] == '2':
                    acls.change_acls(i[0], 'executable')
                elif i[1] == '1':
                    acls.change_acls(i[0], '!executable')
                elif i[1] == '0':
                    acls.change_acls(i[0], '@executable')
        plugin.heart_content = acl_page(plugin, argument)
        return

    p = state.plugins_dict['answered_other']

    if not p.heart_content:
        return

    p.heart_content = ('<p><a class="change_acl" href="?change_acl='
                       + state.form['answered_other'] + '">&nbsp;</a>'
                       + p.heart_content
                       )
