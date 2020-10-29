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

import socket
import http.server
import socketserver
import time
import html
import urllib.request, urllib.parse, urllib.error
import os
import sys
from . import state
from . import configuration
from . import utilities
from . import statistics

cache = None # Do not cache files
cache = {}   # Allow file caching

do_not_cache = set() # Files to not cache

def html_time(t):
    weekdayname = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
    monthname = [None,
                 'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
                 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    year, month, day, hh, mm, ss, wd, y, z = time.gmtime(t)
    s = "%s, %02d %3s %4d %02d:%02d:%02d GMT" % (
        weekdayname[wd],
        day, monthname[month], year,
        hh, mm, ss)
    return s

class CachedFile:
    gmtime = 0
    full_name = os.path.sep
    modification_time = ''
    content = ''
    content_length = 0
    mime_type = None
    
    def __init__(self, filename):
        if '..' in filename or '/' in filename or '?' in filename:
            print('*'*99, 'Inapropriate filename:', filename)
            filename = 'BUG'
        
        self.filename = filename

        if filename.endswith(".css"):
            self.mime_type = 'text/css'
        elif filename.endswith(".html"):
            self.mime_type = 'text/html'
        elif filename.endswith(".png"):
            self.mime_type = 'image/png'
        elif filename.endswith(".jpg"):
            self.mime_type = 'image/jpeg'
        elif filename.endswith(".ps"):
            self.mime_type = 'application/postscript'
        elif filename.endswith(".gif"):
            self.mime_type = 'image/gif'
        elif filename.endswith(".svg"):
            self.mime_type = 'image/svg+xml'
        elif filename.endswith(".ico"):
            self.mime_type = 'image/x-icon'
        elif filename.endswith(".csv"):
            self.mime_type = 'text/comma-separated-values'
        elif filename.endswith(".js"):
            self.mime_type = 'application/x-javascript'
        elif filename.endswith(".tar"):
            self.mime_type = 'application/x-tar'
        else:
            self.mime_type = 'application/octet-stream'

        self.load()

    def load(self):
        for directory in (
            os.path.join(configuration.root, configuration.questions, "HTML"),
            "HTML",                                   # Generated HTML and data
            os.path.join(configuration.root, "HTML"), # Generic HTML data
            ):
            try:
                self.full_name = os.path.join(directory, self.filename)
                f = open(self.full_name, "rb")
                self.content = f.read()
                f.close()
                self.content_length = len(self.content)
                self.gmtime = os.path.getmtime(self.full_name)
                self.modification_time = html_time(self.gmtime)
                return
            except IOError:
                pass
            except OSError:
                pass

    def update(self):
        try:
            if self.gmtime != os.path.getmtime(self.full_name):
                self.load()
        except OSError:
            if len(self.content) == 0:
                self.load()


def get_file(filename):
    if cache == None:
        return CachedFile(filename)
    
    if filename not in cache:
        cache[filename] = CachedFile(filename)
    else:
        cache[filename].update()
        
    return cache[filename]
    
class MyRequestBroker(http.server.BaseHTTPRequestHandler):

    def send_head(self, type, modif_time=None,content_length=None,cached=True):
        if modif_time == None:
            modif_time = self.date_time_string()
        self.send_response(200)
        self.send_header('Content-Type', type)
        if cached and cache != None:
            self.send_header('Cache-Control', 'max-age=3600')            
        else:
            self.send_header('Cache-Control', 'max-age=1')
            self.send_header('Cache-Control', 'private')
            self.send_header('Cache-Control', 'no-store')
        self.send_header('Last-Modified', modif_time)
        self.send_header('Connection', 'close')
        if content_length != None:
            self.send_header('Content-Length', content_length)
        self.end_headers()

    def do_POST(self):
        self.do_GET()

    def do_GET(self):
        self.wfile.write = self.wfile._sock.sendall
        # The 'path' is in the form :
        #                               /prefix/Ticket/number/?action=qu
        #                                         0        1       2
        path = self.path.strip('/')

        if path.startswith(configuration.prefix):
            path = path.replace(configuration.prefix, "", 1)

        path = path.split('/')

        # Try to get the last path component has a file name
        if path[-1] and path[-1][0] != '?':
            c = get_file( path[-1] )
            if c.mime_type != None:
                self.send_head(c.mime_type,
                               modif_time = c.modification_time,
                               content_length = c.content_length,
                               cached = path[-1] not in do_not_cache)
                if isinstance(c.content, bytes):
                    self.wfile.write(c.content)
                else:
                    self.wfile.write(c.content.encode("utf-8"))
                return

        # Get the FORM values
        f = urllib.parse.parse_qs(path[-1].split('?')[-1])
        form = {}
        for i in f:
            form[i] = '\n'.join(f[i])

        if 'guest' in form:
            path[0] = 'guest' + form['guest']

        if 'ticket' not in form:
            form['ticket'] = urllib.parse.unquote(path[0])

        # Get the number
        try:
            number = int(path[1])
        except:
            try:
                number = int(path[0])
            except:
                number = None
        form["number"] = number

        # Get the session state
        print(form['ticket'])
        session = state.get_state(
            self,
            form['ticket'].translate(utilities.safe_ascii),
            form
        )
        if session == None:
            return
        # The session is locked for the student or for all students
        # if a 'not_threaded' plugin is going to run
        # Execute and return page
        sys.stdout.flush() # To really log into the file for 'regtests'
        try:
            session.update_state(self)
            mime, content = session.execute(form)
        finally:
            session.release()

        if mime in ('application/x-javascript', 'text/html', 'text/css'):
            content = content.encode("utf-8")
        sys.stdout.flush()
        self.send_head(mime, cached=False, content_length=len(content))
        self.wfile.write(content)

    def address_string(self):
        """Override to avoid DNS lookups"""
        return "%s:%d" % self.client_address
 

server = None

def function_to_profile(nr_requests):
    global server
    for i in range(nr_requests):
        server.handle_request()

class ThreadingServer(socketserver.ThreadingMixIn, http.server.HTTPServer):
    pass

def run(nr_requests, the_cache):
    f = open("pid", "w")
    f.write(str(os.getpid()))
    f.close()

    # Load students before starting server.
    # If it is not done here, it will be on the first student connexion,
    # and it will fail because it will took too much time.
    s = state.State("fakeserver", 'faketicket', 'fakestudent')
    s.localization = 'fr'
    s.update_plugins() # To update configuration.log_age
    statistics.question_stats()

    global cache
    cache = the_cache

    global server
    server = ThreadingServer(("0.0.0.0", configuration.port)
                             , MyRequestBroker)

    print("\nServer Ready on\n\thttp://%s:%d/guest.html\n\t%s/guest.html" % (
        socket.getfqdn(), configuration.port, configuration.url))
    print("Remove 'guest.html' if you want to use CAS authentication service")
    sys.stdout.flush()
    sys.stderr.flush()

    if nr_requests:
        import hotshot
        p = hotshot.Profile('xxx.hotshot', lineevents=1)
        try:
            p.runcall(function_to_profile,  nr_requests)
        finally:
            p.close()
        # Post-process the hotshot output so it can be read by kcachegrind
        os.system('hotshot2calltree -o xxx.cgr xxx.hotshot')
        os.system('kcachegrind xxx.cgr &')
    else:
        server.serve_forever()
