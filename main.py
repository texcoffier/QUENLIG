#!/usr/bin/env python3

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
import time
import socket
import re

# Make it a package
__package__ = "QUENLIG"
sys.path.insert(0, os.path.sep.join(os.getcwd().split(os.path.sep)[:-1]))
sys.modules["QUENLIG"] = __import__(os.getcwd().split(os.path.sep)[-1])
sys.path.pop(0)
sys.modules["QUENLIG"].__name__ = 'QUENLIG'

from . import statistics
from . import configuration
from . import questions
from . import server
from . import utilities

# To make casauth work we should not use a proxy
# And the mailcheck speed-down shell startup.
for i in ('http_proxy', 'https_proxy', 'MAIL', 'MAILCHECK'):
    if i in os.environ:
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
        self.only_from = ""
        self.dir = os.path.join('Students', name, '')
    def set_questions_directory(self, dirname):
        if not os.path.exists(dirname):
            sys.stderr.write(dirname + ' question directory does not exists\n')
            sys.exit(1)
        utilities.write(self.dir + 'questions', dirname)
    def set_port(self, port):
        utilities.write(self.dir + 'port', port)
    def set_only_from(self, only_from):
        utilities.write(self.dir + 'only_from', only_from)
    def set_url(self, url, overwrite=True):
        utilities.write(self.dir + 'url', url, overwrite)

    def set_option(self, option, values):
        for plugin in plugins.Plugin.plugins_dict.values():
            if plugin["", "option_name"] == option:
                if plugin["", "option_default"] is None:
                    value = None
                else:
                    value = values.pop()
                utilities.write(self.dir + option, value, overwrite=True)
                return True

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
        if self.percentage_time_for_stat:
            configuration.statistics_cpu_allocation = \
            self.percentage_time_for_stat
        configuration.questions = utilities.read(self.dir + 'questions')
        configuration.html = os.path.join(self.dir, "HTML")

        configuration.url = utilities.read(self.dir + 'url')
        configuration.only_from = utilities.read(self.dir + 'only_from')
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
        print()
        print(len(questions.questions), 'questions')
        d = {}
        for q in questions.questions.values():
            for t in q.tests:
                try:
                    name = t.__name__ + '!!!'
                except:
                    name = t.__class__.__name__
                if name not in d:
                    d[name] = 0
                d[name] += 1
        t = list(d.keys())
        t.sort()
        n = 0
        for k in t:
            print('%40s %d' % (k, d[k]))
            n += d[k]
        print(n, 'tests')

    def start(self):
        self.init()
        utilities.write(self.dir + 'pid', str(os.getpid()))
        utilities.write(self.dir + 'hostname', socket.gethostname())
        if os.path.isdir(configuration.html):
            sys.stdout.flush()
            sys.stderr.flush()
            os.system('cd %s ; make 2>/dev/null' % configuration.html)
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
        statistics.graph_dot()
        statistics.graph2_dot()
        sys.exit(0)

    def display_no_more_valid_answers(self):
        self.init()
        os.chdir(self.dir)
        statistics.display_no_more_valid_answers()
        sys.exit(0)

    def check_questions(self):
        analysers = set(('Shell', 'P'))
        testers = set(('Contain', 'Start', 'End', 'Expect'))
        top_level = set(('Good',))
        top_level_or_and = set(('Bad', 'Reject', 'Expect'))
        def formate(q, test, text):
            return '%s.py(%s): [%s] %s' % (os.path.sep.join(q.path),
                                           q.name,
                                           test.__class__.__name__,
                                           text)
        
        def warn_me(q, test, danger, top, top_and):
            cname = test.__class__.__name__
            if cname in analysers:
                danger = True
            if cname in top_level and not top:
                return formate(q, test, "must be toplevel test")
            if cname in testers and danger:
                if test.do_canonize:
                    return formate(q, test, "argument is parsed (dangerous)")
            if cname != 'And':
                top_and = False
            if hasattr(test, 'children'):
                for child in test.children:
                    e = warn_me(q, child, danger, False, top_and)
                    if e:
                        return e
                
        print('Check all questions in ' + utilities.read(self.dir + 'questions'))
        self.init()
        os.chdir(self.dir)
        errors = []
        for q in questions.questions.values():
            for t in q.tests:
                e = warn_me(q, t, danger=False, top=True, top_and=True)
                if e:
                   errors.append(e)
        errors.sort()
        print('\n'.join(errors))

