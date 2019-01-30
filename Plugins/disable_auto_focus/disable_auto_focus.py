#!/usr/bin/env python3
# -*- coding: latin-1 -*-
#    QUENLIG: Questionnaire en ligne (Online interactive tutorial)
#    Copyright (C) 2019 Thierry EXCOFFIER, Universite Claude Bernard
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

"""If active : the input auto focus is disabled.
So it is more usable with screen readers."""


priority_execute = 'debug'

acls = { }

def execute(state, plugin, argument):
    for a_plugin in state.plugins_list:
        if a_plugin.value and '.focus()' in a_plugin.value:
            a_plugin.value = '\n'.join(
                line
                for line in a_plugin.value.split('\n')
                if not ('.focus()' in line
                        and 'document.getElementById(' in line)
                )
