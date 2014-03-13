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

add(name="version",
    required=['cli:show liste'],
    question="""Quelle est la version de l'IOS que vous utilisez&nbsp;?
    <p>
    Elle est de la forme <tt>???.???(???)</tt> avec peut être des caractères
    derrière.
    """,
    tests = (
    #good_if_contains("{C0.remote_port.host.version_IOS}", parse_strings=host),
    HostCiscoIOS(),
    reject("{C0.remote_port.host.version_bootstrap}",
        """Non c'est la version du programme qui charge l'IOS
        dans la mémoire du routeur&nbsp;: c'est l'équivalent
        du LILO/GRUB.""", parse_strings=host),        
    ),
    indices = ( """Évidemment, pour trouver cette information
    on utilise <tt>show</tt> et le bon paramètre""", ),
    )

add(name="register",
    required=['version', 'cli:show liste', 'doc:intro'],
    question="Quelle est la valeur actuelle du registre de configuration de votre routeur&nbsp;?",
    tests=(
    require('0x', """La valeur du registre est en hexadécimal
            et commence donc par '0x'"""),
    good("{C0.remote_port.host.conf_register}",
         "C'est la valeur standard du registre",
         parse_strings=host,
         ),
    good("{C0.remote_port.host.conf_register2}",
         """ATTENTION, avec cette valeur de registre, le routeur ne
         lira pas le fichier de configuration au démarrage et redémarrera
         vierge à chaque démarrage.
         <p>
         La valeur normale du registre est <tt>0x2102</tt>
         """,
         parse_strings=host),
    ),
    indices = ( """C'est affiché avec la même commande que celle
    qui vous a permis de trouver la version""", )
    )



add(name="minicom",
    required=['cli:line parameters'],
    question="""Quelle séquence de touches utilisez-vous
    pour envoyer un <tt>break</tt> avec <tt>minicom</tt>&nbsp;?""",
    tests=(
    require('F', uppercase=True),
    good_if_contains(''),
    ),
    )
    

# add(name="rommon",
#     required=['minicom', 'tp1:final'], # 'register'],
#     before="""<b>NE FAITES CETTE QUESTION QUE POUR EFFACER UN MOT DE PASSE.
#     Si vous essayez de répondre à cette question alors qu'il n'y
#     a pas de mot de passe qui vous empêche de faire le TP
#     vous êtes en train de perdre votre temps.</b>
#     <p>
#     Faites les choses suivantes&nbsp;:
#     <ul>
#     <li> Éteignez physiquement le routeur CISCO.
#     <li> Attendez 5 secondes.
#     <li> Allumer le routeur CISCO.
#     <li> Envoyer un <tt>break</tt> en tapant CTRL-A Z F dans minicom.
#     </ul>
#     Le <em>prompt</em> devrait arriver immédiatement.
#     """,
#     question="""Quel est le <em>prompt</em>&nbsp;?""",
#     tests=(
#     require('1', "On vous demande le premier prompt à s'être affiché"),
#     good("rommon 1 >"),
#     good("rommon1>", "Il faut respecter les espaces... vous ne l'avez pas fait dans cette réponse.",
#          replace=( (' ',''), )),
#     ),
#     )
# 

# add(name="effacer passwd",
#     required=['rommon'],
#     before="""Ceci n'est pas une question à laquelle vous devez répondre.
#     C'est simplement une aide pour effacer un mot de passe.""",
#     question=effacer_password,
#     tests=(
#     reject("", "Ceci n'est pas une question, il n'y a aucune réponse autorisée"),
#     ),
#     )
# 


 



    



