#!/usr/bin/env python3
# -*- coding: latin-1 -*-
#    QUENLIG: Questionnaire en ligne (Online interactive tutorial)
#    Copyright (C) 2011-2015 Thierry EXCOFFIER, Universite Claude Bernard
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
#    Contact: Thierry.EXCOFFIER@univ-lyon1.fr
#
from server import Server
from student import Student
import sys
import os
import time

name = 'test'

def minimal_tests(student, good=0, bad=0, indice=0, title=''):
    if title is None:
        title = 'Guest' + student.name.title()
    student.expect(
        '<span class="statmenu_good0"></span></em>%d' % good,
        '<span class="statmenu_bad0"></span></em>%d' % bad,
        '<span class="statmenu_indice0"></span></em>%d' % indice,
        '<A class="content tips" href="?answered=1">',
        '<A class="content tips" href="?action_help=1">',
        '<TEXTAREA id="comment" NAME="comment" ROWS="10"></TEXTAREA>',
        '<img src="?map=1">',
        'Questions/regtest',
         '<DIV class="title">\n<A class="content tips">\n%s\n<SPAN></SPAN></A>\n</DIV>' % title
        )

def test_0000_initial_display(student):
    minimal_tests(student, title='Guest0000_Initial_Display')
    student.check_question_link('a:a', default=True, max_descendants=True,
                                erasable=True)
    student.expect(
        '<span class="statmenu_time0"></span></em>0:00:00',
        )

def test_0010_goto_question(student):
    student.goto_question('a:a')
    minimal_tests(student, title='a:a')
    student.check_question_link('a:a', default=True, current=True,
                                viewed=True, max_descendants=True,
                                erasable=True)
    student.expect(
        '<table class="box_content"><tbody><tr><td>\n<p>question_a\n</td></tr></tbody></table>',
        '<FORM CLASS="questionanswer"',
        '<DIV class="title">\n<A class="content tips">\na:a\n<SPAN></SPAN></A>\n</DIV>',
        )

def test_0020_give_good_answer(student):
    student.goto_question('a:a')
    student.give_answer('a')
    minimal_tests(student, good=1, title='a:a')
    student.check_question_link('a:b', default=True, max_descendants=True,
                                erasable=True)
    student.check_question_link('a:c', erasable=True)
    student.expect("good_answer__a", "good_answer_comment")

def test_0030_goto_b(student):
    test_0020_give_good_answer(student)
    student.goto_question('a:b')
    minimal_tests(student, good=1, title='a:b')
    student.check_question_link('a:b', default=True, max_descendants=True,
                                current=True, viewed=True, erasable=True)
    student.check_question_link('a:c', erasable=True)

def test_0040_goto_c(student):
    test_0020_give_good_answer(student)
    student.goto_question('a:c')
    minimal_tests(student, good=1, title='a:c')
    student.check_question_link('a:b', default=True, max_descendants=True,
                                erasable=True)
    student.check_question_link('a:c', current=True, viewed=True, erasable=True)

def test_0050_goto_b_c(student):
    # Resigned questions are not 'default' ones.
    test_0020_give_good_answer(student)
    student.goto_question('a:b')
    student.goto_question('a:c')
    minimal_tests(student, good=1, title='a:c')
    student.check_question_link('a:b', viewed=True,
                                max_descendants=True, resigned=True,
                                erasable=True)
    student.check_question_link('a:c', default=True, current=True, viewed=True,
                                erasable=True)

def test_0060_give_bad_answer(student):
    student.goto_question('a:a')
    student.old_base = student.base # For reload
    student.give_answer('a0')
    minimal_tests(student, title='a:a', bad=1)
    student.check_question_link('a:a', viewed=True, bad_answer_given=True,
                                current=True,
                                default=True, max_descendants=True)
    student.expect("bad_answer_comment", "bad_answer__a0")
    
