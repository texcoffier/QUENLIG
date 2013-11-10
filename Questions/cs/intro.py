# -*- coding: latin-1 -*-
#    QUENLIG: Questionnaire en ligne (Online interactive tutorial)
#    Copyright (C) 2008 Thierry EXCOFFIER, Olivier GLÜCK, Universite de Lyon
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

"""
#####################################
Some explanation
#####################################
Voici les infos pour les TP client/serveur en M2PRO.

Pour démarrer le TP :
   su exco
   /home/exco/lance-quenlig-cs

Pour que les étudiants puissent saisir les réponses :
   NFS  : http://demo710.univ-lyon1.fr:4001/
   NIS  : http://demo710.univ-lyon1.fr:4002/
   DNS  : http://demo710.univ-lyon1.fr:4003/
   LDAP : http://demo710.univ-lyon1.fr:4004/

Si jamais l'authentification ne fonctionne pas, ajouter 'guest.html' à la fin.

#####################################
Creation des sessions and launch them
#####################################

create() {
if [ ! -d Students/$1/Logs/Default ]
        then
        mkdir Students/$1/Logs/Default
        fi

./main.py $1 create Questions/$1 $2 url "http://10.0.0.1:$2/"
echo "{
'session_deconnection':('!executable',),
'session_start': ('!executable',),
'session_stop': ('!executable',),
'session_duration':('!executable',),
'action_help':('!executable',),
'statmenu_bad':('!executable',),
'statmenu_smiley':('!executable',),
'statmenu_rank':('!executable',)}" >Students/$1/Logs/Default/acls
./main.py $1 admin thierry.excoffier admin olivier.gluck start &
}

create cs-nfs  4001
create cs-nis  4002
create cs-dns  4003
create cs-ldap 4004 

for I in nfs nis dns ldap ; do ./main.py cs-$I plot ; done
sleep 10
for I in nfs nis dns ldap ; do gv Students/cs-$I/HTML/xxx_graphe.ps & done



#####################################
PROBLEMS
#####################################

NIS : 4.1 configurer client NIS pas en broadcast ?

"""

from questions import *
from check import *


def q():
    import configuration
    return """<h2>TP : %s</h2>
    ATTENTION vous avez une heure pour modifier une réponse,
    vous le faites en passant par le travail fait.
    <p>
    Vous avez choisi le sujet : <big><b>%s</b></big>
    <p>
    Ce service web est conçu pour être utilisé facilement au clavier,
    la touche <tt>entrée</tt> permet de passer à la question suivante.
    <p>
    Avez-vous compris&nbsp;?""" % (configuration.session.name,
                                   configuration.session.name)



add(name="intro",
    question=q,
    tests = ( yes("Répondez OUI"), ),
    )

c = Choices("SIR", "SIRapp", "TIpro", "TIrechLyon1", "TIrechINSA")
add(name="formation",
    required = ["intro"],
    question="Vous êtes dans quelle formation" + c.html(),
    tests = c.test(),
    )

add(name="identité",
    required = ["intro"],
    question="Indiquez vos noms et prénoms.",
    nr_lines = 2,
    tests = (good_if_contains(''),),
    )

c = Choices("TPR1", "TPR2", "TPR3")
add(name="salle",
    required = ["intro"],
    question="Indiquez le nom de la salle dans laquelle vous êtes" + c.html(),
    tests = c.test(),
    )

c = Choices("1", "2", "3", "4")
add(name="séance",
    required = ["intro"],
    question="La séance de TP que vous êtes en train de faire" + c.html(),
    tests = c.test(),
    )


add(name="service",
    required=["séance", "salle", "identité", "formation"],
    question="Quel est le service rendu par le protocole que vous allez installer",
    nr_lines = 5,
    tests = (good_if_contains(''),),
    )

add(name="avantages",
    required=["service"],
    question="Quels sont les principaux avantages de ce service",
    nr_lines = 5,
    tests = (good_if_contains(''),),
    )

add(name="inconvénients",
    required=["service"],
    question="Quels sont les principaux inconvénients de ce service",
    nr_lines = 5,
    tests = (good_if_contains(''),),
    )
