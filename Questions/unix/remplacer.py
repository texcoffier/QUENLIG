# -*- coding: latin-1 -*-
#    QUENLIG: Questionnaire en ligne (Online interactive tutorial)
#    Copyright (C) 2005-2011 Thierry EXCOFFIER, Universite Claude Bernard
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

dumb_replace = (
    ('-re ', '-r '), ('-er ', '-r '),
    (' -e ', ' '), ('g; s', 'g;s'), ('g ; s', 'g;s'),
    )

add(name="intro",
    required=["manuel:chercher"],
    before="""La commande <tt>sed</tt> permet d'éditer
    de très gros fichiers sans les charger en mémoire.
    Par défaut le fichier est lu sur l'entrée standard
    et la nouvelle version est écrite sur la sortie standard.
    La syntaxe de base est la substitution&nbsp;:
    <pre>sed -e 's/<b>ancien texte</b>/<b>nouveau texte</b>/g'</pre>
    Le <tt>g</tt> de la fin indique que l'on remplace
    toutes les occurrences qui sont dans la ligne
    et pas seulement la première.""",
    question="""Donner la ligne de commande permettant de remplacer
    tous les <tt>blue</tt> de l'entrée standard
    par des <tt>black</tt> sur la sortie standard.""",
    tests=(
    require('/g',
            """Si vous n'indiquez pas <tt>/g</tt>
            seul la première occurrence dans la ligne sera substituée"""),
    require('/blue/', """Je ne vois nulle part de <tt>/blue/</tt>"""),
    require('/black/', """Je ne vois nulle part de <tt>/black/</tt>"""),
    require('s/',
            """Je ne vois nulle part le <tt>s/</tt> qui indique
            que l'on veut faire une substitution"""),
    shell_good("sed 's/blue/black/g'", dumb_replace=dumb_replace),
    number_of_is('/',3, """Si vous respectez la syntaxe, il devrait
    y avoir trois / dans la commande"""),
    shell_display,
    ),
    )

add(name="slash",
    required=["intro", "intro:back slash"],
    before="""Le caractère d'échappement utilisé dans les commandes
    <tt>sed</tt> est le même que celui utilisé dans le shell,
    dans le langage C, dans les expressions régulières, ...""",
    question="""Donner la ligne de commande permettant de remplacer
    tous les <tt>/</tt> de l'entrée standard
    par des <tt>:</tt> (deux points) sur la sortie standard.""",
    tests=(
    require('/g', """N'oubliez pas le <tt>/g</tt> !"""),
    reject('[', "N'utilisez pas les crochets pour faire l'échappement"),
    reject("s///",
              """Vous n'avez pas essayé la commande....
              <tt>sed</tt> fait une erreur car il croit qu'on
              lui demande de remplace 'vide' par 'vide'
              et après il y a des caractères qu'il ne comprend pas.
              <p>
              Il faut banaliser le caractère <tt>/</tt> que vous voulez
              remplacer.
              """),
    shell_good(r"sed 's/\//:/g'",
               "L'autre solution était <tt>[/]</tt> au lieu de <tt>\\/</tt>",
               dumb_replace=dumb_replace),
    shell_good(r"sed 's/[/]/:/g'",
               "L'autre solution était <tt>\\/</tt> au lieu de <tt>[/]</tt>",
               dumb_replace=dumb_replace),
    require('\\', "Je ne vois pas le caractère d'échappement nécessaire"),
    reject('-r', "On a pas besoin d'expression régulière étendue"),
    number_of_is('/', 4,
                 """Votre réponse doit contenir 4 slashs.
                 3 sont obligatoires pour faire une substitution normale
                 et il en faut un de plus car on veut remplacer
                 le slash par autre choses."""),
    require(':', "On veut mettre un ':' (deux point) à la place du slash"),
    reject('\\:', "Le ':' n'est pas spécial, pas la peine de le protéger"),
    shell_display,
    ),
    indices=(
    """Vous ne trouverez pas la solution en multipliant les guillemets
    ou les apostrophes car le <tt>/</tt> n'est pas un caractère
    spécial pour le shell mais pour la commande <tt>sed</tt>""",
    "Le caractère d'échappement est \\",
    ),
    )

add(name="dans fichier",
    required=["intro", "sh:'Bonjour' dans 'toto'", "sh:redirection entrée"],
    question="""Donnez la commande prenant le contenu du
    fichier <tt>xxx</tt>, remplaçant tous les <tt>a</tt> par des <tt>b</tt>
    et stockant le résultat dans le fichier <tt>yyy</tt>""",
    tests=(
    reject(('tr', 'cat', '|'),
           """La seule commande qui vous est nécessaire est <tt>sed</tt>"""),
    require('sed', """Il faut utiliser <tt>sed</tt> pour la substitution"""),
    reject("$(", "Pas besoin de remplacement, c'est hors-sujet"),
    require('s/a/b/g',
            """Il faut indiquer à <tt>sed</tt>
            que l'on veux remplacer tous les <tt>a</tt> par des <tt>b</tt>"""),
    shell_good(("sed 's/a/b/g' <xxx >yyy",
                "sed 's/a/b/g' xxx >yyy") , dumb_replace=dumb_replace),
    require(('<', '>'),
            """Il faut rediriger l'entrée
            et la sortie standard de <tt>sed</tt>"""),
    reject("-r", "À quoi sert le <tt>-r</tt>&nbsp;?"),
    Expect('xxx'),
    Expect('yyy'),
    shell_display,
    ),
    indices=("Il faut rediriger l'entrée et la sortie standard",),
    )

add(name="enlève commentaires",
    required=["dans fichier", "slash", "expreg:intro"],
    question="""On veut enlever tous les commentaires définis
    par <tt>// commentaire jusqu'à la fin de la ligne</tt>
    du fichier <tt>tp.c</tt> et stocker le résultat dans
    <tt>tp_.c</tt>
    <p>
    Si <tt>tp.c</tt> contient :
    <pre>jhsla sadf dsafsd afds fds f // sfasdf sdfasfas dsfa
saddasd asfddsafa //
//afsfs
a//b//c</pre>
Alors <tt>tp_.c</tt> contiendra :
<pre>jhsla sadf dsafsd afds fds f 
saddasd asfddsafa 

a</pre>
    """,
    tests=(
    require(".*",
            """Vous n'avez pas indiqué le <em>pattern</em> représentant
            une chaine de caractère quelconque pour indiquer
            ce qu'il y a après le <tt>//</tt>."""),
    reject("^", "Un commentaire ne commence pas forcément en début de ligne"),
    reject("[", """N'utilisez pas les crochets pour annuler la signification
           du '/' mais échappez le."""),
    reject("/g", """L'option <tt>g</tt> de <tt>sed</tt>
    est inutile car il n'y a qu'une seule substitution à faire dans
    la ligne"""),
    Reject('|', 'La réponse est en une seule commande, pas de pipeline'),
    reject("$", """Le <tt>$</tt> est inutile car le <tt>.*</tt>
    prend le maximum de caractères possible,
    il va donc jusqu'à la fin de la ligne"""),    
    shell_good(r"sed 's/\/\/.*//' tp.c >tp_.c", dumb_replace=dumb_replace),
    shell_good(r"sed 's/\/\/.*//' <tp.c >tp_.c", dumb_replace=dumb_replace),
    require('\\/\\/',
            """Je ne vois pas les 2 <em>slashs</em> du commentaire
            dans l'expression.
            Avez-vous oublié de les protéger
            avec un <em>anti-slash</em>&nbsp;?"""),
    require('//', """Il faut indiquer que vous remplacez le commentaire
    par une chaine vide (un espace n'est pas une chaine vide)"""),
    reject('-r',
           """Vous n'avez pas besoin d'expression régulière étendue,
           enlevez les <tt>-r</tt>"""),
    require(("tp.c", "tp_.c"),
            """Je ne trouve pas les 2 noms de fichiers dans la commande"""),
    require('>',
            """Il faut rediriger la sortie standard de la commande vers
            le fichier à créer"""),
    number_of_is('/', 5, 'La bonne réponse contient 5 <em>slash</em>'),
    shell_display,
    ),
    indices=("Il faut rediriger l'entrée et la sortie standard",
             "Il ne faut pas oublier d'annuler le <tt>/</tt>",
             ),
    )

