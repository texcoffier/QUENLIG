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

import socket
import BaseHTTPServer
import time
import cgi
import urllib
import os
import sys
import state
import configuration
import utilities

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
        # XXX Is this secure (UTF8) ?
        if '..' in filename or '/' in filename or '?' in filename:
            print '*'*99, 'Inapropriate filename:', filename
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

        self.load()

    def load(self):
        for directory in (
            os.path.join(configuration.root, configuration.questions, "HTML"),
            "HTML",                                   # Generated HTML and data
            os.path.join(configuration.root, "HTML"), # Generic HTML data
            ):
            try:
                self.full_name = os.path.join(directory, self.filename)
                f = open(self.full_name, "r")
                self.content = f.read()
                f.close()
                if self.filename.endswith(('.html', '.css', '.js')):
                    try:
                        unicode(self.content, 'utf-8')
                    except:
                        self.content = utilities.to_unicode(self.content
                        ).encode("utf-8")
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
    
    if not cache.has_key(filename):
        cache[filename] = CachedFile(filename)
    else:
        cache[filename].update()
        
    return cache[filename]
    
class MyRequestBroker(BaseHTTPServer.BaseHTTPRequestHandler):

    timeout = 0.3 # Some bugged browser do not send the GET
    
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

    def do_GET(self):
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
                self.wfile.write(c.content)
                return

        # Get the FORM values
        f = cgi.parse_qs(path[-1].split('?')[-1])
        form = {}
        for i in f:
            form[i] = ''.join(
                utilities.to_unicode(ff)
                for ff in f[i]) # concatenation of parameters

        if form.has_key('guest'):
            path[0] = 'guest' + form['guest']

        if not form.has_key('ticket'):
            form['ticket'] = urllib.unquote(path[0])

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
        print form['ticket']
        session = state.get_state(self, form['ticket'].translate(utilities.safe_ascii))
        if session == None:
            return
        # Execute and return page
        sys.stdout.flush() # To really log into the file for 'regtests'
        mime, content = session.execute(form)
        if mime in ('application/x-javascript', 'text/html', 'text/css'):
            content = utilities.to_unicode(content).encode("utf-8")
        sys.stdout.flush()
        self.send_head(mime, cached=False, content_length=len(content))
        self.wfile.write(content)

    def address_string(self):
        """Override to avoid DNS lookups"""
        return "%s:%d" % self.client_address
 

server = None

def function_to_profile(nr_requests):
    global server
    for i in xrange(nr_requests):
        server.handle_request()


def run(nr_requests, the_cache):
    f = open("pid", "w")
    f.write(str(os.getpid()))
    f.close()

    global cache
    cache = the_cache

    global server
    server = BaseHTTPServer.HTTPServer(("0.0.0.0", configuration.port)
                                       , MyRequestBroker)

    print "\nServer Ready on\n\thttp://%s:%d/guest.html\n\t%s/guest.html" % (
        socket.getfqdn(), configuration.port, configuration.url)
    print "Remove 'guest.html' if you want to use CAS authentication service"

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
