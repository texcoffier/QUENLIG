#!/usr/bin/env python3
# -*- coding: latin-1 -*-
#    QUENLIG: Questionnaire en ligne (Online interactive tutorial)
#    Copyright (C) 2007,2012 Thierry EXCOFFIER, Universite Claude Bernard
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

"""Allow the students to leave a comment about the question."""

import cgi

priority_display = 'analyse'
css_attributes = (
    "TEXTAREA { font-size: 80% ; width: 100% }",
    "FORM { display: none; margin: 0px }",
    ":hover FORM { display: block }",
    "BUTTON { width: 100% ; }",
    ".comment_given { white-space: normal;}",
    )
acls = { 'Student': ('executable',) }

def execute(state, plugin, argument):
    if argument:
        if state.question:
            q = state.question.name
        else:
            q = "None"
        state.student.add_a_comment(q, argument)
        
        s = '<div class="comment_given">' \
            + cgi.escape(argument) + '</div>'
    else:
        s = ''


    return '''
    <FORM METHOD="GET" ACTION="#">
    <TEXTAREA NAME="%s" ROWS="10"></TEXTAREA><br>
    <button type="submit"><p class="comment_button"></p></button>
    </FORM>
    ''' % plugin.plugin.css_name  + s