dollar_required = require('$',
                     "Je ne vois pas le <tt>$</tt> indiquant la fin de ligne")

add(name="enlever dernier",
    required=["intro", "expreg:ligne de A"],
    question="""Donnez la commande permettant d'enlever
    le dernier caractère de chaque ligne quel qu'il soit.
    <p>
    La commande lit le fichier à transformer sur son entrée
    standard et écrit le résultat sur sa sortie standard.
    C'est donc un filtre.""",
    tests=(
    dollar_required,
    require('.',
            """Je ne vois pas le <tt>.</tt> représentant un
            caractère quelconque"""),
    Bad(Comment(Contain('-r') | Contain('\\1') | Contain('('),
                "Pas besoin d'expression régulière étendue")),
    shell_good("sed 's/.$//'", dumb_replace=dumb_replace),
    shell_bad("sed 's/.$//g'",
              """Le <tt>g</tt> est inutile car il n'y a qu'une seule
              substitution à faire sur la ligne.""",
              dumb_replace=dumb_replace),
    reject('g', """Pas besoin de l'option <tt>g</tt> car la sustitution
    n'est faite qu'une fois par ligne"""),
    reject('s/.$/$/', "Vous remplacez le dernier caractère par un dollar..."),
    require('//', """Je ne vois pas la séquence de caractères,
    indiquant que vous voulez remplacer par rien du tout.
    Je rappelle qu'un espace ce n'est pas rien."""),
    reject('-r',
           """Vous n'avez pas besoin d'expression régulière étendue,
           enlevez les <tt>-r</tt>"""),
    reject('"', "Le guillemet n'annule pas la signification du dollar"),
    shell_display,
    ),
    )

add(name="TAG XML vides",
    required=["expreg:ligne de A", "enlever dernier"],
    before="""Les fichiers XML contiennent des marqueurs (balises) de la forme :
    <pre>Du &lt;NOM_DU_TAG&gt;texte &lt;b&gt;pouvant&lt;/b&gt; contenir&lt;/NOM_DU_TAG&gt; d'autres &lt;x&gt;&lt;/x&gt; marqueurs.</pre>
    Dans le texte précédent il y a 3 marqueurs.
    Le marqueur <tt>x</tt> ne contient rien.
<p>
    ATTENTION: &lt;x&gt;&lt;/y&gt; n'est pas un marqueur vide.
""",
    question="""Donnez la commande réécrivant sur sa sortie standard
    le fichier XML lu sur son entrée standard en éliminant
    les marqueurs ne contenant rien.""",
    tests = (
        Expect('sed'),
        Expect('+',
             """Les noms de TAG font plusieurs caractères et ne sont pas vide.
                Il doit donc y avoir une répétition non vide."""),
        Reject("</", """Vous devez échapper le / de fin de TAG pour qu'il
               ne soit pas interprété par <tt>sed</tt>"""),
        Good(Replace(dumb_replace, Shell(
            Equal("sed -r 's/<([^>]+)><\\/\\1>//g'")))),
        Reject('.+',
              "Le <tt>.</tt> répété va <em>avaler</em> le symbole &lt;"),
        Good(Replace(dumb_replace, Shell(
            Equal("sed -r 's/<([^>]+)><\\/\\1>//g'")))),
        Bad(Comment(Replace(dumb_replace, Shell(
            Equal("sed -r 's/<(.+)><\\/\\1>//g'"))),
                    "Le <tt>.+</tt> va <em>avaler</em> le symbole &lt;"),
            ),
        Expect('/g', """Il peut y avoir plusieurs TAG sur la même ligne,
               il faut donc faire plusieurs remplacements"""),
        Expect('(', """Vous devez définir un groupe pour vérifier que le TAG
        fermant est du même type que le TAG ouvrant."""),
        Expect('-r', """Pour que le groupes fonctionnent, il mettre l'option
        de <tt>sed</tt> pour lui dire d'utiliser
        une expression régulière étendue."""),
        shell_display,
        ),
    )

add(name="ajouter fin",
    required=["enlever dernier"],
    question="""Donnez le filtre ajoutant <tt>toto</tt>
    à la fin de chaque ligne lue.""",
    tests=(
    expect('sed'),
    reject('g', """Pas besoin de l'option 'g' puisque la substitution
    n'est possible qu'une fois par ligne"""),
    shell_good("sed 's/$/toto/'", dumb_replace=dumb_replace),
    shell_bad("sed -r 's/(.)$/\\1toto/'",
              "Ceci ne fonctionne pas si la ligne est vide.",
              dumb_replace=dumb_replace),
    shell_bad("sed 's/.*/&toto/'",
              """Ce filtre fontionne, mais il n'est ni le plus court,
              ni le plus performant.
              <p>
              Il suffit de remplacer la fin de ligne par <tt>toto</tt>""",
              dumb_replace=dumb_replace),
    shell_bad("sed 's/.$/&toto/'",
              """Ceci ne fonctionne pas si la ligne est vide."""
              ,dumb_replace=dumb_replace),
    shell_bad("sed 's/$/&toto/'",
              """Savez-vous que le <tt>&amp;</tt> représente une chaine
              vide dans la substitution que vous faites&nbsp;?
              Vous pouvez donc faire une commande plus courte."""
              ,dumb_replace=dumb_replace),
    number_of_is('/', 3,"Il n'y a pas le bon nombre de / dans votre commande"),
    dollar_required,
    reject('/.$/', """On ne veut pas remplacer le dernier caractère
    de chaque ligne mais la fin de ligne elle même"""),
    reject('/toto$/', """Vous ajoutez <tt>toto$</tt>, le dollar
    dans la partie droite n'est pas spécial"""),
    shell_display,
    ),
    indices=(
    """Commencez par répondre à la question en remplaçant le
    dernier caractère par <tt>toto</tt> puis ensuite modifiez
    la commande pour ne plus tenir compte du dernier caractère.
    <em>N'oubliez pas, on veut la commande la plus courte</em>""",    
    ),
    )
    
