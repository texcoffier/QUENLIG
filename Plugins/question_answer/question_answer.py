#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#    QUENLIG: Questionnaire en ligne (Online interactive tutorial)
#    Copyright (C) 2007-2011 Thierry EXCOFFIER, Universite Claude Bernard
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

"""It both display the INPUT HTML tag to enter the answer
but it also verify the answer.

As the answer may modify the question list, it must be executed
before the question list computation.
"""

import random
import time
import cgi
from QUENLIG import configuration
from QUENLIG import utilities
from QUENLIG import questions

priority_execute = '-question' # To update question list before
priority_display = 'question'

css_attributes = (
    "INPUT { width: 100% ; font-family: times; font-size:120%}",
    "INPUT.checkbox { width: auto}",
    "TEXTAREA { width: 100% ; }",
    "FORM { margin: 0px }",
    "BUTTON { margin-top: 0.5em }",
    "BUTTON P { margin: 0px ; }",
    ".show_on_hover { overflow: hidden ; max-height: 0px ; transition: max-height 1s ;  webkit-transition: max-height 1s ;  }",
    ":hover .show_on_hover { max-height: 10em }",
    )
acls = { 'Wired': ('executable',) }

javascript = """
function disable_tab(event)
{
     if ( window.event )
        event = window.event ;
     key = event.keyCode ;

     if(key == 9)
         {
          event.target.value += '   ' ;
          return false;
         }
     else
          return true;

}

function check_button(e)
{
  while(e.tagName != 'FORM')
     e = e.parentNode ;
  var input = e.getElementsByTagName("INPUT") ;
  var button = e.getElementsByTagName("BUTTON")[0] ;
  for(var i in input)
     if ( input[i].checked )
        {
          button.disabled = false ;
          return ;
        }
  button.disabled = true ;
}

function seconds()
{
  var t = new Date() ;
  return t.getTime() / 1000 ;
}

var suspended_until_time ;

function change_state(state)
{
  var e = document.getElementById("questionanswer") ;
  var t = e.getElementsByTagName("INPUT") ;
  for(var i=0; i<t.length; i++)
     if (state)
        t[i].setAttribute("disabled", state) ;
     else
        t[i].removeAttribute("disabled") ;
}

function update_suspended_time()
{
  var e = document.getElementById("suspended_until") ;
  if ( ! e )
     return ;
  var dt = suspended_until_time - seconds() ;
  change_state(dt > 0);
  if ( dt <= 0 )
     {
      // Activate
      e.innerHTML = " GO!" ;
      e.id = "" ;
      change_state(false);
     }
  else
      e.innerHTML = " <b>" + duration(dt.toFixed(0)) + '</b>' ;
}

function suspended_until(t)
{
   if ( seconds() > t )
      return ;
   document.write('<span id="suspended_until" class="suspended_until"></span>');
   suspended_until_time = t ;
   setInterval(update_suspended_time, 1000) ;
}

"""

def option_set(plugin, value):
    if value == 'always':
        plugin.state.answer_always_visible = True
    elif value == 'hover':
        plugin.state.answer_always_visible = False
    else:
        raise ValueError("Bad value for 'answer-visibility': " + value)

option_name = 'answer-visibility'
option_help = '''"always" or "hover"
        When returning to an answered question the last answer is displayed
        automaticaly or only if the mouse goes on the box title.'''
option_default = "always"


