#!/usr/bin/env python
# -*- coding: latin1 -*-
#    QUENLIG: Questionnaire en ligne (Online interactive tutorial)
#    Copyright (C) 2005-2011 Thierry EXCOFFIER, Universite Claude Bernard
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

import types
import os
import utilities
import inspect
import sys
import cgi
import re

current_evaluate_answer = None
class Required:
    def __init__(self, world, string):
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

    def answered(self, answered):
        for r in self.requireds:
            if not answered.get(r.name, False):
                return False
            if r.answer and not re.match(r.answer, answered[r.name]):
                return False
        return True

    def names(self):
        return [r.name for r in self.requireds]

def transform_question(question):
    if question == None:
        return None
    q = question
    if isinstance(question, types.FunctionType):
        if 'state' not in question.func_code.co_varnames:
            def tmp(state):
                return q()
            return tmp                    
    else:
        def tmp(state):
            return q
        return tmp
    return question
    

class Question:
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

        self.question = transform_question(arg["question"])

        self.tests = arg.get("tests", ())
        self.before = transform_question(arg.get("before", None))
        self.good_answer = arg.get("good_answer", "")
        if not isinstance(self.good_answer, basestring):
            raise ValueError("good_answer must be a string")
        self.bad_answer = arg.get("bad_answer", "")
        if not isinstance(self.bad_answer, basestring):
            raise ValueError("bad_answer must be a string")
        self.nr_lines = int(arg.get("nr_lines", "1"))
        self.comment = []
        self.required = arg.get("required", previous_question)
        self.required = Requireds([Required(world, i) for i in self.required])
            
        self.indices = arg.get("indices", ())
        self.default_answer = arg.get("default_answer", "")
        self.evaluate_answer = current_evaluate_answer
        self.highlight = arg.get("highlight", False)
        self.maximum_bad_answer = int(arg.get("maximum_bad_answer", "0"))

    def answers_html(self, state):
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
        answer = answer.strip(" \n\t\r").replace("\r\n", "\n")
        if self.nr_lines == 1 and answer.find("\n") != -1:
            return False, "VOTRE REPONSE CONTIENT DES RETOURS A LA LIGNE"
        if self.evaluate_answer:
            answer = self.evaluate_answer(answer, state)

        full_comment = []
        for t in self.tests:
            if isinstance(t, types.FunctionType):
                if 'state' in t.func_code.co_varnames:
                    result, comment = t(answer, state=state)
                else:
                    result, comment = t(answer)
            else:
                result, comment = t(answer, state=state)
            if comment not in full_comment:
                full_comment.append(comment)
            if result != None:
                return result, ''.join(full_comment)
        return False, ''.join(full_comment)

    # Comments starting by a white space are not
    # considered as usefull for the student.
    # It is used by questions.py/comment function.
    def answer_commented(self, answer):
        a = self.check_answer(answer, None)
        if a[0]:
            return "*" # Correct answer, so commented.
        c = a[1]
        c = re.sub("<sequence.*</sequence>", "", c.replace("\n",""))
        if c == ' ':
            c = ''
        return c

    def url(self):
        return "?question=%s" % cgi.urllib.quote(self.name)

    def a_href(self):
        return "<A HREF=\"%s\">%s</A>" % (self.url(), cgi.escape(self.name))

    def nr_indices(self):
        return len(self.indices)

    def __str__(self):
        return self.name



    # When storing source, we store the source of the question in a file.
    # when a question is modified, the source of the question is saved
    # and the sources of all the other questions.

    def source_python(self, comment=""):
        s = ["# %s\nadd(name=\"%s\"," % (comment, self.short_name)]
        r = ""
        for required in self.required.names():
            world, name = required.split(':')
            if world == self.world:
                required = name
            r += '"%s",' % required
        s.append("required=[%s]," % r[:-1])
        s.append("before=%s" % self.before )
        s.append(")")
        return '\n'.join(s)

    def store_file(self):
        """Store every questions in the file.py"""
        f = open(os.path.join(self.path) + '.new', 'w')
        for q in questions:
            if q.world != self.world:
                continue
            f.write( q.source_python(self) )
        f.close()

    def store_source(self):
        file_dir = os.path.join(*self.path)
        if not os.path.isdir(file_dir):
            os.mkdir(file_dir)
        question_dir = os.path.join(file_dir, self.short_name) + '.log'
        if not os.path.isdir(question_dir):
            os.mkdir(question_dir)

        history = [-1] + [int(i) for i in os.listdir(question_dir)]
        history.sort()
        new_name = '%04d' % (history[-1] + 1)
        f = open( os.path.join(question_dir, new_name), 'w')
        f.write(self.source_python())
        f.close()
        