if '--silent' not in sys.argv:
    search_command('ppmtogif',
                   'So no the graphical question map for the student (netpbm)')
    search_command('highlight',
                   'So no Python source highlighting for the author')
    search_command('weblint',
                   'So no HTML testing in the regression tests')
    search_command('dot',
                   'So some picture of the question graph are not computed')
    search_command('hotshot2calltree',
                   'No graphic profiling (needs kcachegrind-converters)')
    search_command('kcachegrind',
                   'No graphic profiling')
else:
    questions.silent = True
    sys.argv.remove('--silent')

from . import plugins
plugins.init()

from . import state

class FakeServer:
    headers = {"X-Forwarded-For":'IP?', "User-Agent": 'UI?',
               'accept-language': 'en;fr'}

if 'plugins.html' in sys.argv:
    # These lines are here to create a fake environnement.
    # because the initialisation methods need an environnement to run.
    configuration.url = 'fake'
    class FakeSession:
        name = "fakesession"
    configuration.session = FakeSession
    for i in ('Logs', os.path.join('Logs', 'nostudent')):
        try:
            os.mkdir(i)
        except OSError:
            pass
    s = state.State(FakeServer(), 'noticket', 'nostudent')
    # Now the plugin tree is working
    def display(f, plugin):
        f.write('<tr><td>')
        f.write(plugin.plugin.doc_html())
        f.write('<table class="plugin">')
        for p in plugin.full_content:
            display(f, p)
        f.write('</table>')
        f.write('</tr>')

    def display_TOC(f, plugin):
        if len(plugin.full_content) == 0:
            f.write('<p><a href="#%s">%s</a>' % (
                    plugin.plugin.css_name, plugin.plugin.css_name) )
            return
        if plugin.horizontal:
            colspan = ' colspan="%d"' % len(plugin.full_content)
        else:
            colspan = ''
        f.write('<table class="toc"><tr><th%s><a href="#%s">%s</a>' % (
                colspan, plugin.plugin.css_name, plugin.plugin.css_name))
        if plugin.horizontal:
            f.write('<tr>')
            for p in plugin.full_content:
                f.write('<td>')
                display_TOC(f, p)
            f.write('</tr>')
        else:
            for p in plugin.full_content:
                f.write('<tr><td>')
                display_TOC(f, p)
                f.write('</tr>')
        f.write('</table>')
        
    f = open(os.path.join('Documentation', 'plugins.html'), 'w')
    f.write('''<html>
<meta http-equiv="content-type" content="text/html; charset=UTF-8">
<script src="doc.js"></script>
<body onload="make_style()" onclick="setTimeout('make_style()',100)">
<style>
TR { vertical-align: top; }
BODY { font-family: sans-serif; }
TD.pre { white-space: pre ; }
A { text-decoration: none }
TABLE.plugin TABLE.plugin { padding: 1em; margin-left: auto; margin-right: auto}
TABLE.plugin TD { border: 1px solid black;}
TABLE.attr TD, TABLE.attr TH { background: white ; border: 0px }
TABLE.attr { background: black ; border-spacing: 1px }
TABLE.toc { border: 1px solid black; border-spacing: 0px; margin-top: 1px; margin-bottom: 1px }
TABLE.toc TD, TABLE.toc TH { padding-top: 0px; padding-bottom: 0px; }
TABLE.toc TD P { margin: 0px ; border: 0px; font-size: 80% }
.style { background: #FF8 }

TABLE.attributes { background: black ; border-spacing: 1px }
TABLE.attributes TD, TABLE.attributes TH {  background: white ; border: 0px }

DIV.title {
   background: black ;
   color: white ;
   padding: 0.2em ;
   font-size: 110% ;
}
.bool { background: #888 }
DIV.title A { color: white }
DIV.title A:visited { color: white }
</style>
<h1>Plugins display tree</h1>
Click on plugin names to see the details.
''')
    class FakeServer:
        headers = {'accept-language': 'en', 'User-Agent': ""}
        client_address = '127.0.0.1'
    s.update_state(FakeServer)
    for p in s.roots:
        display_TOC(f, p)

    f.write('<h2>Plugin execution order</h2>')
    for p in s.plugins_list:
        f.write(' <a href="#%s">%s</a>' % (p.plugin.css_name,
                                           p.plugin.css_name))

        

    f.write('''
<h1>Plugin details</h1>
The attributes values are for the english language, all of them
may change in other languages.
<p>
???? indicates a text computed (may be empty) computed by
the plugin and that must be inserted in the page.
<p>
You can click on plugin attributes to see there definition.
''')
    f.write('<table class="plugin">')
    for p in s.roots:
        display(f, p)
    f.write('</table>')

    f.write('''
<h1><a name="plugin_attributes">Plugin Attributes</a></h1>
<table class="attributes">
    ''')
    f.write('<tr><th>Attribute name<th>Default value<th>Documentation</tr>')
    for k in sorted(plugins.Attribute.attributes):
        a = plugins.Attribute.attributes[k]
        if not hasattr(a, 'css_name'):
            f.write(a.doc_html())
    f.write('</table>')

    f.write('''
<h1><a name="plugin_css_attributes">Plugin CSS Attributes</a></h1>
<p>These attributes values are concatened into the CSS file.
<table class="attributes">
    ''')
    f.write('<tr><th>Attribute name<th>CSS name<th>CSS selector<th>Documentation</tr>')
    for k in sorted(plugins.Attribute.attributes):
        a = plugins.Attribute.attributes[k]
        if hasattr(a, 'css_name'):
            f.write(a.doc_html())
    f.write('</table>')
    f.write('&nbsp;<br>'*60)
    f.close()

    tests = []
    for c in questions.__dict__.values():
        try:
            if issubclass(c, questions.TestExpression):
                tests.append(c)
        except TypeError:
            pass

    f = open(os.path.join('Documentation', 'tests.html'), 'w')
    f.write('''<html>
  <script src="doc.js"></script>
  <body onload="make_style()" onclick="setTimeout('make_style()',100)">

<style>
BODY { font-family: sans-serif ; }
PRE { border: 1px solid black ;
margin-width: auto ;
margin-left: 4em ;
margin-top: 0px ;
padding: 0.1em ;
 }

</style>
''')
    tests.sort(key=lambda x: x.__name__)
    def display_tests(t):
        doc = t.__doc__.strip().split('Examples:')
        doc[0] = doc[0].strip('\n ')
        if len(doc) > 1:
            examples = doc[1].strip('\n').split('\n')
            indent = len(examples[0]) - len(examples[0].strip())
            examples = [line[indent:].replace(t.__name__,
                                              '<b>' + t.__name__ + '</b>'
                                              )
                        for line in examples]
            examples = '<pre>' + '\n'.join(examples) + '</pre>'
            examples = re.sub('(#.*)', '<em>\\1</em>', examples)
        else:
            examples = ''
        f.write('<a name="' + t.__name__ + '"><b>' + t.__name__ + '</b></a>: ' + doc[0] + examples)
        for c in tests:
            if c.__bases__[0] == t:
                f.write('<ul>')
                display_tests(c)
                f.write('</ul>')
    display_tests( questions.TestExpression)  
    f.close()

    sys.exit(0)

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
    'only_from IP'
        Only requests directly from this IP are allowed (it can be a proxy)