def test_0070_give_bad_answer_c(student):
    test_0040_goto_c(student)
    student.give_answer('bad')
    minimal_tests(student, title='a:c', good=1, bad=1)
    student.check_question_link('a:c', viewed=True, bad_answer_given=True,
                                current=True)
    student.check_question_link('a:b', default=True, max_descendants=True,
                                erasable=True)

def test_0080_give_bad_answer_c_bad_b(student):
    test_0070_give_bad_answer_c(student)
    student.goto_question('a:b')
    student.give_answer('bad')
    minimal_tests(student, title='a:b', good=1, bad=2)
    student.check_question_link('a:c', viewed=True, bad_answer_given=True,
                                resigned=True)
    student.check_question_link('a:b', default=True, max_descendants=True,
                                viewed=True, bad_answer_given=True,
                                current=True)
    
def test_0090_all_resign(student):
    test_0020_give_good_answer(student)
    student.goto_question('a:b')
    student.goto_question('a:c')
    student.goto_question('a:b')
    minimal_tests(student, good=1, title='a:b')
    # The default question become the first one
    student.check_question_link('a:b', default=True, max_descendants=True,
                                current=True, viewed=True, resigned=True,
                                erasable=True)
    student.check_question_link('a:c', viewed=True, resigned=True,
                                erasable=True)

def test_0100_reload_bad_answer(student):
    test_0060_give_bad_answer(student)
    # Reload last page
    student.get(student.url, base=student.old_base)
    minimal_tests(student, title='a:a', bad=1)
    student.check_question_link('a:a', viewed=True, bad_answer_given=True,
                                current=True,
                                default=True, max_descendants=True)

def test_0110_comment_question(student, comment="MyComment"):
    student.goto_question('a:a')
    student.old_base = student.base
    student.give_comment(comment)
    minimal_tests(student, title='a:a')
    student.check_question_link('a:a', viewed=True, current=True,
                                default=True, max_descendants=True,
                                erasable=True)
    student.expect('<div class="comment_given">' + comment + '</div>')
    student.old_url = student.url
    page = student.get_answered()
    assert(page.count("<PRE>" + comment + "</PRE>") == 1)

def test_0110_comment_question_reload(student):
    test_0110_comment_question(student, "MyComment2")

    # Reload last page
    student.get(student.old_url, base=student.old_base)
    student.reject('<div class="comment_given">MyComment2</div>')

    page = student.get_answered()
    assert(page.count("<PRE>MyComment2</PRE>") == 1)

def test_0120_comment_no_question(student, comment='MyNoComment'):
    student.get_answered()
    student.old_base = student.base # For reload
    student.give_comment(comment)
    student.old_url = student.url
    student.check_question_link('a:a', default=True, max_descendants=True,
                                erasable=True)
    student.expect('<div class="comment_given">' + comment + '</div>')
    student.old_url = student.url
    page = student.get_answered()
    assert(page.count("<PRE>" + comment + "</PRE>") == 1)

def test_0130_comment_no_question_reload(student, comment='MyNoComment2'):
    test_0120_comment_no_question(student, 'MyNoComment2')
    # Reload last page
    student.get(student.old_url, base=student.old_base)
    student.reject('<div class="comment_given">MyNoComment2</div>')
    page = student.get_answered()
    assert(page.count("<PRE>MyNoComment</PRE>") == 0)

def test_0140_comment_after_good_answer(student, comment='My-Comment'):
    test_0020_give_good_answer(student)
    student.old_base = student.base # For reload
    student.give_comment(comment)
    minimal_tests(student, title='a:a', good=1)
    student.expect('<div class="comment_given">' + comment + '</div>')
    student.old_url = student.url
    page = student.get_answered()
    assert(page.count("<PRE>" + comment + "</PRE>") == 1)
    
def test_0150_comment_after_good_answer_reload(student):
    test_0140_comment_after_good_answer(student, 'My-Comment2')
    # Reload last page
    student.get(student.old_url, base=student.old_base)
    minimal_tests(student, title='a:a', good=1)
    student.reject('<div class="comment_given">My-Comment2</div>')
    student.old_url = student.url
    page = student.get_answered()
    assert(page.count("<PRE>My-Comment2</PRE>") == 1)

