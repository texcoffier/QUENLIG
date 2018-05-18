# -*- coding: utf-8 -*-
#    QUENLIG: Questionnaire en ligne (Online interactive tutorial)
#    Copyright (C) 2018 Thierry EXCOFFIER, Universite Claude Bernard
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
#

from QUENLIG.questions import *

add(name="mcq",
    question = "A even integer:",
    preprocesses = MCQ("""
[even] {{{Congratulation! it is a perfect answer}}}
<table><tr><td>
can be defined as:

+A               is not an odd integer
+B[double,even]  is the double of another integer
+G[odd,add]      is an odd integer + 1

<td>
when written, its last digit is :

+C[decimal]      0 2 4 6 8 in decimal
+D[binary]       0 in binary
-E[octal]        0 2 4 6 8 in octal {{{10 is not a digit in decimal system, so in octal...}}}
-F[hexa]         0 2 4 6 8 A C in hexadecimal

</tr></table>
"""),
    tests = ( # Optional comment
        Continue(Comment(~Contain('(A)') | ~Contain('(B)') | ~Contain('(G)'),
                "Some basic properties are missing.")
                ),
                ),
)

