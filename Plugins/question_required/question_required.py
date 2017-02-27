#!/usr/bin/env python3
# -*- coding: latin-1 -*-
#    QUENLIG: Questionnaire en ligne (Online interactive tutorial)
#    Copyright (C) 2007-2017 Thierry EXCOFFIER, Universite Claude Bernard
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

"""Display the informations about the required questions."""

from QUENLIG import utilities
from QUENLIG import questions

priority_display = 'question_indices'
priority_execute = 'question_answer' # We need to know if the answer was answered
acls = { 'Default': ('executable',) }

css_attributes = (
    ".box_content { padding: 0.5em }",
    "DIV.tabs { height: 1.1em; }",
    "DIV.tabs DIV.content { display: none }",
    "DIV.tabs DIV.answer { display: none }",
    "DIV.tab { display: inline ; }",
    """#display_tab { height: 9em;
         overflow: auto;
         background: #FFF ;
         padding-top: 0.4em ;
    }""",
    """DIV.name { border: 1px solid #BBB ;
    display: inline ;
    border-top-right-radius: 0.4em ;
    border-top-left-radius: 0.4em ;
    border-bottom: 0px ;
    margin-right: 0.2em ;
    }""",
    "DIV.content { position: relative; }",
    "DIV.before { position: absolute;top: 0px; left: 50% ; }",
    "DIV.question { position: absolute; top: 0px; left: 0px ; right: 50% ; }",
    )

javascript = """
function goto_tab(t)
{
  while ( t.className != "tab" )
      t = t.parentNode ;
  var selected = t ;
  while ( t.className != "tabs" )
      t = t.parentNode ;
  for(var i = 0 ; i < t.childNodes.length; i++)
    {
     var e = t.childNodes[i] ;
     e.childNodes[0].style.background = ( e === selected ? "#FFF" : "#CCC") ;
    }
  document.getElementById("display_tab").innerHTML = selected.childNodes[1].outerHTML ;
  document.getElementById("display_answer").innerHTML = selected.childNodes[2].outerHTML ;
}
"""

def execute(state, dummy_plugin, dummy_argument):
    if state.question == None:
        return
    if state.student.answered_question(state.question.name):
        return
        
    s = ['<div class="tabs">']
    for p in state.question.required:
        if p.hidden:
            continue
        if p.hide:
            continue
        q = questions.questions[p.name]
        question = q.question(state)
        try:
            answer = utilities.answer_format(
                state.student.answers[p.name].answered,
                question=question)
        except (KeyError, AttributeError):
            answer = ''
        question = question.split("{{{")[0]
        answer = '<div class="answer">' + answer + '</div>'
        if (q.courses  or  p.before) and q.before:
            before = q.before(state)
        else:
            before = ""
        s.append('<div class="tab"')
        if len(s) == 2:
            s.append(' id="first_tab"')
        s.append('><div class="name" onclick="goto_tab((event||window.event).target)">')
        s.append(p.name)
        s.append("</div>")
        s.append('<div class="content">')
        s.append('<div class="before">')
        s.append(before)
        s.append("</div>")
        s.append('<div class="question">')
        s.append(question)
        s.append("</div>")
        s.append("</div>")
        s.append(answer)
        s.append("</div>")
    s.append("</div>")
    s.append('<div id="display_tab"></div>')
    s.append('<div id="display_answer"></div>')
    s.append("<script>goto_tab(document.getElementById('first_tab'))</script>")
    if s:
        return ''.join(s)





