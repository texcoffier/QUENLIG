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

"""Display the session duration."""

from QUENLIG import utilities

priority_display = 'session_stop'
font_size = "70%"
color = "#999"
acls = { 'Student': ('executable',) }
javascript = """
var remaining_seconds, starting_time ;
function decrement_time(s)
{
   remaining_seconds = s ;
   var now = new Date() ;
   starting_time = now.getTime() ;
   setInterval(update_time, 1000) ;
}
function duration(t)
{
    var s ;
    var r = t % 60 ;
    var t = Math.floor(t / 60) ;
    if (r)
      {
        s = r ;
        if (t == 0)
            s += 's' ;
      }
    else
      s = "" ;
    r = t % 60 ;
    t = Math.floor(t / 60) ;
    if (t+r && (r != 0 || s != ""))
        s = r + "m" + s ;
    r = t % 24 ;
    t = Math.floor(t / 24) ;
    if (t+r && (r != 0 || s != ""))
        s = r + "h" + s ;
    r = t % 7 ;
    t = Math.floor(t / 7) ;
    if(t+r && (r != 0 || s != ""))
        s = r + "j" + s ;
    if (t)
        s = t + "s" + s ;
    return s ;
}
function update_time()
{
   var now = new Date() ;
   var s = remaining_seconds - (now.getTime() - starting_time)/1000 ;
   s = s.toFixed(0) ;
   document.getElementById('remaining').innerHTML = duration(s) ;
   if ( s < 300 )
     {
     document.getElementById('remaining').style.color = '#000' ;
     }
   if ( s < 60 )
     {
     document.getElementById('remaining').style.background = '#F00' ;
     document.getElementById('remaining').style.color = '#FFF' ;
     }
}
"""

def execute(state, dummy_plugin, dummy_argument):
    if (state.start > state.start_date
        and state.start < state.stop_date):
        t = int(state.stop_date - state.start)
        return ('<script>decrement_time(%d)</script><var id="remaining">' % t
                + utilities.duration(t) + '</var>')
