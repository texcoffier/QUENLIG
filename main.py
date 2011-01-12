#!/usr/bin/env python

#    QUENLIG: Questionnaire en ligne (Online interactive tutorial)
#    Copyright (C) 2005-2007 Thierry EXCOFFIER, Universite Claude Bernard
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

import os
import sys
import statistics
import time
import configuration
import questions
import server
import socket
import utilities

# To make casauth work we should not use a proxy
# And the mailcheck speed-down shell startup.
for i in ('http_proxy', 'https_proxy', 'MAIL', 'MAILCHECK'):
    if os.environ.has_key(i):
        del os.environ[i]

def search_command(command, comment):
    f = os.popen('which %s' % command, 'r')
    if f.read() == '':
        sys.stderr.write('WARNING: "%s" not found. %s\n' % (command, comment))
    f.close()

def mkdir(name):
    if not os.path.exists(name):
        os.mkdir(name)

def date_to_seconds(date):
    return time.mktime( time.strptime(date.strip(), "%H:%M %d/%m/%Y") )

class Session:
    def __init__(self, name):
        self.name = name
        self.cache = {}
        self.nr_requests = 0
        self.percentage_time_for_stat = None
        self.dir = os.path.join('Students', name, '')
    def set_questions_directory(self, dirname):
        if not os.path.exists(dirname):
            sys.stderr.write(dirname + ' question directory does not exists\n')
            sys.exit(1)
        utilities.write(self.dir + 'questions', dirname)
    def set_port(self, port):
        utilities.write(self.dir + 'port', port)
    def set_begin_date(self, date, overwrite=True):
        utilities.write(self.dir + 'begin_date', date, overwrite)
    def set_end_date(self, date, overwrite=True):
        utilities.write(self.dir + 'end_date', date, overwrite)
    def set_url(self, url, overwrite=True):
        utilities.write(self.dir + 'url', url.strip('/'), overwrite)

    def init(self):
        if questions.questions:
            return

        configuration.session = self
        
        try:
            configuration.port = int(utilities.read(self.dir + 'port'))
        except ValueError:
            sys.stderr.write(
                "You should 'create' the session before starting it\n")
            sys.exit(0)
        configuration.dates = [
            date_to_seconds(utilities.read(self.dir + 'begin_date')),
            date_to_seconds(utilities.read(self.dir + 'end_date')),
            ]
        if self.percentage_time_for_stat:
            configuration.statistics_cpu_allocation = \
            self.percentage_time_for_stat
        configuration.questions = utilities.read(self.dir + 'questions')
        configuration.html = os.path.join(self.dir, "HTML")

        configuration.url = utilities.read(self.dir + 'url')
        if configuration.url == '':
            configuration.url = 'http://%s:%d' % (socket.getfqdn(),
                                                  configuration.port)
        url = configuration.url.split('/')
        if len(url) == 3:
            configuration.prefix = ''
        else:
            configuration.prefix = '/'.join(url[3:]) + '/'

        # Create __init__.py in the question dir.
        i = os.path.join(configuration.questions, "__init__.py")
        if not os.path.exists(i):
            open(i, "w").close()

        questions.modules = utilities.load_directory(configuration.questions)
        questions.sort_questions()

    def question_stats(self):
        self.init()
        print
        print len(questions.questions), 'questions'
        d = {}
        for q in questions.questions.itervalues():
            for t in q.tests:
                try:
                    name = t.__name__ + '!!!'
                except:
                    name = t.__class__.__name__
                if name not in d:
                    d[name] = 0
                d[name] += 1
        t = list(d.iterkeys())
        t.sort()
        n = 0
        for k in t:
            print '%40s %d' % (k, d[k])
            n += d[k]
        print n, 'tests'

    def start(self):
        self.init()
        utilities.write(self.dir + 'pid', str(os.getpid()))
        utilities.write(self.dir + 'hostname', socket.gethostname())
        if os.path.isdir(configuration.html):
            os.system('cd %s ; make' % configuration.html)
        os.chdir(self.dir)
        try:
            server.run(self.nr_requests, self.cache)
        except KeyboardInterrupt:
            sys.stderr.write("A signal has stopped the server\n")
        os.chdir(configuration.root)
        os.remove(self.dir + 'pid')

    def stop(self):
        if utilities.read(self.dir + 'hostname') != socket.gethostname():
            sys.stderr.write("Can't stop server, does not run on this host\n")
            return
        pid = utilities.read(self.dir + 'pid')
        if pid != '':
            try:
                os.kill( int(pid), 15)
            except OSError:
                pass
            os.remove(self.dir + 'pid')

    def plot(self):
        self.init()
        os.chdir(self.dir)
        utilities.write(os.path.join('HTML', 'simple.html'),
                        statistics.html_simple(None))
        statistics.update_stats()
        statistics.graph_dot()
        statistics.graph2_dot()
        sys.exit(0)

    def display_no_more_valid_answers(self):
        self.init()
        os.chdir(self.dir)
        statistics.display_no_more_valid_answers()
        sys.exit(0)


search_command('ppmtogif',
               'So no the graphical question map for the student (netpbm)')
