#    QUENLIG: Questionnaire en ligne (Online interactive tutorial)
#    Copyright (C) 2005-2006 Thierry EXCOFFIER, Universite Claude Bernard
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

import configuration
import questions

student_commands = set(("good", "indice", "bad", "asked",
                        "comment", "login", "erase"))
teacher_commands = set(("grade", "why"))

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
        self.last_time = 0        # The question interaction (user or teacher)
        self.resign = False       # The student saw the question in the past
        self.last_answer = ''     # The last student answer
        self.grades = {}          # The teachers grades
        self.why = {}             # The teachers comments on answer
        self.nr_erase = 0         # #erase to change the question parameters
        self.erase_time = 0       # Last erase time
        self.answer_times = []

    def eval_action(self, action_time, command, value):
        """Return True if the action do not need to be recorded in log"""
        if command in student_commands:
            self.last_time = action_time
            self.last_command = command
        if self.first_time == 0:
            self.first_time = action_time
        if command == "good":
            self.answered = value
            t = questions.questions[self.student.last_asked_question
                                   ].perfect_time
            if action_time - max(self.first_time, self.erase_time) < t:
                self.nr_perfect_answer += 1
            else:
                self.nr_good_answer += 1
            self.answer_times.append(action_time)
        elif command == "indice" :
            self.indice += 1
        elif command == "bad" :
            self.answered = False # Needed for 'any_question'
            self.nr_bad_answer += 1
            self.bad_answers.append(value)
            self.answer_times.append(action_time)
        elif command == "asked" :
            self.nr_asked += 1
            student = self.student
            if (student.last_asked_question
                and student.answer(student.last_asked_question
                                   ).answered == False):
                student.answer(student.last_asked_question).resign = True
            student.last_asked_question = self.question
        elif command == "comment" :
            self.comments.append((action_time, value))
        elif command == "login" :
            self.student.logs.append((action_time,value.split(' ')[0]))
        elif command == "grade" :
            teacher, grade = value.split(',')
            if self.grades.get(teacher, None) == grade: # Yet stored
                return True
            self.grades[teacher] = grade
        elif command == "why" :
            teacher, comment = value.split('\002')
            self.why[teacher] = comment
        elif command == "erase" :
            self.answered = False
            self.indice = -1
            self.last_answer = ''
            self.nr_erase += 1
            self.erase_time = action_time
            self.bad_answers = []
        else:
            raise ValueError("Unknown action %s in %s" % (command, self.student))

    def end_of_action(self, time, command):
        """Called on the next event.
        So we can compute the previous one duration.
        """
        if command not in student_commands:
            return
        if self.nr_erase:
            return # No more count time on retry
        dt = time - self.last_time
        if dt < configuration.timeout_on_question:
            if self.last_command in ("asked", "bad", "indice"):
                self.time_searching += dt
            elif self.last_command in ("good", ):
                self.time_after += dt
            else:
                # comment
                # erase
                # login
                pass
        
    def __str__(self):
        return "%d %d %d %d %g %s %d" % (self.answered != False, self.nr_asked, self.nr_bad_answer, self.indice, self.time_searching+self.time_after, self.question, len(self.comments))
