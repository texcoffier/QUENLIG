#!/usr/bin/env python
# -*- coding: latin1 -*-
#    QUENLIG: Questionnaire en ligne (Online interactive tutorial)
#    Copyright (C) 2011 Thierry EXCOFFIER, Universite Claude Bernard
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
#

from server import Server
from student import Student
import sys

def minimal_tests(student, good=0, bad=0, indice=0, title=''):
    if title is None:
        title = 'Guest' + student.name.title()
    student.expect(
        '<span class="statmenu_good0"></span></em>%d' % good,
        '<span class="statmenu_bad0"></span></em>%d' % bad,
        '<span class="statmenu_indice0"></span></em>%d' % indice,
        '<A class="content tips" href="?answered=1">',
        '<A class="content tips" href="?action_help=1">',
        '<TEXTAREA NAME="comment" COLS="30" ROWS="10"></TEXTAREA>',
        '<img src="?map=1">',
        'Questions/regtest',
         '<DIV class="title">\n<A class="content tips">\n<SPAN></SPAN>\n%s\n</A>\n</DIV>' % title
        )


def test_0000_initial_display(student):
    minimal_tests(student, title='Guest0000_Initial_Display')
    student.check_question_link('a:a', default=True, max_descendants=True)
    student.expect(
        '<span class="statmenu_time0"></span></em>0:00:00',
        )

def test_0010_goto_question(student):
    student.goto_question('a:a')
    minimal_tests(student, title='a:a')
    student.check_question_link('a:a', default=True, current=True,
                                viewed=True, max_descendants=True)
    student.expect(
        '<table class="box_content"><tbody><tr><td>\nquestion_a\n</td></tr></tbody></table>',
        '<FORM CLASS="questionanswer"',
        '<DIV class="title">\n<A class="content tips">\n<SPAN></SPAN>\na:a\n</A>\n</DIV>',
        )

def test_0020_give_good_answer(student):
    student.goto_question('a:a')
    student.give_answer('a')
    minimal_tests(student, good=1, title='a:a')
    student.check_question_link('a:b', default=True, max_descendants=True)
    student.check_question_link('a:c')
    student.expect("good_answer__a", "good_answer_comment")

def test_0030_goto_b(student):
    test_0020_give_good_answer(student)
    student.goto_question('a:b')
    minimal_tests(student, good=1, title='a:b')
    student.check_question_link('a:b', default=True, max_descendants=True,
                                current=True, viewed=True)
    student.check_question_link('a:c')

def test_0040_goto_c(student):
    test_0020_give_good_answer(student)
    student.goto_question('a:c')
    minimal_tests(student, good=1, title='a:c')
    student.check_question_link('a:b', default=True, max_descendants=True)
    student.check_question_link('a:c', current=True, viewed=True)

def test_0050_goto_b_c(student):
    # Resigned questions are not 'default' ones.
    test_0020_give_good_answer(student)
    student.goto_question('a:b')
    student.goto_question('a:c')
    minimal_tests(student, good=1, title='a:c')
    student.check_question_link('a:b', viewed=True,
                                max_descendants=True, resigned=True)
    student.check_question_link('a:c', default=True, current=True, viewed=True)

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
    student.check_question_link('a:b', default=True, max_descendants=True)

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
                                current=True, viewed=True, resigned=True)
    student.check_question_link('a:c', viewed=True, resigned=True)

def test_0100_reload_bad_answer(student):
    test_0060_give_bad_answer(student)
    # Reload last page
    student.get(student.url, base=student.old_base)
    minimal_tests(student, title='a:a', bad=1)
    student.check_question_link('a:a', viewed=True, bad_answer_given=True,
                                current=True,
                                default=True, max_descendants=True)

def test_0110_comment_question(student):
    student.goto_question('a:a')
    student.old_base = student.base
    student.give_comment('MyComment')
    minimal_tests(student, title='a:a')
    student.check_question_link('a:a', viewed=True, current=True,
                                default=True, max_descendants=True)
    student.expect('<div class="comment_given">MyComment</div>')
    student.old_url = student.url
    page = student.get_answered()
    assert(page.count("<PRE>MyComment</PRE>") == 1)

def test_0110_comment_question_reload(student):
    test_0110_comment_question(student)

    # Reload last page
    student.get(student.old_url, base=student.old_base)
    student.expect('<div class="comment_given">MyComment</div>')

    page = student.get_answered()
    assert(page.count("<PRE>MyComment</PRE>") == 1)

