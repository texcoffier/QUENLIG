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

add(name="cable console",
    required=['hard:console eth'],
    before="""Un cable bleu ciel doit relier votre ordinateur
    au routeur CISCO.
    Il permet de communiquer avec le routeur alors que celui-ci n'est
    pas encore configuré (il n'a pas d'accès réseau).
    <ul>
    <li> Sur l'ordinateur il est branché sur la RS232C,
    qui est une prise <a href="http://fr.wikipedia.org/wiki/Image:Sub-D_male_9p.jpg">DB9</a> qui contient 9 broches sur 2 rangées.
    La première sortie RS232C s'appelle <tt>/dev/ttyS0</tt> sous Linux
    et <tt>COM1</tt> sous windows.
    <p>
    <b>S'il y a 2 connecteurs RS232C à l'arrière du PC,
    alors utilisez celui qui a une étiquette CE.</b>
    </li>
    <li> sur le routeur CISCO, il est branché sur la RS232C,
    qui est une prise RJ45 <b>à ne pas confondre avec une prise Ethernet</b>.
    Le mot <em>console</em> est écrit à coté du connecteur.
    </li>
    </ul>
    <p>
    Une liaison série (RS232C) permet d'avoir un flux d'octet bidirectionnel
    entre les 2 machines.
    <p>
    Historiquement, un <b>terminal</b> était la composition d'un <b>écran</b>
    qui affichait ce que la liaison série envoyait et
    tout ce qui était tapé au <b>clavier</b> était envoyé sur
    la liaison série.
    <p>
    L'abbréviation TTY désigne <em>teletype</em>.
    <ul>
    <li> <tt>/dev/ttyS0</tt> : Première liaison série.</li>
    <li> <tt>/dev/tty0</tt> : Première console texte.</li>
    <li> <tt>/dev/pts/0</tt> : Première TTY virtuelle
    (pour la fenêtre terminal par exemple)</li>
    </ul>
    """,
    question = """Répondez OUI quand le cable sera correctement branché.""",
    tests = (yes("Alors branchez-le&nbsp;!"),),
    )


add(name="minicom",
    required=['cable console'],
    before="""
    Il faut lancer une application sur l'ordinateur qui
    permet de faire comme si l'on avait branché un terminal
    sur le routeur CISCO.
    <p>
    Techniquement cette application fait un peu mieux que&nbsp;:
    <ul>
    <li> <tt>stty /dev/ttyS0 9600</tt> : Configuration de la liaison série.
    <li> <tt>cat /dev/ttyS0 &amp;</tt> : Affichage de ce que le routeur CISCO envoie.
    <li> <tt>cat &gt;/dev/ttyS0</tt> : Envoi de ce qui est tapé au clavier au routeur CISCO</li>
    </ul>
    <p>
    L'application que vous devez utiliser est <tt>minicom</tt>.
    <p>
    Si <tt>minicom</tt> proteste à cause d'un verrou et qu'il
    est lancé une seule fois alors détruisez le verrou (<tt>/var/lock/...</tt>)
    <p>
    <b>En cas d'interdiction d'accès, passez <tt>root</tt>
       avant de lancer minicom</b>
    """,
    question = """Ouvrez un terminal et lancez <tt>minicom -D /dev/ttyS1</tt>.
    Que devez-vous taper pour avoir l'aide sur <tt>minicom</tt>&nbsp;?
    <p>
    Attention : ne lancez pas <tt>minicom</tt> en arrière plan,
    il a besoin d'utiliser le clavier et l'écran.
    <p>
    Attention : la réponse attendue n'est pas <tt>man minicom</tt> ni
    <tt>minicom --help</tt>
    """,
    tests = (
    reject('man', """On veut l'aide en ligne du logiciel, pas sa
    page de manuel. Si vous venez de lancer <tt>minicom</tt> la
    réponse est écrite sous yeux."""),
    require( ('A', 'Z', 'CTRL'),
             """Je ne trouve pas tous les éléments de la réponse.
             Faites un copié/collé de la séquence de caractères.""",
             uppercase=True),
    good_if_contains( '' ),
    ),
    indices = ("""La réponse est affichée par <tt>minicom</tt>
    quand vous le lancez.""", ),

    )