def test_0160_comment_after_bad_answer(student, comment='My+Comment'):
    test_0060_give_bad_answer(student)
    student.old_base = student.base # For reload
    student.give_comment(comment)
    minimal_tests(student, title='a:a', bad=1)
    student.expect('<div class="comment_given">' + comment + '</div>')
    student.old_url = student.url
    page = student.get_answered()
    assert(page.count("<PRE>" + comment + "</PRE>") == 1)
    
def test_0170_comment_after_bad_answer_reload(student):
    test_0160_comment_after_bad_answer(student, "My+Comment2")
    # Reload last page
    student.get(student.old_url, base=student.old_base)
    minimal_tests(student, title='a:a', bad=1)
    student.reject('<div class="comment_given">My+Comment2</div>')
    student.old_url = student.url
    page = student.get_answered()
    assert(page.count("<PRE>My+Comment2</PRE>") == 1)
    
def test_0180_ask_one_indice(student):
    test_0010_goto_question(student)
    student.reject('Indice X')
    student.reject('Indice Y')
    student.expect('<A CLASS="first_indice" HREF="?question_indices=1">')
    student.old_base = student.base # For reload
    student.get_indice(1)
    student.old_url = student.url
    minimal_tests(student, title='a:a', indice=1)
    student.expect('Indice X')
    student.expect('<A CLASS="next_indice" HREF="?question_indices=2">')

def test_0190_ask_two_indices(student):
    test_0180_ask_one_indice(student)
    student.reject('Indice Y')
    student.get_indice(2)
    minimal_tests(student, title='a:a', indice=2)
    student.expect('Indice X')
    student.expect('Indice Y')
    
def test_0200_ask_one_indice_reload(student):
    test_0180_ask_one_indice(student)
    # Reload last page
    student.get(student.old_url, base=student.old_base)
    student.reject('Indice Y')
    minimal_tests(student, title='a:a', indice=1)
    student.expect('Indice X')
    
def test_0210_parallel_get(student):
    test_0020_give_good_answer(student)
    
    student.goto_question('a:b')
    minimal_tests(student, title='a:b', good=1)
    student.old_base_1 = student.base # For reload
    student.old_url_1 = student.url

    student.goto_question('a:c')
    minimal_tests(student, title='a:c', good=1)
    student.old_base_2 = student.base # For reload
    student.old_url_2 = student.url

    student.get(student.old_url_1, base=student.old_base_1)
    minimal_tests(student, title='a:b', good=1)

    student.get(student.old_url_2, base=student.old_base_2)
    minimal_tests(student, title='a:c', good=1)

def test_0220_parallel_answer_1(student):
    test_0210_parallel_get(student)
    student.give_answer('b', base=student.old_base_1)
    minimal_tests(student, title='a:b', good=2)
    student.give_answer('c', base=student.old_base_2)
    minimal_tests(student, title='a:c', good=3)

    # Forbiden
    student.give_answer('c', base=student.old_base_1)
    minimal_tests(student, title='a:b', good=3) # XXX dangerous
    
def test_0240_work_done(student):
    student.goto_question('a:a')
    student.get_indice(1)
    student.get_indice(2)
    student.give_answer('bad_one')
    student.give_answer('a')
    student.give_comment('My--Comment')
    student.goto_question('a:b')
    student.give_answer('b')
    student.goto_question('a:c')
    student.give_answer('c')
    student.get_answered()
    minimal_tests(student, title=None, bad=1, indice=2, good=3)
    student.expect('<PRE>My--Comment</PRE>',
                   '<div class="an_answer">c</div><br>good_c</TD>',
                   'short"><A HREF="?question=a%3Ac">a:c</A></em><table class="box_content"><tr><td>question_c<TABLE CLASS="good_answer">',
                   '<div class="an_answer">b</div><br>good_b</TD>',
                   'short"><A HREF="?question=a%3Ab">a:b</A></em><table class="box_content"><tr><td>question_b<TABLE CLASS="good_answer">',
                   '>a</div><br>good_answer_comment<br>good_answer__a</TD>',
                   '<div class="an_answer">bad_one</div>',
                   '<li>Indice X</li>',
                   '<li>Indice Y</li>',
                   )

