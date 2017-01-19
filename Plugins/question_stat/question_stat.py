#!/usr/bin/env python3
# -*- coding: latin-1 -*-
#    QUENLIG: Questionnaire en ligne (Online interactive tutorial)
#    Copyright (C) 2008 Thierry EXCOFFIER, Universite Claude Bernard
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

"""Displays some statistics about the current question."""

from QUENLIG import statistics
from QUENLIG import utilities

priority_display = 'question_bads'
acls = { 'Teacher': ('executable',) }

css_attributes = (
    '> TABLE > TR { vertical-align: top ; }',
    'P { margin: 0.1em ; }',
    )


def absolute_and_relative(v, n):
    if n:
        return "%d (%g)" % ( v, v/float(n) )
    else:
        return "%d" % v


def execute(state, plugin, argument):

    question = state.question
    if question == None:
        return

    statistics.question_stats()
    if not hasattr(question, "stats"):
        return # The question has been reloaded
    if question.stats.given == 0:
        return

    s = '<table><tr><td>'
    s += '<p class="given">%d</p>' % question.stats.given
    s += '<p class="view">%s</p>' % \
         absolute_and_relative(question.stats.view, question.stats.given)
    s += '</td><td>'
    s += '<p class="good">%s</p>' % \
         absolute_and_relative(question.stats.good, question.stats.given)
    s += '<p class="bad">%s</p>' % \
         absolute_and_relative(question.stats.bad, question.stats.given)
    s += '</td><td>'
    s += '<p class="indice">%s</p>' % \
         absolute_and_relative(question.stats.indice, question.stats.given)
    s += '<p class="time">%s (%s)</p>' % (
        utilities.time_format(question.student_time),
        utilities.time_format(question.student_time/
                              (0.1 + question.stats.given) ) )
    s += '<p class="comment">%s</p>' % \
         absolute_and_relative(question.stats.nr_comment, question.stats.given)
    s += '</td></tr></table>'

    return s





    




    

