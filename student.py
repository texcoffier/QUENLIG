#!/usr/bin/env python

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
Manage the students.

Questions are referenced by their names.
Because with this way, there is nothing
to do when a module is reloaded and the questions instances
are destroyed and recreated.
"""

import time
import os
import questions # Only for nr_indices and any_questions
import utilities
import answer
import cgi
import configuration
import statistics
import sys
import random

def unquote(s):
    "Anybody has a better idea for this complex function?"
    return '\\'.join([w.replace("\\r","\r").replace("\\n","\n").replace("\\a", "") for w in s.split('\\\\')])

def quote(s):
    return s.replace('\\', '\\\\').replace('', '\\a').replace("\n", "\\n").replace("\r", "\\r")


def log_directory():
    return "Logs"

class Student:
    """Student work log"""

    def __init__(self, name):
        """Initialise student data or read the log file"""
        self.filename = name.translate(utilities.safe_ascii)
        self.seed = 1
        for c in name:
            self.seed *= ord(c)
        self.name = name.title()
        self.answers = {}
        self.file = os.path.join(log_directory(), self.filename)
        self.previous_time = 0
        self.previous_answer = 0
        self.previous_command = ""
        self.last_asked_question = ""
        self.answerable_any = False
        try:
            os.mkdir(self.file)
        except OSError:
            pass

        self.answerables_cache = None

        # Read log file
        try:
            f = open(os.path.join(self.file, 'log'), "r")
            content = f.readlines()
            f.close()
        except IOError:
            content = ()
                            
        for c in content:
            c = c[:-1].split("")
            decal = int(len(c) == 5) # In order to read old log files

            question_name = c[0]
            action_time = float(c[1])
            command = c[2+decal]
            try:
                value = unquote(c[3+decal])
            except:
                value = None
            answer = self.answer(question_name)
            answer.eval_action(action_time, command, value)
            self.update_time(action_time, answer, command)

    def destroy(self):
        import shutil
        try:
            shutil.rmtree(self.file)
        except OSError:
            pass
        for k in students:
            if students[k] == self:
                del students[k]
                break
        
    def a_href(self):
        return "<A HREF=\"?answered_other=%s\">%s</A>" % (
            self.filename, self.name )
            
    def answer(self, question):
        """Returns the answer from the question, create one the first time"""
        try:
            return self.answers[question]
        except KeyError:
            a = self.answers[question] = answer.Answer(question, self)
            return a

    def update_time(self, time, answer, command):
        if command == "comment":
            return
        dt = time - self.previous_time
        if dt < configuration.timeout_on_question:
            if self.previous_command in ("asked", "bad", "indice"):
                self.previous_answer.time_searching += dt
            else:
                self.previous_answer.time_after += dt
        self.previous_time = time
        self.previous_answer = answer
        self.previous_command = command

    # Returns some statistics, do not modify data structures.

    def number_of_good_answers(self):
        return len( self.answered_questions() )

    def number_of_bad_answers(self):
        return sum([a.nr_bad_answer for a in self.answers.values()])

    def number_of_comment(self):
        return sum([len(a.comments) for a in self.answers.values()])

    def number_of_given_indices(self):
        return sum([a.indice+1 for a in self.answers.values()])

    def number_of_given_questions(self):
        return len([s for s in self.answers.values() if s.nr_asked]) - 1

    def time_searching(self):
        return sum([a.time_searching for a in self.answers.values()])

    def time_after(self):
        return sum([a.time_after for a in self.answers.values()])

    def time_variance(self):
        t = [a.time_searching for a in self.answers.values() if a.answered]
        if t == []:
            return 0.
        m = sum(t) / len(t)
        return (sum([(a.time_searching - m) ** 2
                    for a in self.answers.values() if a.answered]) / len(t)
                ) ** 0.5

    def time_first(self):
        first_times = [a.first_time
                       for a in self.answers.values() if a.nr_asked]
        if first_times:
            return min(first_times)
        else:
            return 0

    def time_last(self):
        last_times = [a.last_time for a in self.answers.values()]
        if last_times:
            return max(last_times)
        else:
            return 0

    def answered_questions(self):
        """Returns the list of questions yet answered"""
        q = {}
        for a in self.answers.values():
            if a.answered != False:
                q[a.question] = a.answered ;
        return q

    def bad_answer_yet_given(self, question, answer):
        return answer in self.answer(question).bad_answers

    def answered_question(self, question):
        return self.answer(question).answered

    def nr_indices_question(self, question):
        return self.answer(question).indice+1

    def bad_answer_question(self, question):
        return self.answer(question).nr_bad_answer

    def resigned_question(self, question):
        return self.answer(question).resign

    def given_question(self, question):
        return self.answer(question).nr_asked != 0

    def answerables(self, any=False):
        if any or self.answerable_any:
            return questions.questions.values()

        if self.answerables_cache:
            return self.answerables_cache        

        t = questions.answerable(self.answered_questions())
        self.answerables_cache = t
        return t

    def answerables_typed(self):
        tt = []
        for i in self.answerables():
            a = self.answer(i.name)
            info = (
                ("", "current_question ")[ self.last_asked_question == i.name]+
                ("", "question_given ")[ a.nr_asked != 0 ] +
                ("", "indice_given ")[ a.indice != -1 ] +
                ("", "bad_answer_given ")[ a.nr_bad_answer > 0 ] +
                ("", "resigned ")[ a.resign ]
                )
            tt.append( (i, info) )
        tt.sort(lambda x,y: cmp(x[0].name, y[0].name))
        return tt
    
    def asked_questions(self):
        """Returns the list of question known by the student"""
        return [a.question for a in self.answers.values()]

    def last_answer(self, question):
        if self.answered_question(question):
            return self.answers[question].answered
        bad_answers = self.answers[question].bad_answers
        if bad_answers:
            return bad_answers[-1]
        else:
            return ""
        

    def question_given(self, question):
        """Returns True if the question was given to the student"""
        if self.answerable_any:
            return True
        else:
            return self.answer(question).nr_asked

    def get_indice(self, question):
        return self.answer(question).indice

    def __str__(self):
        return "\n".join([ str(a) for a in self.answers.values()])

    def stat(self, sort_column=0, html_class='', url=''):
        answers = [ [utilities.date_format(a.first_time),
                     a.answered != False, a.nr_asked, a.nr_bad_answer,
                     "%d/%d" % (a.indice+1, questions.nr_indices(a.question)),
                     len(a.comments), utilities.time_format(a.time_searching),
                     questions.a_href(a.question)
                     ]
                    for a in self.answers.values() if a.nr_asked ]

        return utilities.sortable_table(sort_column, answers,
                                        html_class=html_class, url=url)

    def points(self):
        p = 0
        for a in self.answers.values():
            if a.answered:
                x = 2 ** -len(a.bad_answers) - (a.indice + 1) * 0.1
                if x > 0:
                    p += x
        return p

    def answered_page(self, state):
        t = self.answers.values()
        t.sort(lambda x,y: cmp(x.last_time, y.last_time))
        
        s = ''
        for a in t:
            if a.nr_asked == 0:
                continue
            if a.question == "None":
                continue
            try:
                q = questions.questions[a.question]
            except KeyError:
                continue
            s += "<h3 class=\"short\">" + q.name + "</h3>"
            s += q.question(state)

            if a.indice >= 0 and a.indice < len(q.indices):
                s += utilities.list_format(q.indices[:a.indice+1])

            for b in a.bad_answers:
                number, message = self.check_answer(q, b, state)
                if message:
                    message = "<br>" + message
                s += utilities.div("bad_answer",
                                   utilities.answer_format(b) + \
                                   message)

            if a.answered:
                number, message = self.check_answer(q, a.answered, state)
                if message:
                    message = "<br>" + message
                s += utilities.div("good_answer",
                                   utilities.answer_format(a.answered) + \
                                   '<br>' + q.good_answer + message)

            for comment_time, comment_text in a.comments:
                s += utilities.div('comment',"<PRE>" + \
                                   cgi.escape(comment_text) + "</PRE>")

        return s

    def classement(self):
        stats = statistics.question_stats()
        return "%d/%d" % (stats.sorted_students.index(self)+1,
                          len(stats.sorted_students))

    def time_on_computer(self):
         self.answers.values()

    # Modify data structures and log actions

    # Line format in the log file :
    #	time action parameter
    # "indice" give the number of the question_indice_see given
    # "good" give the correct answer number indice (starting from 1)
    # "bad" give the bad answer itself.

    def log(self, question_name, command, value=""):
        action_time = time.time()
        answer = self.answer(question_name)
        answer.eval_action(action_time, command, value)
        self.update_time(action_time, answer, command)
        
        if value != None:
            value = '' + quote(value)
        else:
            value = ""

        f = open(os.path.join(self.file, 'log'), "a")
        f.write( "%s%f%s%s\n" % (question_name, action_time,
                                      command, value))
        f.close()

    def login(self, value):
        self.log("None", "login", value)

    def tell_question(self, question):
        """Last question displayed to the student"""
        if self.last_asked_question == question:
            return
        if self.last_asked_question \
           and self.answer(self.last_asked_question).answered == False:
            self.answer(self.last_asked_question).resign = True
        self.last_asked_question = question
        self.log(question, "asked")

    def good_answer(self, question, text):
        """The student has correctly answered the question."""
        self.answerables_cache = None
        self.log(question, "good", text)

    def bad_answer(self, question, text):
        """The student has wrongly answered the question."""
        self.log(question, "bad", text)

    def tell_indice(self, question):
        """Indice has been given to the student"""
        self.log(question, "indice")

    def add_a_comment(self, question, comment):
        """The student makes a comment."""
        if comment not in self.answer(question).comments:
            self.log(question, "comment", comment)

    ####################################################
    # All about the question contextual to the student.
    ####################################################

    def check_answer(self, question, answer, state):
        "'state' is a parameter needed for some questions"
        random.seed(self.seed)
        return question.check_answer(answer, state)

    def answer_commented(self, question_name, answer):
        random.seed(self.seed)
        return questions.questions[question_name].answer_commented(answer)

    def mailto(self, subject=None, body=""):
        if subject == None:
            subject = configuration.questions
        return "<A HREF=\"mailto:%s?subject=%s&body=%s\">%s</A>" % (
            '????',
            subject.replace("\"",'%27'),
            body.replace("\"",'%27').replace('\n','%0A'),
            self.name
            )


            
students = {}

def student(name):
    if not students.has_key(name):
        students[name] = Student(name)
    return students[name]

def all_students():
    """Read the directory content in order to return the student list"""
    return [student(student_name)
            for student_name in os.listdir(log_directory())]
    