add(name="enlève mot",
    required=["intro", "expreg:négation"],
    question="""Quel filtre (commande lisant son entrée standard
    et écrivant sur sa sortie standard) permet de remplacer tous
    les caractères du début de la ligne jusqu'au premier espace (inclu)
    par rien du tout.
    <p>
    Et ceci pour toutes les lignes.
    <p>
    La ligne <tt>ggg jjj kkk</tt> devient <tt>jjj kkk</tt>
    """,
    tests=(
        Bad(Comment(Contain("-r") | Contain("+") | Contain('('),
                    "Pas besoin d'expression régulière étendue")),
        shell_good( "sed 's/[^ ]* //'", dumb_replace=dumb_replace),
        shell_bad( "sed 's/.* //'",
		"Essayez avec une phrase contenant plusieurs mots",
		 dumb_replace=dumb_replace),
        reject('g', "On veut faire la substitution qu'une seule fois"),
        reject('/^',"Pas besoin de préciser que c'est le premier de la ligne"),
        Expect('//', "Je ne trouve pas le remplacement pas rien du tout"),
        Expect('[^ ]', """Un mot est une répétition de caractères qui
        ne sont pas des espaces"""),
        shell_display,
        ),
    )



add(name="mot",
    required=["intro", "expreg:négation"],
    before="""On considérera qu'un mot est un ensemble de
    caractères ne contenant pas d'espace (mais pouvant contenir
    d'autres séparateurs).
    <pre>Je&#9251;suis&#9251;une&#9251;&#9251;phrase.</pre>
    <p>Devient
    <pre>MOT&#9251;MOT&#9251;MOT&#9251;&#9251;MOT</pre>
    """,
    question="""Donner la ligne de commande permettant de remplacer
    tous les mots par le texte suivant&nbsp;: <tt>MOT</tt><br>
    On ne changera pas le nombre d'espaces entre les mots.
    """,
    tests=(
    shell_good( ("sed -r 's/[^ ]+/MOT/g'", "sed 's/[^ ][^ ]*/MOT/g'"),
                dumb_replace=dumb_replace,
                ),
    shell_good( "sed 's/[^ ]*[^ ]/MOT/g'",
                "Il est préférable de mettre l'étoile à la fin",
                dumb_replace=dumb_replace,
                ),
    reject("/[^ ]*",
              """L'expression <tt>[^ ]*</tt> représente des chaines
              vide. Donc MOT risque d'être inserré entre chaque paire
              d'espace."""),
    shell_bad("sed 's/[^ ]+/MOT/g'",
              """Presque ! Il faut dire à <tt>sed</tt> que vous
              utilisez une expression régulière étendue""",
              dumb_replace=dumb_replace,
              ),
    reject(".*",
           """<tt>.*</tt> prend la plus grande chaine possible
           il va donc contenir des espaces, ce n'est donc pas un mot"""),
    require("[^ ]",
            """Je ne vois pas l'expression régulière représentant
            un caractère qui n'est pas un espace"""),
    shell_require("[^ ]+",
                  """Je ne vois pas le <em>pattern</em> représentant
                  un mot sans espace""",
                  dumb_replace=( ("[^ ][^ ]*", "[^ ]+"), ),
                  ),
    require('/g', "Vous ne faites la substitution qu'une fois par ligne..."),
    reject(('a-z','A-Z'), """Un mot n'est pas composé de caractères
    alphabétique mais de caractère qui <b>ne sont pas des espaces</b>
    donc enlevez le <tt>a-z</tt> cela ne sera pas accepté."""),
    reject(('/ MOT/', '/MOT /', '/ MOT /'), """Je pense que votre solution ne
    fonctionne pas si le mot est à une extrémité de la ligne..."""),
    shell_display,
    ),
    )

add(name="séquencielle",
    required=["intro"],
    question="""Donner la ligne de commande travaillant sur
    l'entrée standard qui&nbsp;:
    <ul>
    <li> Remplace tous les <tt>bleu</tt> par <tt>blanc</tt>
    <li> <b>puis</b> remplace tous les <tt>c</tt> minuscule par <tt>C</tt> majuscule
    </ul>
    <p>En lançant une seule fois la commande de remplacement.
    """,
    tests=(
    reject('-r', "Pas besoin d'expression régulière étendue"),
    require("/bleu/blanc/",
            "Je ne vois pas la substitution de <tt>bleu</tt> en <tt>blanc</tt>"
            ),
    require("/c/C/",
            "Je ne vois pas la substitutions de <tt>c</tt> en <tt>C</tt>"
            ),
    shell_good("sed -e 's/bleu/blanc/g' -e 's/c/C/g'"),
    shell_good("sed 's/bleu/blanc/g;s/c/C/g'",
               """Dans les exercices suivant, la syntaxe avec le <tt>;</tt>
               sera refusée, il est en effet préférable de faire&nbsp;:
               <pre>sed -e 's/bleu/blanc/g' -e 's/c/C/g'</pre>""",
               dumb_replace=dumb_replace),
    reject((';','|'), "On ne lance <tt>sed</tt> qu'une seule fois"),
    number_of_is('sed', 1, "On utilise <tt>sed</tt> une seule fois"),
    number_of_is('-e', 2,
                 """Vous devez indiquer 2 sustitutions, il devrait
                 y avoir 2 fois l'option <tt>-e</tt>."""),
    number_of_is('/', 6,
                 """Vous devez indiquer 2 sustitutions, il devrait
                 y avoir 6 slashs dans la commande."""),
    number_of_is('/g', 2,
                 """Il devrait y avoir deux fois l'option indiquant
                 que l'on fait toute les substitutions dans la ligne"""),
    shell_display,
    ),
    indices=("Respectez l'ordre de l'énoncé sinon le résultat est différent",
             "Il faut indiquer plusieurs fois <tt>-e</tt>",
             ),
    good_answer="""Lancez la commande en tapant 'BLEUbleu'
    et regardez le résultat, n'est-ce pas étrange ?.
    Il faut que vous notiez que les substitutions sont
    faites les unes après les autres.""",
    )
    
