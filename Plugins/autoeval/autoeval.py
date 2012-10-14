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
'statmenu_bad': ('!executable',),
'statmenu_good': ('!executable',),
'statmenu_indice': ('!executable',),
'statmenu_nr_questions': ('!executable',),
'statmenu_rank': ('!executable',),
'statmenu_smiley': ('!executable',),
'statmenu_time': ('!executable',),
'comment': ('hide',),
'autoeval': ('executable',),
'autoeval_stats': ('executable',),
}


   * These is no more question choice for students.
"""

container = 'heart'
priority_display = 'question_answer'
priority_execute = 'question_answer'
acls = { }

N = 2
P = 1.1

import questions

def autoeval(question, student):
    """Update student en question level"""
    if not hasattr(question, 'autoeval_level'):
        question.autoeval_level = 0
    if not hasattr(student, 'autoeval_level'):
        student.autoeval_level = 0

    d = P**(question.autoeval_level - student.autoeval_level)
    if student.answered_question(question.name):
        d = (N-1) * d
    else:
        d = -P**(-d)
    student.autoeval_level += d
    question.autoeval_level -= d

def recompute_levels():
    """Replay all in order to recompute levels"""
    import student
    t = []
    for s in student.all_students():
        for a in s.answers.values():
            if a.question != 'None':
                t.append((a, s))
    t.sort(key=lambda x: x[0].first_time)
    for answer, a_student in t:
        if answer.question in questions.questions:
            autoeval(questions.questions[answer.question], a_student)
    recompute_levels.done = True

recompute_levels.done = False

def execute(state, dummy_plugin, argument):
    if not hasattr(state.student, "autoeval"):
        if not recompute_levels.done:
            recompute_levels()
        # Restore the current question because the TOMUSS server
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

    if state.question:
        question_done = state.student.answered_question(state.question.name)
    else:
        question_done = False

    if state.question is None or question_done:
        if getattr(state, 'autoeval_question', None):
            # The previous question was answered or givenup.
            # So we update statistics
            q = questions.questions[state.autoeval_question]
            autoeval(q, state.student)
        
        # FINIR CHOIX QUESTION APPROPRIEE
        for q in state.student.answerables():
            a = state.student.answer(q.name)
            if a.nr_asked == 0:
                break
        else:
            state.autoeval_question = None
            return '<p class="nomore_problem"></p>'

    if state.question:
        state.autoeval_question = state.question.name
    else:
        state.autoeval_question = None
    
    if state.question:
        if not question_done:
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

