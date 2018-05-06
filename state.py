#    QUENLIG: Questionnaire en ligne (Online interactive tutorial)
#    Copyright (C) 2005-2018 Thierry EXCOFFIER, Universite Claude Bernard
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

import cgi
import urllib.request, urllib.parse, urllib.error
import time
import re
import sys
import os
import threading
from . import casauth
from . import questions
from . import student
from . import statistics
from . import configuration
from . import plugins
from . import utilities

###############################################################################
# Information filling 
###############################################################################

def client_ip(server):
    try:
        # In cas of proxy
        ip = server.headers["X-Forwarded-For"]
        try:
            # Take the first IP
            return ip.split(",")[0]
        except IndexError:
            return ip
    except (KeyError, AttributeError):
        return server.client_address[0]

def the_service(server):
    path = server.path.split('/')
    if len(path) < 3:
        return configuration.url
    else:
        if path[-1] == '':
            return configuration.url
        path[-1] = re.sub('&ticket=[^&]*','',path[-1])
        return configuration.url + '/' + '/'.join(path[-2:])

###############################################################################
# Plugins for a state 
###############################################################################

class StatePlugin:
    def __init__(self, plugin, state):
        self.plugin = plugin
        self.state = state
        self.value = None
        self.heart_content = None
        self.current_acls = {'executable':True} # Erased with the acls loading
        self.update_attributes()

    def update_attributes(self):
        # Should be done each time an attribute is modified
        for attribute in plugins.Attribute.attributes.values():
            self.__dict__[attribute.name] = self.plugin[self.state.localization,
                                                        attribute.name]

    def priority_compute(self, attribute):
        attribute_int = attribute + '_int'
        if isinstance(self.__dict__[attribute], int):
            self.__dict__[attribute_int] = self.__dict__[attribute]
            return
        try:
            after= self.state.plugins_dict[self.__dict__[attribute].strip('-')]
        except KeyError:
            raise ValueError(self.plugin.css_name
                             + ' use non existent ' + self.__dict__[attribute])
        after.priority_compute(attribute)
        if self.__dict__[attribute][0] == '-':
            self.__dict__[attribute_int] = after.__dict__[attribute_int] - 1
        else:
            self.__dict__[attribute_int] = after.__dict__[attribute_int] + 1
        if self.container == None:
            self.container = after.container

    def css(self):
        s = []
        for a in plugins.Attribute.attributes.values():
            s.append( a.css(self.plugin.css_name, self.__dict__[a.name]) )
        for line in self.css_attributes:
            if line.startswith('//'):
                s.append( "DIV.heartcontent .%s %s" %(self.plugin.css_name,
                                                      line[2:]))
            elif line.startswith('/'):
                s.append( line[1:] )
            else:
                if not line.startswith(':'):
                    line = ' ' + line
                s.append( "DIV.%s%s" % (self.plugin.css_name, line) )
        return '\n'.join([line for line in s if line != ''])

    def __iter__(self):
        yield self
        for c in self.content:
            yield c

    def boxed(self):
        return self.content_is_title or self.title

    def __repr__(self):
        try:
            full_content = ' '.join([p.plugin.css_name
                                     for p in self.full_content])
        except AttributeError:
            full_content = '[NULL]'
        try:
            content = ' '.join([p.plugin.css_name for p in self.content])
        except AttributeError:
            content = '[NULL]'
        return 'StatePlugin(%s,%s,%s,%s,%s,\n\t%s\n\t%s)' % (
            self.plugin.css_name,
            self.priority_display_int, self.priority_execute_int,
            self.container, self.current_acls, full_content, content)

        

###############################################################################
# 
###############################################################################

class State(object):
    def __init__(self, server, ticket, student_name):
        self.student = self.student_real = student.student(student_name)
        self.current_role = self.role_real = 'Student'
        self.old_role = ''
        self.need_update_login = True
        self.need_update_language = True
        self.need_update_plugin = True
        self.ticket = ticket
        statistics.forget_stats()
        self.history = []
        self.client_ip = None
        self.client_browser = None
        self.option = None
        self.time_creation = time.time()
        self.lang = ''

    def update_language(self, server):
        self.lang = lang = server.headers.get('accept-language','')
        lang = []
        lang_normalized = self.lang.lower().replace(';',',').replace('-','_')
        lang_normalized += ',fr'
        for language in lang_normalized.split(','):
            language = language.split("_")[0]
            if len(language) != 2:
                continue
            if language not in lang:
                # XXX Should test if the translation exists
                lang.append(language)
        self.localization = tuple(lang)

    def init_option(self, plugin):
        option = plugin.plugin[self.localization, "option_name"]
        if option:
            if os.path.exists(option):
                plugin.option = utilities.read(option)
            else:
                plugin.option = plugin.plugin[self.localization,
                                            "option_default"]
            plugin.option_set(plugin, plugin.option)
                
    def update_plugins(self):
        self.plugins_dict = {}
        for plugin in plugins.Plugin.plugins_dict.values():
            self.plugins_dict[plugin.css_name] = StatePlugin(plugin, self)

        # Compute display priority and create 'container' attribute

        for plugin in self.plugins_dict.values():
            plugin.priority_compute('priority_display')

        # Create plugin tree
        
        for plugin in self.plugins_dict.values():
            plugin.full_content = []

        self.roots = []
        for plugin in self.plugins_dict.values():
            container = plugin.container
            if container == None:
                self.roots.append(plugin)
                continue
            self.plugins_dict[container].full_content.append(plugin)

        # Compute default 'execute_priority' from 'display_priority'
