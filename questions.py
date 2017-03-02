#!/usr/bin/env python3
# -*- coding: utf-8 -*-
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

import time
import types
import os
import inspect
import cgi
import urllib.request, urllib.parse, urllib.error
import re
import threading
import random
from . import configuration
from . import utilities

current_evaluate_answer = None
current_eval_after = None

class Required:
    unrequired = False
    before = False
    hide = False
    def __init__(self, world, string):
        for k in ('unrequired', 'before', 'hide'):
            kk = '{' + k + '}'
            if kk in string:
                self.__dict__[k] = True
                string = string.replace(kk, '')
        # An unrequired question must not be displayed in requireds
        self.hidden = self.unrequired or (not self.before and self.hide)
        w = string.split(":")
        if len(w) == 2:
            self.world = w[0]
            self.question_name = w[1]
        elif len(w) == 1:
            self.world = world
            self.question_name = string
        else:
            raise ValueError("Do not use ':' in question name")

        q = self.question_name.split('(')
        if len(q) != 1:
            self.question_name = q[0]
            
            if q[1][-1] != ')':
                raise ValueError("Bad required name: " + string)
                        
            self.answer = re.compile(q[1][:-1])
        else:
            self.answer = False

        self.name = self.world + ":" + self.question_name

    def question(self):
        return questions[self.name]

    def full_name(self):
        if self.answer:
            return self.name + '(' + self.answer + ')'
        else:
            return self.name


class Requireds:
    def __init__(self, requireds):
        self.requireds = requireds

    def __iter__(self):
        return self.requireds.__iter__()

    def missing(self, answered, student):
        missings = []
        for r in self.requireds:
            if r.unrequired and student.given_question(r.name):
                continue
            if answered.get(r.name, False) is False:
                missings.append(r.name)
            elif r.answer and not re.match(r.answer, answered[r.name]):
                missings.append(r.name)
        return missings

    def answered(self, answered, student):
        return not self.missing(answered, student)

    def names(self, only_visible=False):
        return [r.name
                for r in self.requireds
                if not only_visible or not r.hidden
            ]

class Question:
    def transform_question(self, question):
        """If the question is a string, return a function
        returning the string"""
        if question == None:
            return None
        if callable(question):
            question._question_ = self
            # Choice test because it contains the question
            if (not isinstance(question, TestExpression)
                and 'state' not in question.__code__.co_varnames):
                def tmp(state):
                    return question()
            else:
                def tmp(state):
                    return question(state)
        else:
            def tmp(dummy_state):
                return question
        tmp.real_question = question
        tmp.lock = threading.Lock()
        return tmp

    def __init__(self, world, arg, previous_question=[]):
        self.name = arg["name"]
        self.path = world
        world = world[-1]
        self.world = world
        self.short_name = self.name.split(':')[1]
        for c in self.name:
            if ord(c) >= 32 and c not in "/":
                continue
            raise ValueError("Bad question name (%s)" % c)

        self.question = self.transform_question(arg["question"])

        self.tests = arg.get("tests", ())
        self.before = self.transform_question(arg.get("before", None))
        self.good_answer = arg.get("good_answer", "")
        if not isinstance(self.good_answer, str):
            raise ValueError("good_answer must be a string")
        self.bad_answer = arg.get("bad_answer", "")
        if not isinstance(self.bad_answer, str):
            raise ValueError("bad_answer must be a string")
        self.nr_lines = int(arg.get("nr_lines", "1"))
        self.comment = []
        self.required = arg.get("required", previous_question)
        self.required = Requireds([Required(world, i)
                                   for i in self.required])
            
        self.indices = arg.get("indices", ())
        self.default_answer = arg.get("default_answer", "")
        self.evaluate_answer = current_evaluate_answer
        self.highlight = arg.get("highlight", False)
        self.maximum_bad_answer = int(arg.get("maximum_bad_answer", "0"))
        self.maximum_time = int(arg.get("maximum_time", "0"))
        self.perfect_time = int(arg.get("perfect_time", "10"))
        self.courses = arg.get("courses", None)
        self.nr_versions = int(arg.get("nr_versions", "1"))

        self.eval_after = current_eval_after
        self.canonize = None
        for test in self.tests:
            if hasattr(test, 'initialize'):
                test.initialize(lambda string, state: string, None)
                test.link_to_question(self)
            if not self.canonize and hasattr(test, 'search_a_canonizer'):
                self.canonize = test.search_a_canonizer()
        if self.canonize is None:
            self.canonize = lambda string, state: string
        self.competences = self.get_competences(self.tests)
        if len(self.competences) == 0:
            self.competences = ("",)

    def init_seed(self, state):
        if state and state.student:
            random.seed(state.student.seed
                        + state.student.answer(self.name).nr_erase)

    def get_question(self, state):
        with self.question.lock:
            self.init_seed(state)
            return self.question(state)

    def get_before(self, state):
        with self.question.lock:
            self.init_seed(state)
            return self.before(state)

    def get_good_answers(self, state):
        with self.question.lock:
            self.init_seed(state)
            for t in self.tests:
                yield from t.get_good_answers(state)

    def answers_html(self, state):
        with self.question.lock:
            self.init_seed(state)
            s = ""
            s += "<table class=\"an_answer\"><caption>" + self.name + "</caption>" +\
                 "<tbody>"
            if self.before:
                s += "<tr class=\"test_info\"><td colspan=\"6\">%s</td></tr>" % \
                     self.before(state)
            s += "<tr class=\"test_info\"><td colspan=\"6\">%s</td></tr>" % self.question(state)
            s += "<tr class=\"test_header\">"
            for i in range(6):
                s += "<th class=\"c%d\"></th>" % i
            s += "</tr>"
            for t in self.tests:
                s += t.html(state=state).replace('%','%%')
            for i in self.indices:
                s += "<tr class=\"test_indice\"><td colspan=\"6\">%s</td></tr>" % i
            if self.bad_answer:
                s += "<tr class=\"test_bad_comment\"><td colspan=\"6\">%s</td></tr>" % self.bad_answer
            if self.good_answer:
                s += "<tr class=\"test_good_comment\"><td colspan=\"6\">%s</td></tr>" % self.good_answer

            s += "<tbody></table>"
        return s

    def check_answer(self, answer, state):
        with self.question.lock:
            self.init_seed(state)
            answer = answer.strip(" \n\t\r").replace("\r\n", "\n")
            if self.nr_lines == 1 and answer.find("\n") != -1:
                return False, "<p class='answer_with_linefeed'></p>"
            if ' ' in answer:
                return False, "<p class='answer_with_nbsp'></p>"
            if self.evaluate_answer:
                answer = self.evaluate_answer(answer, state)

            full_comment = []
            for t in self.tests:
                if isinstance(t, types.FunctionType):
                    if 'state' in t.__code__.co_varnames:
                        result, comment = t(answer, state=state)
                    else:
                        result, comment = t(answer)
                else:
                    result, comment = t(answer, state=state)
                if comment not in full_comment:
                    full_comment.append(comment)
                if result != None:
                    if self.eval_after:
                        full_comment.append(self.eval_after(answer, state))
                    return result, ''.join(full_comment)

            if self.eval_after:
                full_comment.append(self.eval_after(answer, state))
        return False, ''.join(full_comment)

    # Comments starting by a white space are not
    # considered as usefull for the student.
    # It is used by questions.py/comment function.
    def answer_commented(self, answer, state):
        a = self.check_answer(answer, state)
        if a[0]:
            return "*" # Correct answer, so commented.
        c = a[1]
        # XXX Remove parsed unix answer
        c = re.sub("<u:sequence.*</u:sequence>", "", c.replace("\n",""))
        if c == ' ':
            c = ''
        return c

    def url(self):
        return "?question=%s" % urllib.parse.quote(self.name)

    def a_href(self):
        return "<A HREF=\"%s\">%s</A>" % (self.url(), cgi.escape(self.name))

    def nr_indices(self):
        return len(self.indices)

    def __str__(self):
        return self.name

    def python_file(self):
        return os.path.join(configuration.root, configuration.questions,
                            self.world + ".py")

    def answerable(self, student):
        if (self.maximum_bad_answer
            and student.bad_answer_question(self.name)
            >= self.maximum_bad_answer):
            return False
        time_first = student.time_first(self.name)
        if (self.maximum_time and time_first
            and time.time() - time_first >= self.maximum_time):
            return False
        return True

    def get_competences(self, tests):
        competences = set()
        for test in tests:
            if isinstance(test, Grade):
                if test.grade > 0:
                    if test.teacher:
                        if isinstance(test.teacher, str):
                            competences.add(test.teacher)
                        else:
                            competences.update(test.teacher)
            if getattr(test, 'children', None):
                competences.update(self.get_competences(test.children))
        return competences

    def get_nr_versions(self):
        try:
            return self.question.real_question.nr_versions()
        except AttributeError:
            return self.nr_versions

questions = {}
previous_question = ""

