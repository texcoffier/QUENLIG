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
import remplacer

dumb_replace = ( ('-A', '-e'), )

add(name="intro",
    required=["sh:arrière plan"],
    question="""Quel est le nom de la commande permettant
    de lister des processus&nbsp;?""",
    tests=(
    good("ps"),
    good("pstree",
         "J'attendais la commande <tt>ps</tt> qui est standard."),
    bad("top",
        """Cette commande permet de surveiller les processus.
        Ce n'est pas ce qui vous ai demandé"""),
    bad("ls",
        """Cette commande liste des informations sur les fichiers et
        répertoires"""),
    ),
    indices=("""Le nom de la commande est composé de la première
    et de la dernière lettre du mot 'processus'""",
             ),
    )

add(name="tous",
    question="""Donnez la commande permettant de lister
    tous les processus qui fonctionnent sur la machine.""",
    tests=(
    good("ps -e", replace=dumb_replace),
    bad(("ps a", "ps -a", "ps e"),
        """Ceci n'affiche pas les processus systèmes,
        seulement les votres"""),
    reject("pstree", "On vous parle de la commande <tt>ps</tt>"),
    require("ps", "Je ne vois pas la commande <tt>ps</tt>"),
    bad("ps", """Cela affiche seulement les processus lancés
    à partir de votre console, pas les autres"""),
    bad(("ps -ax", "ps -aux", "ps -alx"),
        """Ce sont des options Unix BSD non vues en cours.
        Vous remarquerez le <em>warning</em> affiché par
        la commande <tt>ps</tt> lors de son exécution"""),
    require('-',"Utilisez la syntaxe avec le tiret pour indiquez les options"),
    answer_length_is(5, "La réponse est en 5 caractères"),
    ),
    )

add(name="init",
    question="""Quel est le <tt>PID</tt> du processus <tt>init</tt>&nbsp;?""",
    tests=(
    good("1"),
    require_int(),
    ),
    )

add(name="compte",
    required=["tous", "compte:ligne", "pipeline:intro"],
    question="""Quelle est la commande la plus simple donnant le nombre
    de processus fonctionnant sur votre machine&nbsp;?
    <p>
    Ce n'est pas grave si vous comptez la ligne de titre
    qu'affiche <tt>ps</tt>
    """,
    tests=(
    shell_good("ps -e | wc -l",dumb_replace=dumb_replace),
    shell_bad("ps -e | wc",
               """Il manque une option à <tt>wc</tt> pour qu'il n'affiche
               que le nombre de processus et pas le nombre de caractères
               et de mots.""",
              dumb_replace=dumb_replace),
    require("ps",
            """Vous n'utilisez pas la commande affichant
            la liste des processus&nbsp;!"""),
    require("wc",
            """Vous n'utilisez pas la commande permettant de compter
            des lignes&nbsp;!"""),
    require("-e",
            """On veut le nombre de processus sur votre machine
            pas seulement ceux qui ont été lancés dans votre terminal.
            Il manque donc une option à <tt>ps</tt>""",
            replace=dumb_replace),
    require("|",
            "Vous devez utiliser un pipeline pour lier les deux processus"),
    shell_display,
    ),
    )

add(name="trouver",
    required=["tous", "pipeline:intro", "cribler:simple"],
    before="""Lancez des applications graphiques en arrière plan&nbsp;:
    <pre>xeyes &amp;
xclock &amp;
xfontsel &amp;</pre>""",
    question="""Donnez la ligne de commande affichant les informations
    sur les processus qui contiennent <tt>xeyes</tt> dans
    leur description (lancé par vous ou non).
    <p>
    Vous n'avez pas besoin de lire la documentation pour
    répondre à cette question. Tout est dans les prérequis.""",
    tests=(
    shell_good("ps -e | grep xeyes", dumb_replace=dumb_replace),
    shell_bad("ps | grep xeyes",
              """Cette commande ne va pas fonctionner si vous la lancez
              sur un terminal différent de celui utilisé
              pour lancer <tt>xeyes</tt>.
              Il manque une option à la commande <tt>ps</tt>.
              """),
    shell_bad("ps -C xeyes",
              """<b>C'est tout à fait correcte</b>, mais cela n'affiche
              que les commandes dont le nom est <tt>xeyes</tt>.
              Cela n'affichera pas les commandes qui contiennent
              <tt>xeyes</tt> dans leur description.
              Le but de cet exercice est de vous faire utiliser
              un pipeline."""),              
    require("xeyes",
            "Votre commande ne fait pas référence à <tt>xeyes</tt>&nbsp;!"),
    require("ps",
            "Votre commande ne fait pas référence à <tt>ps</tt>&nbsp;!"),
    require("|",
            "Votre commande ne contient pas de pipeline."),
    require('-e', "Utilisez l'option pour lister tous les processus",
           replace=dumb_replace),
    shell_display,
    ),
    indices = (
    """On utilise la commande <tt>ps</tt> pour lister les processus
    et la commande <tt>grep</tt> pour n'affiche que ceux qui contiennent
    ce que l'on recherche""",
    ),
    )

