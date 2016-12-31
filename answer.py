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
from . import configuration
from . import questions

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
        self.current_time_searching = 0 # The time spend searching the answer
        self.current_time_after = 0  # The time spend without onscreen question
        self.first_time = 0       # The question first display date
        self.comments = []        # The comment sent by the student
        self.bad_answers = []     # The bad answers given by the student
        self.full_bad_answers = []# Random value + bad answer
        self.resign = False       # The student saw the question in the past
        self.last_answer = ''     # The last student answer
        self.grades = {}          # The teachers grades
        self.why = {}             # The teachers comments on answer
        self.nr_erase = 0         # #erase to change the question parameters
        self.erase_time = 0       # Last erase time
        self.was_erasable = True
        self.persistent_random = {} # For Random and Choice
        self.random_history = []
        self.random_max = {}
        self.random_next = {}
        self.answer_times = []
        self.good_answer_times = []

    def erasable(self, action_time):
        return (len(self.answer_times) == 0
                or action_time - self.answer_times[-1]
                    > configuration.erasable_after
                )

    def __str__(self):
        return "%d %d %d %d %g %s %d" % (self.answered != False, self.nr_asked, self.nr_bad_answer, self.indice, self.time_searching+self.time_after, self.question, len(self.comments))


commands = {}

class CreateInstance(type):
    def __init__(cls, name, bases, dct):
        super(CreateInstance, cls).__init__(name, bases, dct)
        cls()

class Command(object, metaclass=CreateInstance):
    question = True
    value = True
    def __init__(self):
        self.name = self.__class__.__name__.split('_')[-1]
        commands[self.name] = self
    def format(self, action_time, question, value):
        t = [time.strftime("%Y%m%d%H%M%S", time.localtime(action_time)),
             self.name]
        if self.question:
            t.append(question)
        if self.value:
            t.append(value)
        return "(%s)" % (','.join(repr(v)
                                  for v in t))

####################
# Question + Value
####################

class Command_good(Command):
    def parse(self, student, action_time, question_name, answer, value):
        answer.answered = value
        answer.nr_good_answer += 1
        if answer.was_erasable:
            # It is possible to NOT be here if the 'erasable_after' value
            # has been augmented after the students started to work
            answer.good_answer_times.append(action_time - student.last_time
                                            + answer.current_time_searching)
            t = questions.questions[question_name].perfect_time
            if answer.good_answer_times[-1] < t:
                answer.nr_perfect_answer += 1
        answer.answer_times.append(action_time)

class Command_bad(Command):
    def parse(self, student, action_time, question_name, answer, value):
        answer.answered = False # Needed for 'any_question'
        answer.nr_bad_answer += 1
        answer.bad_answers.append(value)
        answer.full_bad_answers.append((answer.persistent_random, value))
        answer.answer_times.append(action_time)

class Command_comment(Command):
    def parse(self, student, action_time, question_name, answer, value):
        answer.comments.append((action_time, value))

class Command_grade(Command):
    def parse(self, student, action_time, question_name, answer, value):
        teacher, grade = value
        if answer.grades.get(teacher, None) == grade: # Yet stored
            return True
        answer.grades[teacher] = grade

class Command_why(Command):
    def parse(self, student, action_time, question_name, answer, value):
        answer.why[value[0]] = value[1]

class Command_random(Command):
    def parse(self, student, action_time, question_name, answer, value):
        answer.persistent_random[value[0]] = value[1]

####################
# Only question
####################

class Command_indice(Command):
    value = False
    def parse(self, student, action_time, question_name, answer, dummy_value):
        answer.indice += 1

class Command_asked(Command_indice):
    def parse(self, student, action_time, question_name, answer, dummy_value):
        answer.nr_asked += 1
        if (student.last_asked_question
            and student.answer(student.last_asked_question
                               ).answered == False):
            student.answer(student.last_asked_question).resign = True
        if answer.first_time == 0:
            answer.first_time = action_time
        student.last_asked_question = question_name

class Command_erase(Command_indice):
    def parse(self, student, action_time, question_name, answer, dummy_value):
        answer.was_erasable = answer.erasable(action_time)
        answer.answered = False
        answer.indice = -1
        answer.last_answer = ''
        answer.nr_erase += 1
        answer.erase_time = action_time
        answer.bad_answers = []
        answer.random_history.append(answer.persistent_random)

        # Add 1 to every random value
        for k, v in answer.persistent_random.items():
            if k in answer.random_max:
                answer.random_next[k] = (v + 1) % answer.random_max[k]

        if answer.random_next in answer.random_history:
            # Search a random dict value never used
            for k in sorted(answer.persistent_random):
                if k not in answer.random_max:
                    continue
                save = answer.random_next[k]
                answer.random_next[k] = (
                    answer.random_next[k] + 1 ) % answer.random_max[k]
                if answer.random_next not in answer.random_history:
                    break
                answer.random_next[k] = save
            else:
                # All possible cases done, reset the history
                answer.random_history = []

        answer.persistent_random = {}
        answer.current_time_after = 0
        answer.current_time_searching = 0

####################
# Only value
####################

class Command_globalcomment(Command):
    question = False
    def parse(self, student, action_time, question_name, answer, value):
        answer.comments.append((action_time, value))

class Command_login(Command_globalcomment):
    def parse(self, student, action_time, question_name, answer, value):
        student.logs.append((action_time, value.split(' ')[0]))
