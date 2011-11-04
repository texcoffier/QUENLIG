# -*- coding: latin-1 -*-
#    QUENLIG: Questionnaire en ligne (Online interactive tutorial)
#    Copyright (C) 2005-2006,2011 Thierry EXCOFFIER, Universite Claude Bernard
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


# FAIRe LES QUESTION . * ^ $ +

from questions import *
from check import *

aide = """La méthode la plus simple pour tester les expressions
    régulière est d'exécuter la commande suivante&nbsp;:
    <pre>sed -r 's/votre_expression_regulière/(((&)))/g'</pre>
    Vous tapez ensuite du texte au clavier et les chaînes de caractères
    reconnues apparaîtront dans les triples parenthèses."""

add(name="intro",
    required=["sh:console", "sh:configurer", "remplacer:intro"],
    before=aide,
    question="""Quelle expression régulière représente une chaîne
    de caractère quelconque.""",
    tests=(
    good('.*'),
    bad('*', "Non ça c'est un <em>pattern</em> pour le shell."),
    bad('*.', "L'étoile multiplie ce qui précède."),
    bad(".", "Cette expression régulière représente un caractère quelconque"),
    reject("sed",
           """On demande le <em>pattern</em>,
           pas la ligne de commande permettant de le tester"""),
    reject("[",
           """Vous n'allez pas énumérer tous les
           caractères possibles&nbsp;!
           N'utilisez pas les crochets."""),
    reject('?', """Le <tt>?</tt> indique un caractère quelconque pour
    les <em>pattern</em> du shell.
    On vous demande une expression régulière"""),
    require(".",
            """On indique un caractère quelconque avec un '.'
            Une ligne quelconque est une répétition de caractères
            quelconques."""),
    reject('+', """Si vous utilisez le <tt>+</tt> pour multiplier ce qui
    précéde cela ne permettra pas de représenter une chaine vide
    car dans les expressions régulières <b>étendues</b> il ne
    multiplie pas par zéro."""),
    require("*",
            """On indique que l'on répète ce qui précède
            en utilisant le symbole <tt>*</tt>"""),
    reject("\\.*",
           """<tt>\\.*</tt> représente une série
           de points de longueur quelconque"""),
    reject(("'",'"'),
           """On désire l'expression régulière,
           on ne se soucie pas du shell,
           donc on ne veut pas de <tt>'</tt> ou <tt>\"</tt>
           """),
    ),
    good_answer="Par défaut la chaîne tient dans une seul ligne",
    indices = (
    """C'est la répétition un nombre indéterminé de fois
    d'un caractère quelconque""",
    ),
    )

partie = " Donc la ligne conviendra même si elle ne contient pas que des <tt>A</tt> :-("

add(name="ligne de A",
    question="""Quelle expression régulière <b>étendue</b> représente les
    lignes non vides ne contenant que des caractères A et rien d'autre""",
    tests=(
    good('^A+$'),
    good(('^[A]+$', '^(A)+$', '^AA*$'),
         "Il est plus simple d'écrire <pre>^A+$</pre>"
         ),
    bad(('^A*$', '^[A]*$', '^(A)*$'),
        "Ce n'est pas bon car cela représente aussi les lignes vides."),
    bad('^A$', "Ceci représente les lignes contenant un seul A"),
    require("^",
            """Si vous n'indiquez pas qu'elle commence au début de la ligne,
            l'expression régulière peut commencer n'importe où.""" + partie),
    require("$",
            """Si vous n'indiquez pas qu'elle finit à la fin
            de la ligne, l'expression régulière peut finir n'importe où.""" +
            partie),
    reject("[",
           """Pas besoin de spécifier une liste de
           lettres car il n'y en a qu'une seule&nbsp;: A"""),
    reject(" ",
           """Si vous mettez un espace cela veut dire que vous désirez
           que la chaine de caractère contienne un espace."""
           ),
    number_of_is('A', 1,
                 """Votre réponse ne doit contenir qu'un
                 seul caractère <tt>A</tt>"""),
    ),
    indices=("Le caractère <tt>^</tt> indique le début de ligne",
    "Le caractère <tt>$</tt> indique la fin de ligne",
    ),
    )

