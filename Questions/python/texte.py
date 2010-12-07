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

from questions import *
from check import *

add(name='chien',
    required=['intro:bonjour'],
    question="""Dans le cadre blanc,
    écris la phrase Python pour qu'il écrive <em>chien</em>
    puis tape sur la touche <u>Return</u> ou <u>Entrée</u>.
    """,
    tests=(
    print_required,
    require("chien",
            """Tu veux qu'il écrive <em>chien</em>,
            il faut donc que tu lui dises d'écrire <em>chien</em>."""),
    apostrophe_required,
    python_answer_good('chien\n'),
    ),
    )
    
add(name='un chat',
    required=['texte:chien'],
    question="Fais dire <em>un chat</em> à Python.",
    tests=(
    print_required,
    require("un chat",
            """Tu veux qu'il écrive <em>un chat</em>,
            il faut donc que tu lui dises d'écrire <em>un chat</em>."""),
    apostrophe_required,
    python_answer_good('un chat\n'),
    ),
    )

add(name='à la ligne',
    required=['texte:chien'],
    before="""Quand tu veux que le Python revienne à gauche
    quand il écrit quelque chose, il faut mettre '\\n'.
    Ces deux caractères lui indiquent qu'il ne faut pas continuer
    à écrire vers la droite.
    Le <tt>\\n</tt> s'utilise comme un caractère habituel comme
    <em>a</em>, <em>b</em>, ...""",
    question="""Dis au Python d'écrire '12' en revenant à la ligne
    entre le 1 et le 2.""",
    tests=(
    print_required,
    apostrophe_required,
    lf_required,
    require(('1', '2'), 'Ou sont le 1 et le 2&nbsp;?'),
    reject("'\\n'", 'On met entre les apostrophes le 1 et le \\n et le 2'),
    python_answer_good('1\n2\n'),
    ),
    indices=("""Par exemple <tt>print 'un\\nchien'</tt> affiche
    <pre>un
chien</pre>""",
             ),
    )

add(name='addition texte',
    required=['nombre:addition'],
    before="""Le Python permet d'ajouter autre chose que des nombres.
    L'addition permet de coller ensemble deux textes.""",
    question="Dis au Python d'afficher 'Le' + 'chien'",
    tests=(
    print_required,
    space_required,
    apostrophe_required,
    plus_required,
    comma_rejected,
    python_answer_good('Lechien\n'),
    python_answer_good('lechien\n'),
    ),
    good_answer="""Quand on demande à Python de coller ensemble
    deux textes, il ne met pas un espace entre les deux.""",
    )

add(name='vide',
    required=['à la ligne', 'addition texte'],
    before = """Un texte vide est un texte sans rien entre
    les apostrophes&nbsp;: <tt>''</tt>""",
    question="""Fais afficher la somme de <tt>'car'</tt>,
    du texte vide et de <tt>'ton'</tt>""",
    tests=(
    print_required,
    space_required,
    apostrophe_required,
    plus_required,
    comma_rejected,
    require("''", "Et le texte vide, il est où&nbsp;?"),
    require(("'car'", "'ton'"),
             "Il manque le <tt>car</tt> et le <tt>ton</tt> dans ta réponse"),
    python_answer_good('carton\n'),
    ),
    )
    
add(name='multiplication texte',
    required=['texte:addition texte', 'nombre:multiplication'],
    before="""La multiplication indique que l'on répète quelque chose.
    2*3 veut dire que l'on répète&nbsp;:
    <ul>
    <li> 2 additions de 3 : 3 + 3 = 6</li>
    <li> 3 additions de 2 : 2 + 2 + 2 = 6</li>
    </ul>
    <p>
    Donc 3*'coucou' veut dire 'coucou' + 'coucou' + 'coucou' = 'coucoucoucoucoucou'
    """,
    question="Dis à Python d'afficher 10 fois 'chien '",
    tests=(
    print_required,
    space_required,
    apostrophe_required,
    multiply_required,
    comma_rejected,
    python_answer_good('chien '*10 + '\n'),
    python_answer_good(' chien'*10 + '\n'),
    python_answer_bad('chien'*10 + '\n',
                      "Tous les mots sont collés, ajoute un espace à la fin de chien !"),
    ),
    )

add(name='0 * texte',
    required=['texte:multiplication texte'],
    question='Fais afficher 0 multiplié par un texte de ton choix',
    tests=(
    print_required,
    space_required,
    apostrophe_required,
    multiply_required,
    comma_rejected,
    require('0', 'Tu dois multiplier par 0'),
    python_answer_good('\n'),    
    ),
    good_answer = """Rien ne s'affiche car 0 multiplié par n'importe quoi
    donne toujours 0.""",
    )

