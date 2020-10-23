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

import html
import json

priority_display = 'question_indices'
priority_execute = 'question_answer'
acls = { 'Default': ('!executable',) }

javascript = r"""

var spoil ;

function Spoil(goods)
{
  this.goods = goods ;
  this.spoil_min = 1e30 ;
  this.spoil_max = 0 ;
  for(var i in this.goods)
   {
     this.goods[i] = this.canonize(this.goods[i]) ;
     if ( this.goods[i].length < this.spoil_min )
        this.spoil_min = this.goods[i].length ;
     if ( this.goods[i].length > this.spoil_max )
        this.spoil_max = this.goods[i].length ;
   }
 document.write('<div class="spoiler">'
                + '<div class="spoil" onmouseover="spoil.length(event)">'
                + '<span class="spoil_tip"></span></div>'
                + '<div class="spoil" onmouseover="spoil.diff(event)">'
                + '<span class="spoil_tip"></span></div>'
                + '</div>'
               );
}

Spoil.prototype.canonize = function(txt) {
   var t = [] ;
   txt = txt.replace(/ /g, '') ;
   for(var i=0; i<txt.length; i++)
      t.push(txt.substr(i, 1)) ;
   t.sort() ;
   return t.join('') ;
} ;

Spoil.prototype.answer = function(txt) {
  var f = document.getElementById('questionanswer') ;
  if ( ! f )
     return ;
  var input = (f.getElementsByTagName("INPUT")
               || f.getElementsByTagName("TEXTAREA"))[0]  ;
  return this.canonize(input.value) ;
} ;

Spoil.prototype.feedback = function(event, content) {
  var t = (event || window.event).target ;
  if ( t.className != 'spoil' )
    return ;
  t.firstChild.innerHTML = content ;
} ;

Spoil.prototype.distance = function(a, b) {
  var r1 = 0 ;
  var r2 = 0 ;
  var ca, cb, miss_a = "", miss_b = "" ;
  a += '\uFFFF' ;
  b += '\uFFFF' ;
  while( r1 < a.length || r2 < b.length )
     {
        ca = a.substr(r1, 1) ;
        cb = b.substr(r2, 1) ;
        if ( ca == cb )
           {
             r1++ ;
             r2++ ;
           }
        else if ( ca < cb )
           {
             miss_b += ca ;
             r1++ ;
           }
        else
           {
             miss_a += cb ;
             r2++ ;
           }
    }
 return [miss_a, miss_b] ;
}

Spoil.prototype.diff = function(event) {
  var answer = this.answer() ;
  if ( answer === undefined )
     return ;
  var s = [] ;
  for(var i in this.goods)
     {
       var d = this.distance(answer, this.goods[i]) ;
       var x = '' ;
       if ( d[0] === '' )
           d[0] = '∅ ☺' ;
       if ( d[1] === '' )
           d[1] = '∅ ☺' ;
       s.push('<tr><td>' + (Number(i)+1) + '<td>' + html(d[0])
                                         + '<td>' + html(d[1]) + '</tr>') ;
     }
  if ( s.length )
     this.feedback(event,
             '<p class="spoil_diff"></p>'
             + '<table class="information_table" style="display:inline">'
              + '<tr><th><p class="spoil_answer"><th><p class="spoil_miss"><th><p class="spoil_unexpected"></tr>'
              + s.join('')
              + '</table><p>');
  else
     this.feedback(event, '<p class="spoil_diff_ok"></p>');
} ;

Spoil.prototype.length = function(event) {
  var answer = this.answer() ;
  if ( answer === undefined )
     return ;
  if ( answer.length < this.spoil_min )
     this.feedback(event,
                 '<p class="spoil_less"> ' + (this.spoil_min - answer.length)
                 + ' <span class="spoil_char"></span>') ;
  else if ( answer.length > this.spoil_max )
     this.feedback(event,
                 '<p class="spoil_more"> ' + (answer.length - this.spoil_max)
                 + ' <span class="spoil_char"></span>') ;
  else
     this.feedback(event, '<p class="spoil_ok"></p>');
} ;

function set_spoiler(goods)
{
  if ( goods.length == 0 )
     return ;
  spoil = new Spoil(goods) ;
}
"""

css_attributes = (
    "{ display: inline }",
    ".spoil { display: inline ; position: relative; margin-left: 1em }",
    ".spoil:hover .spoil_tip { opacity: 1 ; transition: opacity 8s; webkit-transition: opacity 8s;  }",
    ".spoil_tip { opacity: 0; pointer-events: none ; position:absolute; bottom:1.5em; left: 0px; padding-right: 1em; transition: opacity 0.5s; webkit-transition: opacity 0.5s;  }",
    ".spoil_tip *, .spoil_tip { background: #FFE ; }",
)

def execute(state, plugin, argument):
    if state.question == None:
        return None
    if state.student.answered_question(state.question.name):
        return
    if '{{{' in state.question.get_question(state):
        return

    goods = [''.join(sorted(good))
             for good in state.question.get_good_answers(state)
    ]
    
    state.plugins_dict["question_answer"].value_title += """
    <script><!--
    set_spoiler({}) ;
    --></script>""".format(json.dumps(goods))
    