add(name="un spécial",
    required=["intro"],
    question="""Quelle expression représente le caractère point (<tt>.</tt>)
    au lieu de représenter un caractère quelconque&nbsp;?""",
    tests=(
    good( ("\\.", "[.]") ),
    require('.', "Je ne vois pas de caractère <tt>.</tt> dans votre réponse"),
    bad( ".", "Cette expression représente un caractère quelconque"),
    reject(('"',"'"),
           """Une expression régulière n'a pas la même syntaxe que le
           shell, les apostrophes et guillemets ne sont pas spéciaux"""),
    reject('\\\\', """Votre expressions demande à avoir un caractère
    <em>backslash</em> car c'est lui que vous avez protégé."""),
    ),
    indices=("""Attention le <tt>.</tt> est un caractère spécial,
    il faut annuler sa signification""",
             """Le caractère d'échappement dans les expressions
             régulière est \\""",
             ),
    )

add(name="deux spécial",
    required=["un spécial"],
    question="""Quelle expression régulière représente la chaine de caractères <tt>2*</tt> (un chiffre deux suivi d'une étoile)&nbsp;?""",
    tests=(
    good( ("2\\*", "2[*]") ),
    bad( "2*", "Cette expression représente une suite de 2"),
    bad('[0-9]\*',
        """Cette expression représente un chiffre suivi d'une étoile,
        on vous demande un <tt>2</tt> suivi d'une étoile."""),
    require('2', 'Je ne vois pas de 2 dans votre réponse&nbsp;!'),
    require('*', 'Je ne vois pas de * dans votre réponse&nbsp;!'),
    reject(('"',"'"),
           """Guillemets et apostrophes sont reconnus par le shell
           pas par les expressions régulières,
           vous devez utiliser autre chose pour annuler
           la signification de l'étoile"""),
    reject('\\2', "Pourquoi protéger le 2, il n'est pas spécial"),
    reject('2\\\\*', "Cette expression représente un 2 suivi d'antislashs."),
    reject('[2*]', '<tt>[2*]</tt> représente un <tt>2</tt> ou une étoile'),
    reject('[2\\*]',
           '''<tt>[2\\*]</tt> représente un <tt>2</tt>, un <tt>\\</tt> ou
           une étoile'''),
    ),
    indices=("""Attention le <tt>*</tt> est un caractère spécial,
    il faut annuler sa signification""",
             """Le caractère d'échappement dans les expressions
             régulière est \\""",
             ),
    )

add(name="spécial",
    required=["un spécial", "intro"],
    question="""Quelle expression représente les lignes complètes
    contenant un caractère <tt>.</tt> quelque part&nbsp;?
    """,
    tests=(
    good( (".*\\..*", ".*[.].*") ),
    bad( ("\\.","[.]"),
         """L'expression représente le <tt>.</tt> pas la ligne complète"""),
    bad(".*\\.*",
        """Cette expression indique une chaine de caractères quelconque
        suivie d'une suite de caractères point."""),
    bad(("*.*", "*'.'*", '*"."*', "*\\.*"),
        """C'est la bonne réponse pour les <em>pattern</em>
        du shell. Mais on vous demande une expression régulière"""),
    reject(('[',']'), """Pas besoin de crochets,
    Utilisez plutôt un anti-slash pour annuler les significations
    des caractères spéciaux"""),
    require(".*",
            """On ne veut pas que le '.' mais aussi
            la chaine de caractères quelconques
            à sa gauche et à sa droite."""),
    reject(("^", "$"),
           """Pas la peine de spécifier les indicateurs
           de début/fin de ligne car le <tt>.*</tt>
           prend la plus grande chaine possible.
           Donc jusqu'au bout"""),
    number_of_is('.*', 2, """Il y a deux chaines de caractères quelconques,
    une à gauche et une à droite du point"""),
    number_of_is('\\', 1, """Il y a un seul caractère spécial pour lequel
    la signification doit être annulée, vous n'avez donc besoin
    que d'un seul anti-slash"""),
    
    ),
    indices=(
    """L'expression solution représente une chaine de caractères quelconques
    suivie d'un point suivie d'une chaine de caractères quelconques""",
    """La réponse la plus courte tient en 6 caractères""",
    """N'oubliez pas que le <tt>.*</tt> correspond
    à la plus longue chaîne possible""",
             ),
    )

