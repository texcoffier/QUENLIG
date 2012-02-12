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

"""Allow to grade and comment the good answers."""

priority_display = 'question_comments'
acls = { 'Teacher': ('executable',) }
sort_column = 0
javascript = r"""
function question_correction(event)
{
  var input = event ? event.target : window.event ;
  var url = "?question_correction=" + input.name + "," + encode_uri(input.value) ;
  var img = document.createElement('IMG') ;
  img.src = url ;
  var td = input.parentNode ;
  if ( td.tagName != 'TD' )
     td = td.parentNode ;
  td.style.background = 'yellow' ;
  input.parentNode.appendChild(img) ;
}

"""

css_attributes = (
    "/.question_correction_table IMG { width: 8px; height: 8px; background: #F00; border: 0px }",
    "/.question_correction_table SPAN { white-space: pre ; }",
    "/.question_correction_comment { text-decoration: underline; }",
)

import utilities
import statistics
import student
import cgi

def execute(state, plugin, argument):
    if state.question == None:
        return

    teacher = state.student.filename

    if argument:
        the_student, grade = argument.split(',')
        if the_student.startswith('*'):
            the_student = the_student[1:]
            comment = unicode(grade,'utf-8').encode('latin-1')
            student.students[the_student].set_why(
                state.question.name,
                teacher + '\002' + comment) # \001 is yet used
        else:
            student.students[the_student].set_grade(
                state.question.name,
                teacher + ',' + grade)
        return 'image/png', '\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x02\x00\x00\x00\x90wS\xde\x00\x00\x00\x01sRGB\x00\xae\xce\x1c\xe9\x00\x00\x00\x0fIDAT\x08\x1d\x01\x04\x00\xfb\xff\x00\x00\xff\x00\x02\x02\x01\x00\x0b\x0e\xaa\xaf\x00\x00\x00\x00IEND\xaeB`\x82'

    stats = statistics.question_stats()
    
    lines = []
    for s in stats.all_students:
        a = s.answer(state.question.name)
        if not a.answered:
            continue
        last = int(a.grades.get(teacher, '-1'))
        why = a.why.get(teacher, '')
            
        lines.append(
            [utilities.answer_format(a.answered),
             '<span><!-- %2d -->' % last
             +''.join('<input name="%s" type="radio" value="%d" onclick="question_correction(event)"%s>&nbsp;%d'
                      % (s.filename, i, ['',' checked'][i == last], i)
                      + {0: '', 1: '', 2:'<br>'}[i%3]
                      for i in range(6)
                      ) + '</span>',
             '<textarea rows="2" cols="40" name="*%s" onchange="question_correction(event)">%s</textarea>' % (s.filename, cgi.escape(why)),
             ])

    if len(lines) == 0:
        return
    return ('<noscript>!!!!!!!JAVASCRIPT NEEDED!!!!!!</noscript>'
            + utilities.sortable_table(plugin.sort_column, lines,
                                       url=plugin.plugin.css_name,
                                       html_class="question_correction_table",
                                       )
            )


def add_a_link(state, question):
    """This function is called by 'answered' plugin."""

    a = state.student.answer(question.name)
    t = []
    for teacher, why in a.why.items():
        t.append('<p class="question_correction_comment">'
                 + cgi.escape(teacher) + '</p><pre>'
                 + cgi.escape(why) + '</pre>')

    return '<div class="question_correction">' + '\n'.join(t) + '</div>'
