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

"""The left column in the page."""

container = 'top'
width = "20%"

transition_hover = "max-width 0.5s"
transition_nhover = "max-width 2s"

css_attributes = (
    "> DIV { overflow: hidden; max-width: 100%; min-width:100%; transition: " + transition_hover + "; webkit-transition: " + transition_hover + "; display: inline-block; z-index: 10 ; }",
    "> DIV:hover { max-width: 25em; transition: " + transition_nhover + "; webkit-transition: " + transition_nhover + " ; overflow: visible  }",
    "> DIV > TABLE > TBODY > TR > TD { white-space: nowrap ; }",
    ".box_title { display: block ; }",
    "/@media print { DIV.menu { display: none ; } ; }"
    )

acls = { 'Wired': ('executable',) }
