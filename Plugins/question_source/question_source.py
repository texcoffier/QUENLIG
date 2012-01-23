#!/usr/bin/env python
# -*- coding: latin-1 -*-
#    QUENLIG: Questionnaire en ligne (Online interactive tutorial)
#    Copyright (C) 2007-2012 Thierry EXCOFFIER, Universite Claude Bernard
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

"""Displays the question Python source."""

import os
import configuration
import cgi

container = 'heart'
priority_display = 10000000
acls = { 'Teacher': ('executable',) }

def extract_question(c, lineno):
    """Extract a question definition from the python source.
    """

    start = lineno
    while not c[start].startswith('add('):
        start -= 1

    end = lineno
    while not c[end].strip() == '':
        end += 1

    return ''.join(c[start:end])

def string(txt):
    if '\n' in txt:
        if '"""' in txt:
            sep = "'''"
        else:
            sep = '"""'
        return sep + txt + sep
    if '"' not in txt:
        return '"' + txt + '"'
    if "'" not in txt:
        return "'" + txt + "'"
    return repr(txt)

def strings(strs, sep=','):
    r = []
    for x in strs:
        r.append(string(x))
    return '[' + sep.join(r) + ']'

def source_python(question, state):
    """Unfinished"""
    s = ["add(name=\"%s\"," % question.short_name]
    r = []
    for required in question.required.names():
        world, name = required.split(':')
        if world == question.world:
            required = name
        r.append(required)
    s.append("    required=%s," % strings(r))
    if question.before:
        s.append("    before=%s," % string(question.before(state)) )
    s.append("    question=%s," % string(question.question(state)) )
    if question.indices:
        s.append("    indices=%s," % strings(question.indices,
                                             sep = ',\n    ') )
    if question.good_answer:
        s.append("    good_answer=%s," % string(question.good_answer) )
    if question.bad_answer:
        s.append("    bad_answer=%s," % string(question.bad_answer) )
    if question.tests:
        s.append("    tests = (")
        for t in question.tests:
            s.append(t.source() + ',\n')
        s.append("    ),")
    s.append(")")
    return '\n'.join(s)

def execute(state, plugin, argument):

    if state.question == None:
        return
    
    f = open( os.path.join(configuration.root, configuration.questions,
                           state.question.world + ".py"), "r")
    c = f.readlines()        
    f.close()

    c = extract_question(c, state.question.f_lineno)

    f = open('xxx.source.py', 'w')
    f.write(c)
    f.close()
    f = os.popen('highlight --xhtml xxx.source.py ; grep -v "body" <highlight.css >HTML/highlight.css', 'r')
    c = f.read().replace('highlight.css', '/highlight.css')
    f.close()

    return c + '<pre>' + cgi.escape(source_python(state.question, state)) + '</pre>'
    



    




    