def execute(state, plugin, argument):
    if state.question == None:
        return
    if state.question.tests == ():
        return
    if state.form.get('erase', False):
        state.student.erase(state.question.name)

    if argument and (
            state.question in state.student.answerables()
            or configuration.allowed_to_change_answer(state)
            or (state.student.answer(state.question.name).nr_good_answer
                and not state.student.answer(state.question.name).answered)
    ):
        if time.time() < state.student.answer(state.question.name
        ).suspended_until():
            return # Cheater

        # Fill 'last_answer' attribute
        state.student.bad_answer_yet_given(state.question.name, argument)
        # Check the answer even if it is a known one because
        # the question tests may have been updated in live
        number, message = state.student.check_answer(argument, state)
        if number:
            state.student.good_answer(state.question.name,argument)
        else:
            # Does not count the same bad answer
            if not state.student.bad_answer_yet_given(state.question.name,
                                                      argument):
                state.student.bad_answer(state.question.name, argument)

    if not state.question.answerable(state.student):
        state.question = None
        return '<p class="maximum_bad_answer">'

    if (not state.question.required.answered(state.student.answered_questions(),
                                            state.student)
        and not state.plugins_dict['questions_all'].current_acls['executable']
        ):
        return ('<p class="missing_required">: '
                + ', '.join(questions.questions[q].a_href()
                            for q in state.question.required.missing(
                                    state.student.answered_questions(),
                                    state.student)))

    if not isinstance(plugin.title, tuple):
        plugin.title = (plugin.title, plugin.title)

    question = state.question.get_question(state)

    if state.student.answered_question(state.question.name):
        # Value setted in question_change_answer plugin
        if not configuration.allowed_to_change_answer(state):
            s = state.student.last_answer(state.question.name)
            plugin.value_title = plugin.title[-1]

            if state.answer_always_visible or argument:
                return utilities.answer_format(s, question=question)
            else:
                return ('<div class="show_on_hover">'
                        + utilities.answer_format(s, question=question)
                        + '</div>')

    plugin.value_title = plugin.title[0]

    s = '<FORM CLASS="questionanswer" ID="questionanswer" accept-charset="utf-8" METHOD="GET" ACTION="#">'

    suspend = state.student.answer(state.question.name).suspended_until()
    s += "<script>suspended_until(" + str(suspend) + ");</script>"

    last_answer = state.student.last_answer(state.question.name)
    if last_answer == "":
        try:
            last_answer = state.question.default_answer(state)
        except TypeError:
            last_answer = state.question.default_answer
        style = ''
    else:
        if state.student.bad_answer_yet_given(state.question.name,
                                              last_answer):
            style = 'background:#FAA'
        else:
            # Assume it was a correct answer
            style = ''

    last_answer_html = (cgi.escape(last_answer)
                        .replace("%","&#37;")
                        .replace("'", "&#39;")
                        .replace('"', '&#34;'))

    if '{{{' in question:
        t = question.split('{{{')[1:]
        if '{{{ shuffle}}}' in question:
            for i in t:
                if i.startswith(" shuffle}}}"):
                    t.remove(i)
                    break
            random.shuffle(t)
        nr_checked = 0
        for i in t:
            j = i.split('}}}')
            if j[0].startswith('↑'):
                j[0] = j[0][1:]
                if s.endswith("<br>"):
                    s = s[:-4]
            if j[0].startswith('!'):
                j[0] = j[0][1:]
                button_type = "radio"
            else:
                button_type = "checkbox"
            if j[0] == '':
                s += j[1] + '<br>'
                continue
            if j[0] in last_answer:
                checked = ' checked'
                if nr_checked == 0:
                    checked += ' id="2"'
                    nr_checked = 1
            else:
                checked = ''
            s += '<label><input onchange="check_button(this)" class="checkbox" type="%s" name="%s" value="%s"%s>' % (
                button_type, plugin.plugin.css_name,
                j[0].replace('"', '&#34;'), checked
            ) + j[1] + '</label><br>'
        if nr_checked == 0:
            checked = ' id="2"'
        else:
            checked = ''
        s += '<button disabled type="submit"%s><p class="answer_button"></p></button>' % checked
    elif state.question.nr_lines == 1:
        s += '<INPUT TYPE="text" ID="2" NAME="%s.%s.%s" SIZE="%d" VALUE="%s" ALT="%s" onkeyup="if(this.value==this.alt && this.alt!==\'\') this.style.background=\'#FAA\'; else this.style.background=\'white\'" style="%s">'% (
            # INPUT NAME
            plugin.plugin.css_name, configuration.session.name,
            cgi.html.escape(state.question.name),
            #
            configuration.nr_columns, last_answer_html,
            style and last_answer_html or '',
            style)
    else:
        s += '<TEXTAREA NAME="%s" ID="2" COLS="%d" ROWS="%d" onkeypress="return disable_tab(event)">%s</TEXTAREA>' % (
            plugin.plugin.css_name,
            configuration.nr_columns,
            state.question.nr_lines,
            last_answer_html)
        s += '<br><button type="submit"><p class="answer_button"></p></button>'
        
    s += '''
</FORM>
<script type="text/javascript">
document.getElementById(2).focus() ;
window.scrollTo(0,0) ;
new PersistentInput("2", "{}") ;
update_suspended_time() ;
</script>'''.format(cgi.html.escape(state.question.name))
    if state.question.maximum_bad_answer:
        s += '<p class="nr_try">%d</p>' % (
            state.question.maximum_bad_answer
            - state.student.bad_answer_question(state.question.name))
    return s



    




    