def add(**arg):
    """Add a question to the question base"""

    attributs = {
    "name": "Nom court de la question. Ne pas donner la reponse dans le nom de la question.",
    "required": "Liste des noms des questions auxquels l'etudiant doit avoir deja repondu",
    "before": "Ce que doit faire l'etudiant avant de lire la question",
    "question": "Texte de la question en HTML ou fonction retournant le texte",
    "indices": "Une liste d'indices pour aider l'etudiant a repondre",
    "tests": "Les tests de verification des reponses",
    "good_answer": "Texte a afficher si l'etudiant donne une bonne reponse",
    "bad_answer": "Texte a afficher si l'etudiant donne une mauvaise reponse",
    "nr_lines": "Nombre de lignes pour la reponse",
    "default_answer": "Reponse par defaut",
    "highlight": "Question à mettre en évidence",
    "maximum_bad_answer": "Nombre maximum de mauvaises réponse",
    "maximum_time": "Temps maximum pour répondre en secondes",
    "perfect_time": "Si on répond plus vite : on maîtrise la question",
    "courses": "Position ('H1', 'H2'...) dans le support de cours",
    "nr_versions": "Nombre de versions pour la question",
    }

    # sys.stdout.write("*")
    # sys.stdout.flush()
    world = inspect.currentframe().f_back.f_globals["__name__"].split(".")
    for a, v in arg.items():
        if a not in attributs.keys():
            print("'%s' n'est pas un attribut de question" % a)
            print("Les attributs possibles de questions sont:")
            for i in attributs.keys():
                print("\t%s: %s" % (i, attributs[i])) 
            raise KeyError("Voir stderr")
    arg["name"] = world[-1] + ":" + arg["name"]
    if arg["name"] in questions.keys():
        raise KeyError("There is always a question with this name: %s"
                       % arg["name"])
    global previous_question
    if previous_question and previous_question.split(":")[0] == world[-1]:
        pq = [previous_question]
    else:
        pq = []
    new_question = Question(world, arg, previous_question=pq)
    questions[arg["name"]] = new_question
    new_question.f_lineno = inspect.currentframe().f_back.f_lineno
    previous_question = arg["name"]

def answerable(answered, student):
    """Returns the authorized question list.
    The parameter is the names of the questions yet answered.
    The prequired are checked here.
    """
    answerable = []
    for q in questions.values():
        if answered.get(q.name, False) or not q.required.answered(answered,
                                                                  student):
            continue
        if q.answerable(student):
            answerable.append(q)
    return answerable

def nr_indices(question_name):
    try:
        return questions[question_name].nr_indices()
    except KeyError:
        return -1

def a_href(question_name):
    try:
        return questions[question_name].a_href()
    except KeyError:
        return question_name

def worlds():
    d = {}
    for q in questions.values():
        d[q.world] = 1
    return list(d.keys())

sorted_questions = []

# Very far from optimal algorithm
def sort_questions():
    for q in questions.values():
        q.level = None
        q.priority = None
        q.used_by = []

    # Compute 'used_by'
    for q in questions.values():
        for r in q.required.names():
            try:
                questions[r].used_by.append(q.name)
            except KeyError:
                print(q.name, '=== REQUIRE ===>', r)

    # Compute 'descendants'
    leave = []
    for q in questions.values():
        q.nr_childs = len(q.used_by)
        if q.used_by:
            q.descendants = dict.fromkeys(q.used_by)
        else:
            q.descendants = {}
            leave.append(q)

    while leave:
        node = leave.pop()
        for q in node.required.names():
            q = questions[q]
            q.descendants.update(node.descendants)
            q.nr_childs -= 1
            if q.nr_childs == 0:
                del q.nr_childs
                leave.append(q)

    # Compute 'level'
    def compute_level(q):
        q = questions[q]
        if q.level is None:
            levels = [compute_level(r) for r in q.required.names()]
            if levels:
                levels = tuple(zip(*levels))
                q.level = max(levels[0]) + 1
                q.level_min = min(levels[1]) + 1
            else:
                q.level = q.level_min = 1
        return q.level, q.level_min
    for q in questions:
        compute_level(q)

    # Compute 'priority'
    def compute_priority(q, p):
        if q.priority is not None:
            return p
        for r in sorted(q.required.names(),
                        key = lambda x: -len(questions[x].used_by)):
            p = compute_priority(questions[r], p)
        q.priority = p
        return p + 1
    priority = 0
    for q in sorted(questions.values(), key=lambda x: -x.level):
        priority = compute_priority(q, priority)

    global sorted_questions
    sorted_questions = list(questions.values())
    sorted_questions.sort(key = lambda x: (x.priority, len(x.used_by)))

    # Compute coordinates.
    # Questions without prerequisites are in the center.
    # Others are the nearer possible from their requisite.
    for q in questions.values():
        q.nr_parents = len(q.required.names())
    nodes = [q for q in questions.values() if q.level == 1]
    pixels = {}    
    while nodes:
        n = nodes.pop()
        r = n.required.names()
        if r:
            cxs = [questions[q].coordinates[0] for q in r]
            cys = [questions[q].coordinates[1] for q in r]
            cx = sum(cxs) / len(cxs)
            cy = sum(cys) / len(cxs)
        else:
            cx = cy = 0
        for d in spiral(cx,cy):
            if d not in pixels:
                n.coordinates = d
                pixels[d] = True
                break
        for q in n.used_by:
            q = questions[q]
            q.nr_parents -= 1
            if q.nr_parents == 0:
                nodes.append(q)
                del q.nr_parents
    minx = min([q.coordinates[0] for q in questions.values()])
    miny = min([q.coordinates[1] for q in questions.values()])
    for q in questions.values():
        q.coordinates = (q.coordinates[0] - minx, q.coordinates[1] - miny)
        


def spiral(x,y):
    yield x,y
    w = 3
    while True:
        y += 1
        yield x,y
        for i in range(w-2):
            x += 1
            yield x,y
        for i in range(w-1):
            y -= 1
            yield x,y
        for i in range(w-1):
            x -= 1
            yield x,y
        for i in range(w-1):
            y += 1
            yield x,y
        w += 2

#
#
#
def _format(s):
    r = ""
    for i in s:
        r += utilities.answer_format(str(i)) + "<BR>"
    return r[:-4]

def return_first_arg(a,b):
    return a.strings

def sort_lines(t):
    t = t.split('\n')
    t.sort()
    return '\n'.join(t)

def replace_strings(replace, string):
    for old, new in replace:
        string = string.replace(old, new)
    return string

###############################################################################
###############################################################################
###############################################################################
# OBSOLETES TEST : DO NOT USE (see after)
###############################################################################
###############################################################################
###############################################################################

class Test(object):
    comment = ''
    replace = ()
    replacement = ()
    strings = ('',)
    html_class = 'test_unknown'
    uppercase = False
    all_agree = False
    sort_lines = False

    def __init__(self,
                 strings=None,
                 comment=None,
                 replace=None,
                 replacement=None,
                 uppercase=None,
                 all_agree=None,
                 parse_strings=None,
                 sort_lines=None,
                 ):
        if comment:
            self.comment = comment
        if replace:
            self.replace = replace
        if replacement:
            self.replacement = replacement
        if uppercase:
            self.uppercase = uppercase
        if all_agree:
            self.all_agree = all_agree
        if sort_lines:
            self.sort_lines = sort_lines
        if parse_strings:
            self.parse_strings = parse_strings
        else:
            self.parse_strings = return_first_arg
        if strings:
            self.strings = utilities.rewrite_string(strings)

    def html(self, state):
        if self.comment:
            comment = self.comment
        else:
            comment = self.__class__.__name__
        if self.uppercase:
            comment = "(U)" + comment
        if self.all_agree:
            comment = "(A)" + comment
        if self.parse_strings == return_first_arg:
            r = ''
        else:
            r = '<hr>After parse_strings<br>' + ''.join(_format(self.parse_strings(self, state)).replace('&lt;/argument&gt;','&lt;/argument&gt;<br>'))
        return ("<TR CLASS=\"a_test " + self.html_class +
                "\"><td class=\"a\"></td>" +
                "<td class=\"b\"></td>" +
                "<td class=\"c\">" + _format(self.strings) + r + "</td>" +
                "<td class=\"d\">" + comment + "</td>" +
                "<td class=\"e\">" + _format(self.replacement) + "</td>" +
                "<td class=\"f\">" + _format(self.replace) + "</td>"
                "</tr>\n")


    def __call__(self, student_answer, state=None):
        if self.uppercase:
            student_answer = student_answer.upper()
        student_answer = replace_strings(self.replace, student_answer)
        student_answer = self.answer_processing(student_answer)
        if self.sort_lines:
            student_answer = sort_lines(student_answer)

        strings = self.parse_strings(self, state)
        for string in strings:
            if self.sort_lines:
                string = sort_lines(string)
                
            if state != None and 'state' in self.test.__code__.co_varnames:
                t = self.test(student_answer, string, state=state)
            else:
                t = self.test(student_answer, string)
            if self.all_agree:
                if t == None:
                    return None, ""
            else:
                if t != None:
                    if t == True or t == False:
                        return t, self.comment
                    else:
                        return t # There is yet a contextual comment
        if self.all_agree:
            if t == True or t == False:
                return t, self.comment
            else:
                return t # There is yet a contextual comment
        return None, ""

    def answer_processing(self, answer):
        return answer


