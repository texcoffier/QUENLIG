#!/usr/bin/env python
# -*- coding: latin1 -*-
#    QUENLIG: Questionnaire en ligne (Online interactive tutorial)
#    Copyright (C) 2007 Thierry EXCOFFIER, Universite Claude Bernard
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

import questions
import os

allow_out_of_sequence_execution = True

priority_display = 'comment'
tip_preformated = True
css_attributes = (
    'IMG { width: 100% ; margin-top: 0.3em ; }',
    )
acls = { 'Default': ('executable',), 'Teacher': ('!executable',) }

def question_color(q, state, answerables):
    if (state.question != None and state.question.name == q.name):
        p = '\377\377\0'
    elif state.student.answered_question(q.name):
        p = '\0\377\0'
    elif state.student.bad_answer_question(q.name):
        p = '\377\0\0'
    elif q.name in answerables:
        if state.student.given_question(q.name):
            p = '\0\377\377'
        else:
            p = '\0\0\377'
    else:
        p = '\200\200\200'
    indice = state.student.nr_indices_question(q.name)
    if indice > 3:
        indice = 3
    ppp = ''
    for pp in p:
        if pp == '\0':
            pp = chr( int(indice**0.5  *  80) )
        ppp += pp
    return ppp

def question_pixel_map_other(state):
    student = state.student_stat
    if student == None:
        student = state.student
    filename = os.path.join(student.file,'map.gif')

    try:
        f = open(filename,'r')
        image = f.read()
        f.close()
        return 'image/gif', image
    except IOError:
        return 'text/plain', '?'


def question_pixel_map_circle(state):
    answerables = [q.name for q in state.student.answerables(any=True)]
    width = max([questions.questions[q].coordinates[0]
                 for q in questions.questions]) + 1
    height = max([questions.questions[q].coordinates[1]
                  for q in questions.questions]) + 1
    picture = []
    for i in range(height):
        picture.append(['\377\377\377']*width)

    for q in questions.questions:
        q = questions.questions[q]
        picture[q.coordinates[1]][q.coordinates[0]] = question_color(q, state, answerables)

    print width, height
    image = 'P6\n%d %d\n255\n' % (width, height)
    for line in picture:
        image += ''.join(line)

    filename = os.path.join(state.student.file,'map.gif')
    f = os.popen('ppmtogif >"%s" 2>/dev/null' % filename, 'w')
    f.write(image)
    f.close()
    f = open(filename,'r')
    image = f.read()
    f.close()
    return 'image/gif', image

def question_pixel_map(state):

    # if state.student.acls['question_pixel_map_circle']:
    #    return question_pixel_map_circle(state)
    
    m = []
    level = None
    answerables = [q.name for q in state.student.answerables(any=True)]
    for q in questions.sorted_questions:
        if q.level != level:
            m.append([])
            level = q.level
        m[-1].append(question_color(q, state, answerables))
    
    width = max([len(x) for x in m])
    image = 'P6\n%d %d\n255\n' % (len(m), width)
    for col in range(width):
        for line in range(len(m)):
            try:
                image += m[line][col]
            except IndexError:
                image += '\377\377\377'
                

    filename = os.path.join(state.student.file,'map.gif')
    f = os.popen('ppmtogif >"%s" 2>/dev/null' % filename, 'w')
    f.write(image)
    f.close()
    f = open(filename,'r')
    image = f.read()
    f.close()
    return 'image/gif', image

def execute(state, plugin, argument):
    if argument:
        return question_pixel_map(state)
    return '<img src="?map=1">'



