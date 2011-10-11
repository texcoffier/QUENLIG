#!/usr/bin/env python
# -*- coding: latin1 -*-
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

import collections
import time
import statistics

priority_display = 'role'
# font_size = "70%"
# color = "#999"
acls = { 'Default': ('!executable',), 'Teacher': ('executable',) }

def execute(state, plugin, argument):
    stats = statistics.question_stats()
    roles = collections.defaultdict(int)
    t = time.time()

    for s in stats.all_students:
        if t - s.the_time_last < 10 * 60:
            try:
                roles[s.current_role] += 1
            except AttributeError:
                pass

    return '<br>'.join(('%s : %d' % (k, v) for k,v in roles.items()))

