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

from questions import *
from check import *

grep_required = require("grep","On utilise <tt>grep</tt> pour cribler")
grep_e_inutile = reject("-e",
                        """L'option <tt>-e</tt> est inutile si
                        il y a un seul <em>pattern</em>""")

add(name="intro",
    required=["manuel:chercher"],
    question="""Quel est le nom de la commande permettant d'afficher
    les lignes d'un fichier contenant une chaine de caractères spécifique.
    """,
    tests=(
    good("grep"),
    good("fgrep", "On utilise plutôt <tt>grep -F</tt> mais dans la suite du TP vous n'utiliserez pas l'option <tt>-F</tt>"),
    good("egrep", "On utilise plutôt <tt>grep -E</tt> mais dans la suite du TP vous n'utiliserez pas l'option <tt>-E</tt>"),
    bad('awk', """Cette commande est un langage de programmation complet.
    On peut donc tout faire avec.
    On veut comme réponse le nom de la commande qui sert seulement
    à cribler."""),
    bad('cat', "Elle affiche tout sans rien enlever"),
    bad('sed',
        "Cette commande n'est pas faite pour ça (mais elle peut le faire)"),
    
    reject('find', """<tt>find</tt> trouve des fichiers,
    elle ne regarde pas leur contenu"""),
    ),
    indices = (
    """Historiquement, le nom de cette commande vient de la ligne
    commande que l'on peut utiliser dans <tt>vi</tt> pour faire
    la même chose&nbsp;:
    <pre>:<big>g</big>/<big>r</big>egular <big>e</big>xpression/<big>p</big></pre>
    """,
    ),
    )

add(name="simple",
    question="""Quelle est la commande la plus simple pour afficher
    toutes les lignes du fichier <tt>/etc/passwd</tt>
    contenant la chaine de caractère <tt>/var</tt>""",
    tests=(
    grep_required,
    reject(("|","<"),
           """On veut une solution simple,
           sans redirection de l'entrée standard
           que cela soit par <tt>&lt;</tt> ou <tt>|</tt>."""),
    require("/etc/passwd",
            """Il faut indiquer le nom du fichier
            dans lequel on veut chercher.
            (Sans fautes d'orthographe)"""),
    grep_e_inutile,
    shell_bad("grep /etc/passwd /var",
              """Les premiers arguments de shell sont les <em>patterns</em>
              et les dernier les noms de fichier"""),
    reject('*', """Pas besoin d'indiquer qu'il y a n'importe quoi avant et
    après, par défaut cherche l'expression n'importe où dans la ligne"""),
    shell_good("grep /var /etc/passwd"),
    expect('/var'),
    shell_display,
    ),
    )

add(name="attention spécial",
    required=["simple", "expreg:deux spécial"],
    question="""Donner la commande permettant d'afficher
    les lignes contenant la chaine de caractères <tt>2*</tt>
    dans le fichier <tt>/etc/passwd</tt>""",
    tests=(
    grep_required,
    grep_e_inutile,
    reject('fgrep',
           "Cette commande est obsolette, il faut utiliser <tt>grep -F</tt>"),
    require("/etc/passwd", "Et <tt>/etc/passwd</tt> ou est-il&nbsp;?"),
    shell_good(("grep -F '2*' </etc/passwd",
                "grep -F '2*' /etc/passwd"),
               "Il était aussi possible de faire <tt>grep '2\\*' /etc/passwd"),
    shell_good(("grep '2\\*' </etc/passwd",
                "grep '2\\*' /etc/passwd",
                "grep '2[*]' /etc/passwd",
                "grep '2[*]' </etc/passwd",
                )),
    reject(" 2* ",
           """Cette commande ne fonctionne pas si vous avez un fichier
           dont le nom commence par <tt>2</tt>"""),
    shell_bad(("grep 2\\* </etc/passwd",
                "grep 2\\* /etc/passwd"),
               """Cette commande ne fonctionne pas car le shell a bien
               compris que l'étoile était un <em>pattern</em>
               qu'il ne fallait pas transformer.
               Mais la commande <tt>grep</tt> voit une étoile
               qui pour elle est un facteur de répétition."""),
     shell_bad(("grep 2\\\\* </etc/passwd",
                "grep 2\\\\* /etc/passwd"),
               """La signification de l'anti-slash est annulée pour
               le shell mais pas celle de l'étoile.
               Donc si un fichier du répertoire courant
               commence par <tt>2\\</tt> la commande <tt>grep</tt>
               ne verra pas le bon paramètre.
               """),
    reject('>', "Pourquoi rediriger la sortie standard&nbsp;?"),
    reject('|', "Vous avez besoin que d'une seule commande."),
    reject('-', "Vous n'avez pas besoin d'indiquer d'option."),
   
    shell_display,
    ),
    indices=(
    """L'étoile est un caractère spécial pour le shell ET pour
    la commande <tt>grep</tt> car il définit une expression régulière""",
    """Il faut annuler 2 fois la signification de l'étoile""",
    )
    )


