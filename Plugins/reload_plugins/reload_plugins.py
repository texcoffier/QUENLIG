#!/usr/bin/env python3
# -*- coding: latin-1 -*-
#    QUENLIG: Questionnaire en ligne (Online interactive tutorial)
#    Copyright (C) 2010 Thierry EXCOFFIER, Universite Claude Bernard
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

"""Reload all the modified Quenlig plugins.
It is currently not working nicely, do not try to use.
"""


import os
import sys
from QUENLIG import plugins
from QUENLIG import utilities

priority_execute = 1000000000
container = 'action'
permanent_acl = True

# link_to_self = True

acls = { 'Developer': ('executable',) }

def execute(state, plugin, argument):
    if argument:
        for plugin in tuple(plugins.Plugin.plugins_dict.values()):
            filename = plugin.plugin.__file__.replace('.pyc','.py')
            if os.path.getmtime(filename) == plugin.plugin.mtime:
                continue
            state.reload = True
            if plugin.plugin.__name__ in sys.modules:
                del sys.modules[plugin.plugin.__name__]
            plugins.Plugin.plugins_dict[plugin.plugin.name] = plugins.Plugin(utilities.load_module(plugin.plugin.name))
    # Keep the current state on screen
    plugin.link = "?reload_plugins=1&" + '&'.join(
        ['%s=%s' % (k,
                    v.replace("+","%2B")
                    .replace("?","%3F")
                    .replace("&","%26"))
         for k, v in state.form.items()
         if k not in ('number', 'ticket', 'reload_plugins')
         ])
    return ''

def init():
    from QUENLIG import state

    old_state = state.State

    class State(state.State):
        def execute(self, form):
            self.reload = False
            a = old_state.execute(self, form)
            if self.reload:
                import Plugins.top.top
                Plugins.top.top.css_cached.cache = {}
                utilities.allow_one_more_call(Plugins.top.top.generate_javascript)
                from QUENLIG import server
                server.cache = {}

                for s in state.states.values():
                    s.update_plugins()

                import Plugins.acls
                Plugins.acls.acls.reload()

            return a

    state.State = State