add(name="inverse",
    required=["intro", "expreg:identique", "mot"],
    before="""On a un fichier contenant dans chaque ligne
    un nom et un prénom.
    On suppose que le SEUL ESPACE de la ligne est entre
    le nom et le prénom.
    <p>
    On suppose aussi qu'il peut arriver que le nom ou le prénom
    soit une chaine vide.
    <pre>Thierry&#9251;EXCOFFIER
&#9251;VANDORPE
Jacques&#9251;
&#9251;</pre>
 <p> Devient
    <pre>EXCOFFIER&#9251;Thierry
VANDORPE&#9251;
&#9251;Jacques
&#9251;</pre>
    """,
    question="""Donnez la ligne de commande utilisant <tt>sed</tt> permettant
    d'inverser le nom et le prénom.
    On laissera <tt>sed</tt> travailler sur l'entrée et la sortie standard.
    <p>
    Testez bien la commande avant de proposer la solution,
    comme d'habitude c'est une solution simple qui est demandée.
    <p>
    Nom et prénom peuvent contenir n'importe quel caractère (sauf espace).
    """,
    tests=(
    shell_good( ("sed -r 's/([^ ]*) ([^ ]*)/\\2 \\1/'",
                 "sed -r 's/(.*) (.*)/\\2 \\1/'"),
                dumb_replace=dumb_replace,
                ),
    shell_bad( ("sed -r 's/([^ ]+) ([^ ]+)/\\2 \\1/'",
                "sed -r 's/(.+) (.+)/\\2 \\1/'"),
               """Presque juste, mais cela ne fonctionne
               pas si le nom ou le prénom est vide.""",
               dumb_replace=dumb_replace),
    reject('/g', """Le <tt>/g</tt> est inutile puisqu'il n'y a qu'une
    répétition dans la ligne"""),
    number_of_is('(', 2, """On a besoin de faire deux groupes
    pour répondre à la question"""),
    number_of_is(')', 2, """On a besoin de faire deux groupes
    pour répondre à la question"""),
    reject('+', "N'oubliez pas que l'on accepte les noms et prénoms vides"),
    require('-r', """Comme on utilise les groupes des expressions régulières,
    il faut indiquer la bonne option à <tt>sed</tt>"""),
    Reject('\\(', 'Il ne faut pas échapper les parenthèses'),
    reject(('^', '$'),
           """<tt>^</tt> et <tt>$</tt> ne sont pas nécessaires pour
           répondre à cette question"""),
    reject('\\2\\1', """N'auriez-vous pas oublié de mettre un espace entre
    le nom et le prénom&nbsp;?"""),    
    shell_display,
    ),
    indices=("""On doit donner une option particulière à <tt>sed</tt>
    pour qu'il utilise les expressions régulière étendues""",
             """Ne mettez pas de caractères inutiles comme le <tt>$</tt>
             ou bien le <tt>g</tt>""",
             """Il faut utiliser le tout sauf espace.""",
             """Pensez à utiliser les groupes.""",
             ),
    )

les_modes = """<p>
Comme vous utilisez <tt>mv</tt> le fichier <tt>xxx</tt>
est remplacé par le fichier <tt>yyy</tt> qui a été créé avec
les modes par défaut. Les modes du fichier <tt>xxx</tt>
sont donc perdu.
Pour conserver les modes, il faut faire&nbsp;:
<tt>cat yyy >xxx ; rm yyy</tt>
"""

add(name="fiable",
    required=["dans fichier", "sh:fiable", "deplacer:intro"],
    before="""Vous aurez besoin d'un nom de fichier temporaire,
    prenez <tt>yyy</tt>""",
    question="""Donnez la ligne commande FIABLE prenant le contenu du
    fichier <tt>xxx</tt>, remplaçant tous les <tt>a</tt> par des <tt>b</tt>
    et stockant le résultat dans le fichier <tt>xxx</tt>""",
    tests=(
    require("mv",
            "Vous aviez utilisé <tt>mv</tt> pour faire le remplacement fiable"),
    require("&&",
            "Vous aviez utilisé <tt>&amp;&amp;</tt> pour faire le remplacement fiable"),
    reject('-i', """L'option <tt>-i</tt> est valide,
    mais vous pouvez répondre à cette question uniquement
    avec ce que vous savez déjà"""),
    reject('rm',
           "Pas besoin de détruire la destination, <tt>mv</tt> le fait"),
    shell_good(("sed 's/a/b/g' <xxx >yyy && mv yyy xxx",
                "sed 's/a/b/g' xxx >yyy && mv yyy xxx"),
               dumb_replace=dumb_replace),
    shell_good( ("if sed 's/a/b/g' <xxx >yyy ; then mv yyy xxx ; fi",
                 "if sed 's/a/b/g' xxx >yyy ; then mv yyy xxx ; fi",
                 ),
                """Une réponse plus simple&nbsp;:
                <tt>sed -e 's/a/b/g' &lt;xxx &gt;yyy && mv yyy xxx</tt>""",
                dumb_replace=dumb_replace),
    shell_bad( ("sed 's/a/b/g' <xxx >xxx", "sed 's/a/b/g' xxx >xxx"),
               """Cette commande ne fonctionne pas car le fichier est vidé
               avant que <tt>sed</tt> ai eu le temps de le lire.
               Vous devez passer par un fichier intermédiaire.""",
               dumb_replace=dumb_replace,
               ),
    shell_bad( ("sed 's/a/b/g' <xxx >yyy ; mv yyy xxx",
                "sed 's/a/b/g' xxx >yyy ; mv yyy xxx",
                ),
               """Cette commande fonctionne, mais elle n'est pas fiable
               car si la substitution est arrêtée, le disque est plein ou
               s'il y a une erreur dans les arguments de <tt>sed</tt>
               le <tt>mv</tt> aura quand même lieu et écrasera votre fichier.
               Il faut que le <tt>mv</tt> s'exécute seulement
               si le remplacement c'est bien passé.
               """,
               dumb_replace=dumb_replace,
               ),
    require(">yyy", """Je ne vois pas comment vous faites pour créer
            le fichier temporaire""", replace=((" ",""),)),
    shell_display,
    ),
    indices=("""Utilisez <tt>mv</tt> pour remplacer <tt>xxx</tt> par
    <tt>yyy</tt>""",
             """Vous devez stocker le résultat de la substitution
             dans <tt>yyy</tt> puis le déplacer à la place <tt>xxx</tt>
             si tout c'est bien passé""",
             ),
    good_answer="""
    Cette solution n'est pas parfaite, en effet les droits d'accès,
    le propriétaire, ... du fichier on pu changer en effet ils
    ont été remplacé par ceux du fichier <tt>yyy</tt> créé
    avec les valeurs par défaut.
    <p>
    On peut contourner ce problème en remplaçant <tt>mv yyy xxx</tt> par&nbsp;:
    <pre>cat yyy >xxx ; rm yyy</pre>
    L'inconvénient majeur de cette solution est qu'elle n'est plus fiable
    en effet si le disque est plein le fichier <tt>xxx</tt> est tronqué.
    <p>
    Une autre manière de contourner est de faire&nbsp;:
    <pre>chmod --reference=xxx yyy && mv yyy xxx</pre>
    Cette solution est fiable dans le cas ou vous êtes propriétaire
    du fichier <tt>xxx</tt>
    """,
    )



