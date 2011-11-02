#!/usr/bin/env python
#    QUENLIG: Questionnaire en ligne (Online interactive tutorial)
#    Copyright (C) 2005-2011 Thierry EXCOFFIER, Universite Claude Bernard
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
#

"""Replay on server 6666 the Unix question as answered
by the students with the server 9999.

This is done in order to simulate exactly the reality, except for:
  - The data files (CSS, images and so on)
  - The proxy usage

Script arguments are:
  - The number of simulated students (50)
  - The time slice for statistics (60 seconds)
  - An existing session name (not modified)
  - Acceleration of the reality (1)
  - Compute server profiling, if 0 NO profiling,
    else it give the number of retrieved URL before exiting
  - The port number
  - The name of the created session
  - If the argument is 'histogram' then store histogram


It prints the mean page load time and the number of loaded page.
"""

import os
import urllib2
import time
import re
import sys
import cgi
import thread

for i in ('http_proxy', 'https_proxy'):
    if os.environ.has_key(i):
        del os.environ[i]

# Is this thread safe ?
class Stats:
    def __init__(self):
        self.nr = 0
        self.sum = 0
    def add(self, value):
        self.sum += value
        self.nr += 1
    def reset(self):
        a = str(self)
        self.__init__()
        return a
    def __str__(self):
        if self.nr:
            return "%f %d" % (self.sum/self.nr, self.nr)
        else:
            return "0 0"

def init_student_rights(name):
    os.mkdir(os.path.join('Students', name, 'Logs', 'Default'))
    f = open(os.path.join('Students', name, 'Logs', 'Default', 'acls'), 'w')
    # If questions are not exactly the same than the answered question,
    # You must allows to answer any question because some
    # preriquise have not been answered.
    # It as also the case if a question use a random seed.
    # ======== question_answerable_any =========
    f.write('''{
    'answered_other': ['!executable'],
    'statmenu_rank': ['executable'],
    'answers': ['!executable'],
    'action_help': ['!executable'],
    'answered': ['!executable'],
    'real_name': ['!executable'],
    'histogramgood': ['executable'],
    'questions_all': ['executable'],
    }''')
    f.close()
    
class Server:
    def __init__(self, port, questions, profiling, name):
        self.port = port
        self.name = name
        self.stats = Stats()
        self.clean()
        if profiling:
            profiling = 'nr-requests-served %s' % profiling
        else:
            profiling = ''
        os.system(
            './main.py %s stop ;' % name +
            'rm -r Students/%s || true ; ' % name +
            './main.py %s create %s %d begin-date "1:1 1/1/1970" end-date "1:1 1/1/2020" url "http://localhost:%d/" ;' % (
            name, questions, port, port)
            )
        init_student_rights(name)
        os.system('./main.py %s %s start 2>Students/%s/logs >&2 &' % (
            name, profiling, name)
            )
        
        # Wait server start
        while True:
            try:
                urllib2.urlopen("http://localhost:%d/" % self.port).close()
                break
            except urllib2.URLError:
                time.sleep(0.4)

    def stop(self):
        os.system('./main.py %s stop' % self.name)
        self.clean()

    def clean(self):
        # os.system("rm -r Students/%s/Logs || true" % self.name)
        pass

    def get(self, url, trace=False):
        if trace:
            print 'GET', url
        start = time.time()
        f = urllib2.urlopen(url)
        p = f.read()
        f.close()
        if True or trace:
            print 'GET %6.3f %s' % (time.time() - start, url)
        self.stats.add(time.time() - start)
        return p

def unquote(s):
    "Anybody has a better idea for this complex function?"
    return '\\'.join([w.replace("\\r","\r").replace("\\n","\n").replace("\\a", "") for w in s.split('\\\\')])

class Action:
    def __init__(self, line):
        line = line.split('')
        if len(line) == 5:
            del line[2] # Seed in the old logs format
        self.question = line[0]
        self.date = float(line[1])
        self.action = line[2]
        self.value = unquote(line[3][:-1])

    def __str__(self):
        return "%s;%f;%s;%s" % (
            self.question, self.date, self.action, self.value)

class Student:
    """Read real student data and replay it.
    Memorize the time to receive the page."""
    def __init__(self, server, student_log, student_name):
        self.server = server
        self.student_log = student_log
        self.student_name = student_name
        self.index = 0
        self.date = None
        self.base = "http://localhost:%d/%s" % (
            self.server.port, self.student_name)
        self.get('')
        self.get('?questions_all=all')

    def get_action(self):
        if self.index == len(self.student_log):
            return None
            
        action = Action(self.student_log[self.index])
        self.index += 1

        return action

    def get(self, url, trace=False):
        page = self.server.get(self.base + url, trace)
        if page.find('<base href='):
            self.base = re.sub('(?s).*<base href="', '', page)
            self.base = re.sub('(?s)".*', '', self.base)
        else:
            sys.stderr.write("Problem in the page\n")
        return page

    def do_an_action(self):
        action = self.get_action()
        if action == None:
            return
        if False and self.date:
            if action.date - self.date < 3600:
                time.sleep((action.date - self.date)/time_acceleration)
        self.date = action.date
        if action.action == 'asked':
            self.get('?question=%s' % cgi.urllib.quote(action.question))
        elif action.action == 'good' or action.action == 'bad':
            self.get('?question_answer=%s' % cgi.urllib.quote(action.value).replace('/','%2F'))
        elif action.action == 'indice':
            self.get('?question_indice=1')
        elif action.action == 'comment':
            self.get('?comment=%s#' % cgi.urllib.quote(action.value))
        elif action.action == 'None':            
            pass
        else:
            pass
            # print action

    def do_all_actions(self):
        while self.index != len(self.student_log):
            self.do_an_action()

def simulate_client(server, logs, name):
    Student(server, logs, name).do_all_actions()
    threads.pop()

try:
    port = int(sys.argv[6])
except:
    port = 6666

sessionname = sys.argv[3]
dirname = os.path.join('Students', sessionname, 'Logs')

f = open(os.path.join('Students', sessionname, 'questions'), 'r')
questiondir = f.read()
f.close()

server = Server(port, questiondir, int(sys.argv[5]), sys.argv[7])

histogram = True
try:
    if sys.argv[8] == 'histogram':
        histogram = True    
except:
    pass

try:
    logs = []
    for filename in os.listdir(dirname):
        try:
            f = open(os.path.join(dirname, filename, 'log'), 'r')
            logs.append( f.readlines() )
            f.close()
        except IOError:
            pass

    nr_students = int(sys.argv[1])
    time_slice = int(sys.argv[2])
    time_acceleration = int(sys.argv[4])

    if histogram:
        user = Student(server, '', 'guestme')
        histogram = open('xxx.histogram', 'w')

    threads = []
    for i in range(nr_students):
        threads.append(i)
        thread.start_new_thread(simulate_client,(server,
                                                 logs[i%len(logs)],
                                                 'guest%d' % i)
                                                 )
        time.sleep(0.1)

    i = 0
    while threads:
        time.sleep(time_slice)
        print i, server.stats.reset()
        i += time_slice
        if histogram:
            p = user.get('?histogramgood=1')
            p = re.sub('(?s).*<pre>', '',p)
            p = re.sub('(?s)</pre>.*', '',p)
            histogram.write(p + '\n')
            histogram.flush()

finally:
    if histogram:
        histogram.close()
    server.stop()


