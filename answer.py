#    QUENLIG: Questionnaire en ligne (Online interactive tutorial)
#    Copyright (C) 2005-2015 Thierry EXCOFFIER, Universite Claude Bernard
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
All this is not working nicely if the student use multiple tab
on the same question.
"""

import time
import configuration
import questions

class Answer:
    """These objects track how a student answer to the question"""
    def __init__(self, question, student):
        self.question = question  # The question answered
        self.student = student    # The answering student
        self.answered = False     # The question is not correctly answered
        self.indice = -1          # No indices have been asked by the student
        self.nr_bad_answer = 0    # The student did not give bad answers
        self.nr_good_answer = 0   # Number of good answer
        self.nr_perfect_answer = 0 # Number of good and fast answer
        self.nr_asked = 0         # The number of display of the question text
        self.time_searching = 0   # The time spend searching the answer
        self.time_after = 0       # The time spend without onscreen question
        self.first_time = 0       # The question first display date
        self.comments = []        # The comment sent by the student
        self.bad_answers = []     # The bad answers given by the student
        self.resign = False       # The student saw the question in the past
        self.last_answer = ''     # The last student answer
        self.grades = {}          # The teachers grades
        self.why = {}             # The teachers comments on answer
        self.nr_erase = 0         # #erase to change the question parameters
        self.erase_time = 0       # Last erase time
        self.answer_times = []

    def __str__(self):
        return "%d %d %d %d %g %s %d" % (self.answered != False, self.nr_asked, self.nr_bad_answer, self.indice, self.time_searching+self.time_after, self.question, len(self.comments))


commands = {}

class CreateInstance(type):
    def __init__(cls, name, bases, dct):
        super(CreateInstance, cls).__init__(name, bases, dct)
        cls()

class Command(object):
    __metaclass__ = CreateInstance
    question = True
    def __init__(self):
        self.name = self.__class__.__name__.split('_')[-1]
        commands[self.name] = self
    def args(self, question, value):
        return (question, value)
    def format(self, action_time, question, value):
        return "('%s','%s',%s)" % (
            time.strftime("%Y%m%d%H%M%S", time.localtime(action_time)),
            self.name,
            ','.join(repr(v)
                     for v in self.args(question, value)
                     ))

####################
# Question + Value
####################

class Command_good(Command):
    def parse(self, student, action_time, question_name, answer, value):
        answer.answered = value
        t = questions.questions[question_name].perfect_time
        answer.nr_good_answer += 1
        if action_time - max(answer.first_time, answer.erase_time) < t:
            answer.nr_perfect_answer += 1
        answer.answer_times.append(action_time)

class Command_bad(Command):
    def parse(self, student, action_time, question_name, answer, value):
        answer.answered = False # Needed for 'any_question'
        answer.nr_bad_answer += 1
        answer.bad_answers.append(value)
        answer.answer_times.append(action_time)

class Command_comment(Command):
    def parse(self, student, action_time, question_name, answer, value):
        answer.comments.append((action_time, value))

class Command_grade(Command):
    def args(self, question, value):
        val = value.split(',')
        return (question, val[0], val[1])
    def parse(self, student, action_time, question_name, answer,
              teacher, grade):
        if answer.grades.get(teacher, None) == grade: # Yet stored
            return True
        answer.grades[teacher] = grade

class Command_why(Command):
    def args(self, question, value):
        val = value.split('\002')
        return (question, val[0], val[1])
    def parse(self, student, action_time, question_name, answer,
              teacher, comment):
        answer.why[teacher] = comment

####################
# Only question
####################

class Command_indice(Command):
    def args(self, question, value):
        return (question,)
    def parse(self, student, action_time, question_name, answer):
        answer.indice += 1

class Command_asked(Command_indice):
    def parse(self, student, action_time, question_name, answer):
        answer.nr_asked += 1
        if (student.last_asked_question
            and student.answer(student.last_asked_question
                               ).answered == False):
            student.answer(student.last_asked_question).resign = True
        if answer.first_time == 0:
            answer.first_time = action_time
        student.last_asked_question = question_name

class Command_erase(Command_indice):
    def parse(self, student, action_time, question_name, answer):
        answer.answered = False
        answer.indice = -1
        answer.last_answer = ''
        answer.nr_erase += 1
        answer.erase_time = action_time
        answer.bad_answers = []

####################
# Only value
####################

class Command_globalcomment(Command_indice):
    question = False
    def args(self, question, value):
        return (value,)
    def parse(self, student, action_time, question_name, answer, value):
        answer.comments.append((action_time, value))

class Command_login(Command_globalcomment):
    def parse(self, student, action_time, question_name, answer, val):
        student.logs.append((action_time, val.split(' ')[0]))