add(name="remplacer hiérarchie",
    required=["fiable", "sh:boucle"],
    before="""Pour remplacer un mot par un autre dans un fichier,
    nous avons fait&nbsp;:
    <pre>sed -e 's/blue/black/g' &lt;xxx &gt;yyy && mv yyy xxx</pre>
    """,
    question="""Quelle ligne de commande permet de remplacer
    <tt>&lt;h1&gt;</tt> par <tt>&lt;h2&gt;</tt>
    dans tous les fichiers se terminant par <tt>.html</tt>
    dans le répertoire courant.
    <em>Les &lt; et &gt; font partis du texte à remplacer car
    ils encadrent le <em>tag</em> HTML</em>.
    <p>
    Vous utiliserez la variable <tt>I</tt> comme indice de boucle.
    Et <tt>yyy</tt> comme fichier temporaire.
    """,
    tests=(
    reject('find', "Dans le répertoire courant, pas dans la hiérarchie"),
    reject('echo', "Pas besoin de la commande <tt>echo</tt>"),
    shell_good((
    "for I in *.html ; do sed 's/<h1>/<h2>/g' <$I >yyy && mv yyy \"$I\" ; done",
    "for I in *.html ; do sed 's/<h1>/<h2>/g' <\"$I\" >yyy && mv yyy \"$I\" ; done",
    "for I in *.html ; do sed 's/<h1>/<h2>/g' \"$I\" >yyy && mv yyy \"$I\" ; done",
    ),
               dumb_replace=dumb_replace),
    shell_bad(
    "for I in *.html ; do sed 's/<h1>/<h2>/g' <$I >yyy && mv yyy $I ; done",
    """Ne fonctionne pas si un nom de fichier contient un espace (il manque
    les guillemets)""",
    dumb_replace=dumb_replace),
    shell_bad((
    """for I in *.html; do sed 's/<h1>/<h2>/g' >yyy && mv yyy "$I";done""",
    """for I in *.html; do sed 's/<h1>/<h2>/g' >yyy && mv yyy $I;done""",
    ),
    """Comment la commande <tt>sed</tt> sait ce qu'elle doit lire&nbsp;?""",
    dumb_replace=dumb_replace),
    
    reject("xxx",
           "Vous devez remplacer <tt>xxx</tt> par le fichier à transformer"),
    require( ("<h1>", "<h2>"), "Je ne vois pas les textes à remplacer"),
    require( "for", "Vous devez faire une boucle"),
    require( "done", "Et le <tt>do</tt> / <tt>done</tt> ?"),
    require( "&&", "N'oubliez pas, on veut une substitution fiable"),
    require( '$I', "Ou utilisez-vous la variable&nbsp;?"),
    require( '"', """Êtes-vous sur que cela fonctionne si le nom
    des fichiers contiennent un espace&nbsp;?"""),
    shell_require("<pattern_char>*</pattern_char>.html",
                  """Je ne vois pas le <em>pattern</em> indiquant
                  tous les fichiers <tt>.html</tt>."""),
    reject("ls",
           "On a pas besoin de <tt>ls</tt> pour avoir la liste des fichiers"),
    require('<', 'Comme d\'habitude, on redirige l\'entrées standard de <tt>sed</tt>'),
    shell_display,
    ),
    )

add(name="traduit PATH",
    required=["intro", "pipeline:intro", "variable:intro",
              "sh:affiche paramètres spéciaux" ],
    question="""Quelle est la commande affichant sur la sortie standard
    le contenu de la variable <tt>PATH</tt> en remplaçant chacun
    de deux points '<tt>:</tt>' par un espace.
    <p>
    ATTENTION : pour cette question on n'acceptera pas que des espaces
    multiples disparaissent de la variable <tt>PATH</tt>.
    """,
    tests = (
        Good(Replace(dumb_replace,Shell(Equal(
            'echo "$PATH" | sed "s/:/ /g"')))),
        Expect('PATH'),
        Expect('$PATH', "On accède au contenu d'une variable avec le..."),
        Expect('"$PATH"',
               "Il faut protéger les espaces existants dans la variable"),
        Expect('sed'),
        Expect("/ /", "Vous n'indiquez pas que vous remplacez par un espace"),
        Expect("/g",
               """Indiquez que vous voulez remplacer toutes les occurrences
               et pas seulement la première de la ligne"""),
        shell_display,
        ),
    )

add(name="cherche PATH",
    required=["intro", "traduit PATH", "sh:boucle", "sh:remplacement",
              "lister:affichage long"],
    before="""Quand on lance la commande <tt>sed</tt>,
    le shell recherche la commande dans tous les répertoires
    indiqués dans la variable <tt>PATH</tt>.
    Il lance la première commande trouvée.
    """,
    question="""On veut exécuter la commande <tt>ls -ld</tt>
    sur tous les fichiers de la forme <tt>XXX/sed</tt>
    ou les <tt>XXX</tt> sont les noms des répertoires indiqués dans
    la variable <tt>PATH</tt>.
    Pour faire cela, vous avez besoin de&nbsp;:
    <ul>
    <li> De la boucle pour pour parcourir les noms de répertoire.
    <li> De remplacer une commande par le résultat de son exécution.
    Ceci pour générer la liste des indices de la boucle
    car les <tt>:</tt> qui sont dans <tt>PATH</tt>
    ne sont pas des séparateurs pour le shell.
    <li> Du corps de boucle pour faire le <tt>ls -ld</tt> en ajoutant
    <tt>sed</tt> au répertoire qui est dans l'indice.
    </ul>
    Vous utiliserez <tt>I</tt> comme indice de boucle.
    """,
    tests=(
    require("I", "Vous n'avez pas utilisé la variable <tt>I</tt>"),
    require("PATH", "Vous n'avez pas utilisé la variable <tt>PATH</tt>"),
    require("/ /", "Vous n'indiquez pas que vous remplacez par un espace"),
    require("/g",
           """Indiquez que vous voulez remplacer toutes les occurrences
           et pas seulement la première de la ligne"""),
    require("/sed",
            """On veut les informations sur le fichier <tt>sed</tt>
            dans chacun des répertoires"""),
    shell_good(
    "for I in $(echo \"$PATH\" | sed 's/:/ /g') ; do ls -ld \"$I\"/sed ; done",
    dumb_replace=dumb_replace),
    shell_good(
        ("for I in $(echo $PATH | sed 's/:/ /g'); do ls -ld \"$I\"/sed ; done",
         "for I in $(echo \"$PATH\" | sed 's/:/ /g'); do ls -ld $I/sed ; done",
         "for I in $(echo $PATH | sed 's/:/ /g'); do ls -ld $I/sed ; done",
         ),
        """Il est fortement recommandé de mettre systématiquement
        des guillemets autour des accès aux variables&nbsp;:
        <tt>"$PATH"</tt> au lieu de <tt>$PATH</tt>""",
        dumb_replace=dumb_replace),
    require("|", """Il faut faire un pipeline avec <tt>echo</tt>
    et <tt>sed</tt> pour obtenir le contenu de la variable <tt>PATH</tt>
    avec des espaces à la place des ':'"""),
    shell_require(">PATH</variable>",
                  "Vous n'utilisez pas le contenu de la variable <tt>PATH</tt>"),
    shell_require(">I</variable>",
                  "Vous n'utilisez pas le contenu de <tt>I</tt>"),
    shell_require("<replacement",
                  """Je ne vois pas de 'remplacement'.
                  La commande <tt>for</tt> a besoin du résultat
                  du pipeline pour avoir la liste des paramètres."""),
    require('-ld', "On veut utiliser <tt>-ld</tt> comme option de <tt>ls</tt>"),
    shell_display,
    ),
    good_answer="""La solution que vous avez proposée est en effet
    la plus simple.
    Mais elle montre l'énorme limitation du shell&nbsp;:
    il peut faire n'importe quoi dès que des variables
    contiennent des espaces.
    <p>
    Si la variable <tt>PATH</tt> contient des noms de répertoires
    avec des espaces votre script ne fonctionnera pas.""",
    )


