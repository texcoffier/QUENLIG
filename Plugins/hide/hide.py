#!/usr/bin/env python
# -*- coding: latin-1 -*-
#    QUENLIG: Questionnaire en ligne (Online interactive tutorial)
#    Copyright (C) 2010 Thierry EXCOFFIER, Universite Claude Bernard
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

"""This plugin allows to remove acls to others users.
It is not yet working."""

import student

priority_execute = '-page'

container = 'administration'

link_to_self = True

acls = { 'Teacher': ('executable',) }

javascript = r"""

function hide_stop_event(event)
{
  if ( event.stopPropagation )
    event.stopPropagation(true) ;
  if ( event.preventDefault )
    event.preventDefault(true) ;
  else
    {
      event.returnValue = false;
      event.keyCode = 0;
    }

  event.cancelBubble = true ;
}

function hide(event, plugin)
{
   hide_stop_event(event) ;
   var who = prompt('«' + plugin + '»\n\n' + hide_message, hide_roles) ;
   window.location = '?hide=' + plugin + ',' + who ;
   return false ;
}

"""


css_attributes = (
    "/TT.hide { background:yellow }",
    "/TT.hide:before { content:'×' }",
    )
    


def execute(state, plugin, argument):

    errors = ''
    
    if argument == '1':
        state.hide = 1 - state.__dict__.get('hide', 0)
        
    if not state.__dict__.get('hide', 0):
        return ''

    if argument and argument != '1' and state.student:
        # Hide the plugin
        args = argument.split(',')
        for role in args[1:]:
            if role not in student.students:
                errors += 'alert("' + role + '?");\n'
                continue
            s = student.students[role]
            # It is normally a tristate : add, remove or inherit
            s.acls.change_acls(args[0], '!executable')
            print '\n\n', args[0], role, '\n\n'
        # XXX : should recompute all, but it can't be done here : deffered
        # state.update_the_plugins = True

        errors += 'window.location = "?" ;\n'

    for a_plugin in state.plugins_list:
        x = '<tt class="hide" onmouseup="hide(event,\'%s\')"></tt>' % a_plugin.plugin.css_name
        if not hasattr(a_plugin, 'content'):
            continue
        if a_plugin.content or a_plugin.boxed():
            try:
                a_plugin.value_title += x
            except (AttributeError, TypeError):
                pass
        else:
            try:
                a_plugin.value += x
            except TypeError:
                a_plugin.value = x
                pass

    make_visible = '</a>'
    for plugin_name, a_plugin in state.plugins_dict.items():
        if not hasattr(a_plugin, 'content'):
            continue
        if a_plugin.value or a_plugin.content:
            continue
        make_visible += '<br><var class="hide" onmouseup="hide(event,\'%s\')">' % plugin_name + '&nbsp;<small>+ ' + plugin_name + '</small></var>'


    return (make_visible + '<script><!--\nhide_roles = ["'
            + state.student.filename
            + '",'
            + ','.join(['"%s"' % role
                        for role in state.student.roles])
            + '] ; %s\n--></script>' % errors)
            

def init():
    import state

    old_state = state.State

    class State(state.State):
        def execute(self, form):
            self.update_the_plugins = False
            a = old_state.execute(self, form)
            if self.update_the_plugins:
                self.update_plugins()
            return a

    state.State = State
