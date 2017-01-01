#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#    TOMUSS: The Online Multi User Simple Spreadsheet
#    Copyright (C) 2009,2016 Thierry EXCOFFIER, Universite Claude Bernard
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
To activate deadlock check, import this module
"""


import threading
import inspect
import weakref

origLock = None

locks = []

def callers(n=2):
    s = []
    for f in inspect.stack()[n:]:
        s.append(f[3])
        if f[3] == 'process_request' or f[3] == 'do_GET':
            break
    return '/'.join(s)

class Lock(object):
    name = ''
    by = ''

    def __init__(self):
        self.lock = origLock()
        for x in tuple(locks):
            if x.name == '':
                locks.remove(x)
        locks.append(self)
        
    def acquire(self, *args):
        # print('ACQUIRE', self, callers())
        self.by = callers()
        return self.lock.acquire(*args)

    def release(self):
        # print('RELEASE', self, callers())
        self.lock.release()

    def locked(self):
        return self.lock.locked()

    def __str__(self):
        name = self.name or repr(self.lock)
        locked = self.lock.locked() and "Locked" or "Unlocked"
        by = self.lock.locked() and (' by: ' + self.by) or ''
        return locked + ' ' + name  

    def __enter__(self):
        return self.acquire()

    def __exit__(self, type, value, tb):
        return self.release()

def lock_list():
    print("*"*79)
    print("LOCK LIST", callers())
    print("*"*79)
    for i in locks:
        print(i, flush=True)
    print("*"*79)
    print("THREADS")
    print("*"*79)
    import traceback
    for t in threading.enumerate():
        try:
            print(traceback.format_stack(t), flush=True)
        except:
            pass

def start_check_deadlock():
    global origLock
    origLock = threading.Lock
    threading.Lock = Lock
    import atexit
    atexit.register(lock_list)
    import signal
    signal.signal(signal.SIGUSR1, lambda x, y: lock_list())

start_check_deadlock()

if __name__ == "__main__":
    l1 = threading.Lock()
    l1.name = "L1"
    l2 = threading.Lock()
    l2.name = "L2"

    class T1(threading.Thread):
        def run(self):
            l1.acquire()
            l1.release()
            l2.acquire()
            l2.release()

    class T2(threading.Thread):
        def run(self):
            l2.acquire()
            l2.release()
            l1.acquire()
            l1.release()

    class T3(threading.Thread):
        def run(self):
            l1.acquire()
            l2.acquire()
            l2.release()
            l1.release()

    class T4(threading.Thread):
        def run(self):
            try:
                l2.acquire()
                l1.acquire()
                l1.release()
                l2.release()
                print('Test3 is BAD: No exception launched')
            except AssertionError:
                print('Test3 is fine: exception launched')

    t1 = T1()
    t1.start()
    t2 = T2()
    t2.start()
    t1.join()
    t2.join()
    print('Test1 is fine: No exception launched')
    t3 = T3()
    t3.start()
    t3.join()
    print('Test2 is fine: No exception launched')
    assert(len(l1.locked_after) == 0)
    assert(len(l2.locked_after) == 1)
    t4 = T4()
    t4.start()
    t4.join()
            
        