##        for root in self.roots:
##            for plugin in root:
##                if plugin.priority_execute == None:
##                    plugin.priority_execute = plugin.priority_display_int

        for plugin in self.plugins_dict.values():
            plugin.priority_compute('priority_execute')
            if plugin.link_to_self:
                plugin.link = '?' + plugin.plugin.css_name + '=1'

        self.plugins_list = list(self.plugins_dict.values())
        self.plugins_list.sort(key = lambda x: (x.priority_execute_int,
                                                x.plugin.css_name
                                            ))


        for plugin in self.plugins_list:
            self.init_option(plugin)
            plugin.full_content.sort(key = lambda x:x.priority_display_int)

        self.roots.sort(key = lambda x:x.priority_display_int)


    def debug_acls(self):
        a = []
        for p in self.plugins_list:
            if p.current_acls != {}:
                a.append((p.plugin.css_name, str(p.current_acls)))
        a.sort()
        return repr(a)

    def dump(self):
        t = [' DUMP'*10]
        for plugin in self.plugins_list:
            t.append(repr(plugin))
        t.append('------------------------------')
        t.append(student.dump())
        t = '\n'.join(t)
        sys.stderr.write(t + '\n%d\n' % hash(t) )

    # The user call the service with a different name (via an apache proxy)
    # Must be called on each page loading to have no problems.
    def update_login(self, server):
        self.time_creation = time.time()

        login = False
        
        new_client_ip = client_ip(server)
        if self.client_ip != new_client_ip:
            login = True
        self.client_ip = new_client_ip

        new_client_browser = server.headers["User-Agent"]
        if self.client_browser != new_client_browser:
            login = True
        self.client_browser = new_client_browser
        
        self.url_base = configuration.url # the_service(server)

        if login:
            self.student.login(self.client_ip + " " + self.client_browser)
        
    def ticket_valid(self, server):
        if time.time() - self.time_creation > configuration.timeout:
            return False
        if self.client_ip != client_ip(server):
            return False
        if self.client_browser != server.headers["User-Agent"]:
            return False
        return True

    def analyse_form(self, form):
        self.form = {}
        for k, v in form.items():
            k = k.split('.')[0]
            if '$' in k: # Manage the case {{{$key}}} in questions
                k, name = k.split("$", 1)
                v = name + '=' + v
            if k in self.form:
                v = self.form[k] + '\n' + v
            self.form[k] = v

        if self.form["number"] == None:
            self.form["number"] = str(len(self.history) - 1)

        try:
            h = self.history[int(self.form["number"])]
            if h:
                self.question = questions.questions[h]
            else:
                self.question = None
        except IndexError:
            self.question = None

        if form.get("question", ""):
            if self.form["question"] == "None":
                self.question = None
            else:
                self.question = questions.questions.get(self.form["question"],
                                                        None)

        sort_column = form.get("sort_column", "").split(' ')
        if len(sort_column) == 2:            
            self.plugins_dict[sort_column[1]].sort_column = int(sort_column[0])

    def execute(self, form):
        self.analyse_form(form)

        self.url_base_full = "%s/%s/%d/" % (self.url_base,
                                            urllib.parse.quote(self.ticket),
                                            len(self.history))

        self.full_page = "No presentation plugin"
        for plugin in self.plugins_list:
            plugin.heart_content = None
            # Use this syntax because it is the 'role' and 'acls' plugins
            # that are initialising the good 'acls' value
            if not plugin.current_acls['executable']:
                plugin.value_title = None
                plugin.value = None
                continue
            plugin.value_title = ''

            # Dans ACLS le plugin content est mis a jours
            plugin_argument = self.form.get(plugin.plugin.css_name, None)
            try:
                v = plugin.execute(self, plugin, plugin_argument)
                # print plugin, plugin_argument, v
            except:
                import traceback
                v = '<br>'.join([cgi.escape(str(i))
                                 for i in (
                                     traceback.format_tb(sys.exc_info()[2])
                                     + [sys.exc_info()[0]]
                                     + [sys.exc_info()[1]]
                                                         )
                                 ])
                if configuration.teacher_mail:
                    configuration.sendmail(
                        configuration.teacher_mail,
                        configuration.teacher_mail,
                        "QUENLIG bug {} {}".format(
                                        configuration.session.name,
                                        self.student.filename),
                        repr(form) + '\n\n'
                        + ''.join([str(i)
                                    for i in (
                                        traceback.format_tb(sys.exc_info()[2])
                                        + [sys.exc_info()[0]]
                                        + [sys.exc_info()[1]]
                                    )]))
                    print("sendmail end")
                print('*'*80, v)
                v = '<div style="font-size:70%;text-align:left;position:relative;background:#FBB">' + v + '</div>'
                
            if plugin.content_is_title:
                plugin.value_title = v
                plugin.value = None
            else:
                plugin.value = v
            if isinstance(plugin.value, tuple):
                return plugin.value

        if self.question:
            self.history.append(self.question.name)
        else:
            self.history.append(None)
        return 'text/html', self.full_page

    def close(self):
        self.old_role = None
        del states[self.ticket]

    def update_state(self, server):
        self.server = server # To retrieve POST data
        if self.lang != server.headers.get('accept-language',''):
            self.old_role = ''
            self.need_update_language = True
            self.need_update_plugin = True
        if self.need_update_login:
            self.update_login(server)
            self.need_update_login = False
        if self.need_update_language:
            self.update_language(server)
            self.need_update_language = False
        if self.need_update_plugin:
            self.update_plugins()
            self.need_update_plugin = False

    def not_threaded(self, form):
        for plugin in plugins.Plugin.plugins_dict.values():
            if plugin['fr','not_threaded'] and form.get(plugin.css_name, None):
                return True

    def lock(self, form):
        if self.not_threaded(form):
            for s in student.students.values():
                while s.lock.locked():
                    time.sleep(0.1)
            # All page loading are terminated.
            self.to_unlock = state_lock
            self.threaded_run = False
        else:
            self.to_unlock = self.student.lock
            self.student.lock.acquire()
            state_lock.release()
            self.threaded_run = True

    def release(self):
        self.to_unlock.release()

    def steal_identity(self, students, answer=None, rand=None):
        """It will not iterate on locked student in order to avoid deadlock"""
        for student in students:
            if student.lock.acquire(False):
                save = student.steal_enter(self, answer, rand)
                try:
                    yield student
                finally:
                    student.steal_exit(self, answer, rand, save)
                    student.lock.release()

