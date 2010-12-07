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
#

from questions import *
from check import *
from configuration_salles import *


add(name="intro",
    required=["tp1:intro"],
    before="""La documentation CISCO est accessible via
    <a href="%(cours_ccna)s">le web</a>.
    <p>
    Cliquez sur le lien avec le bouton du milieu pour créer une nouvelle
    fenêtre, comme cela vous ne perdrez pas cette page.
    <p>
    Si cela ne marche pas, configurez votre navigateur web
    avec comme proxy&nbsp;: <tt>%(proxy)s</tt>
    """ % conf,
    question = "Combien de <em>modules</em> CCNA trouve-t-on sur la page web&nbsp;?",
    tests = ( require_int(), good("4") ),
    )
