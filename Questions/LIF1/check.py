# -*- coding: latin-1 -*-
#    QUENLIG: Questionnaire en ligne (Online interactive tutorial)
#    Copyright (C) 2011 Thierry EXCOFFIER, Universite Claude Bernard
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

from questions import *
import re

def C_clean(txt):
    if isinstance(txt, str):
        # Remove last ';' and replace tabulations with space
        txt = txt.strip(' ;\n\t').replace('\t',' ').replace('\n',' ')
        # A run of spaces if replaced by one space
        txt = re.sub('  +', ' ', txt)
        # Spaces around not a normal letter are removed
        txt = re.sub(' *([^a-zA-Z0-9_]) *', r'\1', txt)
        return txt
    else:
        return [C_clean(i) for i in txt]


class C(TestUnary):
    def __call__(self, student_answer, state=None, parser=no_parse):
        return self.children[0](
            C_clean(student_answer), state,
            lambda string, state, test: parser(C_clean(string), state, test)
            )

