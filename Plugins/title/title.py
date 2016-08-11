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

"""Display the page title."""

font_size = "200%"
container = 'title_bar'
text_align = 'center'
acls = { 'Default': ('executable',) }

option_name = 'title'
option_help = '''"Title of the session"
        It is displayed as the page title if there is no current question.'''
option_default = ""

def execute(state, plugin, dummy_argument):
    try:
        plugin.the_title = state.question.name
    except:
        plugin.the_title = plugin.option or state.student.name

    return plugin.the_title


    

