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
    "A.answered        {color:#0A0;}",
    "A.not_seen        {color:#00F;}",
    "A.perfect_answer  {background:#CFC; color: black}",
    "A.indice_given    {font-style:italic;}",
    "A.current_question{text-decoration:underline;}",
    "A.not_answerable  {color:#DDD;}",
    "A.highlight  { background: black; color: white;text-decoration: blink; }",
    ".nice_results { display: inline-block; vertical-align: bottom; border-spacing: 1px }",
    ".nice_results TD { width: 5px; height: 5px; padding: 0px ; }",
    "/.title_bar DIV.competences .nice_results TD { width: 9px; height: 9px}",
    "/.title_bar DIV.competences .nice_results { border-spacing: 2px;}",
    ".nice_results .good    { background: #00F ; }",
    ".nice_results .bad     { background: #F00 ; }",
    ".nice_results .perfect { background: #0F0 ; }",
    "#competences { width: 15em }",
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
        info[0] = unicode(info[0].name, 'latin-1')
        q.append(info)
    if state.question and state.student.answered_question(state.question.name):
        state.plugins_dict['title'].value += '<div class="competences" style="display:inline"><a class="tips" href="?erase=1"><script>document.write(char_recycle)</script><span class="erase"></span></a></div>'
    question = state.question and unicode(state.question.name, 'latin-1') or ''
    return '<script>display_competences(%s,%s);</script>' % (
        json.dumps(q), json.dumps(question))
