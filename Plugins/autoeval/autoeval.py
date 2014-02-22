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

"""
This plugin allow to do an autoevaluation of questions and students level.

There is no more question choice for students.

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


"""

container = 'heart'
priority_display = 'question_answer'
priority_execute = 'question_answer'
acls = { }

# N specify an objective: the number of question to tell to the student
# before a good answer is done.
# N should be between 1.5 (2 good and one bad for 3 questions) and 3
N = 2

# Width of the level, do not modify.
P = 1.1

import time
import questions
import student

# Must be greater then 1.4 to avoid problems
time_slot_power = 1.5

# The minimum time slot in seconds
time_slot_base = 15

# The time slots are multiple of time_slot_base :
#                     less than 1
#    1                  ... time_slot_power
#    time_slot_power    ... time_slot_power**2
#    time_slot_power**2 ... time_slot_power**3
# ...
# With time_slot_power=1.5, time_slot_base=15 and 20 slots,
# the maximum answer time is 554 minutes
questions.Question.autoeval_level = None
questions.Question.autoeval_level_average = 0
student.Student.autoeval_level = 0
student.Student.autoeval_init = False

def autoeval(question, a_student, answer_time):
    """Update student en question level"""
    answer_time /= time_slot_base
    if question.autoeval_level is None:
        question.autoeval_level = [0]*20

    answered = a_student.answered_question(question.name)
    student_level = a_student.autoeval_level
    t = 1
    #print question.name, a_student.name, a_student.autoeval_level
    #print  '\t', ','.join("%4.1f" % i for i in question.autoeval_level)
    for i, v in enumerate(question.autoeval_level):
        d = P**(v - student_level)
        if answered and answer_time < t:
            d = (N-1) * d
        else:
            d = -P**(-d)
        if answer_time < t and answer_time > t / time_slot_power:
            # Modified only one time: in the good time slot
            a_student.autoeval_level += d
        question.autoeval_level[i] -= d
        t *= time_slot_power
    question.autoeval_level_average = (sum(question.autoeval_level)
                                       / len(question.autoeval_level))

def time_to_answer(question, student_level):
    """Returns the predicted time slot for a student with 'level'"""
    if question.autoeval_level is None:
        return -1
    for i, level in enumerate(question.autoeval_level):
        if student_level > level:
            return i
    return 1000 # Here if the question is impossible for this level

def recompute_levels():
    """Replay all in order to recompute levels"""
    t = []
    for s in student.all_students():
        for a in s.answers.values():
            if a.question != 'None':
                t.append((a, s))
    t.sort(key=lambda x: x[0].first_time)
    for answer, a_student in t:
        if answer.question in questions.questions:
            autoeval(questions.questions[answer.question], a_student,
                     answer.time_searching
                     )
    recompute_levels.done = True

recompute_levels.done = False

def execute(state, dummy_plugin, dummy_argument):
    q = None
    if not state.student.autoeval_init:
        if not recompute_levels.done:
            recompute_levels()
        if state.student.last_asked_question:
            q = questions.questions[state.student.last_asked_question]
        state.student.autoeval_init = True
    if state.question:
        if not state.question.answerable(state.student):
            state.question = None

    if state.question:
        question_done = state.student.answered_question(state.question.name)
    else:
        question_done = False

    if (q is None and state.question is None) or question_done:
        if getattr(state, 'autoeval_question', None):
            # The previous question was answered or givenup.
            # So we update statistics
            q = questions.questions[state.autoeval_question]
            autoeval(q, state.student,
                     (time.time() - state.student.answer(q.name).first_time)
                     )
        
        # Possible questions
        can = [q
               for q in state.student.answerables()
               if state.student.answer(q.name).nr_asked == 0
               ]
        if len(can) == 0:
            state.autoeval_question = None
            return '<p class="nomore_problem"></p>'

        can.sort(key = lambda q:
                     time_to_answer(q, state.student.autoeval_level))
        if can[0].autoeval_level < 0:
            # Never asked question
            q = can[0]
        else:
            q = can[len(can)//2]

    if state.question:
        state.autoeval_question = state.question.name
    else:
        state.autoeval_question = None

    before = '<p class="intro_problem"></p>'
    if state.question:
        if not question_done:
            return '''
<p class="give_solution"></p>
<form method="GET" action="question=None">
<button type="submit" style="background: #FBB">
<p class="giveup_problem"></p>
</button>
</form>
'''
        else:
            before = '<p class="autoeval_good"></p>'

    return before + '''
<form method="GET" action="question=%s">
<button type="submit">
<p class="start_problem"></p>
</button>
</form>
''' % q.name