add(name="minicom parameters",
    required=['minicom'],
    question = """Que tapez-vous dans <tt>minicom</tt>
    pour faire apparaître le menu vous permettant
    de configurer la vitesse de la ligne, la parité,
    le nombre de bits de données, ...""",
    tests = (
    reject('O',
           """Ce menu est un menu général de configuration,
           ce n'est pas le menu <tt>Comm parameters</tt>""",
           uppercase=True),
    require('P', """C'est dans le menu <em>Comm parameters</em> de la
    page d'aide de <tt>minicom</tt>""",
            uppercase=True),
    
    good_if_contains( '' ),
    ),
    )



add(name="line parameters",
    required=['minicom parameters'],
    question = """Configurez la ligne série avec
    une vitesse de 9600 baud, 8 bits de données et 1 stop bit.
    <p>
    Répondez OUI si c'est fait.""",
    tests = (yes("Alors configurez-la correctement&nbsp;!"),),
    )



add(name="allumer CISCO",
    required=['line parameters', 'tp1:stop'],
    before = """Maintenant vous devez pouvoir communiquer avec le routeur CISCO.
    <p>
    Allumez le routeur CISCO.
    <p>
    Des messages de démarrage doivent défiler.
    <p>
    Si le routeur pose la question <em>«Do you want to enter the inital configuration dialog&nbsp;?»</em>
    répondez «no» pour qu'il s'initialise tout seul sans poser de questions.
    <p>
    Si le routeur pose la question <em>«Terminate auto-install&nbsp;?»</em>
    répondez «yes» pour qu'il s'initialise tout seul sans poser de questions.
    <p>
    Quand la procédure de démarrage semble terminée, tapez plusieurs
    fois sur <tt>return</tt> pour voir ce que le routeur CISCO répond.
    <p>
    Si un mot de passe est demandé et que vous ne le trouvez pas,
    suivez la procédure d'effacement de mot de passe indiquée
    dans la page d'aide/explication du menu de gauche.
    """,
    question = """Quel est le prompt (l'invite de commande)&nbsp;?""",
    tests = (
    # Anglais
    good('Router>'),
    bad('router>', "Vous n'auriez pas oublié une majuscule&nbsp;?"),
    bad('Router' , "Vous n'auriez pas oublié un caractère&nbsp;?"),
    bad('router' , "On veut la chaine de caractère exacte."),
    # Français
    bad(('routeur>', 'Routeur>'),
        "Vous avez mal lu... vous l'avez traduit en français"),
    bad(('Routeur', 'Routeur'),
        "Vous avez traduit et en plus vous avez oublié un caractère&nbsp;!"),
    reject('UPDOWN', "Cela ne ressemble pas à un <em>prompt</em>"),
    
    reject('rommon', """Votre routeur a perdu son système&nbsp;?
Faites un arrêt marche et si le prompt est le même
suivez la procédure indiquée dans la page d'aide/explication du menu de gauche."""),
    require('jamaisimpossible',
        """Les étudiants du TP précédents n'ont pas fait le ménage avant
        de terminer le TP.
        Suivez la procédure d'effacement de configuration indiquée
    dans la page d'aide/explication du menu de gauche.
    """),
    
    ),
    indices = (reinit, ),

    )

add(name="initialiser",
    required=['allumer CISCO'],
    before="""Ce sujet de TP suppose que votre routeur est vierge
    de toute configuration.
    Pour être certain de ce fait nous allons effacer sa configuration.
    <p>
    <b>Si vous avez déjà effacé la configuration alors
    ne le refaites pas</b>.
    """,
    question="""
      Si durant la procédure on vous demande un mot de passe,
      essayez """ + mots_de_passe + """
    <p>
      Voici la liste de choses à taper (ne faites pas un copier/coller
      de l'ensemble des lignes).
      Faites néanmoins attention aux questions
      que le routeur vous pose.
      """ + procedure_effacement + """
      <p>
      Quand la procédure est terminée, répondez OUI à cette question.
    """,
    tests = ( yes("Répondez OUI s'il vous plait"), ),
    )

