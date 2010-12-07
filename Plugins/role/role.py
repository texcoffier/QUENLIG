#!/usr/bin/env python
# -*- coding: latin1 -*-
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

import student
import utilities
import os

priority_execute = -100
container = 'identity'
priority_display = 1000
acls = { 'Teacher': ('executable',) }
permanent_acl = True

    
def update_roles(astudent):
    """Initialize the role list for the student and its 'ancestors'""" 
    if 'roles' in astudent.__dict__:
        return
    astudent.roles_filename = os.path.join(astudent.file, 'roles')
    utilities.write(astudent.roles_filename, "['Default']", overwrite=False)
    try:
        astudent.roles = eval(utilities.read(astudent.roles_filename))
    except:
        print 'BUG', astudent, utilities.read(astudent.roles_filename)
        astudent.roles = ['Default']


    astudent.current_role = astudent.roles[0]
    astudent.old_role = None
    
    for role in astudent.roles:
        update_roles( student.student(role) )


def execute(state, plugin, argument):
    update_roles(state.student)

    if argument in state.student.roles: # Change the role if possible
        state.student.current_role = argument
        state.student.old_role = None
    s = []
    for role in state.student.roles:
        if role == state.student.current_role:
            selected = 'selected'
        else:
            selected = ''
        s.append('<option %s>%s</option>' % (selected, role))

    if len(s) <= 1:
        return

    return '''
<select onChange="window.location = '%s?%s=' + value ;">
''' % (state.url_base_full, plugin.plugin.css_name) + '\n'.join(s) + '</select>'
    

    


    