##    def __cmp__(self, other):
##        if other == None:
##            return 1
##        return cmp(self.name, other.name)

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
    }

    sys.stdout.write("*")
    sys.stdout.flush()
    world = inspect.currentframe().f_back.f_globals["__name__"].split(".")
    for a in arg.keys():
        if a not in attributs.keys():
            print "'%s' n'est pas un attribut de question" % a
            print "Les attributs possibles de questions sont:"
            for i in attributs.keys():
                print "\t%s: %s" % (i, attributs[i]) 
            raise KeyError("Voir stderr")
    arg["name"] = world[-1] + ":" + arg["name"]
    if arg["name"] in questions.keys():
        print "Une question porte deja le nom", arg["name"]
        raise KeyError("Voir stderr")
    global previous_question
    if previous_question and previous_question.split(":")[0] == world[-1]:
        pq = [previous_question]
    else:
        pq = []
    questions[arg["name"]] = Question(world, arg, previous_question=pq
                                      )
    previous_question = arg["name"]

def answerable(answered, student):
    """Returns the authorized question list.
    The parameter is the names of the questions yet answered.
    The prequired are checked here.
    """
    answerable = []
    for q in questions.values():
        if not answered.get(q.name,False) and q.required.answered(answered):
            if (q.maximum_bad_answer == 0
                or student.bad_answer_question(q.name) < q.maximum_bad_answer):
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
    return d.keys()

sorted_questions = []

def compare_questions(x, y):
    c = cmp(x.level, y.level)
    if c != 0:
        return c
    return cmp( len(y.used_by), len(x.used_by) ) # Most used first

# Very far from optimal algorithm
def sort_questions():
    for q in questions.values():
        q.level = 0
        q.used_by = []

    # Compute 'used_by'
    for q in questions.values():
        for r in q.required.names():
            try:
                questions[r].used_by.append(q.name)
            except KeyError:
                print q.name, '=== REQUIRE ===>', r

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

    # Compute 'level' (not optimal)
    while True:
        change = False
        for q in questions.values():
            max_level = [ questions[r].level for r in q.required.names() ]
            if max_level:
                max_level = max(max_level)
            else:
                max_level = 0
            if q.level != max_level + 1:
                q.level = max_level + 1
                change = True
        if not change:
            break

    global sorted_questions
    sorted_questions = questions.values()
    sorted_questions.sort(compare_questions)

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

class Test:
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
                
            if state != None and 'state' in self.test.func_code.co_varnames:
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
            return False, \
                   "Je devrais trouver '<tt>%s</tt>' dans la réponse" % string
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
        
    return False, "Je ne comprend pas votre réponse. C'est OUI ou NON."
    
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
# Good(Shell(Contain("<parameter>-z</parameter>")))

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
        return cgi.escape(txt)
    raise ValueError('Unknown output format')

def no_parse(string, state, test):
    return string

class TestExpression(Test):

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

class TestNAry(TestExpression):
    def source(self, state=None, format=None):
        return self.test_name(format) + '(' + \
               ','.join( [c.source(state, format) for c in self.children]) + \
               ')'

class TestUnary(TestExpression):
    def source(self, state=None, format=None):
        return self.test_name(format) + \
               "(%s)" % self.children[0].source(state, format)

