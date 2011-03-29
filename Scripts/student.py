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
#

import server
import urllib
import os

class Student:
    def __init__(self, server, name, acls=None):
        self.server = server
        self.base = server.base + '/?guest=' + name
        self.name = name
        if acls:
            self.set_acls(acls)
        self.get('')

    def get(self, url, trace=False, base=None):
        if base is None:
            base = self.base
        self.page = page = self.server.get(base + url, trace)
        self.url = url
        # print base + url
        if page.find('<base href='):
            self.base = page.split('<base href="')[1].split('"')[0]
        else:
            sys.stderr.write("Problem in the page\n")
        return page

    def logdir(self):
        return self.server.logdir() + 'guest' + self.name + '/'

    def set_acls(self, acls):
        try:
            os.mkdir(self.logdir())
        except OSError:
            pass
        f = open(self.logdir() + 'acls', 'w')
        f.write(acls)
        f.close()

    def goto_question(self, question):
        return self.get('?question=' + urllib.quote(question))

    def give_answer(self, answer):
        return self.get('?question_answer=' + urllib.quote(answer))

    def give_comment(self, answer):
        return self.get('?comment=' + urllib.quote(answer))

    def get_answered(self):
        return self.get('?answered=1')

    def see_all_questions(self):
        return self.get('?questions_all=all')

    def expect(self, *values):
        for value in values:
            if value in self.page:
                continue
            raise ValueError(self.page + "\nExpected: %s" % value)

    def check_question_link(self, name, current=False, viewed=False,
                            max_descendants=False, default=False,
                            resigned=False, bad_answer_given=False):
        s = '<A'
        if default:
            s += ' ID="1"'
        s += ' HREF="?question=' + name.replace(':', '%3A') + '" CLASS="'
        if current:
            s += 'current_question '
        if viewed:
            s += 'question_given '
        if bad_answer_given:
            s += 'bad_answer_given '
        if resigned:
            s += 'resigned '
        if max_descendants:
            s += ' max_descendants'
        s += '">' + name + '</A>'
        self.expect(s)


if __name__ == "__main__":
    try:
        the_server = server.Server()
        student = Student(the_server, 'toto')
        page = student.goto_question('repondre:bonjour')
        assert( "Répondez 'bonjour' à cette question." in page)
        print 'The first question is correctly displayed'
        page = student.give_answer('coucou')
        assert( '<DIV class="question_bad">' in page)
        print 'Bad answer rejected'
        page = student.give_answer('bonjour')
        assert( '<DIV class="question_good">' in page)
        print 'Good answer accepted'
        
    finally:
        the_server.stop()

    


