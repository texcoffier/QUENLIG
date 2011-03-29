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
    assert('/1/' in student.old_base)
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
    assert('/3/' in student.base)
    minimal_tests(student, title='a:a', bad=1)
    student.check_question_link('a:a', viewed=True, bad_answer_given=True,
                                current=True,
                                default=True, max_descendants=True)

def test_0110_comment_question(student):
    student.goto_question('a:a')
    student.old_base = student.base
    assert('/1/' in student.base)
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
    assert('/4/' in student.base)
    student.expect('<div class="comment_given">MyComment</div>')

    page = student.get_answered()
    assert(page.count("<PRE>MyComment</PRE>") == 1)

# TODO
# Comment on no question
# Comment after answer
# Indice before but also after (reload)
# Parallele answer with 2 questions

try:
    the_server = Server(questions='Questions/regtest')
    for test in sorted(globals()):
        if not test.startswith('test_'):
            continue
        print '%-40s' % test,
        sys.stdout.flush()
        globals()[test](Student(the_server, test[len('test_'):]))
        print 'OK'
finally:
    the_server.stop()

    


