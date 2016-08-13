#!/usr/bin/env python3
# -*- coding: latin-1 -*-
#    QUENLIG: Questionnaire en ligne (Online interactive tutorial)
#    Copyright (C) 2016 Thierry EXCOFFIER, Universite Claude Bernard
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
#    Contact: Thierry.EXCOFFIER@univ-lyon1.fr

"""Set the user language for the session.
It is not a persistent option.
"""

container = 'identity'
priority_display = 10
acls = { 'Default': ('executable',) }

def execute(state, plugin, argument):
    if argument:
        if argument == 'fr':
            state.localization = ('fr',)
        else:
            state.localization = (argument, 'fr')
        for plugin in state.plugins_dict.values():
            plugin.update_attributes()
            if plugin.link_to_self:
                plugin.link = '?' + plugin.plugin.css_name + '=1'
    return '''<a href="?language=fr">FR</a>, <a href="?language=en">EN</a>'''

