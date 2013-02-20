#!/usr/bin/env python
# -*- coding: latin-1 -*-
#    QUENLIG: Questionnaire en ligne (Online interactive tutorial)
#    Copyright (C) 2013 Thierry EXCOFFIER, Universite Claude Bernard
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
#    Contact: Thierry.EXCOFFIER@univ-lyon1.fr

"""Displays all the bad answers given for a question."""

import collections
import statistics
import re
import subprocess

priority_display = '-question_bads'
acls = { 'Author': ('executable',) }

def H(x):
    return 'N' + str(hash(x)).replace('-', 'M')

is_comment = '\001'
is_good = '\002'
is_first = '\003'
is_done = '\004'
re_comment = re.compile('    *')

def execute(state, dummy_plugin, dummy_argument):
    if state.question == None:
        return

    stats = statistics.question_stats()

    uncanonize = {}
    
    arcs = collections.defaultdict(lambda: collections.defaultdict(int))
    for s in stats.all_students:
        if state.question.name not in s.answers:
            continue
        a = s.answers[state.question.name]
        last_comment = is_first + state.question.question(state)
        for c_orig in a.bad_answers:
            c = state.question.canonize(c_orig, state)
            uncanonize[c] = c_orig
            commented = is_comment + re_comment.sub("\n", s.answer_commented(a.question ,c_orig))
            arcs[last_comment][c] += 1
            arcs[c][commented] += 1
            last_comment = commented
        if a.answered:
            c = is_good + state.question.canonize(a.answered, state)
            commented = is_done + re_comment.sub("\n", s.check_answer(state.question , a.answered, state)[1])
            commented = re.sub("(?s)<u:sequence.*", "", commented)
            arcs[last_comment][c] += 1
            arcs[c][commented] += 1
            uncanonize[c] = is_good + a.answered
        else:
            arcs[last_comment][a.answered] += 1

    s = '''digraph "%s" {
node[height="0.2",width="0.2",shape=rectangle, margin="0.025", label="",style="filled", fillcolor="white", fontsize="8"];
graph[charset="Latin1", orientation="P",ranksep=0.5,sep=0,nodesep=0.05];
''' % state.question.name
    nodes = set()
    for node, others in arcs.items():
        nodes.add(node)
        for other in others:
            nodes.add(other)
    for node in nodes:
        str_node = str(uncanonize.get(node,node)
                       ).replace('\\', '\\\\'
                                 ).replace('"', '\\"'
                                           ).replace('\n', '\\n')
                                     
        if str(node).startswith(is_comment):
            s += '%s [ label="%s"];\n' % (
                H(node), str_node[1:])
        elif str(node).startswith(is_good):
            s += '%s [ label="%s", style="filled",fillcolor="#88FF88" ];\n' % (
                H(node), str_node[1:])
        elif str(node).startswith(is_first):
            s += '%s [ label="%s" ];\n' % (
                H(node), str_node[1:])
        elif str(node).startswith(is_done):
            s += '%s [ label="%s", style="filled",fillcolor="#00FF00" ];\n' % (
                H(node), str_node[1:])
        elif node is False:
            s += '%s [ style="filled",fillcolor="#FF0000" ];\n' % (
                H(node),)
        else:
            s += '%s [ label="%s", style="filled",fillcolor="#FF8888"   ];\n' % (H(node), str_node)
    for node, others in arcs.items():
        for arc, nb in others.items():
            s += '%s -> %s [penwidth="%d"];\n' % (H(node), H(arc), nb)
    s += '}'


    f = open("xxx.dot", "w")
    f.write(s)
    f.close()
    p = subprocess.Popen(["dot", "-Tsvg", "xxx.dot"], stdout=subprocess.PIPE)
    svg = p.communicate()[0]
    
    try:
        svg = unicode(svg, "utf-8", 'ignore').encode("latin-1").replace("UTF-8", "ISO-8859-1")
    except UnicodeDecodeError:
        print "SVG: UnicodeDecodeError"
    except UnicodeEncodeError:
        print "SVG: UnicodeEncodeError"
        
    return '<div style="width:80em;overflow:auto">' + svg + '</div>'
