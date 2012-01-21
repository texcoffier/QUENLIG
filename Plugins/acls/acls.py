#!/usr/bin/env python
# -*- coding: latin-1 -*-
#    QUENLIG: Questionnaire en ligne (Online interactive tutorial)
#    Copyright (C) 2007-2008 Thierry EXCOFFIER, Universite Claude Bernard
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

"""
The ACLS are not predefined, any plugin can add its own.

The roles ACLS may be defined in the user named after the role.

ACLS are taken from:
  * The default ACLs from plugin:
     acls = {'Default':('executable','hiddable'), 'Teacher':('!executable',)}
  * The ACLs from role
  * The student ACLs
     acls = {plugin_A:('executable',), plugin_B: ('!hiddable', )}
     
The code assume that :
  * The role of a role does not change
  * A role is a student: The ACLs of a role are the ACLs of the student
"""

import student
import utilities
import os

priority_execute = 'role' # Role must have been computed.
acls = { 'Wired': ('executable',) }
container = 'page'

class Acls:
    """ACL helper class for Stateplugin.
    The key is 'executable', 'hideable', ...
    """
    def __init__(self):
        self.reset()
    def update(self, acls, comment=True):
        for acl in acls:
            if acl[0] == '!':
                if self[acl[1:]]:
                    del self.acls[acl[1:]]
                    self.deleted[acl[1:]] = comment
            else:
                self.acls[acl] = comment
    def reset(self):
        self.acls = {}
        self.deleted = {}
    def __getitem__(self, key):
        return self.acls.get(key, False)
    def __str__(self):
        return 'ACLS(' + repr(self.acls) + ')[' + repr(self.deleted) + ']'

class StudentAcls:
    """ACL helper class for student.
     acls = {plugin_A:('executable',), plugin_B: ('!hiddable', )}
    """
    def __init__(self, filename):
        self.acls = {}
        self.filename = filename

    def get_acls(self, plugin):
        """Get all the ACLS for the plugin"""
        return self.acls.get(plugin, ())

    def get_an_acl(self, plugin, key):
        """Return True if set, False if unset, None if neither"""
        if key.startswith('!'):
            ke = key[1:]
        acls = self.get_acls(plugin)
        if key in acls:
            return True
        if '!' + key in acls:
            return False

    def append_an_acl(self, plugin, key):
        """Change the ACL without checking"""
        if plugin in self.acls:
            self.acls[plugin].append(key)
        else:
            self.acls[plugin] = [key]

    def change_acls(self, plugin, key):
        self.add_an_acl(plugin, key)
        utilities.write(self.filename, repr(self.acls))
        reload() # Force plugins tree update

    def add_an_acl(self, plugin, key):
        """Change the ACL with checking"""
        current = self.get_an_acl(plugin, key)
        if current == None:
            self.append_an_acl(plugin, key)
            return
        if key.startswith('!'):
            if current == False:
                return
            try:
                self.acls[plugin].remove(key[1:])
            except ValueError:
                pass
            self.append_an_acl(plugin, key)
        else:
            if current == True:
                return
            self.acls[plugin].remove('!' + key)
        self.append_an_acl(plugin, key)

    def __str__(self):
        return repr(self.acls)
    

def update_student_acls(astudent):
    """Read ACL for a student or a role from the file"""

    if 'acls' in astudent.__dict__:
        return False

    astudent.acls = StudentAcls(os.path.join(astudent.file, 'acls'))
    try:
        c = utilities.read(astudent.acls.filename)
    except:
        pass
    else:
        if c:
            astudent.acls.acls = eval(c)

    for role in astudent.roles:
        update_student_acls(student.student(role))

    return True

def update_role(state, astudent, role):
    role_student = student.student(role)

    # Update current_acls from the parent
    if role_student != astudent:
        # If not the tree root, update from parent value
        astudent.old_role = astudent.current_role
        assert(len(role_student.roles) == 1)
        update_role(state, role_student, role_student.current_role)

    # Update from the plugin default values for me
    for plugin in state.plugins_list:
        plugin.current_acls.update( plugin.acls.get(astudent.name, ()),
                                    comment="From '%s' role" % astudent.name)
        if not plugin.permanent_acl:
            continue
        for role in astudent.roles:
            plugin.current_acls.update( plugin.acls.get(role, ()),
                                        comment="From '%s' Permanent role"
                                        % role)
            role = student.student(role)
            acls = role.acls.get_acls(plugin.plugin.css_name)
            for acl in acls:
                plugin.current_acls.update(acl,
                                           comment="From '%s' permanent role"
                                           % role.name)

            

    # Update from the student or role values from file
    update_student_acls(astudent)

    for plugin, acl_list in astudent.acls.acls.items():
        try:
            state.plugins_dict[plugin].current_acls.update(
                acl_list,
                comment="From '%s' acls" % astudent.name
                )
        except KeyError:
            print 'ERROR ACLS %s : %s' % (astudent.name, plugin)

    return True

def update_my_role(state):
    if state.student.current_role == state.student.old_role:
        return False

    # Clear the plugin ACLS
    for plugin in state.plugins_list:
        if not isinstance(plugin.current_acls, Acls):
            plugin.current_acls = Acls()
        else:
            plugin.current_acls.reset()

    c = update_role(state, state.student, state.student.current_role)

    return c


def update_plugin_content(state):
    for plugin in state.plugins_list:
        plugin.content = [ p
                           for p in plugin.full_content
                           if p.current_acls['executable'] ]

    
def execute(state, plugin=None, argument=None):
    """Initialize the acls list for the student and its 'ancestors'"""

    d1 = update_student_acls(state.student)
    d2 = update_my_role(state)
    if d1 or d2:
        update_plugin_content(state)
   

def reload():
    """Reinitialize all the ACLS"""

    for a_student in student.students.values():
        try:
            # del a_student.roles
            a_student.old_role = 'non existent role'
            del a_student.acls # Must recompute ACLS
        except AttributeError:
            pass

    import Plugins.role.role
    for a_student in student.students.values():
        Plugins.role.role.update_roles(a_student)


    # XXX: get permanent rights in case of the following interaction :
    #    An user update the plugins and so call 'acls.reload()'
    #    The user change of role
    # The permanent rights are lost, so we compute them here in case
    import state
    for a_state in state.states.values():
        execute(a_state)



    


    

