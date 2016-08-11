#!/usr/bin/env python3
# -*- coding: latin-1 -*-
#    QUENLIG: Questionnaire en ligne (Online interactive tutorial)
#    Copyright (C) 2015 Thierry EXCOFFIER, Universite Claude Bernard
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
#    Contact: Thierry.EXCOFFIER@univ-lyon1.fr

"""Display all the questions definition."""

import collections
from QUENLIG import questions

container = 'action'
link_to_self = True
priority_execute = '-question_source'
acls = { 'Default': ('executable',), }
css_attributes = ('/@media screen { .hide_on_screen { display: none ; }} ',
                  """/@media print { .hide_on_print { display: none ; }
                                     BODY, H1,
                                     TABLE.information_table TD,
                                     TABLE.information_table TH
                                     { background: #FFF }
                                     DIV.heart { margin-left: -1em }
                  }""",
                  ".question_title { margin-top: 1.5em ; margin-bottom: 0em }"
                  "/BODY { orphans: 3; widows: 3; }",
                  "/H2 { page-break-after: avoid }",
                  "/H3 { page-break-after: avoid }",
                  "/.course_question { page-break-before: avoid }",
                  )

javascript = """
function add_courses_index()
{
  var t = document.getElementsByTagName("DIV") ;
  var course_menu, keys = [] ;
  for(var i in t)
   {
     if ( t[i].className == 'course_question' )
        {
          var qs = t[i].childNodes ;
          var q = qs[0].textContent ;
          var tt = t[i].getElementsByTagName('KEY') ;
          for(var k=0; k < tt.length; k++)
               keys.push([tt[k].textContent, q]) ;
        }
    else if ( t[i].className == 'courses'
         && t[i].parentNode.className != "heart_content" )
        course_menu = t[i] ;
   }
  var t = document.getElementsByTagName("A") ;
  var toc = [] ;
  for(var i in t)
   {
     if ( ! t[i].name )
        continue ;
     if ( t[i].name.substr(0,3) != 'toc' )
        continue ;
     toc.append('<a href="' + window.location + '#' + t[i].name + '">'
                   + t[i].innerHTML + '</a>') ;
   }

  var s = [] ;
  keys.sort() ;
  for(var j in keys)
      s.push('<a href="?question='+escape2(keys[j][1])+'">' + keys[j][0]) ;
  if ( s.length || toc.length )
       course_menu.innerHTML = '<br>' + toc.join("<br>") + '<br>'
                        + 'Index:</br>'
                        + '<div style="margin-left:1em; font-size: 80%">'
                        + s.join('<br>')
                        + '</div>' ;
}

setTimeout(add_courses_index, 500) ;


"""

def execute(state, plugin, argument):
    if not argument:
        return ''

    toc = collections.defaultdict(list)
    for question in questions.sorted_questions:
        if not question.courses:
            continue
        if not question.before:
            continue
        q = question.before(state)
        if q == '':
            continue
        toc[question.courses].append(question)
    s = []
    last = ()
    n = 0
    for where in sorted(toc):
        identical = True
        if where is not True:
            for i, title in enumerate(where):
                if not identical or len(last) <= i or title != last[i]:
                    identical = False
                    s.append('<h%d><a name="toc%s">%s</a></h%d>'
                             % (i+2, n, title, i+2))
                    n += 1
        last = where
        for question in toc[where]:
            if identical:
                s.append('<hr class="hide_on_screen">')
            identical = True
            s.append('''
<div class="course_question">
<p class="hide_on_print question_title"><b><a href="%s">%s</a></b>
<p>%s</div>''' % (question.url(), question.name, question.before(state)))

    plugin.heart_content = '\n'.join(s)
    state.question = None
    return ''
