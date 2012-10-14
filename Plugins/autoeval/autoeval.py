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

# A FINIR : mettre a jour le niveau des gens/question
#           afficher les niveaux personnes et questions

"""
This plugin allow to do an autoevaluation of questions and students.

To make it work, the ACLS: Students/SESSION/Logs/Student/acls
Must be set to :

{
'question_bad': ('!executable',),
'map': ('!executable',),
'answered': ('!executable',),
'about': ('!executable',),
'about_questions': ('!executable',),
'about_time': ('!executable',),
'about_version': ('!executable',),
'action': ('!executable',),
'question_before': ('!executable',),
'question_good': ('!executable',),
'question_indices': ('!executable',),
'question_required': ('!executable',),
'questions': ('!executable',),
'questions_nomore': ('!executable',),
'questions_shuffle': ('!executable',),
'session_duration': ('!executable',),
'session_start': ('!executable',),
'session_stop': ('!executable',),
'statmenu': ('!executable',),
'statmenu_bad': ('!executable',),
'statmenu_good': ('!executable',),
'statmenu_indice': ('!executable',),
'statmenu_nr_questions': ('!executable',),
'statmenu_rank': ('!executable',),
'statmenu_smiley': ('!executable',),
'statmenu_time': ('!executable',),
'comment': ('hide',),
'autoeval': ('executable',),
}


   * These is no more question choice for students.
"""

container = 'heart'
priority_display = 'question_answer'
priority_execute = '-question'
acls = { }

import questions

def execute(state, plugin, argument):
    if not hasattr(state.student, "autoeval"):
        # Restore the current question if the TOMUSS server
        # has been restarted.
        first_times = [(a.first_time, a.question)
                       for a in state.student.answers.values()]
        if first_times:
            last_asked_question = max(first_times)[1]
            if last_asked_question != "None":
                state.question = questions.questions[last_asked_question]
        state.student.autoeval = True
    if argument == 'stop':
        state.question = None
    if state.question:
        if not state.question.answerable(state.student):
            state.question = None

    if state.question is None:
        # FINIR CHOIX QUESTION APPROPRIEE
        for q in state.student.answerables():
            a = state.student.answer(q.name)
            if a.nr_asked == 0:
                break
        else:
            return '<p class="nomore_problem"></p>'
    
    if state.question:
        return '''
<p class="give_solution"></p>
<form method="GET" action="autoeval=stop">
<button type="submit">
<p class="giveup_problem"></p>
</button>
</form>
'''
    
    return '''<p class="intro_problem"></p>
<form method="GET" action="question=%s">
<button type="submit">
<p class="start_problem"></p>
</button>
</form>
''' % q.name