add(name="attention spécial 2",
    required=["simple", "expreg:un spécial"],
    question="""Donner la commande permettant d'afficher
    les lignes contenant la chaine de caractère <tt>-e</tt>
    dans le fichier <tt>/etc/passwd</tt>""",
    tests=(
    grep_required,
    require("/etc/passwd", "Et <tt>/etc/passwd</tt> ou est-il&nbsp;?"),
    reject('\\-',
           """Il est possible que cette commande fonctionne
           car '\\-' est actuellement remplacé par un tiret
           bien que celui-ci n'ai aucune signification particulière.
           Si dans le futur '\\-' prend une signification alors
           votre commande ne fonctionnera plus.
           <b>On ne doit pas mettre d'</em>antislash</em> devant
           les caractères sans signification particulière.
           """),
           
    shell_good(("grep -e -e </etc/passwd",
                "grep -e -e /etc/passwd",
                )),
    shell_good((
                "grep '.*-e' /etc/passwd",
                "grep '[-]e' /etc/passwd",
                "grep '.*-e' </etc/passwd",
                "grep '[-]e' </etc/passwd",
                ),
               "Syntaxe recommandée : <tt>grep -e -e /etc/passwd</tt>",
               dumb_replace=(('grep -e', 'grep'),)),
    shell_bad((
                "grep -e </etc/passwd",
                ),
               """Cette commande fait une erreur d'exécution"""),
    shell_bad((
                "grep [-]e </etc/passwd",
                "grep [-]e /etc/passwd",
                ),
               """Si un fichier s'appelant <tt>-e</tt> existe alors
               le shell remplace le <em>pattern</em> par ce nom de fichier.
               Dans ce cas, votre commande ne fonctionne pas,
               elle est donc fausse."""),
    shell_bad((
                "grep -e /etc/passwd",
                ),
               """La commande <tt>grep</tt> croit qu'il faut rechercher
               le <em>pattern</em> <tt>/etc/passwd</tt> dans l'entrée
               standard car il n'y a pas de nom de fichier indiqué.
               Il ne faut pas que le <tt>-e</tt> soit compris comme
               une option de la commande.
               """),
    number_of_is('/', 2, """Pourquoi ajouter des <tt>/</tt>&nbsp;? <tt>-e</tt>
    n'est pas un nom de fichier"""),
    reject(("'-e'", '"-e"'),
           """Vous avez protégé le <tt>-e</tt> pour rien car il n'est
           pas particulier. Le shell l'a transmis à la commande <tt>grep</tt>
           qui voit donc une option."""),
    require("-e", "Et <tt>-e</tt> ou est-il&nbsp;?"),
    shell_display,
    ),
    indices=("""Lire le <tt>man</tt>""",
             """Il faut utiliser l'option <tt>-e</tt>""",
             ),
    )