class good(Test):
    html_class = 'test_string test_good test_is'
    def test(self, student_answer, string):
        if student_answer == string:
            return True
class good_if_contains(Test):
    html_class = 'test_string test_good test_is_in'
    def test(self, student_answer, string):
        if string in student_answer:
            return True
class bad(Test):
    html_class = 'test_string test_bad test_is'
    def test(self, student_answer, string):
        if student_answer == string:
            return False
class require(Test):
    html_class = 'test_string test_bad test_require'
    def test(self, student_answer, string):
        if student_answer.find(string) == -1:
            return False
class require_startswith(Test):
    html_class = 'test_string test_bad test_startswith'
    def test(self, student_answer, string):
        if not student_answer.startswith(string):
            return False
class require_endswith(Test):
    html_class = 'test_string test_bad test_endswith'
    def test(self, student_answer, string):
        if not student_answer.endswith(string):
            return False
class expect(require):
    def test(self, student_answer, string):
        if student_answer.find(string) == -1:
            return False, "<p class='string_expected'>«<b>%s</b>»</p>" % string
class reject(Test):
    html_class = 'test_string test_bad test_reject'
    def test(self, student_answer, string):
        if student_answer.find(string) != -1:
            return False
class reject_startswith(Test):
    html_class = 'test_string test_bad test_notstartswith'
    def test(self, student_answer, string):
        if student_answer.startswith(string):
            return False
class reject_endswith(Test):
    html_class = 'test_string test_bad test_notendswith'
    def test(self, student_answer, string):
        if student_answer.endswith(string):
            return False
class answer_length_is(Test):
    html_class = 'test_bad test_require test_length'
    def test(self, student_answer, string):
        if len(student_answer) != string:
            return False

class TestWithoutStrings(Test):
    def __init__(self, comment=None, replace=None):
        Test.__init__(self, comment=comment, replace=replace)

class require_int(TestWithoutStrings):
    html_class = 'test_bad'
    comment = "<p class='int_required'></p>"
    def test(self, student_answer, string):
        try:
            student_answer = int(student_answer.rstrip('.'))
        except ValueError:
            return False

class number_of_is(Test):
    html_class = 'test_bad test_require test_number_of'
    def __init__(self, character, number, comment=None, replace=None):
        Test.__init__(self, strings=((character,number),),
                      comment=comment, replace=replace)
    def test(self, student_answer, string):
        if student_answer.count(string[0]) != string[1]:
            return False

class comment(Test):
    html_class = 'test_string test_bad'
    def __init__(self, comment=None, require='', replace=None):
        Test.__init__(self, strings=require, comment=comment, replace=replace)
    def test(self, student_answer, string):
        if string in student_answer:
            # This is a dirty way to program,
            # but the white space is here to indicate that
            # it is not a real contextual comment on the student answer.
            # This white space is tested by questions.py:answer_commented
            return None, ' ' + self.comment + '<br>'

def yesno(student_answer, yes_is_good):
    if student_answer.upper() in ('O', 'OUI', 'Y', 'YES'):
        if yes_is_good:
            return True, ""
        else:
            return False
    if student_answer.upper() in ('N', 'NON', 'NO'):
        if yes_is_good:
            return False
        else:
            return True, ""
        
    return False, "<p class='yes_or_no'></p>"

class yes(TestWithoutStrings):
    html_class = 'test_string test_bad test_is'
    strings = ('yes',)
    def test(self, student_answer, string, state=None):
        return yesno(student_answer, yes_is_good=True)

class no(TestWithoutStrings):
    html_class = 'test_string test_bad test_is'
    strings = ('no',)
    def test(self, student_answer, string, state=None):
        return yesno(student_answer, yes_is_good=False)


###############################################################################
###############################################################################
###############################################################################
# NEW TESTS : YOU MUST USE THESE
###############################################################################
###############################################################################
###############################################################################


# New syntax for tests.
# Base tests must answer by True or False, no more None
# Root expression returns True(OK) / False(Error) / None(Continue)
# No more string list
# The __call__ has parameters:
#   * self : The test
#   * Student answer parsed by upper operators
#   * 'state' : the session of the student
#   * 'parser' to parse its string, parser argument are
#       * The string to parse
#       * The state
#       * self : the current operator


# Good(Equal('foo'))          'foo' is a good answer
# Bad(Equal('bar'))           'bar' is a bad answer
# Good(~Equal('x'))           if the student don't answer 'x' its a good answer
# Good(Equal('a') | Equal('b')) 'a' and 'b' are both good answer.
# Good(Comment(Equal('a'), "You answered A.") |
#      Comment(Equal('b'), "You answered B."))    with comments
# Good(Comment(UpperCase(Equal('a'))) |
#              Comment(SortLines(Equal('b\nc')), "You answered bc or cb."),
#              "And it is a good answer !")  with a comment + a generic comment
# Bad(~ Contain('B'))                  'require' equivalent
# Good(Contain('A') & ~ Contain('B'))

## Uppercase change the Equal.string
# Good(Uppercase(Equal("a")))
## ShellParse change the Equal.string to parse it
# Good(Shell(Equal("ls a")))
## ShellParse does not parse Contain.string
# Good(Shell(Contain("<parameter>-z</parameter>", canonize=False)))

# Good(Replace('-A', '-a', Equal('ls -a')))
# Good(Replace('-A', '-a', Shell(Equal('ls -a'))))


# Good(Host(Equal('{E0.port}'))
# Host needs to look its 'uppercase' flag.
# Good(Uppercase(Host(Equal('{E0.port}'))))
# Good(Host(UpperCase(Equal('{E0.port}')))) ######## BAD #############


# Good(Yes()) : Student answer :
#         YES ===> good answer
#         NO  ===> continue
#         ??? ===> continue but a comment about YES/NO



def pf(txt, format=None):
    txt = repr(txt)
    if format == None:
        return txt
    if format == 'html':
        txt = cgi.escape(txt).replace("\\n", " ")
        if len(txt) > 20:
            txt = '<div style="display:inline-block;max-width:30em;vertical-align:top">' +txt+ '</div>'
        return txt
    raise ValueError('Unknown output format')

def no_parse(string, state, test):
    return string

class TestExpression(Test):
    """Base class for all tests.
    The test function returns a boolean and a comment.
    If the test function returns True/False, the answer is good/bad and
    the processing stops. If it returns None, then the next test
    is computed."""
    children = ()

    def __init__(self, *children):
        self.children = list(children)
        for c in self.children:
            if not isinstance(c, TestExpression):
                raise ValueError("Bad children for %s"%self.__class__.__name__)

    def html(self, state=None):
        return '<tr class="test_unknown"><td colspan="8"">%s</td></tr>' % \
               self.source(state, 'html')

    def source(self, state=None, format=None):
        return self.test_name(format) + '()'

    def __or__(self, other):
        return Or(self, other)

    def __and__(self, other):
        return And(self, other)

    def __invert__(self):
        return TestInvert(self)

    def test_name(self, format=None):
        if format == None:
            return self.__class__.__name__
        elif format == 'html':
            return '<b>' + self.__class__.__name__ + '</b>'
        raise ValueError('Unknown output format')

    def canonize(self, string, dummy_state):
        """Returns the canonized string (student answer).
        To return an error: return False, "Syntax error"
        """
        return string

    def canonize_test(self, parser, state):
        """Modify test parameters"""
        pass

    def __call__(self, student_answer, state=None):
        """Add a compatibility layer for old tests"""
        student_answer = self.canonize(student_answer, state)
        if isinstance(student_answer, str):
            return self.do_test(student_answer, state)
        else:
            return student_answer

    def initialize(self, parser, state):
        """The string in test description must be canonized"""
        self.parser = parser #Store the parser for future use (See HostReplace)
        self.canonize_test(parser, state)
        for child in self.children:
            child.initialize(lambda string, a_state:
                                 self.canonize(parser(string,a_state),a_state),
                             state
                             )
            
    def search_a_canonizer(self):
        if self.__class__.canonize != TestExpression.canonize:
            return self.canonize
        
        for child in self.children:
            c = child.search_a_canonizer()
            if c:
                return c
        return

    def link_to_question(self, question):
        self._question_ = question
        for child in self.children:
            child.link_to_question(question)

    def block(self, format, items, name=None):
        if name is None:
            name = self.test_name(format)
        if format == 'html':
            return (name
                    + '(<div style="display:inline-block;vertical-align:top;border:1px solid #CCC;margin-top:2px;margin-bottom:2px">'
                    + ',<br>'.join(items)
                    + '</div>)')
        else:
            return name + '(' + ','.join(items) + ')'

    def get_good_answers(self, state):
        for child in self.children:
            for string in child.get_good_answers(state):
                yield self.canonize(string, state)