add(name="garde slash",
    required=["mot", "slash"],
    question="""Donner la commande lisant son entrée standard
    et affichant sur sa sortie standard que les <tt>/</tt>.
<table><tr><th>Entrée<th>Sortie</tr>
<tr><td><pre>/usr/include
/tmp

a/a/a/a/a</pre>
 <td><pre>//
/

////</pre>
</tr></table>
    """,
    tests=(
    reject('*', "Pourquoi utilisez-vous une répétition de caractères&nbsp;?"),
    reject('-r', "Pas besoin d'expression régulière étendue"),
    reject('+', """Le <tt>+</tt> fonctionne avec les expressions
    régulières étendues. Il n'est pas nécessaire de l'utiliser dans
    cet exemple car on remplace par rien et cela ne gène pas
    de remplacer rien par rien."""),
    reject('/^', """Les caractères à substituer peuvent être partout
    dans la ligne.
    Pourquoi dites-vous qu'ils sont en début de ligne&nbsp;?"""),
    reject('!', """Le ! est pour les <em>pattern</em> du shell, pas
    les expressions régulières"""),
    shell_good(r"sed 's/[^/]//g'", dumb_replace=dumb_replace),
    reject( "[^\/]",
                """Les crochets annulent la signification de l'antislash
                et du slash. Entre crochet, le slash et l'antislash
                sont des caractères sans signification particulière.
                Vous n'avez donc pas besoin de les protéger par
                un antislash."""
               ),
    require('//', """Je ne vois pas la liste de caractères indiquant que vous
    voulez remplacer par rien du tout les caractères autres."""),
    require('/g', """Il manque l'option de substitution indiquant qu'il
    y a plusieurs substitutions à faire sur la ligne"""),
    require('^', """On a besoin de la négation pour indiquer 'tout sauf'
    pour un ensemble de caractères."""),
    #    answer_length_is(15, 
    shell_display,
    ),
    )
    
add(name="annule racine",
    required=["mot", "slash"],
    question="""Donner la commande lisant son entrée standard
    et affichant sur sa sortie standard ce qu'elle a lu,
    à l'exception de la ligne dont le contenu exacte est&nbsp;: <tt>/</tt>
	(un caractère unique)
    qui est remplacé par une ligne vide.
    <p>
    <tt>usr/include</tt> est inchangé<br>
    <tt>/</tt> disparait, il reste une ligne vide""",
    tests=(
    expect('sed'),
    reject("/g", """Il n'y a qu'une seule substitution à faire
    sur la ligne, l'option de remplacement 'g' est en trop."""),
    reject('-r', "On a pas besoin d'expression régulière étendue"),
    shell_good(r"sed 's/^\/$//'", dumb_replace=dumb_replace),
    reject( "[/]",
                """Il y a plus simple que les crochets pour
                annuler la signification du slash."""),
    require(('^','$'), """Pour indiquer que <tt>/</tt> est seul sur
    la ligne, il faut indiquer que le <em>pattern</em> représente
    une ligne complète et qu'il va donc du début jusqu'à la fin"""),
    number_of_is('/', 4, "Il n'y a pas le bon nombre de /"),
    require('//', """Je ne vois pas la séquence de caractères indiquant
    que vous remplacer le texte trouvé par rien"""),
    reject('[', "Pourquoi il y a un crochet dans votre réponse&nbsp;?"),
    reject('*', "Pourquoi il y a une étoile dans votre réponse&nbsp;?"),
    shell_display,
    ),
    indices=("""<tt>^</tt> représente le début de ligne et
    <tt>$</tt> représente la fin de ligne""",),
    )

comm = """Donnez la ligne de commande affichant votre profondeur
    dans la hiérarchie de fichier.    
    <p>
    Si vous êtes dans <tt>/</tt> cela doit vous afficher 1.<br>
    Si vous êtes dans <tt>/etc</tt> cela doit vous afficher 2.<br>
    Si vous êtes dans <tt>/usr/include</tt> cela doit vous afficher 3.
    <p>
    Inspirez-vous des questions auxquelles vous avez déjà répondu
    et n'utilisez pas le <tt>|</tt> des expressions régulières.
    <p>
    """

add(name="profondeur wc",
    required=["compte:echo", "sh:directory courant",
              "intro", "annule racine", "garde slash", "pipeline:intro",
              "séquencielle"
              ],
    question=comm + """<b>Vous utiliserez la commande <tt>wc</tt>
    pour calculer la longueur</b>""",
    tests=(
    reject('echo', "Pas besoin de <tt>echo</tt> pour cette question."),
    shell_good(r'''pwd | sed -e 's/^\/$//' -e 's/[^/]//g' | wc -c'''),
    shell_good((r'''pwd | sed   's/^\/$//' -e 's/[^/]//g' | wc -c''',
                ),
               "Généralement on met l'option <tt>-e</tt> deux fois"),
    shell_bad(r'''pwd | sed -e 's/[^/]//g' | wc -c''',
              "Ne fonctionne pas pour la racine"),
    number_of_is("sed", 1,
                 "On lance la commande <tt>sed</tt> une seule fois"),
    reject(r'[^\/]', "Pas besoin d'antislash avant le / entre les crochets"),
    reject(('*','+'), """Pas besoin de '*' ou '+' pour cette question"""),
    require('s/^\/$//', """Je ne vois pas la substitution qui enlève
    les / qui sont tout seul sur une ligne (cas particulier de la racine)"""),
    require('s/[^/]//g', """Je ne vois pas la substitution qui enlève
    tous les caractères qui ne sont pas des slash."""),
    reject('-m', """Utilisez plutôt <tt>-c</tt> à la place de <tt>-m</tt>"""),
    Bad(Comment(Replace((('-e', ''), ("'", ""), ('"', '')),
                        RMS(Contain("s/[^/]//g s/^\\/$//"))),
                            """L'ordre des substitutions est important.
                            Votre version ne marchera pas pour le
                            premier niveau (<tt>/etc</tt> par exemple.)""")),
    reject('s/^\/$//g', """À quoi sert l'option <tt>g</tt> s'il n'y
    a qu'une seule substitution à faire sur la ligne&nbsp;?"""),
    number_of_is('|', 2, "Il y a 3 commandes à faire donc il faut 2 pipe."),
    reject(('-m', '--chars'),
           """Comptez le nombre d'octets plutôt que de caractères."""),
    shell_display,
    ),
    indices=( """Il faut compter le nombre de <tt>/</tt>""",
              """La racine (<tt>/</tt> tout seul) est un cas particulier,
              cela devrait être une chaine vide.""",
              ),
    )

add(name="profondeur expr",
    required=["profondeur wc", "sh:remplacement", "calculer:longueur"],
    question=comm + """<b>Vous utiliserez la commande <tt>expr</tt>
    pour calculer la longueur</b>""",
    tests=(
    reject('/.$/', '''Votre solution est trop astucieuse pour que le système
    puisse la tester.
    Utilisez ce qui est proposé dans les prérequis'''),
    shell_good(r'''expr length "$(pwd | sed -e 's/^\/$//' -e 's/[^/]//g')" + 1'''),
    shell_good(r'''expr length $(pwd | sed -e 's/^\/$//' -e 's/[^/]//g') + 1'''),
    shell_good(r'''expr 1 + length "$(pwd | sed -e 's/^\/$//' -e 's/[^/]//g')"'''),
    shell_good(r'''expr 1 + length $(pwd | sed -e 's/^\/$//' -e 's/[^/]//g')'''),
    shell_good(r'''expr length "$(pwd | sed -e 's/[^/]//g' -e 's/^\/$//' )" + 1'''),
    shell_good(r'''expr length $(pwd | sed -e 's/[^/]//g' -e 's/^\/$//' ) + 1'''),
    shell_good(r'''expr 1 + length "$(pwd | sed -e 's/[^/]//g' -e 's/^\/$//' )"'''),
    shell_good(r'''expr 1 + length $(pwd | sed -e 's/[^/]//g' -e 's/^\/$//' )'''),
    reject(r'[^\/]', "Pas besoin d'antislash avant le / entre les crochets"),
    reject('=', "Vous n'avez pas besoin de =&nbsp;!"),
    expect('pwd'),
    expect("length"),
    expect("expr"),
    Bad(Comment(Start('pwd'),
                """Votre solution fonctionne peut-être, mais pour qu'elle
                soit acceptée, il faut qu'elle commence
                par <tt>expr</tt>""")),
    require('1', "Il faut ajouter 1 au nombre de <em>slash</em> présent"),
    shell_display,               
    ),
    )