class TestString(TestExpression):
    def __init__(self, string):
        if not isinstance(string, basestring):
            raise ValueError("Expect a string")
        self.string = string

    def source(self, state=None, format=None):
        return self.test_name(format) + '(%s)' % pf(self.string, format)

class Or(TestNAry):
    def __call__(self, student_answer, state=None, parser=no_parse):
        all_comments = ""
        bool = False
        for c in self.children:
            bool, comment = c(student_answer, state, parser)
            all_comments += comment
            if bool == True:
                break
        return bool, all_comments

    def __or__(self, other):
        self.children.append(other)
        return self


class And(TestNAry):
    operator = " & "
    def __call__(self, student_answer, state=None, parser=no_parse):
        all_comments = ""
        bool = False
        for c in self.children:
            bool, comment = c(student_answer, state, parser)
            all_comments += comment
            if bool == False:
                break
        return bool, all_comments
    def __and__(self, other):
        self.children.append(other)
        return self

class TestInvert(TestUnary):
    def source(self, state=None, format=None):
        return "~" + self.children[0].source(state, format)
    def __call__(self, student_answer, state=None, parser=no_parse):
        bool, comment = self.children[0](student_answer, state, parser)
        return not bool, comment

class TestFunction(TestUnary):
    """The given function returns a boolean and a comment"""
    def __init__(self, fct):
        if not callable(fct):
            raise ValueError("Expect a callable object")
        self.fct = fct

    def __call__(self, student_answer, state=None, parser=no_parse):
        return self.fct(student_answer, state)


class Equal(TestString):
    def __call__(self, student_answer, state=None, parser=no_parse):
        return student_answer == parser(self.string, state, self), ""

class Contain(TestString):
    def __call__(self, student_answer, state=None, parser=no_parse):
        return parser(self.string, state, self) in student_answer, ""

class Start(TestString):
    def __call__(self, student_answer, state=None, parser=no_parse):
        return student_answer.startswith(parser(self.string, state, parser)),""

class End(TestString):
    def __call__(self, student_answer, state=None, parser=no_parse):
        return student_answer.endswith(parser(self.string,state,parser)), ""

class Good(TestUnary):
    def __call__(self, student_answer, state=None, parser=no_parse):
        bool, comment = self.children[0](student_answer, state)
        if bool == True:
            return bool, comment
        return None, comment

class Bad(TestUnary):
    def __call__(self, student_answer, state=None, parser=no_parse):
        bool, comment = self.children[0](student_answer, state)
        if bool == True:
            return False, comment
        return None, comment

class UpperCase(TestUnary):
    def __call__(self, student_answer, state=None, parser=no_parse):
        return self.children[0](
            student_answer.upper(), state,
            lambda string, state, test: parser(string.upper(), state, test))

class SortLines(TestUnary):
    def __call__(self, student_answer, state=None, parser=no_parse):
        return self.children[0](
            sort_lines(student_answer), state,
            lambda string, state, test: parser(sort_lines(string), state, test)
            )

class Comment(TestUnary):
    def __init__(self, *args):
        if len(args) == 1:
            a = ()
            comment = args[0]
        elif len(args) == 2:
            a = (args[0], )
            comment = args[1]
        else:
            raise ValueError("%s can have only 2 or 1 arguments" %
                             self.__class__.__name__)
        TestExpression.__init__(self, *a)
        self.comment = comment

    def source(self, state=None, format=None):
        if self.children:
            return self.test_name(format) + "(%s,%s)" % (
                self.children[0].source(state,format), pf(self.comment,
                                                               format) )
        else:
            return self.test_name(format) + "(%s)" % pf(self.comment, format)
    
    def __call__(self, student_answer, state=None, parser=no_parse):
        if self.children:
            bool, comment = self.children[0](student_answer, state, parser)
        else:
            return None, self.comment
        if bool == True:
            comment += self.comment
        return bool, comment

