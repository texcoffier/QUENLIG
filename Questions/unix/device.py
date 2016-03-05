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

from QUENLIG.questions import *
from .check import *

add(name="poubelle",
    required=["intro:final", "navigation:final"],
    question="""Quel est le nom absolu du périphérique (<em>device</em>)
    qui sert de poubelle&nbsp;?
    Tout ce qui est écrit dedans est perdu.""",
    indices=("""Les fichiers périphériques sont généralement dans <tt>/dev</tt>""",
            ),

    tests=(
    good("/dev/null"),
    bad(("/dev", "/dev/"),
        """C'est le nom du répertoire contenant la poubelle,
        il faut ajouter le nom du périphérique poubelle."""),
    require("/",
            """On vous demande un chemin absolu,
            il y a donc des <tt>/</tt>"""),
    require("/dev/", "Les périphériques sont dans <tt>/dev</tt>"),
    reject("zero", "Ce n'est pas <tt>zero</tt> car il n'est pas standard."),
    reject("trash", "Ce périphérique n'existe même pas."),
    require('null', "Le périphérique poubelle est <tt>null</tt>"),
    ),
    )

