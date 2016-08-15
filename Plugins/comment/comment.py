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
#    Contact: Thierry.EXCOFFIER@bat710.univ-lyon1.fr

"""Allow the students to leave a comment about the question."""

import cgi

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
    "BUTTON { width: 100% ; }",
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
      this.old_onkeypress = this.input.onkeypress.bind(this) ;
   this.input.onkeypress = this.onkeypress.bind(this) ;
}

PersistentInput.prototype.get_persistent = function()
{
   return localStorage[this.key] || '' ;
} ;
PersistentInput.prototype.set_persistent = function(txt)
{
   localStorage[this.key] = txt ;
   this.show() ;
} ;
PersistentInput.prototype.show = function()
{
   this.form.className = this.input.value != '' ? "highlight" : '' ;
} ;
PersistentInput.prototype.onkeypress_real = function()
{
   this.set_persistent(this.input.value) ;
} ;
PersistentInput.prototype.onkeypress = function(event)
{  // Needed because INPUT.value is modified after the keypress
   setTimeout(this.onkeypress_real.bind(this), 100) ;
   if ( this.old_onkeypress )
      this.old_onkeypress(event) ;
} ;
PersistentInput.prototype.onsubmit = function()
{
   this.set_persistent("") ;
} ;
"""

def execute(state, plugin, argument):
    if argument:
        if state.question:
            q = state.question.name
        else:
            q = "None"
        state.student.add_a_comment(q, argument)
        
        s = '<div class="comment_given">' \
            + cgi.escape(argument) + '</div>'
    else:
        s = ''


    return '''
    <FORM METHOD="GET" ACTION="#">
    <TEXTAREA id="comment" NAME="%s" ROWS="10"></TEXTAREA><br>
    <script>new PersistentInput('comment')</script>
    <button type="submit"><p class="comment_button"></p></button>
    </FORM>
    ''' % plugin.plugin.css_name  + s