add(name="basename",
    required=["sh:boucle", "pattern:.c et .h",
              "sh:remplacement", "deplacer:intro", "slash",
              "enlève commentaires"],
    before="""La commande standard <tt>basename NomFichier Extension</tt>
    fait l'équivalent de&nbsp;:
    <pre>echo NomFichier | sed -e 's/.*\\///' -e 's/Extension$//'</pre>
    Elle enlève donc le nom du répertoire et l'extension.
    <tt>basename /usr/include/stdio.h .h</tt> donne donc <tt>stdio</tt>
    """,
    question="""Pour tous les fichiers <tt>.c</tt> du répertoire
    courant renommez les fichiers en remplaçant le <tt>.c</tt>
    par <tt>.xc</tt>
    <p>
    Vous utiliserez la variable shell <tt>I</tt> comme
    indice de boucle.
    """,
    tests=(
    reject('|', 'Pas besoin de pipe pour cette question'),
    reject("sed",
           """Utilisez la commande <tt>basename</tt>, pas <tt>sed</tt>
           qui était là seulement pour vous expliquer."""),
    Bad(Comment(RMS(~Contain('do mv')),
                "La boucle ne contient qu'une seule commande : <tt>mv</tt>")
        ),
    Bad(Comment(RMS(~Contain('mv $I') & ~Contain('mv "$I"')),
                """Le premier argument de <tt>mv</tt> est le nom fichier
                à déplacer, donc le contenu de la variable de boucle""")
        ),
    reject('echo', "On n'a pas besoin de la commande <tt>echo</tt>"),
    require("mv", "On renomme avec la commande <tt>mv</tt>"),
    require("for", "On doit faire une boucle <tt>for</tt>"),
    require("basename", "On veut utiliser la commande <tt>basename</tt>"),
    reject((" c).xc", ' c)".xc'),
           "Le fichier <tt>to.c</tt> va être renommé en <tt>to..xc</tt>."),
    reject((" .c)xc", ' .c)"xc'),
           "Le fichier <tt>to.c</tt> va être renommé en <tt>toxc</tt>."),
    reject("./", """S'il vous plaît, n'utilisez pas <tt>./</tt> dans votre
            réponse. Bien que cela soit pratique si le nom du fichier
            commence par un tiret."""),
    shell_require("<replacement",
                  """Je ne vois pas de 'remplacement'.
                  La commande <tt>mv</tt> a besoin du résultat
                  de la commande <tt>basename</tt> comme
                  paramètre"""), 
    shell_good('for I in *.c ; do mv "$I" "$(basename "$I" c)xc" ; done'),
    shell_bad(('for I in *.c ; do mv "$I" $(basename "$I" c)xc ; done',
               'for I in *.c ; do mv "$I" "$(basename $I c)"xc ; done'),
              """Presque&nbsp;! Il manque encore des guillemets."""),
    require("xc", "On veut ajouter le suffixe <tt>xc</tt>"),
    require('"',
            """N'oubliez pas le cas où le nom du fichier contient un espace,
            il faut protéger l'accès au variables."""),
    reject(" $I ",
           "Tous les accès aux variables doivent être entre guillemets"),
    shell_good('for I in *.c ; do mv "$I" "$(basename "$I" .c).xc" ; done'),
    shell_bad(('for I in *.c ; do mv "$I" $(basename "$I" .c).xc ; done',
               'for I in *.c ; do mv "$I" "$(basename $I .c)".xc ; done'),
              """Presque&nbsp;! Il manque encore des guillemets."""),
    shell_require("<argument>.c</argument>",
                  """Il manque un argument à <tt>basename</tt> pour
                  lui dire d'enlever le <tt>.c</tt> de <tt>$I</tt>"""),
    require('*', """Où est l'étoile indiquant que vous voulez
    tous les <tt>.c</tt>"""),
    shell_require("<pattern_char>*</pattern_char>",
                  """Il ne faut pas protéger l'étoile. Sinon est est
                  considérée comme une vrai étoile et non
                  un élément de <em>pattern</em>"""),
    require("I", "Je ne vois pas le nom de la variable qui est l'indice"),
    Expect(" *.c", """Je ne vois pas le pattern représentant les fichiers
             <tt>.c</tt> du répertoire courant."""),
    shell_display,               
    ),
    good_answer="""
    Attention, je ne garantis pas que cette commande s'évaluera
    correctement avec tous les interpréteurs shells.
    Il y a en effet une imbrication de guillemets dans cette commande.""",
    )

add(name="enlève sans point",
    required=['intro', 'expreg:un spécial'],
    question="""Quelle ligne de commande filtre l'entrée standard en remplaçant
    sur chacune des lignes le dernier '.' et ce qui est à sa gauche par rien.
    S'il n'y a pas de point rien n'est fait.
    <p>
    Par exemple :
    <table><tr><th>Entrée<th>Sortie</tr>
    <tr><td><pre>toto
toto.c
truc
truc.tar
truc.tar.gz</pre>
<td><pre>toto
c
truc
tar
gz</pre></tr></table>""",
    tests = (
        Bad(Comment(Contain('-r') | Contain('(') | Contain('\\1'),
            "Pas besoin d'expression régulière étendue.")),
        Expect('sed'),
        Reject("$", "On a pas besoin de faire référence à la fin de ligne"),
        Expect('*', """Le remplacement ce fait avec des suites de plusieurs
        caractères. Votre réponse ne contient rien dans ce sens..."""),
        Reject('/^', """Pas besoin de '^' car l'expression cherchée est celle
        qui est le plus au début possible"""),
        Expect('/.*', """Le début de ce que l'on cherche est une chaine de
        caractères quelconques."""),
        Reject('/g', "Une seule substitution est nécessaire donc pas de /g"),
        Expect('//', 'Je ne vois pas le remplacement par un chaine vide'),
        
        Good(Replace(dumb_replace,Shell(
            Equal("sed 's/.*\\.//'") | Equal("sed 's/.*[.]//'") ))),
        shell_display,
        ),
    )

