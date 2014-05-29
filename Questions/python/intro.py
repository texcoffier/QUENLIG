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

add(name='bonjour',
    before="""
    <p>
    Tu sais calculer les additions et les multiplications,
    alors tu peux apprendre la langue du Python.
    Tu écris dans sa langue et il te répond
    s'il te comprend.
    <p>
    Malheureusement le Python ne fait que ce qu'on lui
    demande et rien de plus.
    Par exemple, si tu lui dis <em>Bonjour</em>
    il ne te répondra pas.
    Par contre tu peux lui dire&nbsp;:
    <em>Dis-moi 'Bonjour'</em>.
    <p>
    Dans la langue du Python, <em>Dis-moi</em> s'écrit
    <tt>print</tt>.
    """,
    question="""Dans le cadre blanc,
    écris la phrase Python pour qu'il te dise <em>Bonjour</em>
    puis tape sur la touche <u>Return</u> ou <u>Entrée</u>.
    """,
    good_answer="""Tu as remarqué que le Python t'a dis <tt>Bonjour</tt>
    sans mettre les apostrophes autour.""",
    indices=(
    """Tu dois remplacer dans la phrase <em>Dis-moi 'Bonjour'</em>&nbsp;:<br>
    <em>Dis-moi</em> par <tt>print</tt> pour que le Python comprenne.""",
    ),
    tests=(
    print_required,
    require("onjour",
            """Tu veux qu'il te réponde <em>Bonjour</em>,
            il faut donc que tu lui dises de dire <em>Bonjour</em>."""),
    apostrophe_required,
    python_answer_good('bonjour\n'),
    python_answer_good('Bonjour\n'),
    ),
    )





add(name='ordre des calculs',
    required=['nombre:addition multiple', 'nombre:multiplication', 'nombre:soustraction \xe9norme'],
    before="""Tu as 3 paquets de bonbons contenant 2 bonbons
    rouges et 1 bonbon bleu.
    <ul>
    <li> Chaque paquet contient donc 2+1 bonbons.
    <li> Comme tu as 3 paquets, tu possèdes donc 3 fois 2+1 bonbons.
    <li> Donc 3 fois 3 bonbons.
    <li> Tu as 9 bonbons.
    </ul>
    <p>
    Si tu dis au Python de calculer 3 * 2+1 il va d'abord faire
    3*2 et trouver 6, puis 6+1 et trouver 7. CATASTROPHE.
    <p>
    Pour que le python fasse les calculs dans le bon ordre
    il faut mettre des parenthèses&nbsp;:
    <p>
    <tt>3 * ( 2 + 1 )</tt>
    """,
    question="""Dans chacune des trousses de la classe
    il y a 2 feutres bleus et 3 rouges.
    Fait calculer à Python le nombre de feutres
    que l'on trouverait si l'on vidait les 10 trousses de la classe""",
    tests=(
    print_required,
    space_required,
    apostrophe_rejected,
    multiply_required,
    plus_required,
    comma_rejected,
    bracket_required,
    python_answer_good("50\n"),
    ),    
    )

add(name="gafirove",
    required=['ordre des calculs'],
    question="""5 <b>ga</b>rçons et 3 <b>fi</b>lles mangent
    chacun 2 bonbons <b>ro</b>uges et 6 bonbons <b>ve</b>rts.<p>
    Combien ont-ils mangés de bonbons&nbsp;?
    Fais calculer et afficher la réponse par le python.""",
    tests=(
    print_required,
    space_required,
    apostrophe_rejected,
    plus_required,
    multiply_required,
    require(('5', '3', '2', '6'),
            """Comment le Python va calculer la réponse si tu ne
            lui donne pas les nombres indiqués dans le problème&nbsp;:
            5, 3, 2, 6"""),
    python_answer_good(str((5+3)*(2+6)) + '\n'),
    python_answer_bad(str(5+3*2+6) + '\n',
                      """Tu n'as pas dis au Python dans quel ordre
                      il faut faire les calculs.
                      Comme il considère les multiplications
                      plus importantes que les additions,
                      il a calculé&nbsp;: 5 + (3*2) + 6
                      et ce n'est pas ce que tu veux calculer"""),
    ),    
    indices=(
    """Comme ils ont tous mangé le même nombre de bonbons,
    le nombre de bonbons mangés est égal au nombre d'enfants
    multiplié par le nombre de de bonbons que chaque enfant
    a mangé""",
    """Le calcul à faire faire par le Python est donc&nbsp;:<br>
    nombre de garçons plus nombre de filles<br>
    multiplié par&nbsp;:<br>
    nombre de bonbon rouge plus nombre de bons verts.""",
    ),
    )


add(name="multi lignes",
    required=['si:intro'],
    before="""Les phrases Python ne tiennent pas toutes sur une ligne.
    Pour lui faire faire des choses compliquées,
    il faut écrire sur plusieurs lignes
    """,
    question="""Sur la première ligne demandes à Python
    d'afficher <tt>chien</tt> et sur la deuxième ligne demande
    à Python d'afficher <tt>chat</tt>""",
    nr_lines=3,
    tests=(
    print_required,
    space_required,
    require(('chien', 'chat'), "Où sont passé le chien et le chat&nbsp?"),
    number_of_is('print', 2, "La réponse est sur 2 lignes"),
    python_answer_good('chien\nchat\n'),
    ),
    )

