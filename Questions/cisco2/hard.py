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

from QUENLIG.questions import *
from .check import *
from .configuration_salles import *

add(name="modèle cisco",
    required=["admin:administrateur"],
    question="Quel est le modèle du routeur CISCO que vous allez utiliser&nbsp;? C'est écrit sur la façade avant...",
    tests=(
    HostCiscoModele(),
    ),
    )

add(name="combien d'interfaces",
    required=["admin:administrateur"],
    question="""Combien d'interfaces <b>réseau</b> physique allez-vous utiliser
    sur votre routeur&nbsp;?
    <p>
    Regardez sur le plan.""",
    tests = ( require_int(), NrInterfacesUsed() ),
    )

add(name="connecteur ethernet",
    required=["admin:administrateur"],
    question="Quel est le type des connecteurs éthernet sur le routeur et sur le PC&nbsp;?",
    tests = ( good("RJ45", uppercase=True, replace=((' ',''),('-',''))),
              ),
    indices = ("""C'est le même connecteur que sur les prises murales""",
               ),
    )

add(name="cable ethernet",
    required=["connecteur ethernet"],
    question="""Quel est le type du cable éthernet à brancher&nbsp;?
    <ul>
    <li> on ne vous demande pas s'il est croisé ou non.
    <li> on veut l'acronyme.
    </ul>""",
    tests = (
    bad('RJ45', "C'est le nom du connecteur, pas du cable", uppercase=True),
    bad(('DCE','DTE'),
        "La notion de DTE/DCE n'existe pas avec ethernet", uppercase=True),
    answer_length_is(3, "La réponse est en 3 lettres"),
    good('UTP', uppercase=True),
    good('FTP', uppercase=True),
    ),
    indices = ("<tt>Unshielded Twisted...</tt> ou bien <tt>Foiled Twisted...</tt>", ),
    )

add(name="cable croisé",
    required=["cable ethernet"],
    question="""Le cable éthernet entre le routeur et le
    commutateur (<em>switch</em>) doit-il être croisé&nbsp; <tt>oui</tt> ou <tt>non</tt>?""",
    tests = ( no("Il est croisé en interne dans le commutateur"), ),
    )
    


add(name="M | F",
    required=["admin:administrateur"],
    question="""Quel est le genre (M ou F) du câble que vous allez connecter
    sur le port série 0 de votre routeur&nbsp;?""",
    tests = (
    answer_length_is(1, "Vous devez répondre avec M ou F"),
    good("{C0.remote_port.host.S0.port.type}", uppercase=True,
         replace=(('F','DCE'), ('M', 'DTE')), parse_strings=host),
    ),
    )

add(name="tout brancher",
    required=["admin:nom routeur", "combien d'interfaces",
              "M | F", "cable croisé"],
    question="""Répondez oui quand vous aurez branché tous les cables.
    <b>SAUF les cables reliant directement 2 PC
    sans passer par un <em>switch</em></b>,
    ils seront branchés plus tard.""",
    tests = ( yes("On vous a dit de répondre OUI."), ),
    )
