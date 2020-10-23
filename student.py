#!/usr/bin/env python3
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
import html
import random
import ast
import collections
import hashlib
import threading
import sys
import contextlib
from . import questions # Only for nr_indices and any_questions
from . import utilities
from . import answer
from . import configuration

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
        c = str(c[:-1], "latin-1").split("") # LATIN-1: OK
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
        if command == 'grade':
            value = value.split(",")
            value = (value[0], int(value[1]))
        elif command == 'why':
            value = tuple(value.split("\002"))
        t.append( answer.commands[command].format(action_time,question,value) )
    f = open(filename + '.py', "w")
    f.write('\n'.join(t) + '\n')
    f.close()

def static_hash(txt):
    return int(hashlib.md5(txt.encode('utf-8')).hexdigest(), 16)

secs_cache = {}
def secs(txt):
    day = secs_cache.get(txt[:8], None)
    if day is None:
        day = secs_cache[txt[:8]] = time.mktime(time.strptime(txt[:8],"%Y%m%d"))
    return day + int(txt[8:10])*3600 + int(txt[10:12])*60 + int(txt[12:])

def log_age(name):
    if name[0].isupper():
        return 0 # For roles
    log = os.path.join(log_directory(),
                       name.translate(utilities.safe_ascii),
                       'log.py')
    if os.path.exists(log):
        return time.time() - os.path.getmtime(log)
    log = log[:-3]
    if os.path.exists(log):
        return time.time() - os.path.getmtime(log)
    return 999999 # No file, so do not try to load