class TestNAry(TestExpression):
    """Base class for tests with a variable number of test as arguments."""
    def __init__(self, *args, **keys):
        self.shortcut =  keys.get('shortcut', True)
        TestExpression.__init__(self, *args)

    def source(self, state=None, format=None):
        t = [c.source(state, format)
             for c in self.children]
        if not self.shortcut:
            t.append('shortcut=False')
        return self.block(format, t)

class TestUnary(TestExpression):
    """Base class for tests with one child test."""
    def do_test(self, student_answer, state):
        return self.children[0](student_answer, state)
    
    def source(self, state=None, format=None):
        return self.test_name(format) + \
               "(%s)" % self.children[0].source(state, format)

class TestString(TestExpression):
    """Base class for tests with a string argument.
    By default, the string in parameter is canonized.
    In rare case, it is not the desired behavior, so we reject
    the canonization:
    Examples:
         # The Contain parameter must not be canonized because
         # the constant string is yet a fragment of a canonized shell command.
         Bad(Shell(Contain('&lt;parameter&gt;-z&lt;/parameter&gt;', canonize=False)))
    """
    def __init__(self, string, canonize=True):
        if not isinstance(string, str):
            raise ValueError("Expect a string")
        self.string = string
        self.do_canonize = canonize

    def canonize_test(self, parser, state):
        if self.do_canonize:
            self.string_canonized = parser(self.string, state)
        else:
            self.string_canonized = self.string

    def source(self, state=None, format=None):
        if self.do_canonize:
            canonize = ''
        else:
            canonize = ',canonize=False'
        return self.test_name(format) + '(%s%s)' % (
            pf(self.string, format), canonize)

class Or(TestNAry):
    """Returns True if one child returns True:
    True  False => True,
    True  True  => True,
    True  None  => True,
    None  None  => None,
    None  False => False,
    False False => False.
    the syntax with '|' operator can be used.
    As in other programmation language, by default, the evaluation stops
    is the result is predictible.
    
    Examples:
        Good(Or(Equal('a'), Equal('b'), Equal('c')))
        Good(Equal('a') | Equal('b') | Equal('c'))
        # To continue the test even if the first is True, use shortcut=False.
        # The following test returns 2 comments on 'ab' answer and not
        # only the first one.
        Bad(Or(Comment(Contain('a'), 'comment A'),
               Comment(Contain('b'), 'comment B'),
               shortcut=False
               ))
    """
    def do_test(self, student_answer, state):
        all_comments = ""
        a_bool = None
        for c in self.children:
            aa_bool, a_comment = c(student_answer, state)
            all_comments += a_comment
            if aa_bool is True:
                a_bool = True
                if self.shortcut:
                    break
            elif aa_bool is False:
                if a_bool is None:
                    a_bool = False
        return a_bool, all_comments

    def __or__(self, other):
        self.children.append(other)
        return self


class And(TestNAry):
    """Returns False if one child returns False:
    True  False => False,
    True  True  => True,
    True  None  => True,
    None  None  => None,
    None  False => False,
    False False => False.
    the syntax with '&' operator can be used.
    As in other programmation language, by default, the evaluation stops
    is the result is predictible.
    
    Examples:
        Good(And(Contain('a'), Contain('b'), Contain('c')))
        Good(Contain('a') & Contain('b') & Contain('c'))
        # To continue the test even if the first is False, use shortcut=False.
        # The following test returns a comment on 'b' answer even
        # if the answer does not contains 'a'
        Good(And(Comment(Contain('a'), 'comment A'),
                 Comment(Contain('b'), 'comment B'),
                 shortcut=False
                ))
        """
    operator = " & "
    def do_test(self, student_answer, state):
        all_comments = ""
        a_bool = None
        for c in self.children:
            aa_bool, a_comment = c(student_answer, state)
            all_comments += a_comment
            if aa_bool is False:
                a_bool = False
                if self.shortcut:
                    break
            elif aa_bool is True:
                if a_bool is None:
                    a_bool = True
        return a_bool, all_comments
    def __and__(self, other):
        self.children.append(other)
        return self

class TestInvert(TestUnary):
    """True if the children test returns False (or the reverse),
    the syntax with '~' operator can be used.

    Examples:
        # The answer is good if it is NOT 42.
        Good(TestInvert(Equal('42')))
        Good(~ Equal('42'))
    """
    def source(self, state=None, format=None):
        return "~" + self.children[0].source(state, format)
    def do_test(self, student_answer, state):
        a_bool, a_comment = self.children[0](student_answer, state)
        return not a_bool, a_comment

class TestFunction(TestExpression):
    """The parameter function returns a boolean and a comment.
    The test returns True if the function returns True.

    Examples:
        def not_even(answer, state):
            '''This function should catch ValueError exception'''
            if int(answer) % 2 == 0:
                 return False, ''
            return True, 'The answer is an even integer.'
            
        Bad(TestFunction(not_even))
"""
    def __init__(self, fct):
        if not callable(fct):
            raise ValueError("Expect a callable object")
        self.fct = fct

    def do_test(self, student_answer, state):
        return self.fct(student_answer, state)

    def source(self, state=None, format=None):
        name = str(self.fct.__name__)
        if name == '<lambda>':
            name = repr(self.fct.__code__)
        return self.test_name(format) + '(' + cgi.escape(name) + ')'


class Equal(TestString):
    """Returns True the student answer is equal to the string in parameter.
    
    Examples:
        Bad(Comment(Equal('A bad answer'),
                    "Your answer is bad because..."
                   )
           )
        Good(Equal('A good answer'))
        
    """
    def do_test(self, student_answer, dummy_state):
        return student_answer == self.string_canonized, ''

    def get_good_answers(self, state):
        yield self.string

class Contain(TestString):
    """Returns True the student answer contains the string in parameter.

    Examples:
        Good(Contain('python'))
        Bad(Contain('C++'))
        Good(Contain('')) # This test is always True
    """
    def do_test(self, student_answer, dummy_state):
        return self.string_canonized in student_answer, ''

def contains_one_of(expected, comment=None):
    a = Contain(expected[0], comment)
    for e in expected[1:]:
        a = a | Contain(e, comment)
    return a

class Start(TestString):
    """Returns True the student answer starts by the string in parameter.

    Examples:
        Good(Start("3.141"))
        Bad(Comment(~ Start('1'),
                    "The first digit is one"
                   )
           )
    """
    def do_test(self, student_answer, dummy_state):
        return student_answer.startswith(self.string_canonized), ''

class End(TestString):
    """Returns True the student answer ends by the string in parameter.

    Examples:
        Good(Comment(End('$'),
                     "Yes, the shell prompt is terminated by a $."
                    )
            )
        Bad(Comment(~ End('.'),
                    "An english sentence terminates by a dot."
                   )
           )
           """
    def do_test(self, student_answer, dummy_state):
        return student_answer.endswith(self.string_canonized), ''

class Good(TestUnary):
    """If the child test returns True then the student answer is good.
    The child comment will be visible to the student even if it
    returns False.

    Examples:
        Good(Equal('5'))
        Good(Contain('6'))
        Good(~ Start('x'))
    """
    def do_test(self, student_answer, state):
        a_bool, a_comment = self.children[0](student_answer, state)
        if a_bool == True:
            return a_bool, a_comment
        return None, a_comment

class Bad(TestUnary):
    """If the child test returns True then the student answer is bad.
    Examples:
        Bad(Equal('5') | Contain('6'))
        Bad(~ Equal('AA') & Equal('AA') ) # This one will never be bad...
        
        # The next test will be bad if the answer contains 'x' and 'y'
        # Beware of the And evaluation shortcut, the second test will not
        # be evaluated if the answer does not contains 'x'
        # The comments for the student are:
        #   x  : not bad, but with comment 'x'
        #   y  : not bad, without comment
        #   xy : bad with comments 'x' and 'y' concatened,
        Bad(   Comment(Contain('x'),'x')  &amp;  Comment(Contain('y'),'y'))   )
        
        # The next test will be bad if the answer contains 'x' or 'y'
        # Beware of the Or evaluation shortcut, the second test will not
        # be evaluated if the answer does contains 'x'
        # The comments for the student are:
        #   x  : bad with comment 'x'
        #   y  : bad with comment 'y'
        #   xy : bad with comment 'x'
        Bad(   Comment(Contain('x'),'x')  |  Comment(Contain('y'),'y'))   )
        """
    def do_test(self, student_answer, state):
        a_bool, a_comment = self.children[0](student_answer, state)
        if a_bool == True:
            return False, a_comment
        return None, a_comment

    def get_good_answers(self, state):
        yield from ()

class UpperCase(TestUnary):
    """The student answer is uppercased, and the child test value
    is returned.

    Examples:
      # The 'Equal' parameter is uppercased.
      Good(UpperCase(Equal('aa'))) # True if answer is: 'aa', 'AA', 'Aa' or 'aA'
      
      # The replacement is done before uppercasing, so if the answer
      # contains 'A' it will not be translated into 'X'.
      # So 'a', 'x' and 'X' are good answers, but not 'A'
      Good(Replace((('a','x'),),
                   UpperCase(Equal('a'))
                  )
          )
      # To replace both 'a' and 'A' per 'X' the good order is:
      # So 'a', 'A', 'x' and 'X' are good answers.
      Good(UpperCase(Replace((('A','X'),),
                             Equal('a'), canonize=True)
                    )
          )
      # A more straightforward and intuitive coding is:
      Good(UpperCase(Replace((('A','X'),),
                             Equal('X'))
                    )
          )
    """
    def canonize(self, string, dummy_state):
        return string.upper()

