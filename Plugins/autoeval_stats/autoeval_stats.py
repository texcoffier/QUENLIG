#!/usr/bin/env python
# -*- coding: latin-1 -*-
#    QUENLIG: Questionnaire en ligne (Online interactive tutorial)
#    Copyright (C) 2012 Thierry EXCOFFIER, Universite Claude Bernard
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

container = 'statmenu'
priority_execute = 'autoeval'
acls = { }

import questions
import statistics

def execute(state, plugin, argument):
    stats = statistics.question_stats()
    t = ['Q']
    for q in questions.questions.values():
        print q.name, getattr(q, 'autoeval_level', 999), getattr(q, 'student_given', False)
        if not hasattr(q, 'autoeval_level'):
            continue
        if not getattr(q, 'student_given', False):
            continue
        t.append('%s %s %s' % (
                q.name, q.autoeval_level, q.student_time / q.student_given))

    t.append('S')
    for s in stats.all_students:
        if not hasattr(s, 'autoeval_level'):
            continue
        if s.the_number_of_given_questions == 0:
            continue
        t.append('%s %s %s' % (s.name, s.autoeval_level,
                  s.the_time_searching / s.the_number_of_given_questions))

    return '<br>\n'.join(t)