add(name="source",
    required=["simple", "pattern:final"],
    question="""Quelle est la commande la plus simple pour afficher
    toutes les lignes qui contiennent la chaîne 'sqrt'
    dans tous les fichiers avec l'extension '.c'
    qui sont dans le répertoire courant""",
    tests=(
    shell_good(("grep sqrt *.c","grep -h sqrt *.c") ),
    grep_required,
    grep_e_inutile,
    reject(".C",
           "L'extension est <tt>.c</tt> pas <tt>.C</tt>"
           ),
    reject("./*.c",
           """Simplifiez votre <em>pattern</em>
           il contient des caractères inutiles"""
           ),
    reject("find",
           """Les fichiers du répertoire courant,
           pas ceux qui sont au dessous."""
           ),
    reject("|",
           """Pas besoin de pipeline pour
           faire une commande aussi simple."""
           ),
    reject('-',
           "C'est tellement simple qu'il n'y a pas besoin d'utiliser d'options"
           ),
    require('*', """Il faut utiliser le <em>pattern</em> <tt>*</tt>."""),
    reject('./*.c', """Vous pouvez raccourcir votre <em>pattern</em>"""),
    shell_require('<pattern_char>*</pattern_char>',
                  """Je ne vois pas le <em>pattern</em> <tt>*</tt>
                  dans votre réponse bien que l'étoile soit présente."""),
    require('*.c', """Je ne vois pas le <em>pattern</em> correspondant
    aux noms de tous les fichiers se terminant par <tt>.c</tt>"""),
    expect('sqrt'),
    reject('/',
           "Il n'y a pas de <tt>/</tt> dans la réponse la plus courte."
           ),
    shell_display,
    ),
    )

add(name="ou",
    required=["simple"],
    question="""Quelle est la commande la plus simple pour afficher
    toutes les lignes du fichier <tt>/etc/passwd</tt>
    contenant la chaine de caractères <tt>/var</tt> ou <tt>/usr</tt>.
    <p>
    Vous n'utiliserez pas d'expression régulière,
    on verra cela plus loin dans le TP.""",
    tests=(
    expect(('/var', '/usr', 'grep', '/etc/passwd')),
    shell_good(("grep -e /var -e /usr /etc/passwd",
                "grep -e /usr -e /var /etc/passwd",
                "grep -e /var -e /usr </etc/passwd",
                "grep -e /usr -e /var </etc/passwd",
                )),
    shell_good(("grep -E -e '/usr|/var' /etc/passwd",
                "grep -E -e '(/usr|/var)' /etc/passwd",
                "grep -Ee '/usr|/var' /etc/passwd",
                "grep -Ee '(/usr|/var)' /etc/passwd",
                ),
               """Il y avait plus simple :
               <tt>grep -e /var -e /usr /etc/passwd</tt>"""),
    shell_bad("grep /etc/passwd -e /var /usr",
              """Cette commande est FAUSSE, de plus il faut
              toujours mettre les options au début de la liste
              des arguments"""
              ),
    shell_bad("grep -e /var /usr /etc/passwd",
                 """Quand <tt>grep</tt> lit ses arguments il croit
                 qu'il faut commencer à chercher <tt>/var</tt>
                 dans le fichier nommé <tt>/usr</tt>.
                 Il faut répéter le <tt>-e</tt> devant chaque
                 chaine que l'on désire rechercher."""
                 ),
    reject(("|","[","]","*"),
           """N'utilisez pas d'expression régulière ni de <em>pattern</em>
           pour cet exercice, car la réponse est plus courte mais plus
           compliquée à trouver"""),
    require("-e", "Il faut utiliser l'option <tt>-e</tt>"),
    reject("grep /etc/passwd",
            "On met le <em>pattern</em> avant les fichiers."),
    number_of_is('-e', 2, "Vous devez utiliser plusieurs fois <tt>-e</tt>"),
    shell_display,
    ),
    indices=("""L'option à utiliser est <tt>-e</tt>""",
             ),
    )
    
add(name="casse",
    required=["simple"],
    before="""Bien qu'il soit possible d'écrire des
    <em>patterns</em> de la forme <tt>[Tt][Oo][Tt][Oo]</tt>.
    Ce n'est pas du tout joli et c'est long à écrire.
    La réponse attendue à cette question n'utilise
    donc pas cette astuce.""",
    question="""Quelle est la commande la plus simple pour cribler
    toutes les lignes lues dans l'entrée standard
    contenant <tt>toto</tt> et ceci
    indépendemment de la casse (différence majucule/minuscule).
    """,
    tests=(
    shell_good("grep -i toto"),
    shell_good("grep -i toto -",
               """Le tiret final n'était pas utile.
               Exceptionnellement, cette réponse qui n'est pas la
               plus courte est acceptée."""
               ),
    shell_bad("grep toto -i",
               """Bien que cela fonctionne sur Linux ce n'est pas portable.
               il faut mettre les options avant les autres arguments"""),
    grep_required,
    require("toto", "Quelle chaine de caractère voulez-vous chercher&nbsp;?"),
    require("-", "Vous devez ajouter une option"),
    require('-i', """L'option pour indiquer que l'on ne tiens pas compte
    de la casse n'est pas présente dans la ligne"""),
    reject('|', "On a besoin que d'une seule commande"),
    shell_display,
    ),
    indices=("""En anglais 'casse' se dit 'case' comme dans 'upercase' et
    'lowercase' pour majuscule et minuscule.""",
            """Tapez 'grep --help' pour avoir l'aide""",
            ),
    )

