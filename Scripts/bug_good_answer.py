#!/usr/bin/env python
# -*- coding: latin1 -*-
#    QUENLIG: Questionnaire en ligne (Online interactive tutorial)
#    Copyright (C) 2010 Thierry EXCOFFIER, Universite Claude Bernard
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

"""Check if a student see the good answer given by another student"""

import server
import student
import threading
import time

acls = "{'questions_all': ('executable',)}" # Can answer any question

question = "mode:ajouter"
good_answer = "chmod u+x essai.sh"
question_text = "Quelle ligne de commande permet"

class Reader(threading.Thread):
    def run(self):
        the_student = student.Student(the_server, 'reader', acls=acls)
        page = the_student.see_all_questions()
        while True:
            print 'read'
            page = the_student.goto_question(question)
            assert( question_text in page)
            assert( '<DIV class="question_good">' not in page)
            time.sleep(0.1)

if __name__ == "__main__":
    try:
        the_server = server.Server()

        Reader().start()

        for i in range(1000):
            print 'write'
            the_student = student.Student(the_server, 'toto%d' % i, acls=acls)
            page = the_student.see_all_questions()
            page = the_student.goto_question(question)
            assert( question_text in page)
            page = the_student.give_answer(good_answer)
            assert( '<DIV class="question_good">' in page)
        
    finally:
        the_server.stop()

    


