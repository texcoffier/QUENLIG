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

add(name="RIP",
    required=["tp2:réseaux directs", "lien:routeur eth0", "tp2:Et Hop s0 ?",  "tp2:Et Hop s1 ?"],
    before="""On suppose que vous venez de faire <tt>enable</tt> et
    que vous n'avez rien fait après.""",
    question="""Donnez la liste de toutes les commandes que vous
    tapez pour configurer la liste des <b>réseaux dont vous
    voulez diffuser les adresses</b> avec le protocole RIP.
    <p>
    Pas la peine d'indiquer les <tt>exit</tt> dans la réponse.
    <p>
    
    """,
    nr_lines = 5,
    tests=(
    expect("configure terminal"),
    expect("router rip"),
    expect("network"),
    reject("route ",
           """On ne vous demande pas d'ajouter de routes statiques avec
           la commande <tt>route</tt>"""),
    reject('/', """Pas la peine d'indiquer le masque réseau, le routeur
    le connait déja"""),
    good("""configure terminal
router rip
network {C0.remote_port.host.S0.network}
network {C0.remote_port.host.S1.network}
network {C0.remote_port.host.E0.network}""", parse_strings=host,
         sort_lines=True),
    ),
    )

add(name="table de routage",
    required=["RIP"],
    question="""Quelle commande tapez-vous sur le routeur pour afficher
    la table de routage&nbsp;?""",
    tests = (
    require("show", "On utilise la commande <tt>show</tt> pour afficher..."),
    require('ip', "On veut les routes <tt>ip</tt>"),
    good("show ip route"),
    ),
    good_answer = """Petit à petit vous allez voir la table de routage
    se remplir quand les routeurs vont s'échanger les routes.""",
    )


add(name="préfixe directe",
    required=["table de routage"],
    question = """Quel est le préfixe des routes directement connectées
    à votre routeur&nbsp;?""",
    tests = (
    answer_length_is(1),
    good('C', uppercase=True),
    ),
    )

add(name="préfixe RIP",
    required=["table de routage"],
    question = """Quel est le préfixe des routes obtenues par
    le protocol RIP&nbsp;?""",
    tests = (
    answer_length_is(1),
    good('R', uppercase=True),
    ),
    )

add(name="préfixe statique",
    required=["table de routage"],
    question = "Quel est le préfixe des routes entrées statiquement&nbsp;?",
    tests = (
    answer_length_is(1),
    good('S', uppercase=True),
    ),
    )

for i in (0,1):
    add(name="Et Hop s%d OK" % i,
        required=["tp2:Et Hop s%d ?" % i, "tp2:Et Hop s%d" % i, "préfixe RIP"],
        before = "Attendez d'avoir reçu la table de routage du routeur voisin",
        question="""À partir du routeur,
        le ping du port ethernet du routeur distant via serial%d
        fonctionne-t-il (la commande est en bas de page)&nbsp;?""" % i,
        tests = (
        yes("""Cela devrait fonctionner, il y a un problème."""),        
        ),
        )

