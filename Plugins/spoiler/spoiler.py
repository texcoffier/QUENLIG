#!/usr/bin/env python3
# -*- coding: utf-8 -*-
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

"""Spoil the answer:
  * Minimum and maximum size in characters of the good answers
"""

import cgi
import json

priority_display = 'question_indices'
priority_execute = 'question_answer'
acls = { 'Default': ('!executable',) }

javascript = """
var spoil_goods, spoil_min = 1e30, spoil_max = 0 ;

function spoil_canonize(txt)
{
   return txt.replace(/ /g, "")
}

function spoil_length(event)
{
  var t = (event || window.event).target ;
  var f = document.getElementById('questionanswer') ;
  if ( ! f )
     return ;
  var input = (f.getElementsByTagName("INPUT")
               || f.getElementsByTagName("TEXTAREA"))[0]  ;
  t.parentNode.style.border = "1px solid black" ;
  t.parentNode.style.fontWeight = "normal" ;
  t.parentNode.style.fontSize = "80%" ;
  var answer = spoil_canonize(input.value)
  if ( answer.length < spoil_min )
    {
     t.innerHTML = ' ' + (spoil_min - answer.length) + ' ' ;
     t.className = "spoil_less" ;
     t.nextSibling.className = 'spoil_char' ;
    }
  else if ( answer.length > spoil_max )
    {
     t.innerHTML = ' ' + (answer.length - spoil_max) + ' ' ;
     t.className = "spoil_more" ;
     t.nextSibling.className = 'spoil_char' ;
    }
  else
    {
     t.innerHTML = ' ' ;
     t.className = "spoil_ok" ;
     t.nextSibling.className = '' ;
    }
}

function set_spoiler(goods)
{
spoil_goods = goods ;
for(var i in goods)
   {
     goods[i] = spoil_canonize(goods[i]) ;
     if ( goods[i].length < spoil_min )
        spoil_min = goods[i].length ;
     if ( goods[i].length > spoil_max )
        spoil_max = goods[i].length ;
   }
document.write('<div class="spoiler" style="display:inline"><span class="spoil_empty" onmouseover="spoil_length(event)"> </span><span></span></div>');
}
"""

def execute(state, plugin, argument):
    if state.question == None or state.question.before == None:
        return None
    if state.student.answered_question(state.question.name):
        return

    goods = [''.join(sorted(good))
             for good in state.question.get_good_answers(state)
    ]
    
    state.plugins_dict["question_answer"].value_title += """
    <script><!--
    set_spoiler({}) ;
    --></script>""".format(json.dumps(goods))
    