add(name="aide commande",
    required=['initialiser'],
    before = """Quand vous tapez une commande, vous pouvez à n'importe
    quel moment taper un point d'interrogation pour obtenir&nbsp;:
    <ul>
    <li> La liste des noms de commandes/paramètres qui commencent
    par le mot que vous avez commencé à taper&nbsp;;</li>
    <li> La syntaxe de la commande si son nom est complet&nbsp;;</li>
    <li> Les paramètres possibles si vous avez commencé à taper
    un nom de paramètre&nbsp;;</li>
    <li> Les valeurs possibles pour un paramètre si le nom
    du paramètre est complet.</li>
    </ul>
    <p>ATTENTION : si votre prompt se termine par '#' vous devez
    taper 'exit' pour revenir dans un mode normal.
""",
    question = "Combien de commandes ont un nom qui commence par 's'&nbsp;?",
    tests = (
    require_int(),
    good("3"),
    good("4"),
    bad("5", """Non, il y a la même commande deux fois.
    En effet <tt>*s=show</tt> indique que vous pouvez taper <tt>s</tt>
    au lieu de <tt>show</tt>"""),
    ),
    good_answer = """ATTENTION : dans certains cas des commandes
    existantes et expliquées dans la documentation n'apparaissent
    pas de la liste fournie par le point d'interrogation""",
    )
    


add(name="? seul",
    required=['aide commande'],
    question = """Si vous tapez un '?' seul comme commande,
    voyez-vous la commande <tt>configure</tt>&nbsp;?""",
    tests = (no("""Si vous la voyez c'est que vous êtes passé en mode
    privilégié sans que l'on vous l'ai demandé"""),
             ),
    good_answer = """On ne voit pas cette commande car elle est
    accessible seulement en mode privilégié""",
    )



add(name="voir",
    required=['aide commande', 'doc:intro'],
    before="""<b>Attention, pour la suite des TP seuls les noms
    complets de commande seront acceptés, aucune abréviation
    que cela soit pour les commandes et les paramètres ne sera acceptée</b>.\n""",
    question="""À votre avis, quelle est la <b>commande</b> (n'indiquez
    pas les paramètres) vous permettant
    d'avoir des informations sur le routeur quelque soit le type
    d'informations que l'on désire voir&nbsp;?""",
    tests = (
    reject(" ", "Le nom de la commande sans paramètres s'il vous plait."),
    Bad(Comment(Equal('systat'),
                """Utilisez la commande, vous verrez que cela ne permet
                pas de faire grand chose""")),
    bad(('s','sh','sho'), "Aucune abréviation n'est autorisée."),
    good("show"),
    ),
    )



add(name="show",
    required=['aide commande', 'voir'],
    before="""Deux moyens pour répondre à cette question&nbsp;:
    <ul>
    <li> Essayer bêtement.
    <li> Ou faire lister les premiers paramètres possibles en utilisant
    le point d'interrogation comme premier paramètre.
    </ul>""",
    question="La commande <tt>show</tt> prend-elle des paramètres&nbsp;?",
    tests = ( yes("Vous n'avez pas essayé&nbsp;?"), ),
    )


add(name="copié collé",
    required=['show'],
    before="""Faites un copié/collé des 3 commandes suivantes sur le routeur (sans oublier d'exécuter la dernière commande)&nbsp;:
    <pre>show clock
show hardware
show history</pre>""",
    question="""Qu'elle est la dernière ligne affichée par le routeur
    (à part l'invite de commande)&nbsp;?""",
    tests = (
    reject('Configuration register',
           "Vous avez oublié d'exécuter la dernière commande"),
    good("show history"),
    good("how history",
        """Il y a actuellement un bug avec le copié/collé.
        Nous ne savons pas d'ou il vient,
        certainement du contrôle de flux sur la RS232C.
        <p>
        Exécutez <tt>show history</tt> pour voir ce que cela fait.
        """),
    ),
    )


add(name="commande incomplète",
    required=['show'],
    question = """Est-ce que c'est bien <tt>show</tt>
    qui s'exécute si vous tapez <tt>sho clock</tt>
    au lieu de <tt>show clock</tt>&nbsp;?""",
    tests = ( yes("Montrez cela à un enseignant"), ),
    good_answer = """Cela fonctionne car vous avez tapez suffisemment
    de lettres de la commande pour qu'il n'y ai pas d'ambiguïté.
    Cette pratique est déconseillée quand on fait des scripts.
    <p>
    <b>DANS LA SUITE DU TP, TOUTE COMMANDE INCOMPLÈTE SERA REFUSÉE</b>
    """,
    )
    