error = False

import threading
import random
class User(threading.Thread):
    i = 1000000
    def __init__(self):
        threading.Thread.__init__(self)
        User.i += 1
    def run(self):
        try:
            student = Student(the_server, 'user%d' % User.i)
            while True:
                student.goto_question('a:a')
                minimal_tests(student, title='a:a')
                student.reject('<DIV class="question_good">')
                if random.randrange(0,4) == 0:
                    student.give_answer('a')
                    minimal_tests(student, title='a:a', good=1)
                    sys.stdout.write('*')
                    sys.stdout.flush()
                    break
        except:
            global error
            error = True
            raise

def test_0250_threading(student):
    for i in range(20):
        User().start()
    while threading.activeCount() != 1:
        time.sleep(0.1)
    if error:
        raise ValueError("Thread error")

def test_0260_require_simple(student):
    student.goto_question('a:a')
    student.give_answer('a')
    student.goto_question('a:b')
    student.give_answer('xbx')
    student.reject_questions('b:A', 'b:B', 'b:C')
    student.goto_question('a:c')
    student.give_answer('c')
    student.reject_questions('b:A', 'b:B')
    minimal_tests(student, title='a:c', good=3)
    student.check_question_link('b:C', default=True, max_descendants=True,
                                erasable=True)

    student.goto_question('b:A')
    minimal_tests(student, title='b:A', good=3)
    student.goto_question('b:B')
    minimal_tests(student, title='b:B', good=3)
    student.goto_question('b:C')
    minimal_tests(student, title='b:C', good=3)

def test_0265_required_or(student):
    student.goto_question('a:a')
    student.give_answer('unlockC')
    student.check_question_link('c:Q1', erasable=True)
    student.goto_question('c:Q1')
    student.give_answer('answer1')
    student.check_question_link('c:Q2.1', erasable=True)
    student.reject_questions('c:Q2.2', 'c:Q3')
    student.goto_question('c:Q2.1')
    student.give_answer('any')
    student.check_question_link('c:Q3', erasable=True)
    student.goto_question('c:Q3')
    student.reject(' File ') # Backtrace

def test_0266_required_or(student):
    student.goto_question('a:a')
    student.give_answer('unlockC')
    student.check_question_link('c:Q1', erasable=True)
    student.goto_question('c:Q1')
    student.give_answer('answer2')
    student.check_question_link('c:Q2.2', erasable=True)
    student.reject_questions('c:Q2.1', 'c:Q3')
    student.goto_question('c:Q2.2')
    student.give_answer('any')
    student.check_question_link('c:Q3', erasable=True)

def test_0270_require_test(student):
    student.goto_question('a:a')
    student.give_answer('a')
    student.goto_question('a:b')
    student.give_answer('b')
    student.reject_questions('b:A', 'b:C')
    student.check_question_link('a:c', default=True, max_descendants=True,
                                erasable=True)
    student.check_question_link('b:B', erasable=True)

def test_0280_require_test_regexp(student):
    student.goto_question('a:a')
    student.give_answer('a')
    student.goto_question('a:b')
    student.give_answer('B')
    student.reject_questions('b:C')
    student.check_question_link('a:c', default=True, max_descendants=True,
                                erasable=True)
    student.check_question_link('b:B', erasable=True)
    student.check_question_link('b:A', erasable=True)

def test_0290_root_minimal(student):
    student.check_question_link('a:a', default=True, max_descendants=True,
                                erasable=True)
    student.expect('<option >Teacher</option>',
                   # '<option selected>Default</option>',
                   '?role=',
                   )
    student.reject('?questions_all=')
    student.reject_questions('a:b', 'a:c')

    student.select_role('Teacher')
    student.expect('<option selected>Teacher</option>',
                   # '<option >Default</option>',
                   '?questions_all=',
                   )
    
    student.see_all_questions()
    student.check_question_link('a:a', default=True, max_descendants=True,
                                erasable=True)
    student.check_question_link('a:b', erasable=True)
    student.check_question_link('a:c', erasable=True)
    student.check_question_link('b:B', erasable=True)
    student.check_question_link('b:A', erasable=True)

