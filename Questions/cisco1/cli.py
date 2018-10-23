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

add(name="cable console",
    required=['hard:console eth'],
    before="""Un c�ble bleu ciel doit relier votre ordinateur
    au routeur CISCO.
    Il permet de communiquer avec le routeur alors que celui-ci n'est
    pas encore configur� (il n'a pas d'acc�s r�seau).
    <ul>
    <li> Sur l'ordinateur il est branch� sur la RS232C,
    qui est une prise <a href="http://fr.wikipedia.org/wiki/Image:Sub-D_male_9p.jpg">DB9</a> qui contient 9 broches sur 2 rang�es.
    La premi�re sortie RS232C s'appelle <tt>/dev/ttyS0</tt> sous Linux
    et <tt>COM1</tt> sous windows.
    <p>
    <b>Il y a 2 connecteurs RS232C � l'arri�re du PC,
    utilisez celui qui est sur la carte m�re.</b>
    </li>
    <li> Sur le routeur CISCO, il est branch� sur la RS232C,
    qui est une prise RJ45 <b>� ne pas confondre avec une prise Ethernet</b>.
    Le mot <em>console</em> est �crit � cot� du connecteur.
    </li>
    </ul>
    <p>
    Une liaison s�rie (RS232C) permet d'avoir un flux d'octet bidirectionnel
    entre les 2 machines.
    <p>
    Historiquement, un <b>terminal</b> �tait la composition d'un <b>�cran</b>
    qui affichait ce que la liaison s�rie envoyait et
    tout ce qui �tait tap� au <b>clavier</b> �tait envoy� sur
    la liaison s�rie.
    <p>
    L'abbr�viation TTY d�signe <em>teletype</em>.
    <ul>
    <li> <tt>/dev/ttyS0</tt> : Premi�re liaison s�rie.</li>
    <li> <tt>/dev/tty0</tt> : Premi�re console texte.</li>
    <li> <tt>/dev/pts/0</tt> : Premi�re TTY virtuelle
    (pour la fen�tre terminal par exemple)</li>
    </ul>
    """,
    question = """R�pondez OUI quand le c�ble sera correctement branch�.""",
    tests = (yes("Alors branchez-le&nbsp;!"),),
    )


add(name="minicom",
    required=['cable console'],
    before="""
    Il faut lancer une application sur l'ordinateur qui
    permet de faire comme si l'on avait branch� un terminal
    sur le routeur CISCO.
    <p>
    Techniquement cette application fait un peu mieux que&nbsp;:
    <ul>
    <li> <tt>stty /dev/ttyS0 9600</tt> : Configuration de la liaison s�rie.
    <li> <tt>cat /dev/ttyS0 &amp;</tt> : Affichage de ce que le routeur CISCO envoie.
    <li> <tt>cat &gt;/dev/ttyS0</tt> : Envoi de ce qui est tap� au clavier au routeur CISCO</li>
    </ul>
    <p>
    L'application que vous devez utiliser est <tt>minicom</tt>.
    <p>
    Si <tt>minicom</tt> proteste � cause d'un verrou et qu'il
    est lanc� une seule fois alors d�truisez le verrou (<tt>/var/lock/...</tt>)
    <p>
    <b>En cas d'interdiction d'acc�s, passez <tt>root</tt>
       avant de lancer minicom</b>
    """,
    question = """Ouvrez un terminal et lancez <tt>minicom -D /dev/ttyS0</tt>.
    Que devez-vous taper pour avoir l'aide sur <tt>minicom</tt>&nbsp;?
    <p>
    Attention : ne lancez pas <tt>minicom</tt> en arri�re plan,
    il a besoin d'utiliser le clavier et l'�cran.
    <p>
    Attention : la r�ponse attendue n'est pas <tt>man minicom</tt> ni
    <tt>minicom --help</tt>
    """,
    tests = (
    reject('man', """On veut l'aide en ligne du logiciel, pas sa
    page de manuel. Si vous venez de lancer <tt>minicom</tt> la
    r�ponse est �crite sous yeux."""),
    require( ('A', 'Z', 'CTRL'),
             """Je ne trouve pas tous les �l�ments de la r�ponse.
             Faites un copi�/coll� de la s�quence de caract�res.""",
             uppercase=True),
    good_if_contains( '' ),
    ),
    indices = ("""La r�ponse est affich�e par <tt>minicom</tt>
    quand vous le lancez.""", ),

    )



