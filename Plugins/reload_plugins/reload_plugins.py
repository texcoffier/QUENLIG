#!/usr/bin/env python
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

import plugins
import os
import utilities
import sys

priority_execute = 1000000000
container = 'action'

link_to_self = True

acls = { 'Teacher': ('executable',) }

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
    return ''

def init():
    import state

    old_state = state.State

    class State(state.State):
        def execute(self, form):
            self.reload = False
            a = old_state.execute(self, form)
            if self.reload:
                import Plugins.page.page
                Plugins.page.page.css_cached.cache = {}
                utilities.allow_one_more_call(Plugins.page.page.generate_javascript)
                import server
                server.cache = {}

                for s in state.states.values():
                    s.update_plugins()

                import Plugins.acls
                Plugins.acls.acls.reload()

            return a

    state.State = State

