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

"""Allow to display plugin definition in tips from the plugin interface"""

from QUENLIG import plugins
import cgi
from QUENLIG import student
from QUENLIG import utilities

priority_execute = '-top'
container = 'action'

css_attributes = ( 'a.tips > div.tips > div { white-space: pre; }',
                   )
permanent_acl = True
link_to_self = True
acls = { 'Developer': ('executable',) }

def execute(state, plugin, argument):

    if argument:
        state.debug = 1 - state.__dict__.get('debug', 0)
        
    if not state.__dict__.get('debug', 0):
        return ''

    for a_plugin in state.plugins_list:
        s = ['<h2>' + a_plugin.plugin.css_name + '</h2>']
        for attribute in plugins.Attribute.attributes.keys():
            if a_plugin.__dict__[attribute]:
                v = str(a_plugin.__dict__[attribute])
                v = v.encode('utf-8')
                v = cgi.escape(v)
                v = v.replace(',', ',<br>&nbsp;&nbsp;&nbsp;&nbsp;')
                v = (v)
                s.append('<b>%s</b> : %s<br>' % (attribute, v))

        s.append('current_acls=%s<br>' % a_plugin.current_acls)
        for stu in student.students.values():
            try:
                s.append('%s :: %s<br>' % (stu.name,
                                           stu.acls.get_acls(a_plugin.plugin.css_name)))
            except AttributeError:
                pass
            
        s = '<tt class="tips"><span>' + '\n'.join(s) + '</span>*</tt>'

        if a_plugin.boxed():
            if a_plugin.value_title == None:
                a_plugin.value_title = s
            else:
                a_plugin.value_title += s
        else:
            if a_plugin.value != None:
                a_plugin.value += s
            else:
                a_plugin.value = '(' + s + ')'
    
    return ''
