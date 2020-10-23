#!/usr/bin/env python3
# -*- coding: latin-1 -*-
#    QUENLIG: Questionnaire en ligne (Online interactive tutorial)
#    Copyright (C) 2007,2010 Thierry EXCOFFIER, Universite Claude Bernard
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

"""The questions box, it displays the allowed questions."""

import html

priority_display = 'identity'
priority_execute = 'question' # In order to emphasis current question

css_attributes = (
    "A.max_descendants { font-weight: bold; }",
    "A.question_given  {color:#888;}",
    "A.bad_answer_given{color:#F00;}",
    "A.indice_given    {font-style:italic;}",
    "A.current_question{text-decoration:underline;}",
    "A.highlight       { background: black; color: white;text-decoration: blink; }",
    )
acls = { 'Default': ('executable',), 'Admin': ('!executable',) }

def option_set(plugin, value):
    plugin.state.use_select = int(value)

option_name = 'use-select'
option_help = '''"integer"
        If the number of questions in the menu is greater than
        this number, then pulldown menus are used.'''
option_default = "50" 

def execute(state, plugin, dummy_argument):

    answerables = state.student.answerables_typed()

    if len(answerables) < plugin.state.use_select:

        if len(answerables) == 0:
            return ''

        focusable_found = False
        for info in answerables:
            if info[1].find("resigned ") == -1:
                focusable_found = True
                break

        max_descendants = max([len(info[0].descendants)
                               for info in answerables])
             
        s = ""
        focus_done = False
        for info in answerables:
            q = info[0]
            info = info[1]
            focus = ''
            if not focus_done:
                if not focusable_found or info.find("resigned ") == -1:
                    focus = 'ID="1" '
                    focus_done = True
            if len(q.descendants) == max_descendants:
                info += ' max_descendants'
            if q.highlight:
                info += ' highlight'
                     
            s += "<A %sHREF=\"%s\" CLASS=\"%s\">%s</A><BR>\n" % (
                focus,
                q.url(),
                info,
                html.escape(q.name),
                )
        s += '<!--SCRIPT-->'
        if focus_done:
            s += "<script type=\"text/javascript\">document.getElementById('1').focus();</script>"
    else:
        s = """<form>
        <script>
        function f(x)
        {
        window.location = '?question=' + escape2(x) ;
        }
        </script>
        """
        w = ""
        for info in answerables:
            q = info[0]
            world = q.name.split(":",1)[0]
            if w != world:
                w = world
                if s.find("<select") != -1:
                    s += "</select><br>"
                s += "<select OnChange=\"f(value);\">"
                s += "<option selected=\"1\">%s</option>" % world
            s += "<option>%s</option>\n" % html.escape(q.name)
        s += "</select></form>"

    return s