add(name="minicom parameters",
    required=['minicom'],
    question = """Que tapez-vous dans <tt>minicom</tt>
    pour faire appara�tre le menu vous permettant
    de configurer la vitesse de la ligne, la parit�,
    le nombre de bits de donn�es, ...""",
    tests = (
    reject('O',
           """Ce menu est un menu g�n�ral de configuration,
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
    question = """Configurez la ligne s�rie avec
    une vitesse de 9600 bauds, 8 bits de donn�es et 1 stop bit.
    <p>
    R�pondez OUI si c'est fait.""",
    tests = (yes("Alors configurez-la correctement&nbsp;!"),),
    )



add(name="allumer CISCO",
    required=['line parameters', 'tp1:stop'],
    before = """Maintenant vous devez pouvoir communiquer avec le routeur CISCO.
    <p>
    Allumez le routeur CISCO.
    <p>
    Des messages de d�marrage doivent d�filer.
    <p>
    Si le routeur pose la question <em>�Do you want to enter the inital configuration dialog&nbsp;?�</em>
    r�pondez �no� pour qu'il s'initialise tout seul sans poser de questions.
    <p>
    Si le routeur pose la question <em>�Terminate auto-install&nbsp;?�</em>
    r�pondez �yes� pour qu'il s'initialise tout seul sans poser de questions.
    <p>
    Quand la proc�dure de d�marrage semble termin�e, tapez plusieurs
    fois sur <tt>return</tt> pour voir ce que le routeur CISCO r�pond.
    <p>
    Si un mot de passe est demand� et que vous ne le trouvez pas,
    suivez la proc�dure d'effacement de mot de passe indiqu�e
    dans la page d'aide/explication du menu de gauche.
    """,
    question = """Quel est le prompt (l'invite de commande)&nbsp;?""",
    tests = (
    # Anglais
    good('Router>'),
    bad('router>', "Vous n'auriez pas oubli� une majuscule&nbsp;?"),
    bad('Router' , "Vous n'auriez pas oubli� un caract�re&nbsp;?"),
    bad('router' , "On veut la chaine de caract�re exacte."),
    # Fran�ais
    bad(('routeur>', 'Routeur>'),
        "Vous avez mal lu... vous l'avez traduit en fran�ais"),
    bad(('Routeur', 'Routeur'),
        "Vous avez traduit et en plus vous avez oubli� un caract�re&nbsp;!"),
    reject('UPDOWN', "Cela ne ressemble pas � un <em>prompt</em>"),
    
    reject('rommon', """Votre routeur a perdu son syst�me&nbsp;?
Faites un arr�t marche et si le prompt est le m�me
suivez la proc�dure indiqu�e dans la page d'aide/explication du menu de gauche."""),
    require('jamaisimpossible',
        """Les �tudiants du TP pr�c�dents n'ont pas fait le m�nage avant
        de terminer le TP.
        Suivez la proc�dure d'effacement de configuration indiqu�e
    dans la page d'aide/explication du menu de gauche.
    """),
    
    ),
    indices = (reinit, ),

    )

add(name="initialiser",
    required=['allumer CISCO'],
    before="""Ce sujet de TP suppose que votre routeur est vierge
    de toute configuration.
    Pour �tre certain de ce fait nous allons effacer sa configuration.
    <p>
    <b>Si vous avez d�j� effac� la configuration alors
    ne le refaites pas</b>.
    """,
    question="""
      Si durant la proc�dure on vous demande un mot de passe,
      essayez """ + mots_de_passe + """
    <p>
      Voici la liste de choses � taper (ne faites pas un copier/coller
      de l'ensemble des lignes).
      Faites n�anmoins attention aux questions
      que le routeur vous pose.
      """ + procedure_effacement + """
      <p>
      Quand la proc�dure est termin�e, r�pondez OUI � cette question.
    """,
    tests = ( yes("R�pondez OUI s'il vous plait"), ),
    )

# XXX : param�tre d�pendant du routeur
add(name="aide commande",
    required=['initialiser'],
    before = """Quand vous tapez une commande, vous pouvez � n'importe
    quel moment taper un point d'interrogation pour obtenir&nbsp;:
    <ul>
    <li> La liste des noms de commandes/param�tres qui commencent
    par le mot que vous avez commenc� � taper&nbsp;;</li>
    <li> La syntaxe de la commande si son nom est complet&nbsp;;</li>
    <li> Les param�tres possibles si vous avez commenc� � taper
    un nom de param�tre&nbsp;;</li>
    <li> Les valeurs possibles pour un param�tre si le nom
    du param�tre est complet.</li>
    </ul>
    <p>ATTENTION : si votre prompt se termine par '#' vous devez
    taper 'exit' pour revenir dans un mode normal.
""",
    question = "Combien de commandes ont un nom qui commence par 's'&nbsp;?",
    tests = (
    require_int(),
    good("3"),
    good("4"),
    good("5"),
    bad("6", """Non, il y a la m�me commande deux fois.
    En effet <tt>*s=show</tt> indique que vous pouvez taper <tt>s</tt>
    au lieu de <tt>show</tt>"""),
    ),
    good_answer = """ATTENTION : dans certains cas des commandes
    existantes et expliqu�es dans la documentation n'apparaissent
    pas de la liste fournie par le point d'interrogation""",
    )
    


add(name="? seul",
    required=['aide commande'],
    question = """Si vous tapez un '?' seul comme commande,
    voyez-vous la commande <tt>configure</tt>&nbsp;?""",
    tests = (no("""Si vous la voyez c'est que vous �tes pass� en mode
    privil�gi� sans que l'on vous l'ai demand�"""),
             ),
    good_answer = """On ne voit pas cette commande car elle est
    accessible seulement en mode privil�gi�""",
    )



add(name="voir",
    required=['aide commande', 'doc:intro'],
    before="""<b>Attention, pour la suite des TP seuls les noms
    complets de commande seront accept�s, aucune abr�viation
    que cela soit pour les commandes et les param�tres ne sera accept�e</b>.\n""",
    question="""� votre avis, quelle est la <b>commande</b> (n'indiquez
    pas les param�tres) vous permettant
    d'avoir des informations sur le routeur quelque soit le type
    d'informations que l'on d�sire voir&nbsp;?""",
    tests = (
    reject(" ", "Le nom de la commande sans param�tres s'il vous plait."),
    Bad(Comment(Equal('systat'),
                """Utilisez la commande, vous verrez que cela ne permet
                pas de faire grand chose""")),
    bad(('s','sh','sho'), "Aucune abr�viation n'est autoris�e."),
    good("show"),
    ),
    )



add(name="show",
    required=['aide commande', 'voir'],
    before="""Deux moyens pour r�pondre � cette question&nbsp;:
    <ul>
    <li> Essayer b�tement.
    <li> Ou faire lister les premiers param�tres possibles en utilisant
    le point d'interrogation comme premier param�tre.
    </ul>""",
    question="La commande <tt>show</tt> prend-elle des param�tres&nbsp;?",
    tests = ( yes("Vous n'avez pas essay�&nbsp;?"), ),
    )


add(name="copi� coll�",
    required=['show'],
    before="""Pour faire un copier/coller sous unix, vous s�lectionnez
    avec le bouton de gauche et vous collez en cliquant sur le bouton
    du milieu.""",
    question="""De quoi n'avez-vous <b>pas</b> besoin pour faire un
    copier/coller sous unix�?
    {{{ shuffle}}}
    {{{ctrlC}}} De taper controle-C
    {{{ctrlV}}} De taper controle-V
    {{{droite}}} Du bouton de droite de la souris
    {{{gauche}}} Du bouton de gauche de la souris
    {{{milieu}}} Du bouton du milieu de la souris
    {{{menu}}} De menu d�roulant
    """,
    tests = (
    Good(Contain("ctrlC") & Contain("ctrlV") & Contain("droite")
         & Contain("menu")
         & ~Contain("gauche") & ~Contain("milieu")),
    ),
    )


add(name="commande incompl�te",
    required=['show'],
    question = """Est-ce que c'est bien <tt>show</tt>
    qui s'ex�cute si vous tapez <tt>sho clock</tt>
    au lieu de <tt>show clock</tt>&nbsp;?""",
    tests = ( yes("Montrez cela � un enseignant"), ),
    good_answer = """Cela fonctionne car vous avez tapez suffisemment
    de lettres de la commande pour qu'il n'y ai pas d'ambigu�t�.
    Cette pratique est d�conseill�e quand on fait des scripts.
    <p>
    <b>DANS LA SUITE DU TP, TOUTE COMMANDE INCOMPL�TE SERA REFUS�E</b>
    """,
    )
    


add(name="�dition ligne",
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
    Bleu : Fl�che curseur gauche
    """,
    question="Est-ce que vous pouvez le faire&nbsp;?",
    tests = ( yes("Montrez cela � un enseignant"), ),
    )



add(name="show liste",
    required=['aide commande', 'show'],
    before="""Le premier param�tre de la commande <tt>show</tt>
    permet de choisir ce que l'on peut voir.
    Faites afficher l'ensemble des possibilit�s pour
    ce premier param�tre.""",
    question = """Combien de premiers param�tres possibles
    commencent par la lettre 'h'&nbsp;?""",
    tests = ( require_int(),
              good("4"),
              good("3"),
              good("5"),
              good("2"), # Anciens IOS
              ),
    )

add(name="mauvaise commande",
    required=['tp1_eth:config ethernet'],
    before="""Lancez la commande&nbsp;: <tt>coucou</tt>.
    <p>
    Comme cela n'est pas une commande, le routeur consid�re que
    c'est le nom d'une machine.
    Il commence donc par essayer de trouver son adresse IP.
    Il essaie 3 fois.
    """,
    question="""Sans �teindre le routeur, arrivez-vous � arr�ter
    le processus de recherche&nbsp;?
    <p>
    R�pondez :
    <ul>
    <li> NON si vous n'y arrivez pas.
    <li> comment vous avez fait si vous y arrivez.
    </ul>
    <p>
    <small>
    Si jamais la recherche est instantan�e et que
    le <em>prompt</em> revient tout de suite alors r�pondez NON
    � la question. Cela veut dire que votre routeur n'a
    pas la configuration par d�faut.

    """,
    tests = (
        Good(Comment(UpperCase(Contain('CTRL') &
                               ( Contain('SHFT') | Contain('SHIFT') ) &
                               Contain('6')),
                     """En fait vous venez d'envoyer le caract�re Contr�le-^
                     de code ASCII 0x5E""" 
                     )
             ),
        Good(UpperCase(Contain('^^')
                       | (Contain('CTRL') & Contain('^')))),
        no("Montrez comment vous avez fait � un enseignant"),
        ),
    )

add(name="historique",
    required=['�dition ligne', 'copi� coll�'],
    question="""Pouvez-vous utiliser la fl�che curseur vers le haut
    pour revenir dans l'historique et �diter d'anciennes commandes&nbsp;?""",
    tests = ( yes("R�essayez"), ),
    )


add(name="fin �dition",
    required=['historique', 'commande incompl�te', '? seul', 'show liste'], # 'mauvaise commande',
    before = """La r�ponse � cette question n'est pas li�e � <tt>minicom</tt>.
    De plus elle fonctionne sur tous les terminaux virtuels et sur
    la console Linux.""",
    question="""Sans utiliser la souris et l'ascenseur,
    que tapez-vous au clavier pour voir ce qui a d�fil� au dessus
    de l'�cran&nbsp;?""",
    tests = (
    Bad(Comment(Equal('history'),
                """On ne vous demande pas de faire afficher quelque chose
                de nouveau sur l'�cran.
                On veut voir ce qui a d�j� �t� affich� et qui est
                sorti par le haut...""")),
    Bad(Comment(UpperCase(Contain('CURSEUR')|Contain('CURSOR')|
                          Contain('FLECHE')|Contain('FL�CHE')),
                """Remonter d'une seule ligne n'est pas efficace,
                   on veut remonter page par page...""")),
    reject('9', """Le chiffre 9 ne m'int�resse pas. Ce qu'il faut
    indiquer est la fonction associ�e � la touche."""),
    require(('SHIFT', 'SHFT', 'MAJ'), uppercase=True, all_agree=True),
    require(('PAGE', 'PG', 'CTRL'), uppercase=True, all_agree=True),
    require(('UP', 'HAUT', 'PRECEDENTE', 'PR�C�DENTE'), uppercase=True, all_agree=True),
    # Fait planter
    # require(('B', 'U'), "Ceci ne fonctionne que dans <tt>minicom</tt>", uppercase=True),
    good_if_contains(''),
    ),
    indices = (
    """C'est <tt>shift + page up</tt>""",
    ),
    )