SET PERSISTENT SESSION OPTIONS FOR PLUGINS:
""")
    for plugin in plugins.Plugin.plugins_dict.values():
        if plugin["", "option_name"] is None:
            continue
        sys.stderr.write("    '%s" % plugin["","option_name"])
        if plugin["","option_default"] is not None:
            sys.stderr.write(" \"%s\"" % plugin["","option_default"])
        sys.stderr.write("'\n\t%s\n" % plugin["","option_help"])

    sys.stderr.write("""ACTIONS:
    'start'
        Start the server
    'stop'
        Stop the server
    'plot'
        Creation of all the plots related to this session
    'problems'
        Show the good answers given by the students that are no more
        valid because the question testing was modified.
    'execute plugin-name'
        The plugin is executed, the output is printed and the program stops
        It is useful for the 'exportcsv' plugin.
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
        format = "%-17s %5s %5s@%-8s %-17s\n"

        sys.stderr.write(format % (
            "SESSION NAME", "PORT", "PID", "HOSTNAME", "QUESTIONS BASE"))

        for n in os.listdir('Students'):
            fn = os.path.join('Students', n)
            if not os.path.isdir(fn):
                continue
            sys.stderr.write(format % (
                n,
                utilities.read(os.path.join('Students', n, 'port')),
                utilities.read(os.path.join('Students', n, 'pid')),
                utilities.read(os.path.join('Students', n, 'hostname')),
                utilities.read(os.path.join('Students', n, 'questions')),
                ))    
    sys.exit(1)

