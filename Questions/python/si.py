# -*- coding: latin-1 -*-
#    QUENLIG: Questionnaire en ligne (Online interactive tutorial)
#    Copyright (C) 2006 Thierry EXCOFFIER, Universite Claude Bernard
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

from QUENLIG.questions import *
from .check import *

add(name='intro',
    required=['booleen:recherche 72'],
    before="""On peut dire à Python de faire une action seulement
    si une condition est vraie.
    <p>
    La phrase française : <em>Si tu as froid alors tu met un manteau</em>
    est traduite en Python en remplaçant
    le «<em>si</em>» par <tt>if</tt> et le «<em>alors</em>» par <tt>:</tt>
    <p>
    On peut d'ailleur utiliser le <tt>:</tt> à la place du <em>alors</em>
    dans la phrase en français.
    <p>
    Exemples :
    <ul>
    <li> <tt>if 10 == 2*5: print 'oui'</tt> affiche <tt>oui</tt>
    <li> <tt>if 11 == 2*5: print 'oui'</tt> n'affiche rien
    </ul>
    """,
    question="""Fais afficher <tt>vrai</tt> si 5-5 est égal à 0""",
    tests=(
    do_not_cheat(required=('5', '-', '0', '==')),
    if_required,
    print_required,
    space_required,
    python_answer_good('vrai\n'),
    ),
    )

add(name="multi lignes",
    required=['intro:multi lignes'],
    before="""Quand on écrit le <tt>if</tt> sur plusieurs lignes
    ce qui est à droite du <tt>:</tt> est mis sur la ligne suivante.
    Les lignes qui sont à faire sont décalées à droite du
    même nombre d'espaces.
    <pre>print 'avant'
if 7*7 == 1:
    print 'Vrai !'
    print 'Super !'
print 'après'</pre>
    <p>
    Dans l'exemple précédent seul <tt>avant</tt> et <tt>après</tt>
    sont affichés car <tt>7*7</tt> n'est pas égal à <tt>1</tt>.
""",
    question="""Traduis en Python la phrase&nbsp;:
    <em>si 1+1==2 alors affiche <tt>'1+1=='</tt> et affiche <tt>'2'</tt></em>
    <p>
    Si la condition est vrai, il y a 2 <tt>print</tt> à faire.
    """,
    nr_lines=4,
    tests=(
    print_required,
    space_required,
    apostrophe_required,
    if_required,
    number_of_is('print', 2,
                 "Il doit y avoir 2 <tt>print</tt> dans la phrase Python"),
    python_answer_good('1+1==\n2\n', remove_spaces=True),
    ),    
    )

add(name='cherche',
    required=['pour:cherche 72', 'texte:classeur', 'booleen:égalité textes'],
    question="""Fais afficher <tt>vrai</tt> chaque fois que Python
    trouve la lettre <tt>a</tt> dans la phrase <tt>un grand chat</tt>.
    Normalement, Python devrait afficher&nbsp;:
    <pre>vrai\nvrai</pre>""",
    nr_lines=4,
    tests=(
    print_required,
    for_required,
    space_required,
    apostrophe_required,
    if_required,
    require("un grand chat", """Je ne trouve pas le grand chat dans
 ta réponse"""),
    require("'a'", """Je ne trouve pas <tt>'a'</tt> dans ta réponse"""),
    python_answer_good('vrai\nvrai\n'),
    ),    
    )

def vc():
    s = ''
    for i in 'supercalifragilisticexpialidocious':
        if i in 'aeiou':
            s += 'voyelle\n'
        else:
            s += 'consonne\n'
    return s

add(name='sinon',
    required=['histoire:enlève voyelles'],
    before="""En français on peut dire&nbsp;:
    <em>si il pleut prend un parapluie sinon met une casquette</em>.
    <p>
    En Python, le <em>sinon</em> se dit <tt>else:</tt>.
    <pre>if pleut_il:
    print 'prend ton parapluie'
else:
    print 'met une casquette'</pre>
    <p>
    Attention, le <tt>else:</tt> commence sur la même colonne
    que le <tt>if</tt>.
    """,
    question="""Fais parcourir le texte
    <tt>'supercalifragilisticexpialidocious'</tt>
    lettre par lettre en faisant afficher <tt>'voyelle'</tt>
    si c'est un voyelle sinon <tt>'consonne'</tt>&nbsp;:
    <pre>consonne
voyelle
consonne
voyelle
consonne
consonne
...</pre>""",
    nr_lines=6,
    tests=(
    print_required,
    for_required,
    space_required,
    apostrophe_required,
    if_required,
    else_required,
    require("'aeiou'", "La liste des voyelles est <tt>'aeiou'</tt>"),
    require("'supercalifragilisticexpialidocious'",
            """Je ne trouve pas la formule magique dans  ta réponse"""),
    require("'voyelle'", """Je ne trouve pas <tt>'voyelle'</tt> dans  ta réponse"""),
    require("'consonne'", """Je ne trouve pas <tt>'consonne'</tt> dans  ta réponse"""),
    python_answer_good(vc()),
    ),    
    )