class RemoveSpaces(TestUnary):
    """Remove unecessary spaces/tabs.
    So 'a +   5' become 'a+5' because '+' is not alphanumeric.
    But 'a 5' stays as 'a 5'
    """
    def canonize(self, string, state):
        # Remove white spaces after a separator.
        string = re.sub('([^a-zA-Z0-9_\n\r\t ])[ \t]+', r'\1', string)
        # Remove white spaces before a separator if there is a normal
        # character at the left of the run.
        string = re.sub('([a-zA-Z0-9_])[ \t]+([^a-zA-Z0-9_])', r'\1\2', string)
        return string

class RMS(TestUnary):
    """Replace multiple spaces/tabs by only one.
    Remove spaces from lines begin and end.
    """
    def canonize(self, string, state):
        return re.sub('( $|^ )', '', re.sub('[ \t]+', ' ', string))

class SortLines(TestUnary):
    r"""The lines of the student answer are sorted and child test value
    is returned.

    Examples:
        # The student answer 'b\na' will be fine.
        Good(SortLines(Equal('a\nb')))
    """
    def canonize(self, string, state):
        return sort_lines(string)

class Comment(TestUnary):
    """If the child test returns True then the comment will be displayed
    to the student.
    If the child test is yet commented, then the comment will be concatened.

    Examples:
        Good(Comment(Equal('a'), "'a' is a fine answer"))
        Bad(Comment(Equal('b') | Equal('c'), "Your answer is very bad"))
        # Let know the student it did not fall in a trap :
        Bad(Comment(~ Comment(~Equal('x'),
                             "Good ! You didn't answer 'x'"
                             ),
                       "'x' is a very bad answer..."
                   )
           )
        # The same thing in another way with 2 successive tests:
        Bad(Comment(Equal('x'), "'x' is a very bad answer...'")
        Comment("Good ! You didn't answer 'x'")

        # The following test will be no good nor bad but if it is evaluated
        # it will insert a comment for the student.
        Comment('An explanation')

        # The comment text itself can be canonized
        choices = {"DIRNAME": ("/etc", "/bin")}
        Bad(Random(choices, Comment(~Contain("DIRNAME"),
                                    "Expect DIRNAME in your answer",
                                    canonize=True)))
        """
    def __init__(self, child_or_comment, comment=None, canonize=False):
        if comment is None:
            comment = child_or_comment
            child_or_comment = ()
        else:
            child_or_comment = (child_or_comment, )
        TestExpression.__init__(self, *child_or_comment)
        self.do_canonize = canonize
        self.comment = comment

    def source(self, state=None, format=None):
        t = []
        if self.children:
            t.append(self.children[0].source(state, format))
        t.append(pf(self.comment, format))
        if self.do_canonize:
            t.append("canonize=True")
        return self.block(format, t)

    def canonize_test(self, parser, state):
        if self.do_canonize:
            self.comment_canonized = parser(self.comment, state)
        else:
            self.comment_canonized = self.comment

    def do_test(self, student_answer, state):
        if self.children:
            bool, comment = self.children[0](student_answer, state)
        else:
            return None, self.comment_canonized
        if bool == True:
            comment += self.comment_canonized
        return bool, comment

class Expect(TestString):
    """Returns False if the student answer does not contains
    the string in parameter, if a comment is not provided then
    an automatic one is created.
    It is a shortcut for:  Bad(Comment(~Contain(string), "string is expected"))

    Examples:
         Expect("foo")
         Expect("bar", "You missed a 3 letters word always with 'foo'")
    """
    def __init__(self, *args, **keys):
        if len(args) == 1:
            self.comment = None
        else:
            self.comment = args[1]
        self.do_canonize_comment = keys.pop("canonize_comment", True)
        TestString.__init__(self, args[0], **keys)

    def canonize_test(self, parser, state):
        super().canonize_test(parser, state)
        if self.do_canonize_comment and self.comment:
            self.comment_canonized = parser(self.comment, state)
        else:
            self.comment_canonized = self.comment

    def do_test(self, student_answer, state):
        if self.string_canonized in student_answer:
            return None, ''
        else:
            if self.comment:
                return False, self.comment_canonized
            else:
                return False, '<p class="string_expected">«<b>' + self.string_canonized + '</b>»</p>'

def expects(expected, comment=None):
    a = Expect(expected[0], comment)
    for e in expected[1:]:
        a = a & Expect(e, comment)
    return a

class Reject(Expect):
    """Returns False the student answer contains
    the string in parameter, if a comment is not provided then
    an automatic one is created.
    It is a shortcut for:  Bad(Comment(Contain(string), "string is unexpected"))

    Examples:
         Reject("foo")
         Reject("bar", "Why 'bar'? there is no 'foo'...")
    """
    def do_test(self, student_answer, state):
        if self.string_canonized not in student_answer:
            return None, ''
        else:
            if self.comment:
                return False, self.comment_canonized
            else:
                return False, '<p class="string_rejected">«<b>' + self.string + '</b>»</p>'


def rejects(expected, comment=None):
    a = Reject(expected[0], comment)
    for e in expected[1:]:
        a = a & Reject(e, comment)
    return a


# Set a 'replace' attribute on all the children
class Replace(TestUnary):
    """The first argument is a tuple of (old_string, new_string)
    all the replacements are done on the student answer and
    the test in parameter is then evaluated.
    The replacements strings are NOT canonized by default.

    Examples:
        # Student answers 'aba', 'ab1'... will pass this test.
        Good(Replace( (('a', '1'), ('b', '2')),
                      Equal('121')))
        # Beware single item python tuple, do not forget the coma:
        Good(Replace( (('a', '1'), ),
                      Equal('121')))
        # With UpperCase canoniser, canonization is a good idea
        Good(UpperCase(Replace((('a', 'b'),), Equal('a'), canonize=True)))
    """
    def __init__(self, replace, a, canonize=False):
        TestExpression.__init__(self, a)
        self.replace = replace
        self.do_canonize = canonize

    def canonize_test(self, parser, state):
        if self.do_canonize:
            self.replace_canonized = [
                (parser(old, state), parser(new, state))
                for old, new in self.replace
                ]
        else:
            self.replace_canonized = self.replace

    def source(self, state=None, format=None):
        if self.do_canonize:
            canonize = ',canonize=True'
        else:
            canonize = ''
        return self.test_name(format) + \
               "(%s,%s%s)" % (
            pf(self.replace, format),
            self.children[0].source(state, format), canonize)

    def canonize(self, string, state):
        return replace_strings(self.replace_canonized, string)

class IsInt(TestExpression):
    """Returns True if the student answer is an integer

    Examples:
       # Reject any number != 42
       # If the student answer is not an integer there is no message.
       Bad(Comment(IsInt() & ~Int(42), "The answer is 42"))
    """
    def do_test(self, student_answer, state):
        try:
            int(student_answer)
            return True, ''
        except:
            return None, ''

class TestInt(TestExpression):
    """Base class for integer tests."""
    def __init__(self, integer):
        if not isinstance(integer, int):
            raise ValueError("Expect an integer")
        self.integer = integer
    def source(self, state=None, format=None):
        return self.test_name(format) + '(' + str(self.integer) + ')'

class Int(TestInt):
    """Returns True if the student answer is an integer equal
    to the specified value.

    Examples:
        # If the answer is not an integer a comment is returned.
        Good(Int(1984) | Int(2001))
    """
    def do_test(self, student_answer, state):
        try:
            if self.integer == int(student_answer.rstrip('.')):
                return True, ''
            return False, ''
        except ValueError:
            return False, '<p class="int_required"></p>'

class IntGT(TestInt):
    """Returns True if the student answer is an integer strictly greater than
    the specified value.
    
    Examples:
        # If the answer is not an integer a comment is returned.
        Good(IntGT(1984) & IntLT(2001))
"""
    def do_test(self, student_answer, state):
        try:
            if int(student_answer) > self.integer:
                return True, ''
            return False, ''
        except ValueError:
            return False, '<p class="int_required"></p>'

class IntLT(TestInt):
    """Returns True if the student answer is an integer smaller than
    the specified value.
    
    Examples:
        # If the answer is not an integer a comment is returned.
        Good(IntGT(1984) & IntLT(2001))
"""
    def do_test(self, student_answer, state):
        try:
            if int(student_answer) < self.integer:
                return True, ''
            return False, ''
        except ValueError:
            return False, '<p class="int_required"></p>'

class Length(TestInt):
    """Returns True if the length of the student answer is equal
    to the integer specified.

    Examples:
       # Note the negation of the condition: ~
       Bad(Comment(~Length(3), "The expected answer is 3 character long"))
    """
    def do_test(self, student_answer, state):
        return len(student_answer) == self.integer, ''

