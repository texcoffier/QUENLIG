# -*- coding: latin1 -*-
#    QUENLIG: Questionnaire en ligne (Online interactive tutorial)
#    Copyright (C) 2005-2006 Thierry EXCOFFIER, Universite Claude Bernard
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

import time
import cgi
import types
import os

def time_format(t):
    return "%d:%02d:%02d" % (t/3600, (t/60)%60, t%60)

def date_format(t):
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(t))

def user_date(t):
    now = time.time()
    if t > now and t - now < 3600*6:
        f = "%Hh%M"
    else:
        f = "%Hh%M le %d/%m/%Y"
        
    return time.strftime(f, time.localtime(t))

def duration(t):
    t = int(t)
    t, r = divmod(t, 60)
    if r:
        s = str(r)
        if t == 0:
            s += 's'
    else:
        s = ""
    t, r = divmod(t, 60)
    if t+r and (r != 0 or s != ""):
        s = str(r) + "m" + s
    t, r = divmod(t, 24)
    if t+r and (r != 0 or s != ""):
        s = str(r) + "h" + s
    t, r = divmod(t, 7)
    if t+r and (r != 0 or s != ""):
        s = str(r) + "j" + s
    if t:
        s = str(t) + "s" + s
    return s

def answer_format(t):
    t = str(t)
    if t.find("\n") != -1:
        return '<pre class="an_answer">' + cgi.escape(t) + "</pre>"
    else:
        return '<tt class="an_answer">' + cgi.escape(t) + "</tt>"

def list_format(t):
    s = "<ul>"
    for i in t:
        s += "<li>%s</li>" % i
    return s + "</ul>"


def div(class_name, content=""):
    return """<TABLE CLASS=\"%s\">
    <CAPTION></CAPTION>
    <TBODY>
    <TR><TH></TH></TR>
    <TR><TD>%s</TD></TR>
    </TBODY>
    </TABLE>
    """ % (class_name, content)


def cell_value(cell):
    if isinstance(cell, types.TupleType):
        return cell[1]
    return cell

def cell_attributes(cell):
    if isinstance(cell, types.TupleType):
        return " " + cell[0]
    return ""

def line_attributes(cell):
    if isinstance(cell, types.TupleType):
        try:
            return " " + cell[2]
        except KeyError:
            pass
    return ""


def sortable_table(sort_column, content, html_class='', url=''):
    """Content is a list of line.
    Each line is a list containing the same number of cell.
    If a cell is a list then it contains the attributes
    of the cell and the content of the cell

    If the firt cell of the line contains a list of 3 elements,
    the third is the TR attributes.
    """

    try:
        nr_columns = len(content[0])
    except IndexError:
        nr_columns = 1
    
    if sort_column >= 0:
        ascending = True
    else:
        sort_column = -sort_column - 1
        ascending = False

    if sort_column >= nr_columns:
        sort_column = 0


    s = ['''<table class="information_table %s">
    <caption class="caption"></caption>
    <tbody><tr>''' % html_class]

    i = 0
    for i in range(nr_columns):
        s.append('<TH><A CLASS="c%d tips" HREF="?sort_column=%d+%s"><SPAN></SPAN>'%\
                 (i, (i,-i-1)[ascending], url))
        if sort_column == i:
            s[-1] += ('&#8593;', '&#8595;')[ascending]
        s.append('</A></th>')
        
    s.append("</tr>\n")
    # Append sorted column
    content = [ [cell_value(a[sort_column])] + a for a in content]
    content.sort()
    if not ascending:
        content.reverse()
    for line in content:
        s.append("<tr%s>" % line_attributes(line[1]))
        for cell in line[1:]:
            s.append("<td%s>" % cell_attributes(cell) \
                 + str(cell_value(cell)) + "</td>")
        s.append("</tr>")
    s.append("</tbody></table>")
    return '\n'.join(s)

