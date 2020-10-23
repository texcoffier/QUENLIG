#!/usr/bin/env python3
# -*- coding: latin-1 -*-
#    QUENLIG: Questionnaire en ligne (Online interactive tutorial)
#    Copyright (C) 2007,2012 Thierry EXCOFFIER, Universite Claude Bernard
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

"""Allow the students to leave a comment about the question."""

import html
import traceback
import smtplib
import email.header
import ast
import time
import threading
from QUENLIG import configuration

priority_display = 'analyse'
css_attributes = (
    "TEXTAREA { font-size: 80% ; width: 100% }",
    """FORM {
    max-height: 0px ;
    margin: 0px;
    transition: max-height 1s;
    webkit-transition: max-height 1s;
    overflow: hidden ;
    }""",
    "FORM.highlight { max-height: initial ; }",
    "FORM.highlight BUTTON P { background: #CFC ; }",
    ":hover FORM { max-height: 20em }",
    "BUTTON { width: 100% ; white-space: normal }",
    ".comment_given { white-space: normal;}",
    )
acls = { 'Student': ('executable',) }
javascript = """
function PersistentInput(element_id, name)
{
   this.input = document.getElementById(element_id) ;
   this.form = this.input ;
   while( this.form.tagName != 'FORM' )
      this.form = this.form.parentNode ;
   this.key = 'persistent_input/' + element_id + '/' + (name || '') ;
   if ( this.get_persistent() !== '')
      {
         this.input.value = this.get_persistent() ;
         this.show() ;
      }
   this.form.onsubmit = this.onsubmit.bind(this) ;
   if ( this.input.onkeypress )
      this.old_onkeypress = this.input.onkeypress ;
   this.input.onkeypress = this.onkeypress.bind(this) ;
   this.input.persistent = this ;
}

PersistentInput.prototype.debug = function(txt)
{
   if ( false )
      console.log(this.key + " " + txt + " " + this.input.value) ;
} ;
PersistentInput.prototype.get_persistent = function()
{
   this.debug("GET") ;
   return localStorage[this.key] || '' ;
} ;
PersistentInput.prototype.set_persistent = function(txt)
{
   this.debug("SET") ;
   localStorage[this.key] = txt ;
   this.show() ;
} ;
PersistentInput.prototype.show = function()
{
   this.debug("SHOW") ;
   this.form.className = this.input.value != '' ? "highlight" : '' ;
} ;
PersistentInput.prototype.onkeypress_real = function()
{
   this.debug("KEYREAL") ;
   this.set_persistent(this.input.value) ;
} ;
PersistentInput.prototype.onkeypress = function(event)
{
   this.debug("KEY (" + event.char + ") code=" + event.keyCode) ;
   if ( event.char === '' && event.keyCode != 9 )
      return ;
   // Needed because INPUT.value is modified after the keypress
   setTimeout(this.onkeypress_real.bind(this), 100) ;
   if ( this.old_onkeypress )
      this.old_onkeypress(event) ;
} ;
PersistentInput.prototype.onsubmit = function()
{
   this.debug("SUBMIT") ;
   this.set_persistent("") ;
} ;
"""

def option_set(plugin, value):
    if value:
        value = ast.literal_eval(value)
    else:
        value = (None, None)
    (configuration.teacher_mail, configuration.smtp_server) = value

option_name = 'comment'
option_help = '''("the_teacher@university.org", "smtp.university.org")
        If defined, on each student comment:
        a mail is sent to 'the_teacher@university.org'
        via the 'smtp.university.org' mail server.'''
option_default = ""

def encode(x):
    return email.header.Header(x).encode()

def mail_real(mail_from, mail_to, subject, message):
    e_mail_to = encode(mail_to)
    e_mail_from = encode(mail_from)
    e_subject = encode(subject)
    content = [
        'Subject: ' + e_subject,
        'To: '      + e_mail_to,
        'From: '    + e_mail_from,
        'Content-Transfer-Encoding: 8bit',
        'MIME-Version: 1.0',
        ]
    if message.startswith('<'):
        content.append('Content-Type: text/html; charset="utf-8"')
    else:
        content.append('Content-Type: text/plain; charset="utf-8"')
    content.append('')
    content.append(message)

    session = smtplib.SMTP(configuration.smtp_server)
    session.sendmail(from_addr = e_mail_from,
                     to_addrs = e_mail_to,
                     msg = '\r\n'.join(content).encode('utf-8'))
    session.close()

def mail_with_retry(mail_from, mail_to, subject, message):
    for i in range(8):
        try:
            mail_real(mail_from, mail_to, subject, message)
            return
        except:
            traceback.print_exc()
            time.sleep(2 ** i)
    return "Can't send mail"

class MailThread(threading.Thread):
    to_send = []

    def run(self):
        while self.to_send:
            mail_with_retry(*self.to_send.pop(0))
            time.sleep(60)

def sendmail(mail_from, mail_to, subject, message):
    MailThread.to_send.append((mail_from, mail_to, subject, message))
    if len(MailThread.to_send) <= 1:
        MailThread().start()

configuration.sendmail = sendmail

def send_comment(state, plugin, argument, q):
    if q == "None":
        bads = ""
        before = ""
        question = ""
    else:
        answers = state.student.answer(q)
        bads = '\n'.join("<li>{}".format(html.escape(a))
                         for a in answers.bad_answers)
        if state.question.before:
            before = "<hr>" + state.question.get_before(state)
        else:
            before = ""
        question = "<hr>" + state.question.get_question(state)
    session = smtplib.SMTP(configuration.smtp_server)
    info = state.student.informations
    login = state.student.filename
    student_mail = info.get("mail", login)
    sn = info.get("surname", "")
    fn = info.get("firstname", "")
    sendmail(student_mail, configuration.teacher_mail,
         '{}/{} {} {} {}'.format(configuration.session.name, q, login, sn, fn),
         """<html><b>{}</b>
<p>
{}
{}
{}
<hr>
<ul>
{}
</ul>
""".format(q, html.escape(argument), before, question, bads))

done = set()

def execute(state, plugin, argument):
    if argument and argument not in done:
        done.add(argument)
        if state.question:
            q = state.question.name
        else:
            q = "None"
        state.student.add_a_comment(q, argument)
        if configuration.teacher_mail:
            try:
                send_comment(state, plugin, argument, q)
            except:
                traceback.print_exc()
        
        s = '<div class="comment_given">' \
            + html.escape(argument) + '</div>'
    else:
        s = ''


    return '''
    <FORM METHOD="GET" ACTION="#">
    <TEXTAREA id="comment" NAME="%s" ROWS="10"></TEXTAREA><br>
    <script>new PersistentInput('comment')</script>
    <button type="submit"><p class="comment_button"></p></button>
    </FORM>
    ''' % plugin.plugin.css_name  + s
