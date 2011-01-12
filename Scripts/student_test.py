#!/usr/bin/env python
# -*- coding: latin1 -*-
#    QUENLIG: Questionnaire en ligne (Online interactive tutorial)
#    Copyright (C) 2005-2010 Thierry EXCOFFIER, Universite Claude Bernard
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

    def get(self, url, trace=False):
        page = self.server.get(self.base + url, trace)
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

    def see_all_questions(self):
        return self.get('?questions_all=all')
        

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

    


