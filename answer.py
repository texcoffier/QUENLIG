#    QUENLIG: Questionnaire en ligne (Online interactive tutorial)
#    Copyright (C) 2005-2006 Thierry EXCOFFIER, Universite Claude Bernard
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

class Answer:
    """These objects track how a student answer to the question"""
    def __init__(self, question, student):
        self.question = question
        self.student = student
        self.answered = False
        self.indice = -1
        self.nr_bad_answer = 0
        self.nr_asked = 0
        self.time_searching = 0
        self.time_after = 0
        self.first_time = 0
        self.comments = []
        self.bad_answers = []
        self.last_time = 0
        self.resign = False

    def eval_action(self, action_time, command, value):
        self.last_time = action_time
        if self.first_time == 0:
            self.first_time = action_time
        if command == "good":
            self.answered = value
        elif command == "indice" :
            self.indice += 1
        elif command == "bad" :
            self.answered = False # Needed for 'any_question'
            self.nr_bad_answer += 1
            self.bad_answers.append(value)
        elif command == "asked" :
            self.nr_asked += 1
        elif command == "comment" :
            self.comments.append((action_time, value))
        elif command == "login" :
            pass
        else:
            raise ValueError("Unknown action %s in %s" % (command, self.student))

    def __str__(self):
        return "%d %d %d %d %g %s" % (self.answered != False, self.nr_asked, self.nr_bad_answer, self.indice, self.time_searching+self.time_after, self.question)
