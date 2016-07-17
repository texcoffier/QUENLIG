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

"""Display the information box in case of good answer."""

priority_display = 'question_answer'
priority_execute = 'question_answer'
background = '#CFC'
title_background = '#8F8'
acls = { 'Default': ('executable',) }
css_attributes = (
    "button, p { margin: 0.5em }",
    )
javascript = '''
function click_on_next_button()
{
   var e = document.getElementById(1) ;
   if ( e )
     {
        window.location = e.href ;
     }
   else
     {
     // We want the same behaviour than the enter key
     triggerKeyboardEvent(document.getElementsByTagName('BODY')[0], 13) ;
     }
}
'''

def execute(state, dummy_plugin, dummy_argument):
    if state.question == None:
        return
    if state.question.tests == ():
        return
    if 'question_answer' not in state.form:
        return

    s = state.student.last_answer(state.question.name)

    number, message = state.student.check_answer(s, state)

    if number != True:
        return

    if state.question.good_answer:
        if message:
            message += '<hr>'
        message += state.question.good_answer

    message += '''<p id="question_good_buttons">
    <a class="tips key_enter">
    <button onclick="click_on_next_button()"><p></p></button><span></span>
    </a>
    </p>
    '''

    return message


