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

from questions import *
from check import *
from configuration_salles import *

add(name="intro",
    before="""Le sujet du premier TP est à faire sur <b>deux séances</b>
    (6 heures).
    Vous devez impérativement rester sur le même poste pour la prochaine
    séance.
    En effet, <b>vos réponses dépendent du poste sur lequel vous êtes</b>.
    <p>
    Le but du TP est de faire un réseau
    qui a une topologie de boucle avec quelque routeurs.
    <p>
    Vous aprendrez à configurer les liaisons séries et ethernet
    des routeurs ainsi que de votre PC.
<!--
    <p>
    L'ensemble des réponses que vous allez donner seront analysées
    afin de définir votre note de TP, le calcul ressemblera à :
    <b>Soit les variables 'bonnes', 'mauvaises', 'indices' entre 0 et 1.
    La note de TP est égale à :  bonnes<sup>2</sup>*(20-6*mauvaises<sup>0.3</sup>-2*indices<sup>0.3</sup>).</b>
    En répondant à toutes les questions vous avez donc 12/20 au minimum.
    En répondant à la moitié des questions sans faire aucune erreur
    et sans demander d'indice, vous avez au mieux 5/20.
-->
<p><b>
A la fin de la deuxième séance, vous rendez les feuilles MANUSCRITES
sur lesquelles vous avez pris vos notes au cours des 2 séances de TP.
On ne vous demande pas un compte rendu de TP.
Vous serez noté en fonction de la pertinence de vos notes.
</b>

    <p>
    En dehors des séances vous ne pourrez plus continuer ce TP,
    vous avez donc tout intérêt à vous dépêcher.
    <p>
    Il y a des informations utiles dans le menu de gauche&nbsp;:
    <em>Aide/Explications</em>
    <p>
    ATTENTION, durant ce TP on configure peu à peu le réseau,
    chaque fois que vous avancez dans les questions c'est que le
    réseau est mieux configuré.
    Si par contre il y a une régression de configuration non prévue,
    comme un <em>reboot</em> ou un cable débranché,
    alors le questionnaire ne pourra la deviner et risque de vous
    compter des réponses fausses.
    
    """,
    question="Êtes-vous prêt pour l'aventure&nbsp;? Répondez OUI s'il vous plait.",
    tests = ( yes("Répondez OUI s'il vous plait"), ),
    good_answer = """Vous pouvez directement taper <tt>return</tt> pour
    voir la prochaine question.
    <p>
    Vous devez impérativement répondre immédiatement aux questions
    dont le nom est sur fond noir.
    <p>
    La question en caractères gras est celle qui débloque
    le plus de questions.""",
    )


add(name="stop",
    required=["hard:on off"],
    before = "Si le CISCO est allumé, éteignez-le.",
    question = "Le CISCO est-il éteint&nbsp;?",
    tests = (yes("Alors éteignez-le&nbsp;!"),),
    )

add(name="votre poste",
    required=['stop'],
    before="""Vous devez avoir sous les yeux le plan du réseau que
    vous allez configurer.
    <p>
    Sur les ordinateurs il y a une étiquette avec le nom de l'ordinateur,
    ce nom est composé d'une lettre (A-P) et d'un chiffre (1-3).
    <p>
    Sur le routeur associé à votre poste, vous trouverez
    le même nom préfixé par '<tt>R</tt>'
    et s'il y a un commutateur (<em>switch</em>)
    il est préfixé par '<tt>S</tt>'.
    """,
    question="""Quel est le nom indiqué sur l'étiquette collée
    sur votre ordinateur (pas routeur)&nbsp;?""",
    tests=(
    answer_length_is(2, "La réponse est sur 2 caractères"),
    good("{name}", parse_strings=host, uppercase=True),
    ),
    )

add(name="nom routeur",
    required=['votre poste', 'terminal:quitter'],
    question="""Quel nom devrez-vous donner à votre routeur&nbsp;?
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
                    respecter la casse (différence majuscule/minuscule)""")),
        ),
    good_answer = """Vérifiez bien que le routeur posé à coté
    de votre ordinateur porte bien ce nom.
    Si ce n'est pas le cas, trouvez le bon routeur et mettez le
    à sa place.""",
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
    indices = ( """C'est la même commande que sous Unix.""",
                """En anglais c'est «nom de l'hôte»"""),
    )

