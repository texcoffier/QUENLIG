#!/usr/bin/env python3
# -*- coding: latin-1 -*-
#    QUENLIG: Questionnaire en ligne (Online interactive tutorial)
#    Copyright (C) 2011-2016 Thierry EXCOFFIER, Universite Claude Bernard
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

"""Display the realname of the student."""

import ast

try:
    from QUENLIG import student
except:
    try:
        import student
    except:
        pass


def option_set(plugin, value):
    (plugin.state.ldap_host,
     plugin.state.ldap_port,
     plugin.state.ldap_login,
     plugin.state.ldap_password) = ast.literal_eval(value)

option_name = 'ldap'
option_help = '''"('ldap.domain.org', 636, 'login', 'password')"
        Set the LDAP connection information to retrieve student name and mail.
	The value is a python tuple.'''
option_default = "('', 0, '', '')"

    
acls = { 'Default': ('executable',) }
priority_execute = 'identity'
container = 'identity'

ldap_is_here = False

try:
    import ldap3
    import ssl
    ldap_is_here = True
except ImportError:
    import sys
    sys.stderr.write(
        'WARNING: LDAP Python Package not found: NO real_name plugin\n')

keys = ('samaccountname', 'sn', 'givenName', 'mail')

def get_info(state, student_ids):
    try:
        s = ldap3.Server(state.ldap_host, state.ldap_port,
                         use_ssl = state.ldap_port == 636)
        c = ldap3.Connection(
            s,
            user = state.ldap_login,
            password = state.ldap_password,
            authentication = ldap3.AUTH_SIMPLE,
            raise_exceptions = True,
            client_strategy = ldap3.STRATEGY_ASYNC_THREADED,
        )
        c.tls = ldap3.Tls()
        c.tls.validate = ssl.CERT_NONE
        c.open()
        c.start_tls()
        c.bind()
    except ldap3.LDAPException:
        return ['???' for key in keys]
    msg_id = c.search('dc=univ-lyon1,dc=fr',
                      '(|'
                      + ''.join('(sAMAccountName=%s)' % student_id.lower()
                                for student_id in student_ids)
                      + ')',
                      ldap3.SEARCH_SCOPE_WHOLE_SUBTREE,
                      time_limit = 1,
                      attributes = keys)
    a = c.get_response(msg_id)[0]
    del c
    del s
    d = {}
    if a:
        for i in a:
           if 'attributes' in i:
               i = i['attributes']
               d[i['sAMAccountName'][0].lower()] = tuple(
                   i.get(key,('???',))[0]
                   for key in keys[1:])
    return d

def execute(state, dummy_plugin, dummy_argument):
    if not ldap_is_here:
        return ''

    answered_other = state.form.get('answered_other')
    if answered_other in student.students:
        the_student = student.students[answered_other]
    else:
        the_student = state.student

    if 'mail' in the_student.informations:
        return ''

    if execute.first_time:
        # Request data for all the students
        logins = student.students
        execute.first_time = False
    else:
        # Request data only for the new student
        logins = (the_student.filename,)
    all_infos = get_info(state, logins)
    for login in logins:
        a_student = student.students[login]
        if a_student.filename in all_infos:
            data = all_infos[a_student.filename]
        else:
            data = ('???', '???', '???')

        infos = a_student.informations
        (infos['surname'], infos['firstname'], infos['mail']) = data
            
    return ''
execute.first_time = True

if __name__ == "__main__":
    print(get_info(['thierry.excoffier']))
    print(get_info(['thierry.excofier']))
