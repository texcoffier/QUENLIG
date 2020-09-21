# -*- coding: latin-1 -*-
#    QUENLIG: Questionnaire en ligne (Online interactive tutorial)
#    Copyright (C) 2007-2008 Thierry EXCOFFIER, Universite Claude Bernard
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

add(name="intro",
    before="""Le sujet du premier TP est � faire sur <b>deux s�ances</b>
    (6 heures).
    Vous devez imp�rativement rester sur le m�me poste pour la prochaine
    s�ance.
    En effet, <b>vos r�ponses d�pendent du poste sur lequel vous �tes</b>.
    <p>
    Le but du TP est de faire un r�seau
    qui a une topologie de boucle avec quelque routeurs.
    <p>
    Vous aprendrez � configurer les liaisons s�ries et ethernet
    des routeurs ainsi que de votre PC.
<!--
    <p>
    L'ensemble des r�ponses que vous allez donner seront analys�es
    afin de d�finir votre note de TP, le calcul ressemblera � :
    <b>Soit les variables 'bonnes', 'mauvaises', 'indices' entre 0 et 1.
    La note de TP est �gale � :  bonnes<sup>2</sup>*(20-6*mauvaises<sup>0.3</sup>-2*indices<sup>0.3</sup>).</b>
    En r�pondant � toutes les questions vous avez donc 12/20 au minimum.
    En r�pondant � la moiti� des questions sans faire aucune erreur
    et sans demander d'indice, vous avez au mieux 5/20.
-->
<!--
<p><b>
A la fin de la deuxi�me s�ance, vous rendez les feuilles MANUSCRITES
sur lesquelles vous avez pris vos notes au cours des 2 s�ances de TP.
On ne vous demande pas un compte rendu de TP.
Vous serez not� en fonction de la pertinence de vos notes.
</b>
-->

    <p>
    En dehors des s�ances vous ne pourrez plus continuer ce TP,
    vous avez donc tout int�r�t � vous d�p�cher.
    <p>
    Il y a des informations utiles dans le menu de gauche&nbsp;:
    <em>Aide/Explications</em>
    <p>
    ATTENTION, durant ce TP on configure peu � peu le r�seau,
    chaque fois que vous avancez dans les questions c'est que le
    r�seau est mieux configur�.
    Si par contre il y a une r�gression de configuration non pr�vue,
    comme un <em>reboot</em> ou un cable d�branch�,
    alors le questionnaire ne pourra la deviner et risque de vous
    compter des r�ponses fausses.
    
    """,
    question="�tes-vous pr�t pour l'aventure&nbsp;? R�pondez OUI s'il vous plait.",
    tests = ( yes("R�pondez OUI s'il vous plait"), ),
    good_answer = """Vous pouvez directement taper <tt>return</tt> pour
    voir la prochaine question.
    <p>
    Vous devez imp�rativement r�pondre imm�diatement aux questions
    dont le nom est sur fond noir.
    <p>
    La question en caract�res gras est celle qui d�bloque
    le plus de questions.""",
    )


add(name="stop",
    required=["hard:on off"],
    before = "Si le CISCO est allum�, �teignez-le.",
    question = "Le CISCO est-il �teint&nbsp;?",
    tests = (yes("Alors �teignez-le&nbsp;!"),),
    )

add(name="votre poste",
    required=['stop'],
    before="""Vous devez avoir sous les yeux le plan du r�seau que
    vous allez configurer.
    <p>
    Sur les ordinateurs il y a une �tiquette avec le nom de l'ordinateur,
    ce nom est compos� d'une lettre (A-P) et d'un chiffre (1-3).
    <p>
    Sur le routeur associ� � votre poste, vous trouverez
    le m�me nom pr�fix� par '<tt>R</tt>'
    et s'il y a un commutateur (<em>switch</em>)
    il est pr�fix� par '<tt>S</tt>'.
    """,
    question="""Quel est le nom indiqu� sur l'�tiquette coll�e
    sur votre ordinateur (pas routeur)&nbsp;?""",
    tests=(
    answer_length_is(2, "La r�ponse est sur 2 caract�res"),
    good("{name}", parse_strings=host, uppercase=True),
    ),
    )

add(name="nom routeur",
    required=['votre poste', 'terminal:quitter'],
    question="""Quel nom devrez-vous donner � votre routeur&nbsp;?
    <p>
    Sur le plan il y a une liaison console entre votre PC
    et votre routeur.
    <p>
    <b>Respectez la casse.</b>
    """,
    tests = (
        good("{C0.remote_port.host.name}", parse_strings=host),
        Bad(Comment(HostReplace(UpperCase(Equal('{C0.remote_port.host.name}'))),
                    """Dans la question, en <b>gras</b> on vous dit de
                    respecter la casse (diff�rence majuscule/minuscule)""")),
        ),
    good_answer = """V�rifiez bien que le routeur pos� � cot�
    de votre ordinateur porte bien ce nom.
    Si ce n'est pas le cas, trouvez le bon routeur et mettez le
    � sa place.""",
    )

    
add(name="change nom",
    required=['serie:prompt', 'nom routeur'],
    before=en_mode_config + "<p>Regardez le nom du routeur sur le plan.",
    question="""Que tapez-vous pour mettre le bon nom au routeur&nbsp;?""",
    tests = (
    require('{C0.remote_port.host.name}',
            "Je ne vois pas le nom de votre routeur", parse_strings=host),
    require('host', 'La commande commence par <tt>host</tt>'),
    good('hostname {C0.remote_port.host.name}', parse_strings=host),
    ),
    good_answer = "Lancez la commande pour changer le nom.",
    indices = ( """C'est la m�me commande que sous Unix.""",
                """En anglais c'est �nom de l'h�te�"""),
    )