def test_0300_reload_static(student):
    filename = os.path.join('Students', name, 'HTML', 'foobar.html')
    f = open(filename, 'w')
    f.write('===foobar===')
    f.close()
    t = int(time.time())
    student.get('/foobar.html', base=the_server.base)
    assert(student.page == '===foobar===' )

    while True:
        if t != int(time.time()):
            break
    f = open(filename, 'w')
    f.write('===foo bar===')
    f.close()
    student.get('/foobar.html', base=the_server.base)
    assert(student.page == '===foo bar===' )

def test_0310_root_statmenu_students(student):
    student.select_role('Teacher')
    student.get('?statmenu_students=1')
    student.check_table(12, 'statmenu_students', 1, 1)
    student.get('?sort_column=-2+statmenu_students&statmenu_students=1')
    student.check_table(12, 'statmenu_students', 1, -1)
    student.get('?sort_column=1+statmenu_students&statmenu_students=1')
    student.check_table(12, 'statmenu_students', 1, 1)
    student.get('?sort_column=4+statmenu_students&statmenu_students=1')
    student.check_table(12, 'statmenu_students', 4, 1)

def test_0320_root_statmenu_other_student(student):
    other_student = Student(the_server, 'other_' + student.name)
    other_student.goto_question('a:a')
    other_student.give_answer('a')
    other_student.give_comment('otherComment')
    other_student.expect('otherComment')

    student.select_role('Grader')
    student.get('?statmenu_students=1')
    student.expect('<A HREF="?answered_other=guest' + other_student.name)

    student.get('?answered_other=guest' + other_student.name)
    student.expect('otherComment',
                   '<div class="an_answer">a</div><br>good_answer_comment')
    
def test_0330_root_plugin_reload(student):
    student.select_role('Teacher')
    name = os.path.join('Plugins', 'question', 'question.py')
    f = open(name, 'r')
    g = open(name + '.new', 'w')
    g.write(f.read())
    g.close()
    f.close()
    os.rename(name + '.new', name)
    student.get('?reload_plugins=1')
    student.expect('<DIV class="reload_plugins">')
    student.goto_question('a:a')
    student.expect('<DIV class="reload_plugins">')
    
def test_0340_relog(student):
    student.expect('<A class="content tips" href="?session_deconnection=1">')
    student = Student(the_server, student.name)
    student.expect('<A class="content tips" href="?session_deconnection=1">')
   
def test_0350_logout(student):
    student.expect('<A class="content tips" href="?session_deconnection=1">')
    student.get('?session_deconnection=1')
    student.expect('<script>window.location=')
    student = Student(the_server, student.name)
    student.expect('<A class="content tips" href="?session_deconnection=1">')
   
def test_0360_root_question_reload(student):
    student.select_role('Author')
    student.goto_question('a:a')
    student.reject('a:d')
    student.reject('question__a')
    try:
        name = os.path.join('Questions', 'regtest', 'a.py')
        f = open(name, 'r')
        g = open(name + '.new', 'w')
        g.write(f.read().replace('question_a', 'question__a')
                + '\nadd(name="d",required=[],question="d")\n')
        g.close()
        f.close()
        os.rename(name, name + '.old')
        os.rename(name + '.new', name)

        student.expect('<DIV class="reload_questions">')
        student.get('?reload_questions=1')
        student.expect('question__a')
        student.check_question_link('a:d', erasable=True)
    finally:
        os.rename(name + '.old', name)