if __name__ == "__main__" and len(args) == 0:
    sys.stderr.write("""
    You indicate no action to do about your session named '%s'

    Run without parameters to see the help.

    Or create and run session, for example :

    main.py unix2007 create Questions/unix 55555
    main.py unix2007 admin  guestadmin
    main.py unix2007 start
    \n""" % session.name )
    sys.exit(1)

    
mkdir('Students')
mkdir(session.dir)
mkdir(session.dir + 'Logs' )
mkdir(session.dir + 'HTML' )
configuration.root = os.getcwd()

if __name__ == "__main__":
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
        elif action == 'url':
            session.set_url(args.pop())
        elif action == 'create':
            session.set_questions_directory(args.pop())
            session.set_port(args.pop())
        elif action == 'only_from':
            session.set_only_from(args.pop())
        elif action == 'admin':
            user = os.path.join(session.dir, 'Logs', args.pop())
            mkdir(user)
            user = os.path.join(user, 'roles')
            from .Plugins.role import role
            x = list(role.default_roles)
            x.sort()
            x.remove('Teacher')
            x.insert(0, 'Teacher')
            utilities.write(
                user, '[' + ','.join("'%s'" % r
                                     for r in x)  + ']')
        elif action == 'check-questions':
            session.check_questions()
        elif action == 'question-stats':
            session.question_stats()
        elif action == 'execute':
            session.init()
            os.chdir(session.dir)
            s = state.State(FakeServer(), "noticket", "Default")
            s.update_state(FakeServer())
            p = s.plugins_dict[args.pop()]
            out = p.plugin.plugin.execute(s, p, '1')
            if isinstance(out, tuple):
                out = out[1]
            else:
                out = p.heart_content
            print(out)
            sys.exit(0)
        elif action == 'profile':
            import cProfile
            session.init()
            os.chdir(session.dir)
            from . import student
            import pstats
            print("\n\n\nLoading students profiling\n\n")
            cProfile.run('state.State(FakeServer(), "noticket", "Default")',
                         'xxx.stats')
            p = pstats.Stats('xxx.stats')
            p.sort_stats('cumulative').print_stats()

            print("\n\n\nStudent statistics profiling\n\n")
            cProfile.run("statistics.question_stats()", 'xxx2.stats')
            p = pstats.Stats('xxx2.stats')
            p.sort_stats('cumulative').print_stats()

            sys.exit(0)
        elif action == 'stop-loading':
            # DO NOT USE WHEN THE SESSION IS NOT FULLY TERMINATED.
            
            # Usage example, to stop loading after one hour of student time.
            # stop-loading 'lambda s:s.time_searching()+s.time_after()>3600'
            # I use it to know student rank after one hour of work

            # To have a session snapshot at a fixed time
            # stop-loading "lambda s:s.logs and s.logs[-1][0] > 1393400000"

            # To display competence grades when the student reach 5
            # questions answered correctly:
            # stop-loading "lambda s:s.number_of_good_answers() == 5 and (print(1) or True)" execute competence
            from . import student
            student.stop_loading_default = eval(args.pop())
        else:
            if not session.set_option(action, args):
                sys.stderr.write("""Unknown action : %s\n""" % action)
                sys.exit(2)

