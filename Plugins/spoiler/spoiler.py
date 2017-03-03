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
 document.write('<div class="spoiler" style="display:inline">'
                + '<span class="spoil_empty" onmouseover="spoil.length(event)">'
                + '</span><span></span></div>'
                + '<div class="spoiler" style="display:inline">'
                + '<span class="spoil_empty" onmouseover="spoil.diff(event)">'
                + '</span><span></span></div>'
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

Spoil.prototype.feedback = function(event, content, cls_before, cls_after) {
  var t = (event || window.event).target ;
  while( t.className != 'spoiler' )
     t = t.parentNode ;
  t = t.firstChild ;
  t.parentNode.style.border = "1px solid black" ;
  t.parentNode.style.fontWeight = "normal" ;
  t.parentNode.style.fontSize = "80%" ;
  t.parentNode.style.marginRight = "0.1em" ;
  t.innerHTML = ' ' + content + ' ' ;
  t.className = cls_before ;
  t.nextSibling.className = cls_after ;
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
       if ( d[0] !== '' )
           x += '<b style="color:#0A0">' + html(d[0]) + '</b>' ;
       if ( d[1] !== '' )
           x += '<b style="color:#800">' + html(d[1]) + '</b>' ;
       s.push('«' + x + '» ') ;
     }
  if ( s !== "" )
     this.feedback(event, s.join('&nbsp;&nbsp;&nbsp;'), "spoil_diff", '');
  else
     this.feedback(event, "", "", '');
} ;

Spoil.prototype.length = function(event) {
  var answer = this.answer() ;
  if ( answer === undefined )
     return ;
  if ( answer.length < this.spoil_min )
     this.feedback(event, this.spoil_min - answer.length,
                   "spoil_less",'spoil_char');
  else if ( answer.length > this.spoil_max )
     this.feedback(event, answer.length - this.spoil_max,
                   "spoil_more",'spoil_char');
  else
     this.feedback(event, "", "spoil_ok", "");
} ;

function set_spoiler(goods)
{
  if ( goods.length == 0 )
     return ;
  spoil = new Spoil(goods) ;
}
"""

def execute(state, plugin, argument):
    if state.question == None:
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
    