class LengthLT(TestInt):
    """Returns True if the length of the student answer is smaller then
    the integer specified.

    Examples:
       # Note the negation of the condition: ~
       Bad(Comment(~LengthLT(10),
                   "The expected answer is less than 10 characters long"))
    """
    def do_test(self, student_answer, state):
        return len(student_answer) < self.integer, ''

class NrBadAnswerGreaterThan(TestInt):
    """Returns True if the number of bad student-answers since the last
    question reset is greater than the integer in parameter.

    Examples:
        Bad(Comment(NrBadAnswerGreaterThan(3),
                    "Let me give you a tip: ...."))
    """
    def do_test(self, dummy_student_answer, state):
        if len(state.student.answer(state.question.name).bad_answers
              ) > self.integer:
            return True, ''
        else:
            return None, ''

class NumberOfIs(TestExpression):
    """The number of time the first parameter string is found in the
    student answer must be equal to the integer.

    Examples:
       # Note the negation of the condition: ~
       Bad(Comment(~NumberOfIs("x", 3) | ~NumberOfIs("y", 2),
                   "Your answer must contain 3 'x' and 2 'y'"))
    """
    def __init__(self, string, number, canonize=False):
        if not isinstance(number, int):
            raise ValueError("Expect an integer")
        self.string = string
        self.number = number
        self.do_canonize = canonize

    def source(self, state=None, format=None):
        if self.do_canonize:
            canonize = ',canonize=True'
        else:
            canonize = ''
        return self.test_name(format) + '(' + pf(self.string,format) + ',' + \
               str(self.number) + canonize + ')'

    def do_test(self, student_answer, state=None):
        return student_answer.count(self.string) == self.number, ''

    def canonize_test(self, parser, state):
        if self.do_canonize:
            self.string_canonized = parser(self.string, state)
        else:
            self.string_canonized = self.string


# Should apply the parser on all the dict items

class TestDictionary(TestExpression):
    """Base class for enumeration tests.
    The class is easely derivable by specifying a dictionnary containing
    all the allowed answers and how they are canonized.
    """
    def error_message(self):
        return ('<p class="possible_answers">'
                + ' '.join('«<b>' + i + '</b>»' for i in self.dict)
                + '</p>')
    def do_test(self, student_answer, state=None):
        if self.uppercase:
            student_answer = student_answer.upper()
        if student_answer not in self.dict:
            return False, self.error_message()
        r = self.dict[student_answer]
        if r == self.good:
            return True, ''
        
        return False, ''

class YesNo(TestDictionary):
    """Base class for yes/no tests."""
    def error_message(self):
        return '<p class="yes_or_no"></p>'
    uppercase = True
    dict = {'OUI': 'O', 'Y': 'O', 'YES': 'O', 'O': 'O',
            'NON': 'N', 'NO': 'N', 'N': 'N',
            }

class Yes(YesNo):
    """Returns True if the student answer Yes

    Examples:
        Good(Yes())
    """
    good = 'O'

class No(YesNo):
    """Returns True if the student answer No

    Examples:
        Good(No())
    """
    good = 'N'
    
class Grade(TestUnary):
    """If the first expression is True:
       Set a grade for the student+question+teacher.
       The grade can be a positive or negative number.
       The 'teacher' can be the name of a knowledge, or a list of knowledges.
       Grade always returns the value returned by the first expression.
       The grades are summed per teacher when exporting all the grades.

       BEWARE :
           Grades are computed only when the student answer.
           If formula change, they will not be recomputed.

       It is done so because recomputing every grade on server start
       can be long if there are many students.
          

    Examples:
       # If the student answers:
       #   * '2' or 'two'    then 'point'       is set to 1.
       #   *        'two'    then 'see_student' is set to 1
       #   * integer != 2    then 'calculus'    is set to -2
       #   * not in integer then no grades are changed.
       Good(Grade(Grade(Equal('two'), "see_student", 1)  |  Int(2),
                  "point", 1)
           ),
       Bad(Grade(~Int(2), "calculus", -2))

       # If the student answers:
       #   * 'x'  then 'point' is set to 1.
       #   * 'xy' then 'point' is set to 2.
       # RECURSIVELY GRADING THE SAME THING DOES NOT WORKS
       # BECAUSE THE TOP MOST WINS.
       Good(And(Contain('x'),
                Or(Grade(Contain('y'), "point", 2),
                   Grade(Contain(''), "point", 1), # allow 'x' alone answer
                  )
               )
           ),
    """
    stop_eval = True
    def __init__(self, expression, teacher, grade):
        self.teacher = teacher
        self.grade = grade
        TestUnary.__init__(self, expression)
    def source(self, state=None, format=None):
        return self.block(format,
                          [self.children[0].source(state, format),
                           repr(self.teacher) + ',' + repr(self.grade)])
    def do_test(self, student_answer, state=None):
        goodbad, a_comment = self.children[0](student_answer, state)
        if state.question and goodbad is True:
            grade = self.grade
        else:
            grade = 0
        if isinstance(self.teacher, str):
            teachers = [self.teacher]
        else:
            teachers = self.teacher
        for teacher in teachers:
            state.student.set_grade(state.question.name, teacher, grade)
        if self.stop_eval:
            return goodbad, a_comment
        else:
            return None, a_comment

class GRADE(Grade):
    """As Grade, but return None to not stop the tests after the first grade.

    Examples:
       # Every answer is good, but grades are stored.
       # If 'fast and hot' is answered, 2 grades will be made.
       GRADE(Contain("fast", "understand speed", 1)),
       GRADE(Contain("hot", "understand energy", 1)),
       Good(Contain("")),    
    """
    stop_eval = False

def random_chooser(state, question, key, values):
    if state:
        try:
            return values[state.student.persistent_random(
                state, question, len(values), key)]
        except IndexError:
            # The question has been removed from questionnary
            return values[0]
    else:
        return values[0]

def random_replace(state, question, string, values):
    if not isinstance(values, dict):
        # The values can be a list of dicts:
        # ( {'A':(1,3,5,7,9),'B':("odd",)},
        #   {'A':(0,2,4,6,8),'B':("even",)}
        # )
        # A random dict is chosen
        values = values[state.student.persistent_random(
            state, question, len(values), "__RD__")]
    for k, v in values.items():
        if k in string:
            string = string.replace(k, random_chooser(state, question, k, v))
    return string

def random_question(question, choices):
    def f(state):
        return random_replace(state, f._question_.name, question, choices)
    if isinstance(choices, dict):
        f.nr_const = max(len(v) for v in choices.values())
    else:
        f.nr_const = len(choices)
    f.nr_versions = lambda: f.nr_const
    return f

class Random(TestUnary):
    """The first argument is a dictionnary as in the example.
    
       In all the strings, the dictionnary key is replaced by one
       of the values in the right part.
       The replacement is random, but stay the same for each student.

       An helper function 'random_replace' is provided to apply the same
       replacement in the question text.

       To not break the session history, if you add new choices, add them
       to the end of the list. Random choices will not change.

    Examples:
       choices = {'dirname' : ("usr", "tmp", "bin"),
          'filename': ("x", "y", "z"),
         }
       ...
       question = random_question("How to delete /dirname/filename ?",
                                  choices),
       tests = ( Good(Random(choices,Shell(Equal("rm /dirname/filename")))),
                 Random(choices, Expect("dirname")),
                 Random(choices, Expect("filename")),
               ),
                                                 
    """
    def __init__(self, values, content):
        TestExpression.__init__(self, content)
        self.values = values

    def canonize(self, string, state):
        """Do not canonize the student answer, but the test"""
        if state:
            self.children[0].initialize(
                lambda string, a_state:
                    random_replace(a_state, self._question_.name,
                                   string, self.values),
                state
                )
        return string

    def nr_versions(self):
        if isinstance(self.values, dict):
            # The real number is the product
            return max(len(v)
                       for v in self.values.values())
        else:
            return len(self.values)

    def source(self, state=None, format=None):
        return self.block(format, [repr(self.values),
                                   self.children[0].source(state, format)])

    def __call__(self, student_answer, state=False):
        """Add a compatibility layer for old tests"""
        if state is False:
            return random_replace(student_answer, self._question_.name,
                                  self.children[0](student_answer),
                                  self.values)
        student_answer = self.canonize(student_answer, state)
        return self.do_test(student_answer, state)

