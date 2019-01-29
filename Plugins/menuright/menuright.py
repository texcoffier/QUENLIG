#!/usr/bin/env python3
# -*- coding: latin-1 -*-
#    QUENLIG: Questionnaire en ligne (Online interactive tutorial)
#    Copyright (C) 2019 Thierry EXCOFFIER, Universite Claude Bernard
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

"""If active: the menu is on the right.
Useful for users with a screen reader:
the page content is read first."""

from QUENLIG import student

priority_display = 'top'

acls = { }

javascript = r"""
function put_menu_to_the_right()
{
    var div = document.getElementsByTagName('DIV') ;
    for(var i in div)
    {
        if ( div[i].className == 'menu' )
            {
            var menu = div[i].parentNode ;
            var parent = menu.parentNode ;
            parent.removeChild(menu) ;
            parent.appendChild(menu) ;
            break ;
            }
    }
}
"""

def execute(state, plugin, argument):
    return '<script>put_menu_to_the_right()</script>'