add(name='remplacer',
    required=['multiplication texte', 'classeur:les entiers'],
    before="""Dans un texte, on peut remplacer un mot par un autre
    il suffit d'ajouter après le texte <tt>.replace('un mot','un autre')</tt>
    <p>Exemple&nbsp;:
    <pre>print 'un grand chien'.replace('grand', 'petit')</pre>
    Va afficher&nbsp;:
    <pre>un petit chien</pre>
    """,
    question="""Fais afficher le texte <tt>'un cartable bleu'</tt> dans
    lequel on remplace le mot <tt>cartable</tt> par <tt>chien</tt>.""",
    tests=(
    print_required,
    space_required,
    apostrophe_required,
    replace_required,
    do_not_cheat(rejected='un chien bleu'),
    number_of_is('cartable', 2,
                 """Le mot <tt>cartable</tt> doit apparaître deux fois
                 dans la phrase que tu tapes, la première fois pour
                 donner la phrase initiale <tt>'un cartable bleu'</tt>
                 et la deuxième fois pour dire de le faire remplacer
                 par le mot <tt>chien</tt>"""),
    python_answer_good('un chien bleu\n'),
    ),
    good_answer="""<tt>replace</tt> est l'une de méthodes
    que les textes python connaissent""",
    )
    
add(name='remplace multiple',
    required=['remplacer'],
    before="""Un texte dans lequel on a remplacé un mot par un autre
    est un texte&nbsp;!
    On peut donc remplacer un mot par un autre dans le résultat.""",
    question="""Faire afficher le texte <tt>u g c</tt>
    en faisant les remplacements suivants&nbsp;:
    <ul>
    <li> <tt>u</tt> par <tt>un</tt>
    <li> <tt>g</tt> par <tt>grand</tt>
    <li> <tt>c</tt> par <tt>chien</tt>
    </ul>""",
    default_answer="print 'u g c'",
    tests=(
    print_required,
    space_required,
    apostrophe_required,
    replace_required,
    do_not_cheat(rejected='un grand chien'),
    number_of_is('replace', 3,
                 """Tu dois utiliser 3 fois la méthode <tt>replace</tt>"""),
    require(("'un'", "'grand'", "'chien'", "'u'", "'g'", "'c'"),
            """Tu dois faire 3 remplacements, il faut donc que tu
            indiques 6 mots (3 anciens et 3 nouveaux).
            Ces mots ne sont pas tous dans ta réponse."""),
    python_answer_good('un grand chien\n'),
    ),
    indices=(
    """Un exemple pour aider&nbsp;:
    <pre>print '1+1=2'.replace('1','9').replace('2','18')</pre>
    Affiche <tt>9+9=18</tt>""",
    ),
    )

add(name='remplace gag',
    required=['remplace multiple'],
    before="""L'ordre des remplacements est important,
    cela peut donner des résultats surprenants""",
    question="""Faire afficher le texte <tt>u c v</tt>
    en faisant les remplacements suivants&nbsp;:
    <ul>
    <li> <tt>u</tt> par <tt>un</tt>
    <li> <tt>c</tt> par <tt>cheval</tt>
    <li> <tt>v</tt> par <tt>vert</tt>
    </ul>""",
    default_answer="print 'u c v'",
    tests=(
    print_required,
    space_required,
    apostrophe_required,
    replace_required,
    number_of_is('replace', 3,
                 """Tu dois utiliser 3 fois la méthode <tt>replace</tt>"""),
    require(("'un'", "'cheval'", "'vert'", "'u'", "'c'", "'v'"),
            """Tu dois faire 3 remplacements, il faut donc que tu
            indiques 6 mots (3 anciens et 3 nouveaux)"""),
    python_answer_good('un chevertal vert\n'),
    ),
    good_answer="""Lis bien la phrase que le python a écrit.
    Elle est comme ça car il y a 2 <tt>v</tt> dans la phrase
    <tt>un cheval v</tt>""",
    )

cla = """u
n
 
c
h
a
t"""

add(name='classeur',
    required=['pour:feuilleter un classeur'],
    before='Pour python un texte est un classeur, on peut donc le feuilleter.',
    question="""Fais afficher par Python toute les lettres
    du texte <tt>'un chat'</tt> en mettant une lettre par ligne.
    <pre>%s</pre>""" % cla,
    tests=(
    print_required,
    space_required,
    apostrophe_required,
    for_required,
    require("'un chat'", """Je ne trouve pas <tt>'un chat'</tt>
    dans ta réponse"""),
    python_answer_good(cla + '\n'),
    ),
    )
    