class Choice(TestExpression):
    """Allow to choose a random question in a list.

       To not break the session history, if you add new choices, add them
       to the end of the list. Random choices will not change.

    Examples:
        choices = Choice(('1+1 is equal to:',
                          Good(Int(2)),
                          Bad(Comment(Int(10), "Decimal base please"))
                         ),
                         ('How do you translate 2 in french?',
                          Good(Equal("deux")),
                         ),
                        )
        add(name="stupid",
            question = choices,
            tests = (choices,),
           )
    """
    def __init__(self, *args):
        self.children = []
        self.args = list(args)
        for i, arg in enumerate(args):
            question = arg[0]
            if not callable(question):
                self.args[i] = list(self.args[i])
                def tmp(dummy_state, question=question):
                    return question
                self.args[i][0] = tmp
            arg = arg[1:]
            self.children += arg
            for test in arg:
                test.initialize(lambda string, state: string, None)

    def initialize(self, parser, state):
        """The string in test description must be canonized"""
        self.parser = parser #Store the parser for future use (See HostReplace)
        for arg in self.args:
            for test in arg[1:]:
                test.initialize(lambda string, a_state:
                                self.canonize(parser(string,a_state),a_state),
                                state
                            )

    def choice(self, state):
        if not state:
            return self.args[0]
        return self.args[state.student.persistent_random(
            state, self._question_.name, len(self.args), "__CHOICE__")]

    def do_test(self, student_answer, state):
        all_comments = ""
        a_bool = False
        for c in self.choice(state)[1:]:
            a_bool, a_comment = c(student_answer, state)
            all_comments += a_comment
            if a_bool is not None:
                break
        return a_bool, all_comments

    def nr_versions(self):
        return len(self.args)

    def source(self, state=None, format=None):
        s = []
        for arg in self.args:
            question = arg[0](state)
            t = [pf(question, format)]
            for a in arg[1:]:
                t.append(a.source(state, format))
            s.append(self.block(format, t, name=""))
        return self.block(format, s)

    def __call__(self, student_answer, state=False):
        if state is False:
            return self.choice(student_answer)[0](student_answer)
        else:
            return self.do_test(student_answer, state)

    def get_good_answers(self, state):
        for c in self.choice(state)[1:]:
            yield from c.get_good_answers(state)

