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

"""Display the mean time used by student to answer the current question."""

import time

priority_display = 'title_time'
priority_execute = 'question_answer'
acls = { 'Default': ('executable',) }
css_attributes = (
    "#ttl { font-size: 70%; font-weight: bold }",
    )

def execute(state, plugin, argument):
    if (state.question
        and state.question.maximum_time
        and not state.student.answered_question(state.question.name)
        ):
        if not state.question.answerable(state.student):
            return
        t = state.student.time_first(state.question.name)
        if t:
            t = time.time() - t # Used time
            return '''<var id="ttl">%d</var>
<script><!--
setInterval(
function() {
    var t = document.getElementById("ttl") ;
    t.innerHTML = Number(t.innerHTML) - 1 ;
}, 1000) ;
--></script>
''' % (state.question.maximum_time - t)
        