add(name="nouveau prompt",
    required=['change nom'],
    before=en_mode_config,
    question="Quel est le <em>prompt</em>&nbsp;?",
    tests = (
    good('{C0.remote_port.host.name}(config)#', parse_strings=host),
    good('Router(config)#', "Vous n'aviez pas chang� le nom du routeur. Faites-le maintenant !"),
    ),
    highlight = True,
    )

add(name="arr�t marche",
    required=['nouveau prompt'],
    before="""
    <ul>
    <li> �teignez physiquement le routeur.
    <li> Attendez 5 secondes.
    <li> Allumez-le.
    <li> R�pondez <tt>no</tt> s'il demande si vous voulez entrer
    dans le dialogue de configuration initial.
    </ul>
    <p>
    Attendez qu'il red�marre puis faites appara�tre le <em>prompt</em>
    en tapant plusieurs fois sur la touche <tt>Return</tt>.
    """,
    question="Quel est le <em>prompt</em>&nbsp;?",
    tests = (
    bad('Router', 'Je pense que vous avez oubli� un caract�re...'),
    good('Router>'),
    good('Router#', 'On ne vous a pas demande de faire <tt>enable</tt>...'),
    ),
    bad_answer = """Cette situation est absolument impossible.
    <p>
    Ou vous n'avez pas lu et fait ce qui est expliqu�
    dans �<em>avant de r�pondre</em>�.
    <p>
    Ou vous avez sauvegard� la configuration sans que l'on
    vous l'ai demand�.
    <p>
    Ou le <em>prompt</em> n'�tait pas �gal � <tt>Router&gt;</tt>
    la premi�re fois que vous avez d�marr� le routeur.
    Dans ce cas, vous avez menti en r�pondant au questionnaire.
    <p>
    """,
    )

add(name="sauve config",
    required=['doc:intro', 'arr�t marche', 'change nom'],
    before="""Remettez le bon nom au routeur.""",
    # et refaites  <tt>no ip domain lookup</tt>""",
    question="""Que tapez-vous pour sauvegarder la configuration
    en cours d'utilisation dans la configuration qui sera
    utilis�e au d�marrage&nbsp;?""",
    tests = (
    good("copy running-config startup-config"),
    bad('copy', "Le routeur vous dit que la commande est incompl�te"),
    bad("copy running-config", "Il faut indiquez o� vous sauvez"),
    reject("copy running-config ",
        """Si vous copiez ailleurs que dans <tt>startup-config</tt>
        la configuration ne sera pas lue au d�marrage"""),
    expect('copy'),
    expect('startup-config'),
    expect('running-config'),
    ),
    indices = (
    """La commande fait une <b>copie</b> de la configuration courante qui
    est en train de fonctionner dans la configuration qui sera
    utilis�e lors du d�marrage du routeur""",
    """La commande est <tt>copy</tt>""",
    ),
    good_answer = """Attention :
    <ul>
    <li> vous ne devez en aucun cas �teindre le routeur pendant la sauvegarde.
    <li> vous ne devez pas faire de sauvegarde apr�s avoir mis un mot de passe.
    </ul>
    <p>
    Si le registre de configuration vaut <tt>0x2142</tt>
    alors au prochain d�marrage votre configuration ne sera
    pas prise en compte.
    <p>
    Pour changer le registre de configuration et qu'il permette
    la lecture de votre configuration, il faut taper&nbsp;:
<pre>
configure terminal 
config-register 0x2102
</pre>
    """,
    )

add(name="routeur nomme machine",
    required=["tp1_eth:config pc eth", "votre poste", "tp1_route:les routes"],
    question="""Quelle commande tapez-vous dans le routeur pour associer
    le bon nom � l'adresse IP de votre ordinateur&nbsp;?
    <p>
    <b>Respectez la casse pour le nom de la machine.</b>
    """,
    tests=(
    require_startswith("ip ", "On utilise la commande <tt>ip</tt>"),
    require_startswith("ip host",
                       """On utilise le param�tre <tt>host</tt> de
                       la commande <tt>ip</tt>"""),
    require("{name}", "Je ne vois pas le petit nom de votre machine.",
            parse_strings=host),
    require("{E0.port.ip}", "Je ne vois pas l'adresse IP de votre machine.",
            parse_strings=host),
    good("ip host {name} {E0.port.ip}", parse_strings=host),
    bad("ip host {E0.port.ip} {name}",
        "L'ordre des param�tres est important...", parse_strings=host),
    ),
    )

add(name="machine nomme routeur",
    required=["tp1_route:les routes"],
    question="""Quel fichier modifiez-vous sous unix pour
    donner un petit nom au routeur&nbsp;?
    <p>
    Donnez le nom absolu.
    """,
    tests=(
    require_startswith("/", "Un nom absolu commence par '/'"),
    require_startswith("/etc", "Le fichier est dans <tt>/etc</tt>"),
    good("/etc/hosts"),
    bad("/etc/hostname",
        "Ce fichier donne un nom � votre machine, pas votre routeur"),
    ),
    )

add(name="AVANT DE PARTIR",
    required=["sauve config"],
    question=avant_de_partir,
    )


add(name="final",
    required=["hard:flash", "terminal:password console",
              "terminal:combien", "tp1_route:arp nombre",
              "machine nomme routeur", "routeur nomme machine",
              "tp1_route:statiques", "tp1_route:combien",
              "tp1_route:connect�es", "tp1_route:arp nombre",
              ],
    question="""Red�marrez votre ordinateur sous windows,
    et configurez les interfaces r�seaux windows pour
    que votre ordinateur puisse pinguer les autres routeurs.
    <p>
    R�pondez OUI � cette question en �tant sous Windows
    et quand tout fonctionnera.""",
    tests = ( yes("R�pondez OUI"), ),
    )





    
