#!/usr/bin/env python3
# -*- coding: latin-1 -*-
#    QUENLIG: Questionnaire en ligne (Online interactive tutorial)
#    Copyright (C) 2017 Thierry EXCOFFIER, Universite Claude Bernard
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

"""Allow to evaluate arbitrary Python code for debugging."""

import html

# To simplify debugging:
from QUENLIG import configuration
from QUENLIG import questions
from QUENLIG import student
from QUENLIG import statistics

priority_display = 'analyse'
css_attributes = (
    "TEXTAREA { font-size: 80% ; width: 100% }",
    "FORM.highlight BUTTON P { background: #CFC ; }",
    "BUTTON { width: 100% ; }",
    )
acls = { 'Developer': ('executable',) }

def execute(state, plugin, argument):
    if argument:
        plugin.heart_content = ('<div class="evaluate_result"><br>'
             + html.escape(str(eval(argument))).replace("\n", "<br>") + '</div>')
    else:
        argument = ''

    return '''
    <FORM METHOD="GET" ACTION="#">
    <TEXTAREA id="evaluate" NAME="%s" ROWS="10">%s</TEXTAREA><br>
    <script>new PersistentInput('evaluate')</script>
    <button type="submit"><p class="evaluate_button"></p></button>
    </FORM>
    ''' % (plugin.plugin.css_name, html.escape(argument))