def regression_tests():
    # Regression test on new tests.
    grades = {}
    class A:
        nr_erase = 0
    class S:
        import collections
        answers = collections.defaultdict(A)
        seed = 0
        def persistent_random(self, *args):
            return A.nr_erase % args[2]
        def set_grade(self, q, t, g):
            grades[q] = (t, g)
    class Q:
        name = 'x'
    class St:
        student = S()
        question = Q()
    q = Q()
    def create(txt):
        grades.clear()
        o = eval(txt)
        o.initialize(lambda string, state: string, None)
        o.link_to_question(q)
        # print o.source()
        # print txt
        src = o.source()
        if src != txt:
            print(txt)
            print(src)
            raise ValueError("Bad source")
        return o

    a = create("Equal('5')")
    assert( a('5') == (True, '') )
    assert( a('6') == (False, '') )
    assert( a.source(format='html') == "<b>Equal</b>('5')" )

    a = create("Good(Equal('7'))")
    assert( a('5') == (None, '') )
    assert( a('7') == (True, '') )
    
    a = create("Good(Comment(Equal('8'),'x'))")
    assert( a('5') == (None, '') )
    assert( a('8') == (True, 'x') )

    a = create("Bad(Equal('9'))")
    assert( a('5') == (None, '') )
    assert( a('9') == (False, '') )
    
    a = create("Bad(Comment(Equal('1'),'x'))")
    assert( a('5') == (None, '') )
    assert( a('1') == (False, 'x') )

    a = create("Comment(Comment(Equal('2'),'y'),'z')")
    assert( a('5') == (False, '') )
    assert( a('2') == (True, 'yz') )

    a = create("Comment(~Comment(~Equal('2'),'y'),'z')")
    assert( a('5') == (False, 'y') )
    assert( a('2') == (True, 'z') )
    
    a = create("Bad(Comment(~Comment(~Equal('2'),'y'),'z'))")
    assert( a('2') == (False, 'z') )
    assert( a('5') == (None, 'y') )
    

    a = create("Contain('a')")
    assert( a('bab') == (True, '') )
    assert( a('bbb') == (False, '') )

    a = create("Start('a')")
    assert( a('abb') == (True, '') )
    assert( a('bab') == (False, '') )
    assert( a('bba') == (False, '') )
    
    a = create("End('a')")
    assert( a('abb') == (False, '') )
    assert( a('bab') == (False, '') )
    assert( a('bba') == (True, '') )
    
    a = create("Or(Equal('c'),Equal('d'),Equal('e'))")
    assert( a('c') == (True, '') )
    assert( a('d') == (True, '') )
    assert( a('e') == (True, '') )
    assert( a('f') == (False, '') )

    a = create("Or(Comment(Contain('f'),'F'),Comment(Contain('g'),'G'))")
    assert( a('fg') == (True, 'F') )
    assert( a('gf') == (True, 'F') )
    assert( a('f') == (True, 'F') )
    assert( a('g') == (True, 'G') )
    assert( a('x') == (False, '') )

    a = create("Or(Comment(Contain('f'),'F'),Comment(Contain('g'),'G'),shortcut=False)")
    assert( a('fg') == (True, 'FG') )

    a = create("And(Comment(Contain('f'),'F'),Comment(Contain('g'),'G'))")
    assert( a('x') == (False, '') )
    assert( a('f') == (False, 'F') )
    assert( a('g') == (False, '') )
    assert( a('fg') == (True, 'FG') )
    assert( a('gf') == (True, 'FG') )

    a = create("Comment(And(Comment(Contain('f'),'F'),Comment(Contain('g'),'G')),'H')")
    assert( a('x') == (False, '') )
    assert( a('f') == (False, 'F') )
    assert( a('g') == (False, '') )
    assert( a('fg') == (True, 'FGH') )

    a = create("UpperCase(Equal('a'))")
    assert( a('a') == (True, '') )
    assert( a('A') == (True, '') )

    a = create("UpperCase(Equal('A'))")
    assert( a('a') == (True, '') )
    assert( a('A') == (True, '') )
    assert( a('b') == (False, '') )

    a = create("UpperCase(Or(Equal('A'),Equal('B')))")
    assert( a('a') == (True, '') )
    assert( a('A') == (True, '') )
    assert( a('b') == (True, '') )
    assert( a('B') == (True, '') )
    
    a = create("~Equal('K')")
    assert( a('k') == (True, '') )
    assert( a('K') == (False, '') )

    a = create("~Comment(Equal('K'),'L')")
    assert( a('k') == (True, '') )
    assert( a('K') == (False, 'L') )

    a = create("Comment(~Equal('K'),'M')")
    assert( a('k') == (True, 'M') )
    assert( a('K') == (False, '') )

    a = create("Replace((('a', '1'), ('b', '2')),Equal('abc'))")
    assert( a('12c') == (True, '') )
    
    a = create("Replace((('a', '1'), ('b', '2')),Equal('c12'))")
    assert( a('c12') == (True, '') )
    assert( a('cab') == (True, '') )
    assert( a('ca') == (False, '') )

    a = create("Replace((('a', '1'), ('b', '2')),Equal('12c'))")
    assert( a('abc') == (True, '') )
    assert( a('12c') == (True, '') )

    a = create("UpperCase(Replace((('a', '1'), ('b', '2')),Equal('abc')))")
    # The string in the replacement are not uppercased.
    # Replace is no more usable with the shell parser if they are.
    assert( a('12c') == (False, '') )

    a = create("UpperCase(Replace((('a', '1'), ('b', '2')),Equal('abc'),canonize=True))")
    # The string in the replacement are uppercased.
    assert( a('12c') == (True, '') )
    
    a = create("UpperCase(Replace((('a', '1'), ('b', '2')),Equal('12C')))")
    assert( a('12c') == (True, '') )
    assert( a('abc') == (False, '') )

    a = create("UpperCase(Replace((('A', '1'), ('B', '2')),Equal('12c')))")
    assert( a('abc') == (True, '') )

    a = create("UpperCase(Replace((('A', '1'), ('B', '2')),Equal('abc')))")
    assert( a('abc') == (True, '') )


    a = create("Replace((('a', 'x'),),UpperCase(Equal('a')))")
    assert( a('a') == (True, '') )
    assert( a('A') == (False, '') )

    a = create("Replace((('a', 'x'),),UpperCase(Equal('A')))")
    assert( a('a') == (False, '') )
    assert( a('A') == (True, '') )

    a = create("Replace((('a', 'x'),),UpperCase(Equal('x')))")
    assert( a('a') == (True, '') )
    assert( a('A') == (False, '') )

    a = create("Replace((('a', 'x'),),UpperCase(Equal('X')))")
    assert( a('a') == (True, '') )
    assert( a('A') == (False, '') )

    a = create("Replace((('a', '1'), ('b', '2')),UpperCase(Equal('abc')))")
    assert( a('12c') == (True, '') )
    assert( a('abc') == (True, '') )
    assert( a('ABc') == (False, '') )

    a = create("Replace((('a', '1'), ('b', '2')),UpperCase(Equal('12c')))")
    assert( a('abc') == (True, '') )
    assert( a('ABc') == (False, '') )

    a = create("SortLines(Equal('a\\nb'))")
    assert( a('a\nb') == (True, '') )
    assert( a('b\na') == (True, '') )
    assert( a('ba') == (False, '') )

    a = create("And(Or(Contain('a'),Contain('b')),Or(Contain('c'),Contain('d')))")
    assert( a('a') == (False, '') )
    assert( a('b') == (False, '') )
    assert( a('c') == (False, '') )
    assert( a('d') == (False, '') )
    assert( a('ab') == (False, '') )
    assert( a('ac') == (True, '') )
    assert( a('ad') == (True, '') )
    assert( a('bc') == (True, '') )
    assert( a('bd') == (True, '') )
    assert( a('cd') == (False, '') )

    a = create("Bad(Or(Comment(And(Start('a'),~Contain('1')),'a->1'),Comment(And(Start('b'),~Contain('2')),'b->2')))")
    assert( a('x') == (None, '') )
    assert( a('a') == (False, 'a->1') )
    assert( a('b') == (False, 'b->2') )
    assert( a('a1') == (None, '') )
    assert( a('b2') == (None, '') )

    a = create("Int(6)")
    assert( a('6') == (True, '') )
    assert( a('+6') == (True, '') )
    assert( a('6.5')[0] == False and a('6.5')[1] != '' )
    assert( a('x')[0] == False and a('x')[1] != '')

    a = create("Length(1)")
    assert( a('') == (False, '') )
    assert( a('6') == (True, '') )
    assert( a('66') == (False, '') )

    a = create("Yes()")
    assert( a('')[0]  == False and a('')[1] != '' )
    assert( a('N') == (False, '') )
    assert( a('Y') == (True, '') )
    assert( a('non') == (False, '') )
    assert( a('oui') == (True, '') )

    a = create("Good(No())")
    assert( a('N') == (True, '') )
    assert( a('Y') == (None, '') )
    assert( a('')[0] == None and a('')[1] != '' )
    
    a = create("NumberOfIs('a',2)")
    assert( a('papa') == (True, '') )
    assert( a('ppa') == (False, '') )

    a = create("Comment(NumberOfIs('a',2),'good')")
    assert( a('papa') == (True, 'good') )
    assert( a('ppa') == (False, '') )

    a = create("Comment(~NumberOfIs('a',2),'bad')")
    assert( a('papa') == (False, '') )
    assert( a('ppa') == (True, 'bad') )

    a = create("Bad(Comment(~NumberOfIs('a',2),'bad'))")
    assert( a('papa') == (None, '') )
    assert( a('ppa') == (False, 'bad') )

    a = create("~Comment(~NumberOfIs('a',2),'bad')")
    assert( a('papa') == (True, '') )
    assert( a('ppa') == (False, 'bad') )

    a = create("UpperCase(Contain('a'))")
    assert( a('bab') == (True, '') )
    assert( a('bbb') == (False, '') )
    assert( a('bAb') == (True, '') )

    a = create("UpperCase(Contain('A'))")
    assert( a('bab') == (True, '') )
    assert( a('bbb') == (False, '') )
    assert( a('bAb') == (True, '') )

    a = create("Bad(Or(Comment(Contain('x'),'x'),Comment(Contain('y'),'y')))")
    assert( a('x') == (False, 'x') )
    assert( a('y') == (False, 'y') )
    assert( a('yx') == (False, 'x') )
    
    a = create("Bad(And(Comment(Contain('x'),'x'),Comment(Contain('y'),'y')))")
    assert( a('x') == (None, 'x') )
    assert( a('y') == (None, '') )
    assert( a('xy') == (False, 'xy') )
    assert( a('yx') == (False, 'xy') )

    a = create("Good(RemoveSpaces(Equal('a + 5')))")
    assert( a('a+5') == (True, '') )
    assert( a('a + 5') == (True, '') )
    assert( a('a  +  5') == (True, '') )

    a = create("Good(RemoveSpaces(Equal('a + - 5')))")
    assert( a('a+-5') == (True, '') )
    assert( a('a  +   -   5') == (True, '') )

    a = create("Grade(Equal('a'),'john',4)")
    st = St()
    assert( a('b',st) == (False, '') )
    assert( grades == {'x': ('john', 0)} )
    assert( a('a',st) == (True, '') )
    assert( grades == {'x': ('john', 4)} )

    a = create("Good(Random({'$a$': ('x', 'x')},Equal('[$a$]')))")
    assert( a('x', st) == (None, '') )
    assert( a('[x]', st) == (True, '') )
    assert( a('$a$', st) == (None, '') )

    a = create("Random({'$a$': ('x', 'x')},Expect('[$a$]'))")
    assert( a('x', st)
            == (False, '<p class="string_expected">«<b>[x]</b>»</p>') )

    a = create("Good(And(Contain('x'),Or(Grade(Contain('y'),'point',2),Grade(Contain(''),'point',1))))")
    assert(a('z', st) == (None, ''))
    assert(grades == {})
    grades.clear()
    assert(a('x', st) == (True, ''))
    assert(grades == {'x': ('point', 1)})
    grades.clear()
    assert(a('y', st) == (None, ''))
    assert(grades == {})
    grades.clear()
    assert(a('xy', st) == (True, ''))
    assert(grades == {'x': ('point', 2)})

    a = create("Good(And(Contain('x'),Contain('y')))")
    assert(a('x', st) == (None, ''))

    a = create("Good(IsInt())")
    assert(a('x') == (None, ''))
    assert(a('42') == (True, ''))

    a = create("Random({'D': ('E',)},Comment('(D)'))")
    assert( a('x',st) == (None, '(D)') )
    a = create("Random({'D': ('E',)},Comment('(D)',canonize=True))")
    assert( a('x',st) == (None, '(E)') )

    a = create("Choice(('a',Good(Comment(Equal('1'),'U')),Bad(Comment(Equal('2'),'D'))))")
    assert( a('x',st) == (None, '') )
    assert( a('1',st) == (True, 'U') )
    assert( a('2',st) == (False, 'D') )

    a = create("Replace((('2', '1'),),Choice(('a',Good(Comment(Equal('1'),'U')))))")
    assert( a('2',st) == (True, 'U') )

    a = create("Choice(('a',Good(Replace((('2', '1'),),Comment(Equal('2'),'U')))))")
    assert( a('2',st) == (True, 'U') )
    assert( a(st) == 'a' )

    a = create("Replace((('2', '1'),),Choice(('a',Good(Comment(Equal('2'),'U')))),canonize=True)")
    assert( a('2',st) == (True, 'U') )

    a = create("Grade(Good(Equal('a')),'GG1',1)")
    assert( a('2',st) == (None, '') )
    assert( grades['x'] == ('GG1', 0) )
    assert( a('a',st) == (True, '') )
    assert( grades['x'] == ('GG1', 1) )

    a = create("Grade(Bad(Equal('a')),'GG1',2)")
    assert( a('2',st) == (None, '') )
    assert( grades['x'] == ('GG1', 0) )
    assert( a('a',st) == (False, '') )
    assert( grades['x'] == ('GG1', 0) )

    a = create("Random({'F': ('1', '2')},Choice(('{F}',Good(Comment(Equal('(F)'),'[F]')))))")
    assert( a('(1)',st) == (True, '[F]') )
    assert( a(st) == '{1}' )
    A.nr_erase = 1
    assert( a(st) == '{2}' )
    assert( a('(2)',st) == (True, '[F]') )
    A.nr_erase = 0

    a = create("Random({'F': ('1', '1')},Choice(('{F}',Good(Comment(Equal('(F)'),'[F]',canonize=True)))))")
    assert( a(st) == '{1}' )
    assert( a('F',st) == (None, '') )
    assert( a('(1)',st) == (True, '[1]') )

    a = create("Random({'F': ('1', '2', '3')},Choice(('Fa',Good(Comment(Equal('(F)a'),'[F]a',canonize=True))),('Fb',Good(Comment(Equal('(F)b'),'[F]b',canonize=True)))))")
    assert( a(st) == '1a' )
    assert( a('(1)a',st) == (True, '[1]a') )
    A.nr_erase = 1
    assert( a(st) == '2b' )
    assert( a('(2)b',st) == (True, '[2]b') )
    A.nr_erase = 2
    assert( a(st) == '3a' )
    assert( a('(3)a',st) == (True, '[3]a') )
    A.nr_erase = 3
    assert( a(st) == '1b' )
    assert( a('(1)b',st) == (True, '[1]b') )
    A.nr_erase = 0

    good = "Good(Contain('AF'))"
    bad = "Bad(Comment(Contain('ZF'),'BaD'))"
    for operator in ('And', 'Or'):
        for x, y in ( (good, bad), (bad, good) ):
            a = create(
                "Random({'F': ('1', '2')},%s(Expect('F'),Reject('X'),%s,%s))"
                 % (operator, x, y))
            assert( a('3',st)==(False,'<p class="string_expected">«<b>1</b>»</p>'))
            assert( a('X1',st)==(False,'<p class="string_rejected">«<b>X</b>»</p>'))
            assert( a('A1',st)==(True, ''))
            assert( a('Z1',st)==(False, 'BaD'))
            assert( a('Y1',st)==(None, ''))

            if operator == 'And':
                assert(a('A1Z1',st)==(False, 'BaD'))
            else:
                assert(a('A1Z1',st)==(True, '' if x == good else 'BaD'))

if True:
    regression_tests()