states = {}

def get_state_(server, ticket):
    if (configuration.only_from
        and server.client_address[0] != configuration.only_from):
        return None

    service = urllib.parse.quote(the_service(server))

    if ticket == "":
        print('No ticket, redirect to authentication service')
        casauth.redirect(server, service)
        return None

    if ticket.startswith("guest"):
        if ticket in states:
            if not states[ticket].ticket_valid(server):
                states[ticket].need_update_login = True
        else:
            print('New guest ticket for', ticket)
            student_name = ticket
            states[ticket] = State(server, ticket, student_name)
        return states[ticket]

    if ticket in states: # The ticket is known
        if states[ticket].ticket_valid(server): # The ticket is valid
            return states[ticket]
        print('Ticket no more valid (too old or other changes), forget it.')
        casauth.redirect(server, service)
        return None

    print('Ticket unknown:', ticket)
    try:
        student_name = casauth.get_name(ticket, service)
    except IOError:
        print('Invalid ticket, ask a new one')
        casauth.redirect(server, service)
        return None
    
    if getattr(plugins.Plugin.plugins_dict['role'], 'single_session', False):
        # Search if it is a new ticket for an existing student
        for s in states.values():
            if s.student.filename == student_name:
                print('Affect the new ticket to an existing session.')
                del states[s.ticket]
                states[ticket] = s
                s.ticket = ticket
                s.need_update_login = True
                return s

    print('Session created for ticket', ticket)
    
    states[ticket] = State(server, ticket, student_name)
    return states[ticket]


state_lock = threading.Lock()

def get_state(server, ticket, form):
    state_lock.acquire()
    try:
        s = get_state_(server, ticket)
        if s is None:
            state_lock.release()
            return s
    except:
        state_lock.release()
        raise

    s.lock(form) # May release state_lock
    s.start = time.time()
    return s