def test_0370_choice(student):
    student.goto_question('a:a')
    student.give_answer('a')
    student.goto_question('a:b')
    student.give_answer('b')
    student.goto_question('b:choice')
    student.expect('<input onchange="check_button(this)" class="checkbox" type="checkbox" name="question_answer" value="b"> B')
    student.expect('<input onchange="check_button(this)" class="checkbox" type="checkbox" name="question_answer" value="c"> C')

    student.get('?question_answer=b')
    student.expect('<input onchange="check_button(this)" class="checkbox" type="checkbox" name="question_answer" value="b" checked id="2"> B')
    student.expect('<input onchange="check_button(this)" class="checkbox" type="checkbox" name="question_answer" value="c"> C')

    student.get('?question_answer=b&question_answer=c')
    student.expect('<input onchange="check_button(this)" class="checkbox" type="checkbox" name="question_answer" value="b" checked id="2"> B')
    student.expect('<input onchange="check_button(this)" class="checkbox" type="checkbox" name="question_answer" value="c" checked> C')
    
    student.get('?question_answer=c')
    student.expect('<p class="maximum_bad_answer">')
    student.reject('name="question_answer"')

def test_0400_root_reload_questions(student):
    student_bad = Student(the_server, 'user_bad')
    student_bad.goto_question('a:a')
    student_bad.give_answer('bad')

    student_bad2 = Student(the_server, 'user_bad2')
    student_bad2.goto_question('a:a')
    student_bad2.give_answer('bad')
    student_bad2.give_comment('MyComment')

    student_bad3 = Student(the_server, 'user_bad3')
    student_bad3.goto_question('a:a')
    student_bad3.give_answer('a')
    student_bad3.goto_question('a:b')
    student_bad3.give_answer('bad')
    student_bad3.goto_question('a:c')
    student_bad3.give_answer('bad')

    student_see = Student(the_server, 'user_good')
    student_see.goto_question('a:a')

    student_bad4 = Student(the_server, 'user_bad4')

    student.select_role('Developer')
    student.goto_question('a:a')
    student.get('?reload_questions=1')
    student.goto_question('a:b')
    student.get('?reload_questions=1')

    student_bad4.goto_question('a:a')
    minimal_tests(student_bad4, good=0, bad=0, title='a:a')

    student_bad2.goto_question('a:a')
    minimal_tests(student_bad2, good=0, bad=1, title='a:a')

    student_bad3.goto_question('a:b')
    minimal_tests(student_bad3, good=1, bad=2, title='a:b')

    student_see.give_answer('a')
    minimal_tests(student_see, good=1, title='a:a')

    student_bad.give_answer('a')
    minimal_tests(student_bad, good=1, bad=1, title='a:a')

def test_0410_CHOICE(student):
    q = '51' # For user
    r = '45' # For root
    student.goto_question('a:a')
    student.give_answer('unlockCHOICES')
    student.goto_question('b:z')
    minimal_tests(student, title='b:z', good=1)
    student.give_answer(q)
    minimal_tests(student, title='b:z', good=2)
    root = Student(
        the_server, 'root_0410',
        roles="['Default','Teacher','Author','Grader', 'Developer','Admin']")
    root.goto_question('a:a')
    root.give_answer('unlockCHOICES')
    root.goto_question('b:z')
    minimal_tests(root, title='b:z', good=1)
    root.give_answer(r)
    minimal_tests(root, title='b:z', good=2)
    root.select_role('Teacher')
    root.get('?answered_other=guest' + student.name)
    assert('Question ' + q in root.page)
    assert('class="an_answer">' + q + '<' in root.page)

def test_0420_not_threaded(student):
    for i in range(20):
        User().start()
    root = Student(
        the_server, 'root_0420',
        roles="['Default','Teacher','Author','Grader', 'Developer','Admin']")
    root.goto_question('b:z')
    root.goto_question('a:b')
    root.select_role('Teacher')
    while threading.activeCount() != 1:
        root.goto_question('a:a')
        os.system("touch Questions/regtest/a.py")
        root.get('?reload_questions=1')
        root.get('?statmenu_questions=1')
        root.expect('>b:z<')
        root.expect('>a:b<')
        os.system("touch Plugins/question_answer/question_answer.py")
        root.get('?reload_plugins=1')
        time.sleep(0.1)
    if error:
        raise ValueError("Regression tests thread error")