add(name='négation',
    before=aide,
    required=["intro"],
    question="""Quelle expression régulière représente un caractère qui ne soit
    ni une lettre de l'alphabet en minuscule ni un chiffre""",
    tests=(
    reject("!", "La négation n'est pas la même que celle du shell"),
    reject(".",
           """Vous n'avez pas besoin du caractère '<tt>.</tt>',
           il n'y a aucun caractère quelconque ici."""),
    reject(('(', ')'), "Vous n'avez pas besoin de parenthèses"),
    reject('A', "Pas en minuscule, j'ai pas dis pas en majuscule"),
    reject("^[a", """La négation est le premier caractère après
    le crochet. Sinon elle indique un début de ligne."""),
    reject(' ', "Attention, les espaces sont significatifs"),
    reject(('+', '*'), "On cherche un seul caractère, pas une suite"),
    reject('$', "Le caractère est n'importe où sur la ligne"),
    reject(('ab','12'),
           """Ne lister pas tous les caractères un par un.
           Définissez un interval de caractères avec les crochets."""),
    
    require(("[", "]"),
            """Il faut spécifier une liste de caractères en utilisant
            les crochets"""),
    require("-", "Il faut utiliser le <tt>-</tt> pour indiquer un intervalle"),
    require("^", "Je ne trouve pas le caractère indiquant <em>tout sauf</em>"),
    number_of_is('^',1,
                 """Vous ne devez employer la négation qu'une seule fois"""),
    require('0-9', """Je ne trouve pas l'intervalle indiquant tous les
    chiffres de 0 à 9 inclus"""),
    require('a-z', """Je ne trouve pas l'intervalle indiquant toutes les
    lettres de 'a' à 'z' inclus"""),
    good("[^a-z0-9]"),
    good("[^0-9a-z]",
         """J'attendais <tt>[^a-z0-9]</tt>, j'accepte votre
         solution car elle fonctionne mais s'il vous plais
         ne changez pas l'ordre de ce qui es demandé dans l'énoncé."""),
    expect('a-z0-9'),
    ),
    )

add(name='suite de chiffres',
    before=aide,
    required=["intro"],
    question="""Quelle expression représente des suites de chiffres
           quelconques d'au moins un chiffre (même <tt>000</tt>
           ou <tt>01</tt> par exemple)""",
    tests=(
    reject('sed',
           "On ne veut pas la commande, seulement l'expression régulière"),
    bad("[0-9]*", """Cette expression correspond aussi à une chaine vide,
    mais nous recherchons les chaines contenant au moins un chiffre"""),
    bad('[:digit:]+', """C'est une expression régulière qui répond
    à la question, mais on vous demande une solution qui n'utilise
    que des connaissances de base."""),
    require(('0-9','[','-',']'),
            "Je ne trouve pas l'intervalle des chiffres de 0 à 9"),
    reject('.', """Une suite de chiffre ne contient pas de caractères
    quelconques, pourquoi indiquez-vous le caractère '.'&nbsp;?"""),
    reject(('(',')'), "Pas besoin de parenthéser"),
    reject(('[0-9]+[0-9]*', '[0-9]*[0-9]+'),
           """Vous pouvez faire deux fois plus court.
           En effet votre expression décrit deux suites de chiffres
           l'un collée à l'autre"""),
    good( "[0-9]+",
    "C'est un expression réguière étendue car vous utilisez <tt>+</tt>"),
    good( "[0-9][0-9]*" ),
    good( "[0-9]*[0-9]", "On écrit plutôt <tt>[0-9][0-9]*</tt>" ),
    require(('*','+'), """Je ne vois pas le symbole indiquant que l'on répète
    les chiffres""", all_agree=True),
    ),
    )