add(name="nouveau prompt",
    required=['change nom'],
    before=en_mode_config,
    question="Quel est le <em>prompt</em>&nbsp;?",
    tests = (
    good('{C0.remote_port.host.name}(config)#', parse_strings=host),
    good('Router(config)#', "Vous n'avez pas changé le nom du routeur"),
    ),
    highlight = True,
    )

add(name="arrêt marche",
    required=['nouveau prompt'],
    before="""
    <ul>
    <li> Éteignez physiquement le routeur.
    <li> Attendez 5 secondes.
    <li> Allumez-le.
    <li> Répondez <tt>no</tt> s'il demande si vous voulez entrer
    dans le dialogue de configuration initial.
    </ul>
    <p>
    Attendez qu'il redémarre puis faites apparaître le <em>prompt</em>
    en tapant plusieurs fois sur la touche <tt>Return</tt>.
    """,
    question="Quel est le <em>prompt</em>&nbsp;?",
    tests = (
    bad('Router', 'Je pense que vous avez oublié un caractère...'),
    good('Router>'),
    good('Router#', 'On ne vous a pas demande de faire <tt>enable</tt>...'),
    ),
    bad_answer = """Cette situation est absolument impossible.
    <p>
    Ou vous n'avez pas lu et fait ce qui est expliqué
    dans «<em>avant de répondre</em>».
    <p>
    Ou vous avez sauvegardé la configuration sans que l'on
    vous l'ai demandé.
    <p>
    Ou le <em>prompt</em> n'était pas égal à <tt>Router&gt;</tt>
    la première fois que vous avez démarré le routeur.
    Dans ce cas, vous avez menti en répondant au questionnaire.
    <p>
    """,
    )

add(name="sauve config",
    required=['doc:intro', 'arrêt marche', 'change nom'],
    before="""Remettez le bon nom au routeur.""",
    # et refaites  <tt>no ip domain lookup</tt>""",
    question="""Que tapez-vous pour sauvegarder la configuration
    en cours d'utilisation dans la configuration qui sera
    utilisée au démarrage&nbsp;?""",
    tests = (
    good("copy running-config startup-config"),
    bad('copy', "Le routeur vous dit que la commande est incomplète"),
    bad("copy running-config", "Il faut indiquez où vous sauvez"),
    reject("copy running-config ",
        """Si vous copiez ailleurs que dans <tt>startup-config</tt>
        la configuration ne sera pas lue au démarrage"""),
    expect('copy'),
    expect('startup-config'),
    expect('running-config'),
    ),
    indices = (
    """La commande fait une <b>copie</b> de la configuration courante qui
    est en train de fonctionner dans la configuration qui sera
    utilisée lors du démarrage du routeur""",
    """La commande est <tt>copy</tt>""",
    ),
    good_answer = """Attention :
    <ul>
    <li> vous ne devez en aucun cas éteindre le routeur pendant la sauvegarde.
    <li> vous ne devez pas faire de sauvegarde après avoir mis un mot de passe.
    </ul>
    <p>
    Si le registre de configuration vaut <tt>0x2142</tt>
    alors au prochain démarrage votre configuration ne sera
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
    le bon nom à l'adresse IP de votre ordinateur&nbsp;?
    <p>
    <b>Respectez la casse pour le nom de la machine.</b>
    """,
    tests=(
    require_startswith("ip ", "On utilise la commande <tt>ip</tt>"),
    require_startswith("ip host",
                       """On utilise le paramètre <tt>host</tt> de
                       la commande <tt>ip</tt>"""),
    require("{name}", "Je ne vois pas le petit nom de votre machine.",
            parse_strings=host),
    require("{E0.port.ip}", "Je ne vois pas l'adresse IP de votre machine.",
            parse_strings=host),
    good("ip host {name} {E0.port.ip}", parse_strings=host),
    bad("ip host {E0.port.ip} {name}",
        "L'ordre des paramètres est important...", parse_strings=host),
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
        "Ce fichier donne un nom à votre machine, pas votre routeur"),
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
              "tp1_route:connectées", "tp1_route:arp nombre",
              ],
    question="""Redémarrez votre ordinateur sous windows,
    et configurez les interfaces réseaux windows pour
    que votre ordinateur puisse pinguer les autres routeurs.
    <p>
    Répondez OUI à cette question en étant sous Windows
    et quand tout fonctionnera.""",
    tests = ( yes("Répondez OUI"), ),
    )





    