search_command('highlight',
               'So no Python source highlighting for the author')
search_command('weblint',
               'So no HTML testing in the regression tests')
search_command('xvcg',
               'So some picture of the question graph are not computed')
search_command('dot',
               'So some picture of the question graph are not computed')
search_command('hotshot2calltree',
               'No graphic profiling (needs package kcachegrind-converters)')
search_command('kcachegrind',
               'No graphic profiling')

# Analyse command line options

name = sys.argv[0]
args = sys.argv[1:]
args.reverse()

try:
    session = Session(args.pop())
except IndexError:
    sys.stderr.write(name + """ the_session_name action1 action2 ...

SET PERSISTENT SESSION OPTIONS: 
    'create TheQuestionDirectory ThePortNumber'
        Create the session. For example: 'create Questions/unix 9999'
    'begin-date "%%H:%%M %%d/%%m/%%Y"'
        Set the date after which the students can answers questions.
        For example: 'create begin-date "09:00 1/1/2005"'
    'end-date "%%H:%%M %%d/%%m/%%Y"'
        Set the date after which the students can NOT answers questions.
    'admin login_name'
        Give to 'login_name' the administrator role
    'url public_URL_of_the_server'
        Use it if there is URL rewrite. For example, server run on :
           http://intranet.univ.org:7777/
        And students have only access to another server:
           http://www.univ.org/quenlig
        Apache configuration example:
           RewriteEngine On
           RewriteRule ^/quenlig(.*) http://intranet.univ.org:7777/$1 [P]

ACTIONS:
    'start'
        Start the server
    'stop'
        Stop the server
    'plot'
        Creation of all the plots related to this session
    'problems'
        Show the good answers given by the students that are no more
        valid because the question testing was modified.
SET TEMPORARY SESSION OPTIONS:
     'nocache'
         Does not cache HTML, CSS, PS, ... files
     'nr-requests-served #requests'
         The server stops after the number of request indicated
     'percentage-time-for-stat'
         Percentage of the time used by the server to compute stats.
         The default is %s%%
""" % configuration.statistics_cpu_allocation)

    if os.path.isdir('Students'):
        format = "%-12s %-5s %5s@%-8s %-17s %16s %s\n"

        sys.stderr.write(format % (
            "SESSION NAME", "PORT", "PID", "HOSTNAME", "QUESTIONS BASE",
            "START DATE", "DURATION"))

        for n in os.listdir('Students'):
            fn = os.path.join('Students', n)
            if not os.path.isdir(fn):
                continue
            begin_date =utilities.read(os.path.join('Students',n,'begin_date'))
            end_date = utilities.read(os.path.join('Students', n, 'end_date'))
            duration = date_to_seconds(end_date) - date_to_seconds(begin_date)
            duration = utilities.duration(int(duration))
            sys.stderr.write(format % (
                n,
                utilities.read(os.path.join('Students', n, 'port')),
                utilities.read(os.path.join('Students', n, 'pid')),
                utilities.read(os.path.join('Students', n, 'hostname')),
                utilities.read(os.path.join('Students', n, 'questions')),
                begin_date,
                duration,
                ))    
    sys.exit(1)

mkdir('Students')
mkdir(session.dir)
session.set_begin_date('1:1 1/1/1970', overwrite=False)
session.set_end_date('3:3 3/3/2033', overwrite=False)    
mkdir(session.dir + 'Logs' )
mkdir(session.dir + 'HTML' )
configuration.root = os.getcwd()

configuration.version = os.path.basename(os.getcwd())

import plugins
plugins.init()

if __name__ == "__main__":
    if len(args) == 0:
        sys.stderr.write("""
    You indicate no action to do about your session named '%s'

    Run without parameters to see the help.

    Or create and run session, for example :

    main.py unix2007 create Questions/unix 55555
    main.py unix2007 admin  guestadmin
    main.py unix2007 start
    """ % session.name )
        sys.exit(1)


    while args:
        action = args.pop()
        if action == 'start':
            session.start()
        elif action == 'stop':
            session.stop()
        elif action == 'nocache':
            session.cache = None
        elif action == 'plot':
            session.plot()
        elif action == 'problems':
            session.display_no_more_valid_answers()
        elif action == 'nr-requests-served':
            session.nr_requests = int(args.pop())
        elif action == 'percentage-time-for-stat':
            session.percentage_time_for_stat = int(args.pop())
        elif action == 'begin-date':
            session.set_begin_date(args.pop())
        elif action == 'end-date':
            session.set_end_date(args.pop())
        elif action == 'url':
            session.set_url(args.pop())
        elif action == 'create':
            session.set_questions_directory(args.pop())
            session.set_port(args.pop())
        elif action == 'admin':
            user = os.path.join(session.dir, 'Logs', args.pop())
            mkdir(user)
            user = os.path.join(user, 'roles')
            utilities.write(user, "['Default','Teacher']\n")
        elif action == 'question-stats':
            session.question_stats()
        else:
            sys.stderr.write("""Unknown action : %s\n""" % action)
            sys.exit(2)