flat = "\x00\x01\x02\x03\x04\x05\x06\x07\x08\x09\x0a\x0b\x0c\x0d\x0e\x0f\x10\x11\x12\x13\x14\x15\x16\x17\x18\x19\x1a\x1b\x1c\x1d\x1e\x1f ! #$%&'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\\]^_`abcdefghijklmnopqrstuvwxyz{|}~?\x80\x81\x82\x83\x84\x85\x86\x87\x88\x89\x8a\x8b\x8c\x8d\x8e\x8f\x90\x91\x92\x93\x94\x95\x96\x97\x98\x99\x9a\x9b\x9c\x9d\x9e\x9f?????Y|?????????????'u?.????????AAAAAA?CEEEEIIIIDNOOOOOXOUUUUY?Baaaaaa?ceeeeiiiionooooo??uuuuy?y"


# Safe for use in shell scripts between ' or "
# SAfe for a file name.
safe_ascii = ''
for i in range(256):
    i = chr(i)
    if i in " #%()*+,-.0123456789;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[]^_abcdefghijklmnopqrstuvwxyz{|}~ÀÁÂÃÄÅÆÇÈÉÊËÌÍÎÏÐÑÒÓÔÕÖØÙÚÛÜÝÞßàáâãäåæçèéêëìíîïðñòóôõöøùúûüýþÿ":
        safe_ascii += i
    else:
        safe_ascii += '?'



def rewrite_string(s, parser=None):
    if not isinstance(s, tuple):
        s = (s, )

    if parser:
        s = [ parser(x) for x in s ]
        
    return s
    

def rewrite_string_string(s, parser=None):
    """
    The output has the following form :
    ( ( ('a', 'b', 'c'), 'd'),
      ( ('e', 'f', 'g'), 'h'),
    )
    The input can be more ambiguous :
    'a'              ==>   ( ( ('a', ), '' ), )
    ( ('a', 'd'), )  ==>   ( ( ('a', ), 'd' ), )
    ( 'a', 'b' )     ==>   ( ( ('a', ), '' ), ( ('b', ), '' ))
    ( 'a', 'b',('c', 'd'))==>( ( ('a', ), '' ), ( ('b', ), '' ), (('c',),'d'))
    """

    if isinstance(s, (basestring, types.FunctionType)):
        s = (s, )

    r = []
    for t in s:
        if isinstance(t, (basestring, types.FunctionType)):
            t = ((t,), '')
        left, right = t
        if isinstance(left, (basestring, types.FunctionType) ):
            left = (left, )
        if parser:
            left = [ parser(x) for x in left ]
        r.append( (left, right) )

    return r

import configuration

def load_module(filename):
    name = filename.replace(os.path.sep, '.')
    # Get module object
    module = __import__(name)
    for directory in name.split('.')[1:]:
        module = module.__dict__[directory]
    module.mtime = os.path.getmtime(module.__file__.replace('.pyc','.py'))
    module.name = name
    try:
        module.init()
    except AttributeError:
        pass
    return module

def load_directory(dirname, py=True):
    modules = {}
    sorted_plugins = os.listdir(dirname)
    sorted_plugins.sort() # To be sure to have a deterministic order.
    for i in sorted_plugins:
        if i == '__init__.py':
            continue
        if i.startswith('.'):
            continue
        if py:
            if not i.endswith('.py'):
                continue
            i = i[:-3]
            print '\n%20s' % str(i),
        else:
            if not os.path.isdir(os.path.join(dirname,i)):
                continue
            print '\n%20s' % str(i),
            i = os.path.join(i , i)
        try:
            modules[i] = load_module(os.path.join(dirname, i))
        except:
            print "*"*99, "Can't load module", i
        
    return modules

def write(filename, text, overwrite=True):
    if not overwrite and os.path.exists(filename):
        return
    f = open(filename, 'w')
    f.write(text)
    f.close()

def read(filename):
    try:
        f = open(filename, 'r')
    except IOError:
        return ''
    c = f.read()
    f.close()
    return c.strip()

def only_one_call(f):
    def ff(*args,**keys):
        if hasattr(ff, 'done'):
            return
        ff.done = True
        f(*args,**keys)
    return ff

def allow_one_more_call(f):
    try:
        del f.done
    except AttributeError:
        pass
