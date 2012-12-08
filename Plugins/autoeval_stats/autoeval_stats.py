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

"""Displays a graphical state of the questions and students"""

height = 30
container = 'statmenu'
priority_execute = 'autoeval'
acls = { }
css_attributes = (
    "{ position: relative; height: 35em }",
    "DIV { position: absolute; font-family: monospace }",
    ".me { background: #FF0; }",
    ".bad { color:red }",
    ".ok { color:green  }",
    "A.tips:hover TT { left:30em; width:24em; top: -3em; font-size: 100% }",
    "SPAN { top: 5em; left:20em; width:20em }",
    )

import Plugins.autoeval.autoeval

javascript = """

function time_to_slot(x)
{
  return Math.log(x/%d) / Math.log(%f) ;
}

function histogram(t, time_searching)
{
  var s = '' ;
  var h = 17 ;
  var m = 1.7 ;
  var mx = 1 ;
  var dx = 3 ;
  var x ;
  var slot = time_to_slot(time_searching).toFixed(0) ;
  for(var i=5; i<2*h; i++)
     s += '&nbsp;<br>' ;
  for(var i in t)
    {
      s += '<div style="height:' + Math.abs(m*t[i]).toFixed(1)
           + 'em;left:' + (dx+mx*i).toFixed(1)
           + 'em;top:' + Math.min(h-m*t[i], h).toFixed(1)
           + 'em;border:1px solid black'
           + (i == slot ? ';background:green' : '')
           + '">'
           + '&nbsp;'
           + '</div>' ;
    }
  for(var i=-9; i<=9; i++)
    {
      s += '<div style="left:0px;top:' + (h-m*i-0.5).toFixed(1)
           + 'em">'
           + (i >= 0 ? '&nbsp;' + i : i )
           + '</div>' ;
    }
  for(var i=1; i<200; i*=5)
    {
      x = dx + mx * time_to_slot(i*60) ;
      s += '<div style="left:' + x.toFixed(0) + 'em;top:' + (2*h) + 'em">'
           + i
           + 'min.</div>' ;
    }
  document.write(s) ;
}
""" % (Plugins.autoeval.autoeval.time_slot_base,
       Plugins.autoeval.autoeval.time_slot_power,
       )

import math
import questions
import statistics

def px(v, vmin, vmax, size):
    return '%6.2fem' % ( size * (v-vmin) / (vmax-vmin) )

def pos(y, x, text, tip=""):
    v = ('<div style="left:' + px(x, pos.xmin,pos.xmax,10)
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
            d = 'x'
            time_searching = -1
            if q is state.question:
                d = '<var class="me">x</var>'
            elif q.name in state.student.answers:
                a = state.student.answers[q.name]
                if a.answered:
                    d = '<var class="ok">x</var>'
                    time_searching = a.time_searching
                else:
                    if a.nr_asked:
                        d = '<var class="bad">x</var>'
            t.append((q.autoeval_level_average,
                      math.log(1 + q.student_time / q.student_given),
                      d, q.name
                      + '<script>histogram('
                      + repr(q.autoeval_level)
                      + ',' + repr(time_searching) + ')</script>'))

    for s in stats.all_students:
        if not hasattr(s, 'autoeval_level'):
            continue
        if s.the_number_of_given_questions == 0:
            continue
        if s.the_time_searching:
            t.append((s.autoeval_level,
                      math.log(1 + s.the_time_searching
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
        s.append(pos(i, 0, ("%2d" % i).replace(' ', '&nbsp;')))
    for i in t:
        s.append(pos(*i))

    return '\n'.join(s) + '<br>'*height + '&nbsp;'*40