add(name='entier positif',
    before=aide,
    required=["suite de chiffres"],
    question="""Quelle expression régulière étendue représente
    des suites de chiffres
    ne commençant pas par <tt>0</tt> sauf pour le nombre <tt>0</tt>.
    Exemple de ce que l'on doit trouver&nbsp;:
           
           <pre>dfsfd<span class='boxed'>67</span>sdfsfds-<span class='boxed'>0</span>sdfdsf++<span class='boxed'>0</span><span class='boxed'>8090</span>dsfs<span class='boxed'>0</span><span class='boxed'>0</span>ppp</pre>


           """,
    tests=(
    reject('sed', "On veut l'expression régulière, pas la commande"),
    reject('[^0]',
           """<tt>[^0]</tt> indique un caractère quelconque sauf <tt>0</tt>
           Par exemple <tt>A</tt>"""),
    bad(('[1-9]+[0-9]*|0', '([1-9]+[0-9]*|0)'),
        """Cette solution est correcte mais vraiment pas naturelle.
        Vous obtiendrez la bonne réponse en enlevant
        une caractère de la votre..."""),
        
    reject('^', "On a pas besoin de <tt>^</tt>"),
    reject('+', """N'utilisez pas le <tt>+</tt> il n'est pas utile ici.
    Je pense que vous devriez plutôt utiliser <tt>*</tt>"""),
    reject('.',
           "Un nombre entier, pas un nombre flottant, donc pas de point"),
    reject(' ', """Si vous mettez un espace dans une expression régulière,
    cet espace devra être trouvé"""),
    reject('[0]', "Il est plus simple d'écrire <tt>0</tt> que <tt>[0]</tt>"),
    require('|', """Il faut utiliser un <b>ou</b>, en effet,
    c'est zéro ou un nombre de commençant pas par zéro."""),
    require('[0-9]',
           "Vous n'autorisez pas les nombres à contenir des 0&nbsp;: 608"),
    require('[1-9]', """Vous n'indiquez pas que le premier chiffre est
    entre 1 et 9"""),
    require('*', """Vous n'indiquez pas qu'il y a un nombre indéfini de
    chiffre après le premier (y compris aucun)"""),

    good( "0|[1-9][0-9]*" ),
    bad( "0|([1-9][0-9]*)",
         "Cela fonctionne, mais les parenthèses ne sont pas au bon endroit"),
    good( "(0|[1-9][0-9]*)" ),
    good( "[1-9][0-9]*|0" ),
    good( "([1-9][0-9]*|0)" ),
        
    ),
    )

class test_nombre_entier(bad):
    def test(self, a, string):
        if a.find("\\") != -1:
            return False, "Il n'y a pas besoin d'antislash pour cette question"
        if a.find("[1-9]") == -1:
            return False, '''Tous les nombres entiers commencent par un chiffre
            différent de 0 sauf 0.'''
        if " " in a:
            return False, '''Les espaces sont <b>significatif</b>'''
        if a.find("|") == -1:
            return False, "0 est un cas à part car on ne lui met pas un signe"
        if a.count("|") > 1:
            return False, '''Un seul | suffit, ne compliquez pas inutilement'''
        if a[0] != "(" or a[-1] != ")":
            return False, """Je n'accepterais la solution que si vous
            parenthésez le <tt>ou</tt>,
            écrivez <tt>(a|b)</tt> au lieu de <tt>a|b</tt>"""
        if a.find("[0-9]*") == -1:
            return False, """La fin d'un nombre entier contient un nombre
            indéfini de nombre entre 0 et 9."""
        if a.find("[+-]") != -1:
            return False, """Si une liste de caractères entre crochets contient
            '-' il faut le mettre en premier. Sinon il représente un intervalle."""
        if a.find("[-+][0-9]") != -1 or a.find("[-+]?[0-9]") != -1:
            return False, """Un nombre entier ne commence pas par 0 sauf 0"""
        if a.find("[-+][0-9]") != -1:
            return False, """Un nombre entier peut être écrit sans signe."""
        return False, """Si après avoir testé votre expression régulière elle
        vous semble juste alors laissez un commentaire pour le faire savoir."""
    
    

