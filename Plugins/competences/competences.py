#!/usr/bin/env python
# -*- coding: latin-1 -*-
#    QUENLIG: Questionnaire en ligne (Online interactive tutorial)
#    Copyright (C) 2015 Thierry EXCOFFIER, Universite Claude Bernard
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

"""The questions box, it displays the list of competences."""

import json
import collections
import questions
import utilities
import configuration

priority_display = 'identity'
priority_execute = 'question' # In order to emphasis current question
css_attributes = (
    "A.max_descendants { font-weight: bold; }",
    "A.question_given  {color:#888;}",
    "A.bad_answer_given{color:#F00;}",
    "A.answered        {color:#040;}",
    "A.not_seen        {color:#00F;}",
    "A.perfect_answer  {color:#0A0;}",
    "A.indice_given    {font-style:italic;}",
    "A.current_question{text-decoration:underline;}",
    "A.not_answerable  {color:#DDD;}",
    "A.highlight  { background: black; color: white;text-decoration: blink; }",
    "VAR { font-style: normal }",
    "/.opacity_feedback { opacity: 0.6 }",
    "/.opacity_feedback:hover { opacity: 1 }",
    ".nice_results { display: inline-block; vertical-align: bottom; border-spacing: 1px }",
    """CANVAS.opacity_feedback:hover, .openclose:hover CANVAS, .nice_results:hover CANVAS {
    animation-duration: 0.6s;
    animation-name: zoom_in;
    -webkit-animation-duration: 0.6s;
    -webkit-animation-name: zoom_in;
    transform: scale(2,2) ;
    position: relative ;
    z-index: 1 ;
    }
@keyframes zoom_in {
    from { transform: scale(1,1) ; }
    to { transform: scale(2,2)  ; }
}
@-webkit-keyframes zoom_in {
    from { transform: scale(1,1) ; }
    to { transform: scale(2,2)  ; }
}""",
#     """.openclose CANVAS, .nice_results CANVAS {
#     animation-duration: 0.2s;
#     animation-name: zoom_out;
#     transform: scale(1,1) ;
#     }
# @keyframes zoom_out {
#     from { transform: scale(2,2) ; }
#     to { transform: scale(1,1)  ; }
# }""",
    ".nice_results TD { width: 5px; height: 5px; padding: 0px ; }",
    "/.title_bar DIV.competences .nice_results TD { width: 9px; height: 9px}",
    "/.title_bar DIV.competences .nice_results { border-spacing: 2px;}",
    ".nice_results .good    { background: #00F ; }",
    ".nice_results .bad     { background: #F00 ; }",
    ".nice_results .perfect { background: #0F0 ; }",
    "#competences { width: 15em }",
    '.box_title { padding-top: 1em; padding-bottom: 1em; }',
    )
acls = {}

javascript = utilities.read("Plugins/competences/competences.js")
if javascript == '':
    javascript = utilities.read(configuration.root
                                + "/Plugins/competences/competences.js")

def execute(state, plugin, dummy_argument):
    answerables = state.student.answerables_typed(any=True)
    q = []
    for info in answerables:
        info = list(info)
        info.append(tuple(info[0].competences))
        info.append(info[0].level)
        info.append(info[0].get_nr_versions())
        info.append(info[0].get_nr_versions())
        info[0] = info[0].name
        q.append(info)
    question = state.question and state.question.name or ''
    return '<script>display_competences(%s,%s);</script>' % (
        json.dumps(q), json.dumps(question))