def test_0120_comment_no_question(student):
    student.get_answered()
    student.old_base = student.base # For reload
    student.give_comment('MyNoComment')
    student.old_url = student.url
    student.check_question_link('a:a', default=True, max_descendants=True)
    student.expect('<div class="comment_given">MyNoComment</div>')
    student.old_url = student.url
    page = student.get_answered()
    assert(page.count("<PRE>MyNoComment</PRE>") == 1)

def test_0130_comment_no_question_reload(student):
    test_0120_comment_no_question(student)
    # Reload last page
    student.get(student.old_url, base=student.old_base)
    student.expect('<div class="comment_given">MyNoComment</div>')
    page = student.get_answered()
    assert(page.count("<PRE>MyNoComment</PRE>") == 1)

def test_0140_comment_after_good_answer(student):
    test_0020_give_good_answer(student)
    student.old_base = student.base # For reload
    student.give_comment('My-Comment')
    minimal_tests(student, title=None, good=1)
    student.expect('<div class="comment_given">My-Comment</div>')
    student.old_url = student.url
    page = student.get_answered()
    assert(page.count("<PRE>My-Comment</PRE>") == 1)
    
def test_0150_comment_after_good_answer_reload(student):
    test_0140_comment_after_good_answer(student)
    # Reload last page
    student.get(student.old_url, base=student.old_base)
    minimal_tests(student, title=None, good=1)
    student.expect('<div class="comment_given">My-Comment</div>')
    student.old_url = student.url
    page = student.get_answered()
    assert(page.count("<PRE>My-Comment</PRE>") == 1)

def test_0160_comment_after_bad_answer(student):
    test_0060_give_bad_answer(student)
    student.old_base = student.base # For reload
    student.give_comment('My+Comment')
    minimal_tests(student, title='a:a', bad=1)
    student.expect('<div class="comment_given">My+Comment</div>')
    student.old_url = student.url
    page = student.get_answered()
    assert(page.count("<PRE>My+Comment</PRE>") == 1)
    
def test_0170_comment_after_bad_answer_reload(student):
    test_0160_comment_after_bad_answer(student)
    # Reload last page
    student.get(student.old_url, base=student.old_base)
    minimal_tests(student, title='a:a', bad=1)
    student.expect('<div class="comment_given">My+Comment</div>')
    student.old_url = student.url
    page = student.get_answered()
    assert(page.count("<PRE>My+Comment</PRE>") == 1)
    
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
    minimal_tests(student, title=None, good=3)
    
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
                   '<tt class="an_answer">c</tt><br>good_c</TD>',
                   '"short">a:c</h3>question_c<TABLE CLASS="good_answer">',
                   '<tt class="an_answer">b</tt><br><br>good_b</TD>',
                   'short">a:b</h3>question_b<TABLE CLASS="good_answer">',
                   '>a</tt><br>good_answer_comment<br>good_answer__a</TD>',
                   '<tt class="an_answer">bad_one</tt>',
                   '<li>Indice X</li>',
                   '<li>Indice Y</li>',
                   )
    
def test_0250_threading(student):
    import threading
    import random
    import time
    class User(threading.Thread):
        def run(self):
            student = Student(the_server, 'user%d' % id(self))
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
    for i in range(20):
        User().start()
    while threading.activeCount() != 1:
        time.sleep(0.1)

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
    student.check_question_link('b:C', default=True, max_descendants=True)

    student.goto_question('b:A')
    minimal_tests(student, title=None, good=3)
    student.goto_question('b:B')
    minimal_tests(student, title=None, good=3)
    student.goto_question('b:C')
    minimal_tests(student, title='b:C', good=3)
    
def test_0270_require_test(student):
    student.goto_question('a:a')
    student.give_answer('a')
    student.goto_question('a:b')
    student.give_answer('b')
    student.reject_questions('b:A', 'b:C')
    student.check_question_link('a:c', default=True, max_descendants=True)
    student.check_question_link('b:B')

def test_0280_require_test_regexp(student):
    student.goto_question('a:a')
    student.give_answer('a')
    student.goto_question('a:b')
    student.give_answer('B')
    student.reject_questions('b:C')
    student.check_question_link('a:c', default=True, max_descendants=True)
    student.check_question_link('b:B')
    student.check_question_link('b:A')

 

    

############
# TODO
############

try:
    the_server = Server(questions='Questions/regtest')
    if len(sys.argv) > 1:
        try:
            tests = sorted(globals())[int(sys.argv[1])-1:]
        except ValueError:
            tests = sys.argv[1:]
    else:
        tests = sorted(globals())
    for test in tests:
        if not test.startswith('test_'):
            continue
        print '%-45s' % test,
        sys.stdout.flush()
        globals()[test](Student(the_server, test[len('test_'):]))
        print 'OK'
finally:
    the_server.stop()

    