class Student:
    """Student work log"""
    writable = True

    def __init__(self, name, stop_loading=lambda x: False):
        """Initialise student data or read the log file"""
        self.filename = name.translate(utilities.safe_ascii)
        self.seed = static_hash(configuration.session.name + name)
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
        self.lock = threading.Lock()

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
        line = [v for v in ast.literal_eval(line)]
        action_time = secs(line[0])
        command = answer.commands[line[1]]
        if command.question:
            question_name = line[2]
            if question_name not in questions.questions:
                return
        else:
            question_name = "None"
        the_answer = self.answer(question_name)
        v = command.parse(self, action_time, question_name, the_answer,
                          line[-1])
        if self.last_time:
            dt = action_time - self.last_time
            if dt < configuration.timeout_on_question:
                if self.last_command == 'good':
                    self.previous_answer.time_after += dt
                    self.previous_answer.current_time_after += dt
                else:
                    self.previous_answer.time_searching += dt
                    self.previous_answer.current_time_searching += dt
        self.previous_answer = the_answer
        self.last_command = command.name
        self.last_time = action_time
        return v

    def destroy(self):
        import shutil
        try:
            os.rename(self.file, self.file + "~")
        except OSError:
            pass
        for k in students:
            if students[k] == self:
                del students[k]
                break
        
    def a_href(self, body="", subject=None):
        return "<A HREF=\"?answered_other=%s\">%s</A>%s" % (
            self.filename, self.name,
            self.mailto(body=body, subject=None, link='@')
        )
            
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
            return list(questions.questions.values())
        if self.answerables_cache:
            return self.answerables_cache

        t = questions.answerable(self.answered_questions(), self)
        self.answerables_cache = t
        return t

    def answerables_typed(self, any=False):
        tt = []
        answerable_set = set(self.answerables())
        now = time.time()
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
                ("", "erasable ")[ int(a.erasable(now)) ] +
                ("", "suspended_until ")[ a.suspended_until() > now ] +
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

    def level(self):
        """Copy paste from competence.js"""
        class Level:
            nr = 0
            nr_accessible = 0
            nr_view = 0
            nr_good = 0
            nr_perfect = 0
            nr_versions = 0
            nr_total_versions = 0
            answerable_set = set(self.answerables())
            total_bad = 0
            total_good = 0
            for q in self.answerables(any=True):
                a = self.answer(q.name)
                nr += 1
                if q in answerable_set or a.nr_good_answer:
                    nr_accessible += 1
                if a.nr_asked:
                    nr_view += 1
                if a.nr_good_answer:
                    nr_good += 1
                if a.nr_perfect_answer:
                    nr_perfect += 1
                if a.nr_good_answer >= q.get_nr_versions():
                    nr_versions += 1
                total_bad += a.nr_bad_answer
                total_good += a.nr_good_answer

            if nr_accessible < nr:
                level = nr_accessible / nr
            elif nr_view < nr:
                level = 1 + nr_view / nr
            elif nr_good < nr:
                level = 2 + nr_good / nr
            elif nr_versions < nr:
                level = 3 + nr_versions / nr
            else:
                level = 4 + nr_perfect / nr
            del q, a
        return Level

    def grading_teachers(self):
        teachers = set()
        for a in self.answers.values():
            teachers.update(a.grades)
        return teachers

    def grades(self):
        summed = collections.defaultdict(int)
        for a in self.answers.values():
            for teacher, grade in a.grades.items():
                summed[teacher] += float(grade)
        return summed

    def answered_page(self, state):
        try:
            state.student.writable = False
            return self.answered_page_(state)
        finally:
            state.student.writable = True

    def answered_page_(self, state):
        t = list(self.answers.values())
        t.sort(key= lambda x: x.first_time)

        s = []
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
            from QUENLIG.Plugins.question_change_answer.question_change_answer import add_a_link
            more = add_a_link(state, q)
            s.append('<div class="question_history">')
            s.append("<em class=\"box_title short\">" + q.a_href() + more +"</em>")
            s.append('<table class="box_content"><tr><td>')
            question_text = q.get_question(state)
            s.append(question_text.split('{{{')[0])

            if a.indice >= 0 and a.indice < len(q.indices):
                s.append(utilities.list_format(q.indices[:a.indice+1]))
                
            for b in a.bad_answers:
                number, message = self.check_answer(b, state)
                if message:
                    message = "<br>" + message
                s.append(utilities.div(
                    "bad_answer",
                    utilities.answer_format(b,question=question_text)
                    + message))

            if a.answered:
                messages = [utilities.answer_format(a.answered,
                                                    question=question_text)]
                if q.good_answer:
                    messages.append(q.good_answer)
                try:
                    number, mess = self.check_answer(a.answered, state)
                    if mess:
                        messages.append(mess)
                except IOError:
                    messages.append('???BUG???')
                s.append(utilities.div("good_answer", '<br>'.join(messages)))
                if state.current_role == 'Grader':
                    s.append('<br>' + repr(a.grades)
                             + '<br>' + ' '.join(
                                 time.strftime("%H:%M:%S", time.localtime(t))
                                 for t in a.answer_times))

            for comment_time, comment_text in a.comments:
                s.append(utilities.div('comment',"<PRE>" + \
                                       html.escape(comment_text) + "</PRE>"))

            from QUENLIG.Plugins.question_correction.question_correction import add_a_link
            s.append(add_a_link(state, q))
            s.append('</tr></table></div><br>')

        state.question = saved_question

                
        if none and none.comments:
            s.append("<h3 class=\"short\">?</h3>")
            for comment_time, comment_text in none.comments:
                s.append(utilities.div('comment',"<PRE>" + \
                                       html.escape(comment_text) + "</PRE>"))
        return ''.join(s)

    def classement(self):
        from . import statistics
        stats = statistics.question_stats()
        if self in stats.sorted_students:
            return "%d/%d" % (stats.sorted_students.index(self)+1,
                              len(stats.sorted_students))
        else:
            return '?/%d' % len(stats.sorted_students)

    # Modify data structures and log actions

    def log(self, question_name, command, value=""):
        if not self.writable:
            return
        v = answer.commands[command].format(time.time(), question_name, value)
        if self.eval_line(v):
            return # Do not store: unchanged value
        f = open(os.path.join(self.file, 'log.py'), "a")
        f.write(v + "\n")
        f.close()

    def set_grade(self, question, teacher, grade):
        if question in self.answers:
            self.log(question, "grade", (teacher, grade))

    def set_why(self, question, teacher, comment):
        if question in self.answers:
            self.log(question, "why", (teacher, comment))
            
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

    def persistent_random(self, state, question, maximum, key='', real=False):
        if not state:
            return 0
        a = self.answer(question)
        if key not in a.persistent_random:
            if key in a.random_next:
                v = a.random_next[key]
                if real:
                    random.seed(v)
                    v = random.randrange(0, maximum)
            else:
                v = int(self.seed + a.nr_erase + static_hash(key))
            a.persistent_random[key] = v % maximum
            self.log(question, "random", (key, a.persistent_random[key]))
        # always because it is not stored in the log file
        a.random_max[key] = maximum
        return a.persistent_random[key]

    def erase(self, question):
        if question in self.answers:
            self.log(question, "erase", '')

    ####################################################
    # All about the question contextual to the student.
    ####################################################

    def check_answer(self, answer, state):
        "'state' is a parameter needed for some questions"
        return state.question.check_answer(answer, state)

    def answer_commented(self, question_name, answer, state):
        return questions.questions[question_name].answer_commented(answer,state)

    def mailto(self, subject=None, body="", link=None):
        if subject is None:
            subject = configuration.questions
        if link is None:
            link = self.name
        return "<A HREF=\"mailto:%s?subject=%s&body=%s\">%s</A>" % (
            self.informations.get('mail', self.filename),
            subject.replace("\"",'%27'),
            body.replace("\"",'%27').replace('\n','%0A'),
            link
            )

    ####################################################
    # Steal the identity of a student
    ####################################################
    def steal_enter(self, state, answer, rand):
        self.writable = False
        save = []
        if state is not None:
            save.append(state.student)
            state.student = self
        if answer is not None and rand is not None:
            save.append(answer.persistent_random)
            answer.persistent_random = rand
        return save

    def steal_exit(self, state, answer, rand, save):
        if answer is not None and rand is not None:
            answer.persistent_random = save.pop()
        if state is not None:
            state.student = save.pop()
        self.writable = True
            
students = {}
stop_loading_default = lambda x: False

@utilities.add_a_lock
def student(name):
    if name not in students:
        students[name] = Student(name, stop_loading=stop_loading_default)
    return students[name]

def all_students():
    """Read the directory content in order to return the student list"""
    age_and_name = [
        (log_age(student_name), student_name)
        for student_name in os.listdir(log_directory())
        if not student_name.endswith("~")
    ]
    if configuration.log_age >= 0:
        print("Load students active the last {} days".format(
            configuration.log_age), file=sys.stderr)
        return [student(name)
                for age, name in age_and_name
                if age < configuration.log_age * 86400
        ]
    # Load active student firsts
    age_and_name.sort()
    s = []
    t = time.time()
    for age, name in age_and_name:
        s.append(student(name))
        if time.time() - t > -configuration.log_age:
            break
    print("{} students loaded in {} seconds".format(len(s), time.time() - t),
          file=sys.stderr)
    return s

def dump():
    t = []
    for s in all_students():
        t.append(' '.join(['\t%s:%s\n' %(k, v)
                           for k, v in s.__dict__.items()
                           ]))
    return '\n'.join(t)

               