add(name="enlève point gauche",
    required=['intro','expreg:négation', 'expreg:ligne de A'],
    question="""Quelle ligne de commande filtre l'entrée standard en remplaçant
    les lignes ne contenant <b>pas</b> le caractère '.' par une ligne vide.
    <p>
    Par exemple :
    <table><tr><th>Entrée<th>Sortie</tr>
    <tr><td><pre>toto
toto.c
truc
truc.tar
truc.tar.gz</pre>
<td><pre>&nbsp;
toto.c

truc.tar
truc.tar.gz</pre></tr></table>""",
    tests = (
        Expect('sed'),
        Reject("\\.]", """On a pas besoin d'échapper le point quand il
               est entre les crochets"""),
        Reject(".*", """<tt>.*</tt> peut contenir des '.' donc ils peuvent
               être effacés."""),
        Bad(Comment(Replace(dumb_replace + (('/g','/'),),Shell(
            Equal("sed 's/[^.]//'") | Equal("sed 's/[^.]*//'")
            )),
                    """Vous enlevez les caractères qui ne sont pas
                    des points dans la ligne !""")),
        Expect('^',
               """Vous n'avez pas indiqué que l'expression commençait en début
               de ligne"""),
        Expect('$',
               """Vous n'avez pas indiqué que l'expression finissait en fin
               de ligne"""),
        Expect('*', """Le remplacement ce fait avec des suites de plusieurs
        caractères. Votre réponse ne contient rien dans ce sens..."""),
        
        Bad(Comment(Replace(dumb_replace,Shell(Equal("sed 's/^[^.]*$//g'"))),
                    "Une seule substitution est nécessaire")),
        Good(Replace(dumb_replace,Shell(Equal("sed 's/^[^.]*$//'")))),
        shell_display,
        ),
    )

add(name="extensions",
    required=["enlève sans point", "enlève point gauche", "séquencielle"],
    question="""Combiner CORRECTEMENT les questions auquelles vous avez
    déjà répondu pour obtenir le résultat suivant :
<table><tr><th>Entrée<th>Sortie</tr>
    <tr><td><pre>toto
toto.c
truc
truc.tar
truc.tar.gz</pre>
<td><pre>&nbsp;
c

tar
gz</pre></tr></table>""",
    tests = (
        Reject("|", """Une seule commande est nécessaire, pas besoin de pipe
               ni d'expression régulière étendues"""),
        Bad(Comment(Contain("-r") | Contain("("),
                    """Pas besoin d'expression régulière étendues""")),
        Good(Shell(Equal("sed -e 's/^[^.]*$//' -e 's/.*\\.//'"))),
        shell_display,
        ),
    )

add(name="liste extensions",
    required=["extensions", "trier:unique"],
    question="""Donnez la ligne de commande listant les extensions de fichiers
    utilisées dans le répertoire courant.
    Ne répétez pas les mêmes extensions plusieurs fois.
    <p>
    Ce n'est pas grave si une ligne vide est affichée.""",
    tests = (
        Good(Shell(
            Equal("ls | sed -e 's/^[^.]*$//' -e 's/.*\\.//' | sort -u")
            | Equal("ls | sed -e 's/^[^.]*$//' -e 's/.*[.]//' | sort -u")
            )),
        Expect('sort', "Chaque extension doit être affichée une seule fois"),
        ),
    default_answer = "ls | ",
    )

from awk import awk_compte

add(name="compter extensions",
    required=["extensions", "awk:compte"],
    question="""Donnez la commande qui pour chaque extension de fichier
    trouvée dans le répertoire courant,
    indique pour combien de fichiers elle s'applique.
    <p>
    Recopiez exactement les différents morceaux de commande sinon
    la réponse ne sera pas acceptée.
    """,
    default_answer = "ls | ",
    tests = (
        Good(Shell(
            Equal("ls | sed -e 's/^[^.]*$//' -e 's/.*\\.//' | %s" % awk_compte)
            | Equal("ls | sed -e 's/^[^.]*$//' -e 's/.*[.]//' | %s"%awk_compte)
            )),
        ),
    )

add(name="indent",
    required=["ajouter fin", "expreg:identique"],
    question="""Quel est le filtre qui ajoute un espace au début de chaque
    ligne de texte contenant un caractère <tt>X</tt>
    <p>
    Exemple :
    <table>
    <tr><th>Entrée<th>Sortie attendue</tr>
    <tr><td><pre>sdfafs
sdfffs
dsffsdXsdafsdf
----X-----X----
afsdfsf
X
(XXX)</pre><td><pre>sdfafs
sdfffs
 dsffsdXsdafsdf
 ----X-----X----
afsdfsf
 X
 (XXX)</pre></tr></table>""",
    tests = (
        Expect('sed'),
        Expect('X'),
        Reject('+',"Vous n'avez pas besoin de <tt>+</tt> pour cette question"),
        Reject("[", "Pas besoin de crochets pour répondre à cette question"),
        Expect(".*", """Pour insérer un espace en début de ligne il faut
        que votre expression trouve tous les caractères qui sont à gauche
        du <tt>X</tt>. Vous devez donc indiquer cette suite de caractères
        quelconques dans votre expression régulière."""),        
        Reject("^", """Vous n'avez pas besoin d'utiliser <tt>^</tt> pour
        indiquer le début de ligne. En effet, la suite de caractères
        quelconques étant la plus longue possible, elle arrivera forcément
        jusqu'au début de ligne."""),
        Bad(Comment(~Contain("X/") & ~Contain("X)/"),
                    """Cela n'a aucun intérêt d'indiquer qu'il y a quelque
                    chose à droite du <tt>X</tt>, cela ne fait
                    que rallonger votre commande.""")),
        Bad(Comment(Contain('-r') & ~Contain('('),
                    """Pas besoin d'expression régulière étendue si
                    vous n'utilisez pas de groupe""")),
        Bad(Comment(~Contain('-r') & Contain('('),
                    """Vous avez besoin d'expression régulière étendue si
                    utilisez un groupe""")),
        Reject("$", """Pas besoin d'indiquer de fin de ligne, puisque
               seul le début vous intéresse"""),
        Reject("-e", """Pas besoin d'indiquer de l'option <tt>-e</tt>
               car il n'y a qu'une seule commande"""),
        Good(Replace(dumb_replace,Shell(
                    Equal("sed 's/.*X/ &/'")
                    | Equal("sed -r 's/(.*X)/ \\1/'")
                    ))),
        shell_display,
        ),
    )
    



# Pas possible
##add(name='balise HTML',
##    required=[],
##    question="""Quelle commande tapez-vous pour copier le
##    fichier <tt>xxx.html</tt> sous le nom  <tt>yyy.html</tt>
##    en passant en majuscules les balises HTML.
##    <table>
##    <tbody>
##    <tr>
##    <th>Avant</th>
##    <td>
##    &lt;p&gt;La traduction de &lt;span lang=\"en\"&gt;directory&lt;/span&gt;
##    est répertoire.&lt;/p&gt;
##    </td>
##    </tr>
##    <tr>
##    <th>Après</th>
##    <td>
##    &lt;P&gt;La traduction de &lt;SPAN lang=\"en\"&gt;directory&lt;/SPAN&gt;
##    est répertoire..&lt;/P&gt;
##    </td>
##    </tr>
##    </tbody>
##    </table>
##    """,
##    tests=(
##    good("sed xxx.html >yyy.html 's/<")
##    ),
    
##    )

# Faire le 2> /dev/null
# Faire la version avec while

              
    
    
    
    
