#!/usr/bin/env python
# -*- coding: latin-1 -*-
#    QUENLIG: Questionnaire en ligne (Online interactive tutorial)
#    Copyright (C) 2008 Thierry EXCOFFIER, Universite Claude Bernard
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
Launch the script to run the server.
Example of URL to run /bin/sh in the web client :

    http://lirispaj.univ-lyon1.fr:11111/exec=/bin/sh
    

To use unbuffered 'printf' in C :
    setlinebuf(stdout);

if ( 1 )
    printf(...

if ( 1 )
    setlinebuf(stdout),printf(...

"""

url = 'key='
port = 11111

import sys
import subprocess
import thread
import os
import urllib2
import cgi
import utilities
import re
import tempfile
import signal
import socket

def check_configuration():
    f = os.popen('sudo -u nobody echo ok', 'r')
    if f.read() != 'ok\n':
        sys.stderr.write("""Please use the command 'visudo' to add the line:
	
	login_name_of_the_user_running_the_server   ALL=(nobody)   NOPASSWD: ALL
	
	This allow the server to use 'sudo nobody'
	""")
	sys.exit(1)
    f.close()

check_configuration()

def execute(command_line,
	    cpu_limit=1,
	    memory_limit=10000,
	    stdin = None,
	    stdout = None,
	    stderr = subprocess.STDOUT,
	    ):
    """Execute ``safely´´ a program.
    Returns the process handler so it is possible to write to the process
    or read its output.
    By default, the input is stdin and output is stdout.
    Use os.pipe() to communicate to the process.
    """

    directory = tempfile.mkdtemp()

    if re.match('[^-. 0-9a-zA-Z_/]', command_line):
       raise ValueError('Not a valid command line: ' + command_line)
    
    command = ('ulimit -t ' + str(cpu_limit) + '\n' +
	       'ulimit -v ' + str(memory_limit) + '\n' +
	       'cd ' + directory + '\n' +
	       'chmod 777 . 2>/dev/null\n' +
	       'sudo -u nobody ' +  command_line + ' 2>&1\n'
	       )
    f = subprocess.Popen(command,
			 shell = True,
			 stdin = stdin,
			 stdout = stdout,
			 stderr = stderr,
			 )
    f.directory = directory
    return f

head = utilities.read('interactive.html')

def send(output, text):
        output.write('<script>char(' + repr(text) + ')</script>')
        output.flush()

def html(interactive):
    input = interactive.pipe_in
    output = interactive.output
    try:
        while True:
            send(output, input.readline())
    except socket.error:
        interactive.stop()

class Interactive:
    def __init__(self, command, output):
        (self.pipe_in, self.pipe_out) = os.pipe()
        self.pipe_in = os.fdopen(self.pipe_in, 'r')
        self.process = execute(command,
			       stdin = subprocess.PIPE,
			       stdout = self.pipe_out,
			       )
        self.output = output
        self.pid = self.process.pid
        thread.start_new_thread(html, (self,))
        
    def send(self, string):
        string = urllib2.unquote(string)
        self.process.stdin.write(string + '\n')
        self.process.stdin.flush()

    def stop(self):
        os.kill(self.pid, signal.SIGKILL)
        self.output.close()
        os.system(
        'sudo -u nobody chmod -R 777 '+self.process.directory+' 2>/dev/null\n'+
        'rm -r ' + self.process.directory)


if __name__ == "__main__":
    class NoFile:
        closed = True
        def close(self):
            pass

    import BaseHTTPServer
    class MyRequestBroker(BaseHTTPServer.BaseHTTPRequestHandler):
        processes = {}
        
        def do_GET(self):
            print self.path
            if self.path.startswith('/exec='):
                process = MyRequestBroker.application = Interactive(
                    urllib2.unquote(self.path.split('/exec=')[1]),
                    self.wfile)
                MyRequestBroker.processes[process.pid] = process

                self.send_response(200)
                self.send_header('Content-Type', 'text/html')
                self.send_header('Cache-Control', 'max-age=0')
                self.send_header('Cache-Control', 'private')
                self.send_header('Cache-Control', 'no-store')
                self.end_headers()
                self.wfile.write(head % ('/' + url + str(process.pid) + '/'))
                self.wfile.flush()
                self.wfile = NoFile()
            elif url in self.path:
                code = self.path.split(url)[1]
                pid, code = code.split('/',1)
                try:
                    MyRequestBroker.processes[int(pid)].send( code )
                except IOError:
                    MyRequestBroker.processes[int(pid)].stop()
                    del MyRequestBroker.processes[int(pid)]
                except KeyError:
                    pass


    server = BaseHTTPServer.HTTPServer(("0.0.0.0", port), MyRequestBroker)
    server.serve_forever()

    
        

    
