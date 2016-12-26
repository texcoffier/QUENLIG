#!/usr/bin/env python3
# -*- coding: latin-1 -*-
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
import urllib.request, urllib.parse, urllib.error
import os

class Student:
    def __init__(self, server, name, acls=None, roles="['Student']"):
        self.server = server
        self.base = server.base + '/?guest=' + name
        self.name = name
        if acls:
            self.set_acls(acls)
        self.set_roles(roles)
        self.number = 0
        self.get('')

    def get(self, url, trace=False, base=None):
        if base is None:
            base = self.base
        self.page = page = self.server.get(base + url, trace)
        self.url = url
        # print base + url
        try:
            if page.find('<base href='):
                self.base = page.split('<base href="')[1].split('"')[0]
            else:
                sys.stderr.write("Problem in the page\n")
            f = open('xxx.%03d.html' % self.number, 'w')
            f.write(page)
            f.close()
            self.number += 1
        except IndexError:
            # Pas une page HTML
            pass
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

    def set_roles(self, roles):
        try:
            os.mkdir(self.logdir())
        except OSError:
            pass
        f = open(self.logdir() + 'roles', 'w')
        f.write(roles)
        f.close()

    def goto_question(self, question):
        return self.get('?question=' + urllib.parse.quote(question))

    def give_answer(self, answer, base=None):
        return self.get('?question_answer=' + urllib.parse.quote(answer), base=base)

    def give_comment(self, answer):
        return self.get('?comment=' + urllib.parse.quote(answer))

    def get_answered(self):
        return self.get('?answered=1')

    def get_indice(self, n):
        return self.get('?question_indices=%d' % n)

    def select_role(self, n):
        return self.get('?role=%s' % n)

    def see_all_questions(self):
        return self.get('?questions_all=all')

    def expect(self, *values):
        for value in values:
            if value in self.page:
                continue
            raise ValueError(self.page + "\nExpected: %s" % value)

    def reject(self, *values):
        for value in values:
            if value not in self.page:
                continue
            raise ValueError(self.page + "\nRejected: %s" % value)

    def reject_questions(self, *names):
        self.reject(*[' HREF="?question=' + name.replace(':', '%3A') + '"'
                    for name in names])

    def check_question_link(self, name, current=False, viewed=False,
                            max_descendants=False, default=False,
                            resigned=False, bad_answer_given=False,
                            erasable=False):
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
        if not viewed:
            s += 'not_seen '
        if erasable:
            s += 'erasable '
        if max_descendants:
            s += ' max_descendants'
        s += '">' + name + '</A>'
        self.expect(s)

    def check_table(self, nr, table, selected, direction):
        for i in range(nr):
            s = '<A CLASS="c%d tips" HREF="?sort_column=%d+%s&%s=1">' \
                '<SPAN></SPAN>' % (i, (i,'',-1-i)[direction+1], table, table)
            if i == selected:
                s += {1: '&#8595;', -1: '&#8593;'}[direction]
            self.expect(s)

        col = []
        for line in self.page.split('<td><A HREF="?answered_other=')[1:]:
            col.append(line.split('<td')[selected].split('>')[1].split('<')[0])
        if direction == 1:
            assert( sorted(col) == col )
        elif direction == -1:
            reverse = sorted(col)
            reverse.reverse()
            assert( reverse == col )
        else:
            bug

if __name__ == "__main__":
    try:
        the_server = server.Server()
        student = Student(the_server, 'toto')
        page = student.goto_question('repondre:bonjour')
        assert( "Répondez 'bonjour' à cette question." in page)
        print('The first question is correctly displayed')
        page = student.give_answer('coucou')
        assert( '<DIV class="question_bad">' in page)
        print('Bad answer rejected')
        page = student.give_answer('bonjour')
        assert( '<DIV class="question_good">' in page)
        print('Good answer accepted')
        
    finally:
        the_server.stop()

    


