#!/usr/bin/env python
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
Manage the students.

Questions are referenced by their names.
Because with this way, there is nothing
to do when a module is reloaded and the questions instances
are destroyed and recreated.
"""

import time
import os
import cgi
import random
import ast
import collections
import questions # Only for nr_indices and any_questions
import utilities
import answer
import configuration
import statistics

def unquote(s):
    "Anybody has a better idea for this complex function?"
    return '\\'.join([w.replace("\\r","\r").replace("\\n","\n").replace("\\a", "") for w in s.split('\\\\')])

def quote(s):
    return s.replace('\\', '\\\\').replace('', '\\a').replace("\n", "\\n").replace("\r", "\\r")

def log_directory():
    return "Logs"

def translate_log(filename):
    """Translate old log format to the new one"""
    f = open(filename, "r")
    content = f.readlines()
    f.close()
    t = []
    for c in content:
        c = unicode(c[:-1], "latin-1").split("")
        decal = int(len(c) == 5) # In order to read old log files

        question = c[0]
        action_time = float(c[1])
        command = c[2+decal]
        try:
            value = unquote(c[3+decal])
        except:
            value = None
        if question == "None" and command == "comment":
            command = "globalcomment"
        t.append( answer.commands[command].format(action_time,question,value) )
    f = open(filename + '.py', "w")
    f.write('\n'.join(t) + '\n')
    f.close()

class Student:
    """Student work log"""
    writable = True

    def __init__(self, name, stop_loading=lambda x: False):
        """Initialise student data or read the log file"""
        self.filename = name.translate(utilities.safe_ascii)
        self.seed = abs(hash(name))
        self.name = name.title()
        self.answers = {}
        self.file = os.path.join(log_directory(), self.filename)
        self.last_time = 0
        self.previous_answer = self.answer('None')
        self.last_command = ""
        self.last_asked_question = ""
        self.answerable_any = False
        self.logs = []
        # The informations dict is filled by your plugins.
        # Do not fill it here.
        # Recommended keys : mail, firstname, surname
        # The mail will be automaticaly used if found.
        self.informations = {}
        try:
            os.mkdir(self.file)
        except OSError:
            pass

        self.answerables_cache = None
        self.read_log(stop_loading)

    def read_log(self, stop_loading):
        new_log = os.path.join(self.file, 'log.py')
        if not os.path.exists(new_log):
            old_log = os.path.join(self.file, 'log')
            if os.path.exists(old_log):
                translate_log(old_log)
            else:
                return
        f = open(new_log, "r")
        for line in f:
            self.eval_line(line)
            if stop_loading(self):
                self.writable = False
                break
        f.close()

    def eval_line(self, line):
        line = [v.encode('latin-1') for v in ast.literal_eval(line)]
        action_time = time.mktime(time.strptime(line.pop(0), "%Y%m%d%H%M%S"))
        command = answer.commands[line.pop(0)]
        if command.question:
            question_name = line.pop(0)
            if question_name not in questions.questions:
                return
        else:
            question_name = "None"
        the_answer = self.answer(question_name)
        command.parse(self, action_time, question_name, the_answer, *line)
        if self.last_time:
            dt = action_time - self.last_time
            if dt < configuration.timeout_on_question:
                if (self.last_command == 'good'
                    or self.previous_answer.nr_erase != 0):
                    self.previous_answer.time_after += dt
                else:
                    self.previous_answer.time_searching += dt
        self.previous_answer = the_answer
        self.last_command = command.name
        self.last_time = action_time

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
        return len([s for s in self.answers.values() if s.nr_asked])

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

    def time_first(self, question=None):
        if question:
            return self.answer(question).first_time
        first_times = [a.first_time
                       for a in self.answers.values() if a.nr_asked]
        if first_times:
            return min(first_times)
        else:
            return 0

    def time_last(self):
        return self.last_time

    def answered_questions(self):
        """Returns the list of questions yet answered"""
        q = {}
        for a in self.answers.values():
            if a.nr_good_answer != 0:
                q[a.question] = a.answered or ""
        return q

    def bad_answer_yet_given(self, question, answer):
        self.answer(question).last_answer = answer
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

        t = questions.answerable(self.answered_questions(), self)
        self.answerables_cache = t
        return t

    def answerables_typed(self, any=False):
        tt = []
        answerable_set = set(self.answerables())
        for i in self.answerables(any=any):
            a = self.answer(i.name)
            info = (
                ("", "current_question ")[ self.last_asked_question == i.name]+
                ("", "question_given ")[ a.nr_asked != 0 ] +
                ("", "not_seen ")[ a.nr_asked == 0 ] +
                ("", "indice_given ")[ a.indice != -1 ] +
                ("", "bad_answer_given ")[ a.nr_bad_answer > 0 ] +
                ("", "perfect_answer ")[ a.nr_perfect_answer > 0 ] +
                ("", "resigned ")[ a.resign ] +
                (i not in answerable_set and a.nr_good_answer == 0
                 and "not_answerable " or "") +
                ("", " answered ")[int(a.answered != False)]
                )
            tt.append( (i, info, a.nr_bad_answer, a.nr_good_answer,
                        a.nr_perfect_answer) )
        tt.sort(key=lambda x: x[0].name)
        return tt
    
    def asked_questions(self):
        """Returns the list of question known by the student"""
        return [a.question for a in self.answers.values()]

    def last_answer(self, question):
        q = self.answers[question]
        if q.last_answer:
            return q.last_answer
        if self.answered_question(question):
            return q.answered or ''
        if q.bad_answers:
            return q.bad_answers[-1]
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
                     a.nr_good_answer != 0, a.nr_asked, a.nr_bad_answer,
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
            if a.nr_good_answer != 0:
                x = 2 ** -len(a.bad_answers) - (a.indice + 1) * 0.1
                if x > 0:
                    p += x
        return p

    def grading_teachers(self):
        teachers = set()
        for a in self.answers.values():
            teachers.update(a.grades)
        return teachers

    def grades(self):
        p = ''
        summed = collections.defaultdict(int)
        for a in self.answers.values():
            if a.grades:
                p += repr(a.grades)
            for teacher, grade in a.grades.items():
                summed[teacher] += float(grade)
        return summed

    def init_seed(self, question):
        """Set the random seed for the question"""
        random.seed(self.seed + self.answers[question].nr_erase)

    def answered_page(self, state):
        t = self.answers.values()
        t.sort(lambda x,y: cmp(x.first_time, y.first_time))
        
        s = ''
        none = None
        saved_question = state.question
        for a in t:
            if a.question == "None":
                none = a
                continue
            if a.nr_asked == 0:
                continue
            try:
                q = questions.questions[a.question]
                state.question = q
            except KeyError:
                continue
            import Plugins.question_change_answer.question_change_answer
            more = Plugins.question_change_answer.question_change_answer.add_a_link(state, q)
            s += "<h3 class=\"short\">" + q.name + more + "</h3>"
            self.init_seed(a.question)
            question_text = q.question(state)
            s += question_text.split('{{{')[0]

            if a.indice >= 0 and a.indice < len(q.indices):
                s += utilities.list_format(q.indices[:a.indice+1])

            def answer_format(answer):
                if '{{{' in question_text:
                    ss = ''
                    for i in question_text.split('{{{')[1:]:
                        j = i.split('}}}')
                        if j[0] in answer:
                            ss += '<br>' + utilities.answer_format(j[1])
                else:
                    ss = utilities.answer_format(answer)
                return ss
                
            for b in a.bad_answers:
                number, message = self.check_answer(b, state)
                if message:
                    message = "<br>" + message
                s += utilities.div("bad_answer",
                                   answer_format(b) + message)

            if a.answered:
                try:
                    number, message = self.check_answer(a.answered, state)
                except IOError:
                    message = '???BUG???'
                if message:
                    message = "<br>" + message
                    
                s += utilities.div("good_answer",
                                   answer_format(a.answered) + \
                                   '<br>' + q.good_answer + message)
                if state.current_role == 'Grader':
                    s += '<br>' + repr(a.grades)
                    s += '<br>' + ' '.join(
                        time.strftime("%H:%M:%S", time.localtime(t))
                        for t in a.answer_times)

            for comment_time, comment_text in a.comments:
                s += utilities.div('comment',"<PRE>" + \
                                   cgi.escape(comment_text) + "</PRE>")

            import Plugins.question_correction.question_correction
            s += Plugins.question_correction.question_correction.add_a_link(state, q)
        state.question = saved_question

                
        if none and none.comments:
            s += "<h3 class=\"short\">?</h3>"
            for comment_time, comment_text in none.comments:
                s += utilities.div('comment',"<PRE>" + \
                                   cgi.escape(comment_text) + "</PRE>")
            


        return s

    def classement(self):
        stats = statistics.question_stats()
        return "%d/%d" % (stats.sorted_students.index(self)+1,
                          len(stats.sorted_students))

    # Modify data structures and log actions

    def log(self, question_name, command, value=""):
        if not self.writable:
            return
        question_name = unicode(question_name, "latin-1")
        value = unicode(value, "latin-1")
        v = answer.commands[command].format(time.time(), question_name, value)
        if self.eval_line(v):
            return # Do not store: unchanged value
        f = open(os.path.join(self.file, 'log.py'), "a")
        f.write(v + "\n")
        f.close()

    def set_grade(self, question, grade):
        if question in self.answers:
            self.log(question, "grade", grade)

    def set_why(self, question, comment):
        if question in self.answers:
            self.log(question, "why", comment)
            
    def login(self, value):
        self.log("None", "login", value)

    def tell_question(self, question):
        """Last question displayed to the student"""
        if self.last_asked_question == question:
            return
        self.log(question, "asked")

    def good_answer(self, question, text):
        """The student has correctly answered the question."""
        self.answerables_cache = None
        self.log(question, "good", text)

    def bad_answer(self, question, text):
        """The student has wrongly answered the question."""
        if questions.questions[question]:
            self.answerables_cache = None
        self.log(question, "bad", text)

    def tell_indice(self, question, indice):
        """Indice has been given to the student"""
        if indice > self.get_indice(question)+1:
            self.log(question, "indice")

    def add_a_comment(self, question, comment):
        """The student makes a comment."""
        for date_comment in self.answer(question).comments:
            if date_comment[1] == comment:
                return
        if question == 'None':
            self.log(question, "globalcomment", comment)
        else:
            self.log(question, "comment", comment)

    def persistent_random(self, state, question, maximum, seed=0):
        if not state:
            return 0
        a = self.answer(question)
        if a.persistent_random is None:
            a.persistent_random = (self.seed + a.nr_erase + seed ) % maximum
            self.log(question, "random", str(a.persistent_random))
        return a.persistent_random

    def erase(self, question):
        if question in self.answers:
            self.log(question, "erase", '')

    ####################################################
    # All about the question contextual to the student.
    ####################################################

    def check_answer(self, answer, state):
        "'state' is a parameter needed for some questions"
        self.init_seed(state.question.name)
        return state.question.check_answer(answer, state)

    def answer_commented(self, question_name, answer, state):
        self.init_seed(state.question.name)
        return questions.questions[question_name].answer_commented(answer,state)

    def mailto(self, subject=None, body=""):
        if subject == None:
            subject = configuration.questions
        return "<A HREF=\"mailto:%s?subject=%s&body=%s\">%s</A>" % (
            self.informations.get('mail', self.filename),
            subject.replace("\"",'%27'),
            body.replace("\"",'%27').replace('\n','%0A'),
            self.name
            )


            
students = {}
stop_loading_default = lambda x: False

def student(name):
    if not students.has_key(name):
        students[name] = Student(name, stop_loading=stop_loading_default)
    return students[name]

def all_students():
    """Read the directory content in order to return the student list"""
    return [student(student_name)
            for student_name in os.listdir(log_directory())]


def dump():
    t = []
    for s in all_students():
        t.append(' '.join(['\t%s:%s\n' %(k, v)
                           for k, v in s.__dict__.items()
                           ]))
    return '\n'.join(t)

               
