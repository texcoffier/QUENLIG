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




add(name='multiple',
    required=['texte:un chat', 'nombre:nombre'],
    before="""Quand on veut dire <em>et</em> comme dans la phrase
    <em>un chat et un chien</em> on remplace le mot
    <em>et</em> par une virgule pour que le Python comprenne""",
    question="Dis à python d'écrire <em>5 et 'bonbons'</em>.",
    tests=(
    print_required,
    space_required,
    apostrophe_required,
    comma_required,
    require(('5', 'bonbons'),
            """Comment lui faire afficher <em>5</em> et
            <em>'bonbons'</em> si tu ne lui dis pas
            ces 2 choses."""),
    reject('5 bonbons',
           """<tt>print '5 bonbons'</tt> fait bien afficher ce que
           l'on veut à Python, mais on veut lui faire afficher
           <em>5</em> et <em>'bonbons'</em> et non <em>'5 bonbons'</em>.
           Dans un cas on lui dit d'afficher 2 choses et dans
           l'autre une seule.
           """
           ),
    python_answer_good('5 bonbons\n'),
    ),
    indices=(
    "Il faut traduire en Python&nbsp;: <em>Dis-moi 5 et 'bonbons'</em>",
    ),
    good_answer="""Tu as remarqué que le Python a mis un espace
    entre <em>5</em> et <em>bonbons</em>&nbsp;?""",
    )

add(name='formule et résultat',
    required=['dis:multiple', 'nombre:addition'],
    question= "Traduis en Python&nbsp;: <em>Dis-moi 1 et '+' et 1 et '=' et 1+1</em>",
    tests=(
    print_required,
    space_required,
    apostrophe_required,
    comma_required,
    reject('2',
           """On ne veut pas que tu dises à Python de donner la solution,
           on veut que le python la calcule tout seul.
           Tu ne dois pas lui dire que la solution est 2.
           """),
    reject("'1+1'",
           """Si tu met des apostrophes autour de <em>1+1</em> il va
           afficher <tt>1+1</tt> au lieu de faire le calcul."""),
    python_answer_good('1 + 1 = 2\n'),
    ),
    indices=(
    """Il faut faire comme dans les questions précédentes.
    Remplacer <em>Dis-moi</em> par <tt>print</tt> et les <em>et</em>
    par des virgules""",
    )
    )

add(name='même ligne',
    required=['pour:compter de 2 en 2'],
    before="""On veut parfois faire un <tt>print</tt> sans
    retourner au début de la ligne.
    Pour cela on termine le <tt>print</tt> par une virgule.
    <pre>for nombre in range(5): print nombre,</pre>
Va afficher&nbsp;: <tt>0 1 2 3 4</tt>.""",
    question="""Fais afficher sur <b>une seule ligne</b>
    les nombres paires de 0 à 20""",
    tests=(
    print_required,
    space_required,
    apostrophe_rejected,
    comma_required,
    for_required,
    range_required(11),
    do_not_cheat(rejected='4'),
    python_answer_good('0 2 4 6 8 10 12 14 16 18 20\n'),
    ),
    )

add(name='rien',
    required=['même ligne', 'pour:multi lignes'],
    before="""Parfois, on veut simplement revenir à la ligne
    sans rien écrire.
    Pour faire cela, il faut dire <tt>print</tt> sans rien écrire après""",
    question="""Dis à Python de faire <tt>print 'a',</tt> dix fois
    puis de faire faire <tt>print 'b',</tt> dix fois.
    <p>
    Regarde le résultat (ta réponse est refusée),
    normalement c'est une ligne contenant 10 <tt>a</tt>
    puis 10 <tt>b</tt>
    <p>
    Après avoir faire ceci, met un <tt>print</tt> solitaire
    entre les deux boucles.""",
    nr_lines=6,
    tests=(
    print_required,
    space_required,
    for_required,
    do_not_cheat(rejected='3'),
    range_required(),
    python_answer_good('a'*10 + '\n' + 'b'*10 + '\n', remove_spaces=True),
    ),    
    )

add(name='espace',
    required=['même ligne', 'intro:multi lignes'],
    nr_lines = 4,
    question="""Fais écrire un <tt>un  chat</tt>,
     utilisant 3 <tt>print</tt> et avec 2 espaces entre
     <tt>un</tt> et <tt>chat</tt>""",
    default_answer = """print 'un',
print
print 'chat'""",
    tests=(
    print_required,
    space_required,
    reject('print ,',
           """Pour une raison connue seulement de son créateur,
           Python refuse de comprendre <tt>print ,</tt>
           <p>
           Il faut donc absolument lui faire afficher un texte."""),
    number_of_is('print', 3, 'On veut absolument 3 <tt>print</tt>'),
    python_answer_good('un  chat\n'),
    python_answer_bad('un   chat\n',
                      'Il y a 3 blanc entre le <tt>un</tt> et le chat'),
    python_answer_bad('un\nchat\n',
                      """N'oublie pas de ne pas revenir à la ligne
                      pour le <tt>print</tt> du milieu"""),
    ),
    good_answer = """Le <tt>print '',</tt> affiche donc un
    espace sans revenir à la ligne""",
    )
    
    
    