add(name="sauve pid",
    required=["trouver", "sh:deuxième mot"],
    question="""Stockez le PID du premier processus
    <tt>xeyes</tt> trouvé dans la variable <tt>Y</tt>
    <p>
    Si vous avez besoin de variables, appelez les <tt>A</tt>, <tt>B</tt>, ...
    """,
    tests=(
    reject('-A',
           "Utilisez <tt>-e</tt> au lieu de <tt>-A</tt>, il est standard"),
    shell_good((
    "Y=$(ps -e | grep xeyes | (read A B ; echo $A))",
    'Y=$(ps -e | grep xeyes | (read A B ; echo "$A"))',
    'Y=$(ps -e | grep xeyes | (read A Y ; echo "$A"))',
    'Y=$(ps -e | grep xeyes | (read Y A ; echo "$Y"))',
                ), dumb_replace=dumb_replace),
    reject(('cut', 'head', 'sed'),
           """La réponse attendue est composée de morceaux venant
           des deux questions indiquées auxquelles vous avez déjà répondu.
           Vous ne devez pas utiliser <tt>cut</tt>, <tt>head</tt>, <tt>sed</tt>
           <p>
           Votre réponse est peut-être juste, je ne peux pas
           vérifier tous les cas possibles."""),
    require(('B', '-e'),
           """La réponse attendue est composée de morceaux venant
           des deux questions indiquées auxquelles vous avez déjà répondu.
           <p>
           Votre réponse est peut-être juste, je ne peux pas
           vérifier tous les cas possibles."""),
    expect('Y'),
    expect('Y='),
    shell_display,
    ),
    )

class test_kill(Test):
    comment = "kill PID"
    def test(self, student_answer, string):
        
        reponse = [x for x in student_answer.split(" ") if x != '']
        if len(reponse) != 2:
            return False, """Il suffit de lancer la commande <tt>kill</tt>
            avec comme paramètre le PID du processus à tuer."""

        if reponse[0] != "kill":
            return False, "La commande s'appelle <tt>kill</tt>"
   
        try:
            i = int(reponse[1])
            return True, ""
        except ValueError:
            return False, "Vous devez donner le PID du processus"

add(name="tuer",
    before="""Lancez une application graphique en arrière plan&nbsp;:
    <pre>xeyes &
</pre>
L'entier affiché est le PID du processus lancé.
""",
    required=["tous"],
    question="""Quelle commande lancez-vous pour tuer la commande
    <tt>xeyes</tt> en spécifiant son PID&nbsp;?
    <em>Donnez la ligne de commande complète que vous avez tapé pour le tuer.</em>
    """,
    tests=(
    reject('xeye',
           """Ne faites pas de choses compliquées, indiquez seulement
           le PID du processus <tt>xeyes</tt>"""),
    reject('-9', """<tt>-9</tt> est l'option de la dernière chance.
    Utilisez-la à vos risques et périls car l'application va être stoppée
    sans avoir été prévenue, elle ne sauvegardera donc pas ses données.
    Elle pourrait ne pas libérer des zones de mémoire partagées ou
    détruire des verrous (firefox)."""),
    reject('-', "Vous n'avez besoin d'aucune option"),
    test_kill(),
    ),
    )

add(name="tuer un shell",
    before="""Lancez un nouveau terminal,
    trouvez le PID du shell en train de tourner dans
    ce terminal avec la commande <tt>ps</tt> (sans argument).
    <p>
    Essayez de tuer le shell en faisant <tt>kill SON_PID</tt>
""",
    required=["tuer"],
    question="""Quel argument faut-il ajouter à la commande <tt>kill</tt>
    pour pouvoir tuer un shell&nbsp;?""",
    tests=(
    good("-1"),
    good(("-s 1", "-HUP", "-s HUP"), "<tt>-1</tt> est plus court à taper"),
    reject(("9", "-kill"),
           """Le signal <tt>9</tt> est extrêmement violent.
           Il ne demande pas au processus de se terminer proprement.
           Il n'est à utiliser qu'en dernier recours"""),
    reject("kill", """On veut seulement l'option à ajouter,
    pas la commande complète"""),
    bad("-l", "Vous avez confondu le chiffre 1 et la lettre l"),
    require("-",
            "On veut une option, il y a donc un <tt>-</tt> quelque part."
            ),
    reject(' ', "Il ne devrait pas y avoir d'espace dans votre réponse"),
    
    ),
    indices = (
    """Il faut envoyer le signal HUP (<em>hang up</em>)
    qui veut dire raccrocher la ligne et qui porte le numéro <tt>1</tt>""",
    )
    )

