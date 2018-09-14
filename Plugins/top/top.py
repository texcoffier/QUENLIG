#!/usr/bin/env python3
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
    # "> DIV > TABLE { width: 100% ; }",
    ".heart > DIV P { max-width: 45em ; }",
    ".heart > DIV UL { max-width: 45em ; }",
    )
horizontal = True
acls = { 'Wired': ('executable',) }
priority_execute = priority_display = 2000000000

themes = {
    'green':
    '''
.box_title { background: #CFC ; }
table.box_content { background: #EFE ; }
    ''',
    'gray':
    '''
.box_title { background: #E8E8E8 ;
    border-top-right-radius: 0.4em ;
    border-top-left-radius: 0.4em ;
    }
table.box_content { background: #EEE ; }
    ''',
    }

def option_set(plugin, value):
    if value in themes:
        plugin.state.theme = value
        css_cached.cache.clear()
    else:
        raise ValueError("Bad value for 'theme': " + value)

option_name = 'theme'
option_help = ' or '.join('"%s"' % t
                          for t in themes) + '''
        The GUI theme.'''
option_default = "gray"

import os
import json
from QUENLIG import utilities

def css(state):
    s = []
    for p in state.plugins_dict.values():
        s.append( p.css() )
        preformatted = False
        if p.tip and '\\A' in p.tip:
            preformatted = True
        elif p.translations and '\\A' in ''.join(list(p.translations.values())):
            preformatted = True
        if preformatted:
            s.append('DIV.%s A.tips > SPAN { white-space: pre ; }' % \
                     p.plugin.css_name)
    s.append(themes[state.theme])
    return """

body {
   background: #DDD ;
   font-family: sans-serif ;
   margin: 0px ;
}

DIV.top > TABLE { width: 100%; table-layout: fixed ; }

TT { font-weight: bold ; }

/* BOXES */

.box_title {
   font-weight: bold ;
   text-align: center; 
   white-space: nowrap;
   border: 1px solid black ;
   border-bottom: 0px ;
   margin-top: 0.3em ;
   }

table.box_content {
   border: 1px solid black ;
   width: 100% ;
   border-spacing: 0px ;
}

TABLE.information_table {
border-spacing: 0px ;
margin: 0.4em;
}

TABLE.information_table, TABLE.information_table TR TD, TABLE.information_table TR TH {
border: 1px solid #888 ;
    }

TABLE.information_table TD, TABLE.information_table TH {
background: #EEE ;
}


table > tbody > tr > td { vertical-align: top ; padding: 2px ; }

/* TIPS */

A.tips > SPAN, TT.tips > SPAN, DIV.tips > TT {
  font-size: 10pt ;
  text-align: left ;
  font-weight: 500 ;
  text-decoration: none ;
  position:absolute;
  background-image: url('tip.png');
  color:#000;
  border:2px solid #00F;
  padding:0.2em;
  white-space:normal;
  opacity: 0;
  visibility: hidden ;
  transition: opacity 1s;
  top: -2000px ;
  left: -2000px ;
  z-index: 1;
  margin-left: 1em ;
}

A.tips:hover > SPAN, TT.tips:hover > SPAN , DIV.tips:hover > TT {
  opacity:1;
  top: auto ;
  left: auto ;
  visibility: visible ;
}

A.tips > SPAN:hover, TT.tips > SPAN:hover , DIV.tips > TT:hover {
  opacity:0;
  top: -2000px ;
  left: -2000px ;
  visibility: hidden ;
}

A { text-decoration: none ; }
A[href]:hover { text-decoration: underline ; }
A.tips:hover { text-decoration: none ; }


/* Only here to fix a Chrome bug */
A { background-image: url('transparent.png'); }


PRE { background-color: #FF0 ; border: 1px solid black ; }

""" + '\n'.join(s)

def css_cached(state):
    try:
        return css_cached.cache[state.localization]
    except KeyError:
        pass
    css_cached.cache[state.localization] = the_css = css(state)
    utilities.write(os.path.join('HTML', ','.join(state.localization) + '.css'),
                    the_css)
    return the_css # The cache may have been cleared

css_cached.cache = {}
                   
@utilities.only_one_call
def generate_javascript(state):
    s = ['''
var messages = {} ;

function add_messages(lang, dict)
{
  for(var i in dict)
    {
      if ( messages[lang] === undefined )
           messages[lang] = {} ;
      messages[lang][i] = dict[i] ;
    }
}

function _(message)
{
  for(var lang in languages)
    if ( messages[languages[lang]] !== undefined
      && messages[languages[lang]][message] !== undefined )
       return messages[languages[lang]][message] ;
  return message ;
}

function triggerKeyboardEvent(el, keyCode)
{
    var eventObj = document.createEventObject
      ? document.createEventObject()
      : document.createEvent("Events") ;

    if(eventObj.initEvent){
      eventObj.initEvent("keypress", true, true) ;
    }

    eventObj.keyCode = keyCode ;
    eventObj.which = 0 ;
    eventObj.charCode = keyCode ;
    eventObj.target = el ;
    eventObj.eventPhase == Event.AT_TARGET ;

    if ( el.dispatchEvent )
      el.dispatchEvent(eventObj) ;
    else
      el.fireEvent("onkeypress", eventObj) ;
}

    ''']
    for p in state.plugins_dict.values():
        if p.javascript:
            s.append( '/* PLUGIN: ' + p.plugin.css_name + ' */')
            s.append( p.javascript )
    utilities.write(os.path.join('HTML','quenlig.js'), '\n'.join(s))
    

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
        s.append('<!-- EMPTY %s -->' % plugin.plugin.css_name)
        return

    s.append('<DIV class="%s">' % plugin.plugin.css_name)

    cl = 'content'
    if plugin.tip:
        cl += ' tips'
    if plugin.link:
        s.append('<A class="%s" href="%s">' % (cl, plugin.link))
    elif plugin.tip or plugin.boxed():
        s.append('<A class="%s">' % cl)

    if plugin.boxed():
        s.append('<em class="box_title">')
        if plugin.value_title:
            s.append(plugin.value_title)
        s.append('</em>')
        if plugin.tip:
            s.append('<SPAN></SPAN>')
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
        if plugin.tip or plugin.link:
            s.append('<SPAN></SPAN></A>')
        
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
    <script src="%s/questions.js"></script>
    <link REL="icon" HREF="%s/favicon.ico">
""" % (
        state.plugins_dict['title'].the_title,
        state.url_base_full,
        state.url_base,
        ','.join(state.localization),
        state.url_base, state.url_base, state.url_base) + '\n'.join(
        ['<link rel="stylesheet" href="%s/questions.%s.css" type="text/css">'
         % (state.url_base, x) for x in state.localization]) + """
    <META HTTP-EQUIV="Content-Type" CONTENT="text/html; charset=UTF-8">
    <script src="%s/quenlig.js"></script>
    <script>var languages = %s ;</script>
  </head>
  <body><div class="page">
  """ % (
        state.url_base, json.dumps(state.localization)
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
            try:
                i.encode("utf-8")
            except:
                print('*'*999)
            print(repr(i))
        raise

