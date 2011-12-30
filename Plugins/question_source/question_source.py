#!/usr/bin/env python
# -*- coding: latin-1 -*-
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

"""Displays the question Python source."""

import os
import re
import configuration

container = 'heart'
priority_display = 10000000
acls = { 'Teacher': ('executable',) }

def extract_question(c, function):
    """Extract a question definition from the python source.
    Extract some text before.
    Bugs:
       - Inside the 'add' the text must not go to the first column
       """
    
    function = re.escape(function)
    c = re.sub('\nadd[ \t]*\(', '\n', c) # simplify the not matching

    lines_starting_by_space_or_empty = "(\n+[ \t][^\n]*)*"

    not_an_add = "\n+[a-zA-Z][^\n]*"
    not_an_add_bloc = not_an_add + lines_starting_by_space_or_empty
    
    the_add = '\n+name=[\'"]'+ function + '[\'"][^\n]*'
    the_add_bloc = the_add + lines_starting_by_space_or_empty
    
    interesting_part = "(" + not_an_add_bloc + ")*" + the_add_bloc
    
    c = re.sub('(?s)(' + interesting_part + ")", '\\1', c)
    c = re.sub('(?s).*', '', c)
    c = re.sub('(?s).*', '', c)
    c = c.replace('', 'add(')

    return c

def execute(state, plugin, argument):

    if state.question == None:
        return
    
    f = open( os.path.join(configuration.root, configuration.questions,
                           state.question.world + ".py"), "r")
    c = f.read()        
    f.close()

    c = extract_question(c, state.question.short_name)

    f = open('xxx.source.py', 'w')
    f.write(c)
    f.close()
    f = os.popen('highlight --xhtml xxx.source.py ; grep -v "body" <highlight.css >HTML/highlight.css', 'r')
    c = f.read().replace('highlight.css', '/highlight.css')
    f.close()

    return c
    



    




    