def test_0500_preprocesses(student):
    grader = Student(the_server, 'grader_0500',
        roles="['Default','Teacher','Author','Grader', 'Developer','Admin']")
    grader.select_role('Grader')
    student.goto_question('a:a')
    student.give_answer('mcq')
    student.goto_question('a:mcq')
    minimal_tests(student, title='a:mcq', good=1)
    student.expect('value="(id_a)"')
    student.expect('value="(id_b)"')
    student.expect('value="(id_c)"')
    student.expect('choice a')
    student.expect('choice b')
    student.expect('choice c')
    student.give_answer('(id_a)')
    minimal_tests(student, title='a:mcq', good=1, bad=1)
    g = grader.grades()['guest0500_preprocesses']
    assert(g['GA'] == -1 and g['GB'] == 0 and g['GC'] == 0)
    student.give_answer('(id_b)')
    minimal_tests(student, title='a:mcq', good=1, bad=2)
    g = grader.grades()['guest0500_preprocesses']
    assert(g['GA'] == 0 and g['GB'] == -1 and g['GC'] == 0)
    student.expect('bad b')
    student.give_answer('(id_c)')
    minimal_tests(student, title='a:mcq', good=2, bad=2)
    g = grader.grades()['guest0500_preprocesses']
    assert(g['GA'] == 0 and g['GB'] == 0 and g['GC'] == 1)

def test_0510_root_session_graph(student):
    dot = 'Students/test/HTML/xxx_graphe.dot'
    student.get('/?session_graph=1')
    assert not os.path.exists(dot)
    student.reject('xxx_graphe.png')
    student.select_role('Author')
    student.get('/?session_graph=1')
    student.expect('xxx_graphe.png')
    student.reject('File "') # Backtrace
    with open(dot, "r") as f:
        content = f.readlines()
    for line in r'''"a\na" -> "a\nb"[];
"a\na" -> "a\nc"[];
"a\na" -> "a\nmcq"[penwidth=3 headlabel="a\na\nmcq"];
"a\na" -> "b\nA"[];
"a\nb" -> "b\nA"[penwidth=3 headlabel="a\nb\nB"];
"a\na" -> "b\nB"[];
"a\nb" -> "b\nB"[penwidth=3 headlabel="a\nb\n[bB]"];
"a\nc" -> "b\nC"[];
"a\nb" -> "b\nC"[];
"a\na" -> "b\nchoice"[];
"a\nb" -> "b\nchoice"[];
"a\na" -> "b\nz"[penwidth=3 headlabel="a\na\nunlockCHOICES"];
"a\na" -> "c\nQ1"[penwidth=3 headlabel="a\na\nunlockC"];
"c\nQ1" -> "c\nQ2.1"[penwidth=3 headlabel="c\nQ1\nanswer1"];
"c\nQ1" -> "c\nQ2.2"[penwidth=3 headlabel="c\nQ1\nanswer2"];
"c\nQ2.1" -> "c\nQ3"[color="#00FF00" style=dashed];
"c\nQ2.2" -> "c\nQ3"[color="#00FF00"];'''.split('\n'):
        if line + '\n' not in content:
            raise ValueError(content)

############
# TODO
############

exit_value = 1
try:
    the_server = Server(questions='Questions/regtest', name=name)
    tests = sorted(globals())
    if len(sys.argv) > 1:
        tests = [t
                 for t in tests
                 if t in sys.argv
                 ]
    for test in tests:
        if not test.startswith('test_'):
            continue
        print('%-45s' % test, end=' ')
        sys.stdout.flush()
        if '_root_' in test:
            roles="['Default','Teacher','Author','Grader','Developer','Admin']"
        else:
            roles = "['Student']"
        globals()[test](Student(the_server,
                                test[len('test_'):],
                                roles=roles,
                                ))
        print('OK')
    print('All tests are fine')
    exit_value = 0
finally:
    the_server.stop()

sys.exit(exit_value)


