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
Allow to change session options
"""

container = 'action'
sort_column = 0
link_to_self = True
acls = { 'Teacher': ('executable', ), 'Admin': ('executable',) }
priority_execute = '-question'

import utilities
import plugins
import cgi
import configuration

def the_options(state, m_plugin):
    t = []
    for plugin in state.plugins_list:
        a_plugin = plugin.plugin
        name = a_plugin["", "option_name"]
        if name:
            t.append( ['<b>' + name + '</b><br><small>' + a_plugin.css_name,
                       a_plugin[state.localization, "option_help"],
                       a_plugin[state.localization, "option_default"],
                       '<TEXTAREA name="option__%s">' % a_plugin.css_name
                       + cgi.escape(plugin.option)
                       + '</TEXTAREA>',
                       ])

    button = '<BUTTON type="submit" class="save_options" name="%s" value="set"></BUTTON>' % m_plugin.plugin.css_name
            
    return ('<FORM action="?">'
            + button
            + utilities.sortable_table(m_plugin.sort_column, t)
            + button
            + '</FORM>')

def save_options(a_state, m_plugin):
    for plugin in a_state.plugins_list:
        a_plugin = plugin.plugin
        name = a_plugin["", "option_name"]
        if not name:
            continue
        value = a_state.form.get('option__' + a_plugin.css_name)
        if value is None:
            continue
        value = value.strip()
        if plugin.option == value:
            continue
        utilities.write(name, value,overwrite=True)

    import state
    for s in state.states.values():
        for p in s.plugins_list:
            s.init_option(p)

def execute(state, plugin, argument):
    if argument == '1':
        plugin.heart_content = the_options(state, plugin)
        state.question = None
    elif argument == 'set':
        save_options(state, plugin)
        plugin.heart_content = the_options(state, plugin)
        state.question = None
        
    return ''