add(name="pstree",
    required=["tous"],
    before="""La commande <tt>pstree</tt> n'est pas standard
    mais bien pratique.
    Elle affiche la liste de tous les processus sous la forme
    d'un arbre de processus.""",
    question="""Quel est le nom du processus qui est
    à la racine de la hiérarchie des processus&nbsp;?""",
    tests=(
    good("init"),
    bad('1', "Le nom du processus, pas son <tt>PID</tt>"),
    ),
    )

add(name="top",
    required=["tous"],
    before="""La commande <tt>top</tt> n'est pas standard
    mais bien pratique.
    Elle affiche périodiquement sur l'écran la liste
    de processus utilisant le plus de temps CPU actuellement.
    <p>
    Si vous tapez le caractère <tt>?</tt> pendant que la commande
    fonctionne, elle affichera une page d'aide.
    """,
    question="""Quelle commande (définie par un seul caractère)
    utilisez-vous pour inverser la direction du tri&nbsp;?""",
    tests=(
    good("R"),
    bad("r", "Cette commande sert à changer la priorité d'un processus"),
    bad('o', "Cette commande permet de changer l'ordre des colonnes"),
    bad('b', "Cette commande met en évidence les processus actifs"),
    bad(('<','>'), "Cette commande change la colonne à trier"),
    answer_length_is(1, "On vous a dit que la réponse était sur 1 caractère"),
    ),
    indices = (
    """Vous lancez la commande, vous tapez <tt>?</tt> comme c'est indiqué
    dans l'énoncé et vous lisez la page d'aide,
    la réponse est indiquée vers le milieu.""",
    ),
    )

add(name="utilisateurs",
    required=["tous", "remplacer:enlève commentaires", "trier:unique",
              "pipeline:intro"],
    question="""Donnez la ligne de commande complète commençant
    par <tt>ps -fe |</tt> affichant la liste des utilisateurs
    qui ont un processus dans la machine (en enlevant les doublons).
    <p>
    Ce n'est pas grave si <tt>UID</tt> est listé comme un utilisateur.""",
    default_answer="ps -fe | ",
    tests=(
    reject('/g',
           "Il n'y a qu'une seule substitution à faire, donc d'option 'g'"),
    reject("$", """La plus grande chaine est prise, elle ira donc jusqu'au
    bout. Le <tt>$</tt> est donc inutile"""),
    reject('uniq', """La commande <tt>uniq</tt> n'a pas été utilisées
    pour répondre aux question précédentes, utilisez <tt>sort -u</tt>"""),
    shell_good("ps -fe | sed 's/ .*//' | sort -u",
               replace=remplacer.dumb_replace),
    shell_good("ps -fe | sed -e 's/ .*//' | sort -u",
               replace=remplacer.dumb_replace),
    shell_good("ps -fe | cut -d' ' -f1 | sort -u",
               "On pouvait le faire sans <tt>cut</tt> mais avec <tt>sed</tt>"),
    shell_good("ps -fe | tail +2 | sed 's/ .*//' | sort -u",
               replace=remplacer.dumb_replace),
    shell_good("ps -fe | tail +2 | sed -e 's/ .*//' | sort -u",
               replace=remplacer.dumb_replace),
    reject(":", "Pourquoi avez-vous un ':' dans votre réponse&nbsp;?"),
    require('sort', "Chaque utilisateur doit être affiché une seule fois."),
    require('-u', """Manque une option à <tt>sort</tt> :
    chaque utilisateur doit être affiché une seule fois."""),
    reject('-r', """La substitution faite pas <tt>sed</tt> est triviale,
    vous n'avez pas besoin d'expression régulières étendues."""),
    shell_display,
    ),
    indices=(
    """Le nom étant le premier mot de la ligne, on enlève
    tout ce qui suit cet espace.""",
    """On a seulement besoin de <tt>sed</tt> et de <tt>sort</tt>""",
    ),
    )
