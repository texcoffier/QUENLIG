#!/usr/bin/env python3
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
import cgi
from QUENLIG import utilities

container = 'heart'
priority_display = 10000000
acls = { 'Author': ('executable',) }
priority_execute = '-reload_questions'

javascript = r'''
function encode_uri(t)
{
  return encodeURI(t).replace(/\?/g, "%3F").replace(/#/g, "%23")
    .replace(/[.]/g, "%2E").replace(/;/g, "%3B").replace(/&/g, "%26")
    .replace(/\//g, "%2F").replace(/,/g, "%2C").replace(/[+]/g, '%2B') ;
}
'''

def question_lines(c, question):
    start = question.f_lineno
    while not c[start].startswith('add('):
        start -= 1
    while start > 0 and c[start].strip() != '':
        start -= 1
    if c[start].strip() == '':
        start += 1

    end = question.f_lineno
    while end < len(c) and not c[end].strip() == '':
        end += 1
    if c[end].strip() == '':
        end -= 1
    return start, end

def extract_question(c, question):
    """Extract a question definition from the python source.
    """
    start, end = question_lines(c, question)
    return c[start:end+1]

def replace_question(c, question, source, state, encoding):
    # Save old file
    f = open(question.python_file() + '.old', 'wb')
    f.write('\n'.join(c).encode(encoding))
    f.close()

    start, end = question_lines(c, question)
    f = open(question.python_file(), 'wb')
    f.write(('\n'.join(c[:start]) + '\n'
             + source + '\n'
             + '\n'.join(c[end+1:])).encode(encoding))
    f.close()

    from QUENLIG import plugins
    reload_questions = plugins.Plugin.plugins_dict['reload_questions']
    try:
        reload_questions.plugin.execute(state, reload_questions, '1')
        return 'OK'
    except Exception as e:
        os.system("cat " + question.python_file())
        os.rename(question.python_file() + '.old', question.python_file())
        reload_questions.plugin.execute(state, reload_questions, '1')
        return '<pre class="python_error">' + cgi.escape(str(e)) + '</pre>'

def edit_python(source):
    return (
        '<FORM action="javascript:window.location=(\'?question_source=\' + encode_uri(document.getElementById(\'src\').value));">' +
        '<TEXTAREA id="src" style="width:100%%; height: %sem">' % (
            1.3 * source.count('\n'))
        + cgi.escape(source)
        + '</TEXTAREA><BUTTON class="save_source"></BUTTON></FORM>')

def execute(state, dummy_plugin, argument):
    if state.question == None:
        return

    f = open(state.question.python_file(), "rb")
    c, encoding = utilities.get_encoding(f.read())
    c = c.split('\n')
    f.close()

    before = ''
    if argument:
        source = argument
        try:
            compile(source, 'nofilename', 'exec')
        except SyntaxError as e:
            before = ('<pre class="python_error">' +
                      cgi.escape(str(e)) + '</pre>')
        if before == '':
            before = replace_question(c, state.question, source, state,
                                      encoding)
    else:
        source = '\n'.join(extract_question(c, state.question))


    if False:
        f = open('xxx.source.py', 'w')
        f.write('\n'.join(source))
        f.close()
        f = os.popen('highlight --xhtml xxx.source.py ; grep -v "body" <highlight.css >HTML/highlight.css', 'r')
        highlighted = f.read().replace('highlight.css', '/highlight.css')
        f.close()
        return highlighted

    # To remove problem with the reload plugin url
    state.form.pop('question_source', 1)
    
    return before + edit_python(source)
