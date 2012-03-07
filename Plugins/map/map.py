#!/usr/bin/env python
# -*- coding: latin-1 -*-
#    QUENLIG: Questionnaire en ligne (Online interactive tutorial)
#    Copyright (C) 2007,2011 Thierry EXCOFFIER, Universite Claude Bernard
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

"""Display a graphical map of the questions."""

import questions
import os

priority_display = 'comment'
css_attributes = (
    'IMG { width: 100% ; margin-top: 0.3em ; }',
    )
acls = { 'Student': ('executable',) }

try:
    import PIL.Image
    def convert_to_gif(width, height, data, state):
        filename = os.path.join(state.student.file, 'map.gif')
        im = PIL.Image.new("RGB", (width, height))
        im.putdata(data)
        im.save(filename, 'GIF')
        f = open(filename,'r')
        image = f.read()
        f.close()
        return image
except ImportError:
    def convert_to_gif(width, height, data, state):
        image = ['P6\n%d %d\n255\n' % (width, height)]
        for p in data:
            image.append( chr(p[0]) + chr(p[1]) + chr(p[2]) )

        filename = os.path.join(state.student.file, 'map.gif')
        f = os.popen('ppmtogif >"%s" 2>/dev/null' % filename, 'w')
        f.write(''.join(image))
        f.close()
        f = open(filename,'r')
        image = f.read()
        f.close()
        return image
    print "To speed up Quenlig, install PIL package"


def question_color(q, state, answerables):
    if (state.question != None and state.question.name == q.name):
        p = (255, 255, 0)
    elif state.student.answered_question(q.name):
        p = (0, 255, 0)
    elif state.student.bad_answer_question(q.name):
        p = (255, 0, 0)
    elif q.name in answerables:
        if state.student.given_question(q.name):
            p = (0, 255, 255)
        else:
            p = (0, 0, 255)
    else:
        p = (128, 128, 128)
    indice = state.student.nr_indices_question(q.name)
    if indice == 0:
        return p
    
    # Make lighter color on indices
    if indice > 3:
        indice = 3
    return tuple([
        pp and pp or int(indice**0.5  *  80)
        for pp in p
        ])

def question_pixel_map(state):
    m = []
    level = None
    answerables = [q.name for q in state.student.answerables(any=True)]
    for q in questions.sorted_questions:
        if q.level != level:
            m.append([])
            level = q.level
        m[-1].append(question_color(q, state, answerables))
    
    width = max([len(x) for x in m])
    image = []
    for col in m:
        image.append(col + [(255,255,255)] * (width - len(col)))
    image = sum(zip(*image), ())
    
    return 'image/gif', convert_to_gif(len(m), width, image, state)

def execute(state, dummy_plugin, argument):
    if argument:
        return question_pixel_map(state)
    return '<img src="?map=1">'



