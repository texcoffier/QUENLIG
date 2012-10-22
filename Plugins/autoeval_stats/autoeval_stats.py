#!/usr/bin/env python
# -*- coding: latin-1 -*-
#    QUENLIG: Questionnaire en ligne (Online interactive tutorial)
#    Copyright (C) 2012 Thierry EXCOFFIER, Universite Claude Bernard
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

height = 400
container = 'statmenu'
priority_execute = 'autoeval'
acls = { }
css_attributes = (
    "{ position: relative; height: 35em }",
    "DIV { position: absolute; font-family: monospace }",
    ".me { background: green; color:white  }",
    "A.tips:hover TT { left:30em; width:20em; top: -3em; font-size: 100% }",
    "SPAN { top: 5em; left: 20em; width: 20em }",
    )
javascript = """

function histogram(t)
{
  var s = '' ;
  for(var i=0; i<17; i++)
     s += '&nbsp;<br>' ;
  var m = 17 ;
  for(var i in t)
    {
      s += '<div style="height:'     + Math.abs(m*t[i]).toFixed(0)
           + 'px;left:' + (30+17*i).toFixed(0)
           + 'px;top:' + Math.min(200-m*t[i], 200).toFixed(0)
           + 'px;border:1px solid black">'
           + '&nbsp;'
           + '</div>' ;
    }
  for(var i=-10; i<=10; i++)
    {
      s += '<div style="left:0px;top:' + (200-m*i-10).toFixed(0)
           + 'px">'
           + i
           + '</div>' ;
    }
  document.write(s) ;
}


"""

import math
import questions
import statistics

def px(v, vmin, vmax, size):
    return str( int( size * (v-vmin) / (vmax-vmin) ) ) + 'px'

def pos(y, x, text, tip=""):
    v = ('<div style="left:' + px(2+x, pos.xmin,pos.xmax,100)
         + ';top:' + px((pos.ymin+ pos.ymax)-y, pos.ymin, pos.ymax, height)
         + '">' + text + '</div>' )
    if tip:
        v = '<div class="tips">' + v + '<tt>' + tip + '</tt></div>'
    return v

def execute(state, dummy_plugin, dummy_argument):
    stats = statistics.question_stats()
    t = []
    for q in questions.questions.values():
        if not hasattr(q, 'autoeval_level'):
            continue
        if not getattr(q, 'student_given', False):
            continue
        if q.student_time:
            t.append((q.autoeval_level_average,
                      math.log(3 + q.student_time / q.student_given),
                      'x', q.name
                      + '<script>histogram('
                      + repr(q.autoeval_level) + ')</script>'))

    for s in stats.all_students:
        if not hasattr(s, 'autoeval_level'):
            continue
        if s.the_number_of_given_questions == 0:
            continue
        if s.the_time_searching:
            t.append((s.autoeval_level,
                      math.log(3 + s.the_time_searching
                               / s.the_number_of_given_questions),
                      s is state.student and '<var class="me">·</var>'
                      or '·',
                      s is state.student and state.student.name or ''))

    if not len(t):
        return ''
    pos.ymin = min(i[0] for i in t)
    pos.ymax = max(i[0] for i in t)
    pos.xmin = 0
    pos.xmax = max(i[1] for i in t)

    s = []
    for i in range(int(pos.ymin), int(pos.ymax)+1):
        s.append(pos(i, -2, ("%2d" % i).replace(' ', '&nbsp;')))
    for i in t:
        s.append(pos(*i))

    return '\n'.join(s) + '<br>'*35