add(name='nombre entier',
    required=["entier positif"],
    before=aide,
    question="""Quelle expression régulière étendue représente les nombres
    entiers avec leur signe&nbsp;:
    <pre>dfsfd<span class='boxed'>+6</span>sdfsfds-<span class='boxed'>0</span>sdfdsf++<span class='boxed'>0</span>sdfs<span class='boxed'>89</span>dsfs<span class='boxed'>-45</span>sdff+<span class='boxed'>-342</span>fd<span class='boxed'>56</span>ssfsdf<span class='boxed'>0</span><span class='boxed'>76</span>werwer-<span class='boxed'>0</span><span class='boxed'>89</span>sdf\\<span class='boxed'>106</span></pre>
    Les boites indiquent les nombres que votre expression régulière doit trouver.
    """,
    tests=(    
    good( ('([-+]?[1-9][0-9]*|0)',
           '(0|[-+]?[1-9][0-9]*)',
           '((-|+|)[1-9][0-9]*|0)',
           '(0|(-|+|)[1-9][0-9]*)',
           '((+|-|)[1-9][0-9]*|0)',
           '(0|(+|-|)[1-9][0-9]*)'
           ) ),
    good( '(0|+[1-9][0-9]*|-[1-9][0-9]*)',
          "Il est plus court d'écrire : <pre>(0|[-+]?[1-9][0-9]*)</pre>"),
    bad( ('(0|[-+][1-9][0-9]*)', '([-+][1-9][0-9]*|0)'),
          "Cela ne trouve pas les nombre sans signe."
          ),
    reject('[1-9]+', "Il y a un + qui n'est pas nécessaire..."),
    bad( ('(0|([-+]?[1-9][0-9]*))', ),
          "Cela fonctionne, mais faites plus court (parenthèses en trop)."
          ),
    test_nombre_entier(),
    ),
    )
    
    
add(name="identique",
    question="""Quelle expression régulière étendue représente les
    lignes ne contenant <b>que</b> des caractères identiques au premier
    de la ligne.
    """,
    tests=(
    reject(('a','A'),
           "Que vient faire un <tt>a</tt> dans votre réponse&nbsp;?"),
    require(('(',')'),
            """Vous devez grouper des caractères et réutiliser le texte
            trouvé par le groupe"""),
    require(('^', '$'),
            """Vous devez indiquer le début et la fin de ligne sinon
            l'expression pourra correspondre à une suite de caractères
            identiques en plein milieu"""),
    require('\\1', """Vous devez utiliser les caractères trouvés par le groupe
            pour indiquer que le reste de la ligne est identique"""),
    good('^(.)\\1*$'),
    good('(^.)\\1*$', "Je préfère : <tt>^(.)\\1*$</tt>"),
    bad('^(.)\\1+$', """Presque, mais cela ne trouve pas
    les lignes d'un seul caractère"""),
    reject('+', """Vous ne devez pas utiliser le <tt>+</tt>
    car une ligne contenant un seul caractère contient que des caractères
    identiques !"""),
    require_startswith('^', """Pour ce problème,
    le <tt>^</tt> doit être en début d'expression régulière""") ,
    require_endswith('$', """Pour ce problème,
    le <tt>$</tt> doit être en fin d'expression régulière""") ,
    bad('^(.)\\1$', """Vous trouvez seulement les lignes contenant
    deux caractères identiques"""),
    ),
    indices=("""Il faut mettre le premier caractère de la ligne dans
    un groupe et dire que le reste de la ligne est la répétition
    du contenu de ce groupe""",
             """Les groupes sont définis par les parenthèses&nbsp;:
             <tt>a(.*)b(.*)c</tt>
             <p>
             Cette expression définit 2 groupes sans les utiliser.
             """,
             """Les groupes sont nommés anti-slash numéro de groupe.
             <tt>\\1</tt> est le numéro du premier groupe.
             """,
             """Pour cette exercice, le premier groupe est un caractère
             quelconque et la suite de la ligne est une répétition
             du premier groupe.
             """,
             ),
    )


