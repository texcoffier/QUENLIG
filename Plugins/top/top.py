#!/usr/bin/env python
# -*- coding: latin-1 -*-
#    QUENLIG: Questionnaire en ligne (Online interactive tutorial)
#    Copyright (C) 2007 Thierry EXCOFFIER, Universite Claude Bernard
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

"""Top level plugin. It defines the 3 columns of the page:
the left menu, the heart of the page and the administrator menu.

This plugin is the page composer, it must be
the last one to be executed.
"""

css_attributes = (
    "> DIV > TABLE { width: 100% ; }",
    )
horizontal = True
acls = { 'Wired': ('executable',) }
priority_execute = priority_display = 2000000000

import utilities
import os
import cgi
import configuration


def css(state):
    s = []
    for p in state.plugins_dict.values():
        s.append( p.css() )
        preformatted = False
        if '\\A' in str(p.tip):
            preformatted = True
        elif p.translations and '\\A' in ''.join(p.translations.values()):
            preformatted = True
        if preformatted:
            s.append('DIV.%s A.tips > SPAN { white-space: pre ; }' % \
                     p.plugin.css_name)

    return """

body {
   background: #DDD ;
   font-family: sans ;
   margin: 0px ;
}

TT { font-weight: bold ; }

/* BOXES */

.box_title {
   font-weight: bold ;
   background: #CFC ;
   text-align: center; 
   white-space: nowrap;
   border: 1px solid black ;
   border-bottom: 0px ;
   margin-top: 0.3em ;
   }

table.box_content {
   border: 1px solid black ;
   background: #EFE ;
   width: 100% ;
   border-spacing: 0px ;
}

TABLE.information_table {
background-color: black ;
border-spacing: 1px ;
margin: 0.4em;
}

TABLE.information_table TD, TABLE.information_table TH {
background: #EEE ;
border: 1px ;
}

table > tbody > tr > td { vertical-align: top ; padding: 2px ; }

/* TIPS */

A.tips > SPAN, TT.tips > SPAN, DIV.tips > TT { display: none; }

A.tips:hover > SPAN, TT.tips:hover > SPAN , DIV.tips:hover > TT {
  font-size: 10pt ;
  text-align: left ;
  font-weight: 500 ;
  text-decoration: none ;
  margin-top: 3em;
  position:absolute;
  background-image: url('tip.png');
  color:#000;
  border:2px solid #00F;
  padding:0.2em;
  display:block;
  white-space:normal;
  z-index: 10;
}

/* Only here to fix a Chrome bug */
A { background-image: url('transparent.png'); }


PRE { background-color: #FF0 ; border: 1px solid black ; }

""" + '\n'.join(s)

def css_cached(state):
    try:
        return css_cached.cache[state.localization]
    except KeyError:
        pass
    css_cached.cache[state.localization] = css(state)
    utilities.write(os.path.join('HTML', ','.join(state.localization) + '.css'),
                    css_cached.cache[state.localization])
    return css_cached.cache[state.localization]

css_cached.cache = {}

                   
@utilities.only_one_call
def generate_javascript(state):
    s = []
    for p in state.plugins_dict.values():
        if p.javascript:
            s.append( '/* PLUGIN: ' + p.plugin.css_name + ' */')
            s.append( p.javascript )
    utilities.write(os.path.join('HTML','quenlig.js'),
                    '\n'.join(s))
    

def display(plugin, s):
    if plugin.current_acls['hide']:
        plugin.value = '???'
        plugin.content = []
        s.append('<!-- HIDDEN -->')
        return
    if not hasattr(plugin, 'value'):
        plugin.value = '???'
    if not hasattr(plugin, 'content'):
        plugin.content = []
        
    
    if plugin.value == None and len(plugin.content) == 0:
        s.append('<!-- EMPTY -->')
        return

    s.append('<DIV class="%s">' % plugin.plugin.css_name)

    cl = 'content'
    if plugin.tip:
        cl += ' tips'
    if plugin.link:
        s.append('<A class="%s" href="%s">' % (cl, plugin.link))
    else:
        s.append('<A class="%s">' % cl)

    if plugin.tip:
        s.append('<SPAN></SPAN>')

    if plugin.boxed():
        s.append('<em class="box_title">')
        if plugin.value_title:
            s.append(plugin.value_title)
        s.append('</em>')
        s.append('</A><table class="box_content"><tbody><tr><td>')

    if plugin.horizontal:
        s.append('<table><tbody><tr>')
        for p in plugin.content:
            if p.width:
                width = ' style="width:' + p.width + '"'
            else:
                width = ''
            s.append('<td%s>' % width)
            display(p, s)
            s.append('</td>')
        s.append('</tr></tbody></table>')
    else:
        for p in plugin.content:
            display(p, s)

    if plugin.value:
        s.append( plugin.value )

    if plugin.boxed():
        s.append('</td></tr></tbody></table>')
    else:
        s.append('</A>')
        
    s.append('</DIV>')


def execute(state, plugin, argument):
    css_cached(state)
    generate_javascript(state)

    body = """<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN">
<html>
  <head>
    <title>%s</title>
    <base href="%s">
    <link rel="stylesheet" href="%s/%s.css" type="text/css">
    <link rel="stylesheet" href="%s/questions.css" type="text/css">
""" % (
        state.plugins_dict['title'].the_title,
        state.url_base_full,
        state.url_base,
        ','.join(state.localization),
        state.url_base) + '\n'.join( 
        ['<link rel="stylesheet" href="%s/questions.%s.css" type="text/css">'
         % (state.url_base, x) for x in state.localization]) + """
    <META HTTP-EQUIV="Content-Type" CONTENT="text/html; charset=ISO-8859-1">
    <script src="%s/quenlig.js"></script>
  </head>
  <body><div class="page">
  """ % (
        state.url_base,
        )

    s = [body]
    for a_plugin in state.roots:
        s.append('<!-- ' + a_plugin.plugin.css_name + ' -->')
        display(a_plugin, s)

    s.append('</div></body></html>')
    try:
        state.full_page = '\n'.join(s)
    except:
        for i in s:
            print i
        raise