add(name="lister",
    required=["simple", "pattern:final"],
    question="""Quelle est la commande la plus simple pour
    lister les noms des fichiers qui sont dans <tt>/etc</tt>
    qui contiennent (dans le fichier, pas dans son nom)
    la chaine de caractères <tt>a4</tt>
    Ce n'est pas grave si votre commande affiche des erreurs
    parce qu'elle ne peut pas lire les répertoires.
    <p>
    Si le fichier contient 10 fois <tt>a4</tt> son nom ne
    devra être listé qu'une seule fois.""",
    tests=(
    shell_good("grep -l a4 /etc/*"),
    grep_required,
    reject('find',
           """On n'a pas besoin de <tt>find</tt> car on veut chercher
           les fichiers dans le répertoire, pas dans la hiérarchie
           complète"""),
    
    require("/etc/*",
            """Pour passer à <tt>grep</tt> la liste de tous les fichiers qui
            sont dans <tt>/etc</tt> on utilise un <em>pattern</em>"""
            ),
    reject('-H', """Cette option <tt>-H</tt> ne sert à rien, le nom du fichier
    est toujours affiché"""),
    reject('-m',
           """L'option <tt>-m</tt> n'est pas utile pour cette question,
           Enlevez cette option bien qu'elle permette d'économiser
           du temps CPU."""),
    require("-l",
            """Il manque l'option indiquant que l'on veut
            SEULEMENT lister les noms des fichiers qui contiennent
            cette ligne et que l'on
            <b>ne veux pas afficher les lignes trouvées</b>"""),
    reject("-L",
           """On veut lister les fichiers qui contienne
           le texte. Pas ceux qui ne le contiennent pas."""),
    number_of_is('-', 1, "Vous n'avez besoin que d'une seule option"),
    shell_display,
    ),
    bad_answer="""On veut lister les noms des fichiers,
    pas les lignes qu'ils contiennent,
    regardez à nouveau les options de <tt>grep</tt>""",
    indices = (
    """Vous n'avez pas besoin d'autre chose que de <tt>grep</tt>""",
    """<tt>grep</tt> peut prendre plusieurs noms de fichiers en paramètre""",
    ),
    )

add(name="lister sans erreur",
    required=["lister", "sh:redirection erreur", "device:poubelle"],
    question="""Complétez la commande suivante
    pour que les messages d'erreur existant ne s'affiche pas.
    <pre>grep -l a4 /etc/*</pre>
    """,
    tests=(
    reject(('-ls', '-s', '--no-messages'),
           """Cette réponse est refusée pour trois raisons:
           <ul>
           <li> Ce n'est pas portable (c'est indiqué dans le manuel)</li>
           <li> La solution que l'on vous demande est plus générale
           et est applicable à toutes les commandes. </li>
           <li> Vous n'avez pas utilisé ce que vous avez appris.</li>
           </ul>"""),
    require("2>", "Il faut rediriger la sortie d'erreur"),
    require("/dev/null", "Il faut utiliser le périphérique poubelle"),
    reject(("-s", "-ls", "-sl"),
           """La documentation vous dit de ne pas utiliser
           L'option <tt>-s</tt>"""),
    shell_good("grep -l a4 /etc/* 2>/dev/null"),
    reject(';', """S'il y a un <tt>;</tt> c'est qu'il y a 2 commandes.
    Hors, ce n'est pas le cas, il ne doit y avoir qu'une seule commande."""),
    shell_display,
    ),
    )
    