add(name="édition ligne",
    required=['show'],
    before="""Sur la ligne de commande du routeur,
    tapez 'shw version' sans valider par <tt>Return</tt>
    puis modifiez la ligne de commande afin
    de transformer la ligne en <tt>show version</tt> en utilisant
    les touches curseur <b>sans utiliser le <em>backspace</em></b>.
    <p>
    <img src="clavier.png" align="left">
    Jaune : le backspace<br>
    Orange : Carriage Return<br>
    Bleu : Flèche curseur gauche
    """,
    question="Est-ce que vous pouvez le faire&nbsp;?",
    tests = ( yes("Montrez cela à un enseignant"), ),
    )



add(name="show liste",
    required=['aide commande', 'show'],
    before="""Le premier paramètre de la commande <tt>show</tt>
    permet de choisir ce que l'on peut voir.
    Faites afficher l'ensemble des possibilités pour
    ce premier paramètre.""",
    question = """Combien de premiers paramètres possibles
    commencent par la lettre 'h'&nbsp;?""",
    tests = ( require_int(),
              good("4"),
              good("3"),
              good("2"), # Anciens IOS
              ),
    )

add(name="mauvaise commande",
    required=['tp1_eth:config ethernet'],
    before="""Lancez la commande&nbsp;: <tt>coucou</tt>.
    <p>
    Comme cela n'est pas une commande, le routeur considère que
    c'est le nom d'une machine.
    Il commence donc par essayer de trouver son adresse IP.
    il essaie 3 fois.
    """,
    question="""Sans éteindre le routeur, arrivez-vous à arrêter
    le processus de recherche&nbsp;?
    <p>
    Répondez :
    <ul>
    <li> NON si vous n'y arrivez pas.
    <li> comment vous avez fait si vous y arrivez.
    </ul>
    <p>
    <small>
    Si jamais la recherche est instantanée et que
    le <em>prompt</em> revient tout de suite alors répondez NON
    à la question. Cela veut dire que votre routeur n'a
    pas la configuration par défaut.

    """,
    tests = (
        Good(Comment(UpperCase(Contain('CTRL') &
                               ( Contain('SHFT') | Contain('SHIFT') ) &
                               Contain('6')),
                     """En fait vous venez d'envoyer le caractère Contrôle-^
                     de code ASCII 0x5E""" 
                     )
             ),
        Good(UpperCase(Contain('^^')
                       | (Contain('CTRL') & Contain('^')))),
        no("Montrez comment vous avez fait à un enseignant"),
        ),
    )

add(name="historique",
    required=['édition ligne', 'copié collé'],
    question="""Pouvez-vous utiliser la flèche curseur vers le haut
    pour revenir dans l'historique et éditer d'anciennes commandes&nbsp;?""",
    tests = ( yes("Réessayez"), ),
    )


add(name="fin édition",
    required=['historique', 'commande incomplète', '? seul', 'show liste'], # 'mauvaise commande',
    before = """La réponse à cette question n'est pas liée à <tt>minicom</tt>
    de plus elle fonctionne sur tous les terminaux virtuels et sur
    la console Linux.""",
    question="""Sans utiliser la souris et l'ascenseur,
    que tapez-vous au clavier pour voir ce qui a défilé au dessus
    de l'écran&nbsp;?""",
    tests = (
    Bad(Comment(Equal('history'),
                """On ne vous demande pas de faire afficher quelque chose
                de nouveau sur l'écran.
                On veut voir ce qui a déjà été affiché et qui est
                sortie par le haut...""")),
    reject('9', """Le chiffre 9 ne m'intéresse pas, ce qu'il faut
    indiquer est la fonction associée à la touche."""),
    require(('SHIFT', 'SHFT', 'MAJ'), uppercase=True, all_agree=True),
    require(('PAGE', 'PG', 'CTRL'), uppercase=True, all_agree=True),
    require(('UP', 'HAUT', 'PRECEDENTE', 'PRÉCÉDENTE'), uppercase=True, all_agree=True),
    # Fait planter
    # require(('B', 'U'), "Ceci ne fonctionne que dans <tt>minicom</tt>", uppercase=True),
    good_if_contains(''),
    ),
    indices = (
    """C'est <tt>shift + page up</tt>""",
    ),
    )
