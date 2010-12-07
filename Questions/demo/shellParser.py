#!/usr/bin/env python
# -*- coding: latin-1 -*-
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
#

# TODO : while $$ $# $1 $* # { } fonctions

from shellSyntax import sh
import tpg
import utilities
import types

def canonise_option(xml, short_opt, long_opt, take_argument):
    """Replace long options by short one
    and paste the option with the argument if take_option=True
    """
    if long_opt:
        xml = re.sub( "<argument>" + long_opt + "=?",
                       "<argument>" + short_opt,
                       xml)
    if take_argument:
        xml = re.sub("<argument>" + short_opt + "</argument>" +
                      "<argument>([^<]*)</argument>",
                      "<argument>" + short_opt + "\\1</argument>",
                      xml)            
    return xml

import re
re_comment = re.compile("<comment>[^<]*</comment>")

def real_parse(answer, replacement=(), dumb_replace=()):
    """Returns XML and canonised XML"""
    for olds, new in dumb_replace:
        if not isinstance(olds, (types.ListType, types.TupleType)):
            olds = (olds, )
        for old in olds:
            answer = answer.replace(old, new)

    try:
        c = sh(answer)
    except tpg.LexicalError:
        return "<p class='shell_syntax_error'>", ""
    except tpg.SyntacticError:
        return "<p class='shell_syntax_error'>", ""

    c_student = c = str(c)
    for short_option, long_option, take_option in replacement:
        c = canonise_option(c, short_option, long_option, take_option)
    for short_option, long_option, take_option, command in (
        ("-d", "--delimiter"         , 1, None  ),
        ("-e", "--regexp"            , 1, None  ),
        ("-f", "--fields"            , 1, None  ),
        ("-h", "--no-filename"       , 0, None  ),
        ("-i", "--ignore-case"       , 0, None  ),
        ("-k", "--key"               , 1, None  ),
        ("-l", "--files-with-matches", 0, "grep"),
        ("-l", "--lines"             , 0, "wc"  ),
        ("-n", "--numeric-sort"      , 0, "sort"),
        ("-n", "--lines"             , 1, "tail"),
        ("-n", "--lines"             , 1, "head"),
        ("-t", "--field-separator"   , 1, None  ),
        ("-u", "--unique"            , 0, None  ),
        ):
        if command==None \
           or c.find("<argument>" + command + "</argument>") != -1:
            c = canonise_option(c, short_option, long_option, take_option)
    return c_student, re_comment.sub("", c)


last_answer = ""
last_replacement = ()
last_parsed = ""
last_uncommented = ""
last_dumb_replace = ()

def parse(answer, replacement=(), dumb_replace=()):
    global last_answer, last_replacement, last_parsed, last_uncommented
    global last_dumb_replace
    
    if (answer != last_answer
        or replacement != last_replacement
        or dumb_replace != last_dumb_replace
        ):
       last_parsed, last_uncommented = real_parse(answer, replacement, dumb_replace)
       last_replacement = replacement
       last_dumb_replace = dumb_replace
    return last_parsed, last_uncommented


def parse_only_not_commented(answer):
    commented, uncommented = parse(answer)
    return uncommented












