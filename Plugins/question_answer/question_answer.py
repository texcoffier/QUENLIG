#!/usr/bin/env python
# -*- coding: latin-1 -*-
#    QUENLIG: Questionnaire en ligne (Online interactive tutorial)
#    Copyright (C) 2007-2011 Thierry EXCOFFIER, Universite Claude Bernard
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

"""It both display the INPUT HTML tag to enter the answer
but it also verify the answer.

As the answer may modify the question list, it must be executed
before the question list computation.
"""

import configuration
import cgi
import utilities

priority_execute = '-questions' # To update question list before
priority_display = 'question'

css_attributes = (
    "INPUT { width: 100% ; font-family: times; font-size:120%}",
    "TEXTAREA { width: 100% ; }",
    "FORM { margin: 0px }",
    )
acls = { 'Wired': ('executable',) }

javascript = """
function disable_tab(event)
{
     if ( window.event )
        event = window.event ;
     key = event.keyCode ;

     if(key == 9)
         {
          event.target.value += '   ' ;
          return false;
         }
     else
          return true;

}
"""

def execute(state, plugin, argument):
    if state.question == None:
        return
    if state.question.tests == ():
        return
    if argument:
        # Fill 'last_answer' attribute
        state.student.bad_answer_yet_given(state.question.name, argument)
        # Check the answer even if it is a known one because
        # the question tests may have been updated in live
        number, message = state.student.check_answer(state.question,
                                                     argument,
                                                     state)
        if number:
            state.student.good_answer(state.question.name,argument)
        else:
            # Does not count the same bad answer
            if not state.student.bad_answer_yet_given(state.question.name,
                                                      argument):
                state.student.bad_answer(state.question.name,argument)

    if (state.question.maximum_bad_answer
        and state.student.bad_answer_question(state.question.name) >= state.question.maximum_bad_answer):
        state.question = None
        return '<p class="maximum_bad_answer">'

    if state.student.answered_question(state.question.name):
        # Value setted in question_change_answer plugin
        if (not hasattr(state.student, 'allowed_to_change_answer')
            or not state.student.allowed_to_change_answer):
            s = state.student.last_answer(state.question.name)
            return utilities.answer_format(s)

    s = '<FORM CLASS="questionanswer" METHOD="GET" ACTION="#">'

    last_answer = state.student.last_answer(state.question.name)
    if last_answer == "":
        last_answer = cgi.escape(state.question.default_answer)
        style = ''
    else:
        if state.student.current_role != 'Teacher':
            style = 'background:#FAA'
        else:
            style = ''

    last_answer_html = last_answer.replace("%","&#37;").replace("'", "&#39;").\
                  replace('"', '&#34;')

    question = state.question.question(state)
    if '{{{' in question:
        t = question.split('{{{')[1:]
        for i in t:
            j = i.split('}}}')
            if j[0] in last_answer:
                checked = ' checked'
            else:
                checked = ''
            s += '<input type="checkbox" name="%s" value="%s"%s>' % (
                plugin.plugin.css_name, j[0], checked) + j[1] + '<br>'
        s += '<br><button type="submit"><p class="answer_button"></p></button>'
    elif state.question.nr_lines == 1:
        s += '<INPUT TYPE="text" ID="2" NAME="%s.%s" SIZE="%d" VALUE="%s" ALT="%s" onkeyup="if(this.value==this.alt && this.alt!==\'\') this.style.background=\'#FAA\'; else this.style.background=\'white\'" style="%s">'% (
            plugin.plugin.css_name, state.question.name,
            configuration.nr_columns, last_answer_html,
            last_answer_html, style)
    else:
        s += '<TEXTAREA NAME="%s" ID="2" COLS="%d" ROWS="%d" onkeypress="return disable_tab(event)">%s</TEXTAREA>' % (
            plugin.plugin.css_name,
            configuration.nr_columns,
            state.question.nr_lines,
            last_answer_html)
        s += '<br><button type="submit"><p class="answer_button"></p></button>'
        
    s += '<script type="text/javascript">document.getElementById(2).focus();</script>'
    s += '</FORM>'
    return s



    




    

