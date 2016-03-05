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

add(name="mode privilégié",
    required=['doc:intro', 'cli:aide commande', 'cli:fin édition'],
    question = """Quelle commande permet de passer en mode privilégié
    sur le routeur (équivalent à <tt>su</tt> sous Unix)&nbsp;?""",
    tests = (
    good("enable"),
    ),
    indices = (
    """C'est <tt>enable</tt>.
    La réponse est dans le module 2 chapitre 3 de la documentation.""",
    ),
    good_answer = """Une fois cette commande tapée, vous êtes
    le super utilisateur sur le routeur.""",
    )

add(name="prompt privilégié",
    required=['mode privilégié'],
    question = """Passez en mode privilégié,
    quelle est l'invite de commande&nbsp;?
    <p>
    Si un mode de passe est demandé, regardez l'indice.""",
    tests = (
    good("Router#"),
    bad("router#", "Pensez à la casse."),
    ),
    indices = ( reinit, ),
    )

add(name="redémarrer",
    required=["cli:? seul", "mode privilégié"],
    question="""Quelle commande tapez-vous pour redémarrer le routeur&nbsp;?
    <p>
    <b>Ne le faites pas, vous perdrez du temps pour rien</b>""",
    tests = (
    good("reload"),
    bad("restart", "Pas loin, c'est la traduction de 'recharge'"),
    ),
    indices = ( "Cela commence par 'r'", ),
    )


add(name="sortir",
    required=['cli:? seul', 'prompt privilégié'],
    question = "Quelle commande permet de quitter le mode privilégié&nbsp;?",
    tests = (
    good('exit'),
    good(('logout', 'disable', 'end'),
         "La commande 'exit' est celle recommandée par CISCO"),
    ),
    )