class Expect(TestString):
    def __init__(self, *args):
        if len(args) == 1:
            self.comment = None
        else:
            self.comment = args[1]
        TestString.__init__(self, args[0])

    def __call__(self, student_answer, state=None, parser=no_parse):
        if parser(self.string, state, self) in student_answer:
            return None, ''
        else:
            if self.comment:
                return False, self.comment
            else:
                return False, "Je devrais trouver '<tt>%s</tt>' dans la réponse" % self.string

def expects(expected, comment=None):
    a = Expect(expected[0], comment)
    for e in expected[1:]:
        a = a & Expect(e, comment)
    return a

class Reject(Expect):
    def __call__(self, student_answer, state=None, parser=no_parse):
        if parser(self.string, state, self) not in student_answer:
            return None, ''
        else:
            if self.comment:
                return False, self.comment
            else:
                return False, "Je devrais pas trouver '<tt>%s</tt>' dans la réponse" % self.string
    


# Set a 'replace' attribute on all the children
class Replace(TestUnary):
    def __init__(self, replace, a):
        TestExpression.__init__(self, a)
        self.replace = replace

    def source(self, state=None, format=None):
        return self.test_name(format) + \
               "(%s,%s)" % (
            pf(self.replace, format),
            self.children[0].source(state, format) )

    def __call__(self, student_answer, state=None, parser=no_parse):
        return self.children[0](
            replace_strings(self.replace,student_answer), state,
            lambda string, state, test: parser(replace_strings(self.replace,string), state, test)
            )


class TestInt(TestExpression):
    def __init__(self, integer):
        if not isinstance(integer, int):
            raise ValueError("Expect an integer")
        self.integer = integer
    def source(self, state=None, format=None):
        return self.test_name(format) + '(' + str(self.integer) + ')'

class Int(TestInt):
    def __call__(self, student_answer, state=None, parser=no_parse):
        try:
            if self.integer == int(student_answer.rstrip('.')):
                return True, ''
            return False, ''
        except ValueError:
            return False, '<p class="int_required"></p>'

class IntGT(TestInt):
    def __call__(self, student_answer, state=None, parser=no_parse):
        try:
            if int(student_answer) > self.integer:
                return True, ''
            return False, ''
        except ValueError:
            return False, '<p class="int_required"></p>'

class IntLT(TestInt):
    def __call__(self, student_answer, state=None, parser=no_parse):
        try:
            if int(student_answer) < self.integer:
                return True, ''
            return False, ''
        except ValueError:
            return False, '<p class="int_required"></p>'

class Length(TestInt):
    def __call__(self, student_answer, state=None, parser=no_parse):
        return len(student_answer) == self.integer, ''

class LengthLT(TestInt):
    def __call__(self, student_answer, state=None, parser=no_parse):
        return len(student_answer) < self.integer, ''

class NumberOfIs(TestExpression):
    def __init__(self, string, number):
        if not isinstance(number, int):
            raise ValueError("Expect an integer")
        self.string = string
        self.number = number

    def source(self, state=None, format=None):
        return self.test_name(format) + '(' + pf(self.string,format) + ',' + \
               str(self.number) + ')'

    def __call__(self, student_answer, state=None, parser=no_parse):
        return student_answer.count(parser(self.string,state,self)) \
               == self.number, ''


# Should apply the parser on all the dict items

class TestDictionary(TestExpression):
    def __call__(self, student_answer, state=None, parse=None):
        if self.uppercase:
            student_answer = student_answer.upper()
        if student_answer not in self.dict:
            return False, 'Possible answers are:' + str(self.dict.keys())
        r = self.dict[student_answer]
        if r == self.good:
            return True, ''
        
        return False, ''

class YesNo(TestDictionary):
    uppercase = True
    dict = {'OUI': 'O', 'Y': 'O', 'YES': 'O', 'O': 'O',
            'NON': 'N', 'NO': 'N', 'N': 'N',
            }

class Yes(YesNo):
    good = 'O'

class No(YesNo):
    good = 'N'
    





if True:
    # Regression test on new tests.

    def create(txt):
        o = eval(txt)
        # print o.source()
        # print txt
        assert(o.source() == txt)
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
