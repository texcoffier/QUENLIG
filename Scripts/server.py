#!/usr/bin/env python3
#    QUENLIG: Questionnaire en ligne (Online interactive tutorial)
#    Copyright (C) 2005-2010 Thierry EXCOFFIER, Universite Claude Bernard
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

import os
import urllib.request, urllib.error, urllib.parse
import time
import stats
import sys
import shutil

class Server:
    def __init__(self,
                 port=10101,
                 questions='Questions/unix',
                 profiling=False,
                 name="test"):
        print('Start server', port, questions, profiling, name)
        self.port = port
        self.name = name
        self.stats = stats.Stats()
        self.base = 'http://localhost:%d' % self.port
        shutil.rmtree("/tmp/Students%s" % self.name, True)
        try:
            os.remove("Students/%s" % self.name) # Symlink
        except FileNotFoundError:
            pass
        os.mkdir("/tmp/Students%s" % self.name)
        os.symlink("/tmp/Students%s" % self.name, "Students/%s" % self.name)
        if profiling:
            profiling = 'nr-requests-served %s' % profiling
        else:
            profiling = ''
        os.system(
            '(./main.py %s stop ;' % name +
            'rm -r %s || true ; ' % self.sessiondir() +
            './main.py %s create %s %d begin-date "1:1 1/1/1970" end-date "1:1 1/1/2037" url "%s" start &) >xxx.log 2>&1' % (
            name, questions, port, self.base)
            )
        print('Log file is: xxx.log')
        print('Wait server start: ', end=' ')
        while True:
            try:
                urllib.request.urlopen(self.base + '/fr.css').close()
                break
            except urllib.error.URLError:
                sys.stdout.write('*')
                sys.stdout.flush()
                time.sleep(0.4)
            except KeyboardInterrupt:
                self.stop()
        print()

    def sessiondir(self):
        return 'Students/%s/' % self.name

    def logdir(self):
        return self.sessiondir() + 'Logs/'

    def stop(self):
        print('Stop server')
        os.system('./main.py %s stop >>xxx.log 2>&1' % self.name)
        print('Server stopped, log are in "xxx.log"')

    def get(self, url, trace=False):
        if trace:
            print('GET', url)
        start = time.time()
        f = urllib.request.urlopen(url)
        p = f.read().decode("utf-8")
        f.close()
        if trace:
            print('GET', time.time() - start)
        self.stats.add(time.time() - start)
        return p

if __name__ == "__main__":
    server = Server()
    print('len(css.css) =', len(server.get('http://localhost:%d/css.css' % server.port)))
    server.stop()
    

