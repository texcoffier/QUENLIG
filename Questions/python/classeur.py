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

from QUENLIG.questions import *
from .check import *



add(name='intro',
    required=['nombre:multiplication', 'nombre:addition'],
    before="""De la même façon que tu ranges des pages dans des classeurs,
    Python peut faire de même.
    Un classeur est constitué par&nbsp;:
    <ul>
    <li> le devant de sa couverture,
    <li> une première page
    <li> et une deuxième page
    <li> et une troisième page
    <li> ...
    <li> et la dernière page
    <li> l'arrière de la couverture.
    </ul>
    <p>
    On traduit cela en Python&nbsp;:
    <ul>
    <li> On indique le devant de la couverture par <tt>[</tt>
    <li> À la place des pages tu peux mettre tout ce que
    le python comprend&nbsp;: textes, nombres, ...
    <li> Le «<em>et</em>» s'écrit virgule comme d'habitude
    <li> L'arrière de la couverture s'écrit <tt>]</tt>
    </ul>
    <p>
    Voici un classeur&nbsp;:
    <tt>[3, 'chien', 5, 'chat', 2*5]</tt>
    """,
    question="""Dis à Python d'afficher le classeur contenant
    6 et 1+1 et 'toto'""",
    tests=(
    print_required,
    space_required,
    plus_required,
    comma_required,
    square_bracket_required,
    python_answer_good("[6, 2, 'toto']\n"),
    ),
    good_answer="""Tu remarqueras que le 1+1 est devenu 2&nbsp;!<br>
    Python effectue les calculs quand il fabrique son classeur.""",
    )



add(name='les entiers',
    required=['classeur:intro'],
    before="""Le Python sait compter, il suffit de lui demander.
    Tu lui dis <tt>range(4)</tt> et il répond <tt>[0, 1, 2, 3]</tt>.
    <p>
    Il te fabrique un classeur contenant les nombres
    les uns après les autres.""",
    question="""Dis à Python d'afficher un classeur contenant
    les nombres de 0 à 19 (sans le 20)""",
    tests=(
    print_required,
    space_required,
    bracket_required,
    require("range", "Tu dois utiliser <tt>range</tt>"),
    reject('19', "Il va aller jusqu'à 18, pas 19."),
    python_answer_good(str(list(range(20)))+'\n'),
    ),
    )

add(name='un dé',
    required=['les entiers'],
    before="""<tt>range(5)</tt> fabrique le classeur <tt>[0,1,2,3,4]</tt>
    mais parfois on veut les nombres à partir d'autre chose que <tt>1</tt>.
    On l'indique à <tt>range</tt>.
    <p>
    <tt>range(5,9)</tt> fabrique le classeur <tt>[5,6,7,8]</tt>
    """,
    question="""Fais afficher le classeur contenant
    les chiffres indiqués par un dé.""",
    tests=(
    print_required,
    space_required,
    apostrophe_rejected,
    range_required(),
    require('1',
            """Le plus petit chiffre indiqué sur un dé est 1,
            on indique donc <tt>1</tt> à <tt>range</tt>"""),
    require('7',
            """Le plus grand chiffre indiqué sur un dé est 6,
            on indique donc <tt>7</tt> à <tt>range</tt>"""),
    python_answer_good(str([1,2,3,4,5,6]) + '\n'),
    ),
    )
    
    


add(name="dans classeur",
    required=['classeur:intro'],
    question="""Dis à Python d'afficher un classeur contenant
    deux classeurs&nbsp;:
    <ul>
    <li> le premier contient 'chien' et 4,</li>
    <li> le deuxième contient 'rouge' et 'homme' et 2.</li>
    </ul>""",
    tests=(
    print_required,
    space_required,
    comma_required,
    square_bracket_required,
    apostrophe_required,
    number_of_is('[',3,
                 """Il doit y avoir 3 devants de couvertures de classeur
                 car il y a un gros classeur et deux petits"""),
    number_of_is(']',3,
                 """Il doit y avoir 3 derrières de couvertures de classeur
                 car il y a un gros classeur et deux petits"""),    
    number_of_is(',',4,
                 """Il doit y avoir 4 virgules car il y a 4 <em>et</em>&nbsp;:
                 <ul>
                 <li> 'chien' ET 4
                 <li> premier petit classeur ET deuxième petit classeur
                 <li> 'rouge' ET 'homme' ET 2
                 </ul>"""),
    require(("'chien'", "'homme'", "'rouge'", '4', '2'),
            """Tu dois dire à Python qu'il y a 'rouge', 'chien', 'homme', 4, 2
            dans les classeurs"""),
    reject("'2'", "Le nombre 2, pas le texte '2'"),
    python_answer_good("[['chien', 4], ['rouge', 'homme', 2]]\n"),
    ),
    indices=(
    """Dans l'ordre tu trouve&nbsp;:
    <ul>
    <li> Devant de la couverture du gros classeur
    <li> Devant de la couverture du premier des deux classeurs
    <li> 'chien' et 4
    <li> Derrière de la couverture du premier des deux classeurs
    <li> et devant de la couverture du deuxième des deux classeurs
    <li> 'rouge' et 'homme' et 2
    <li> Derrière de la couverture du deuxième des deux classeurs
    <li> Derrière de la couverture du gros classeur
    <ul>
    <p>
    Heureusement, c'est plus court à écrire en Python&nbsp;!
    """,
    
    ),
    )
    



add(name="addition",
    required=['classeur:intro', 'texte:addition texte'],
    before = """Comme les nombres et les textes, les classeurs
    peuvent s'additionner.
    Quand on ajoute deux classeurs, un nouveau classeur est
    créé contenant toutes les pages dans l'ordre,
    même si des pages sont identiques.
    <p>
    <tt>["chien", 4, "homme", 2] + ["pieuvre", 8]</tt><br>
    donne le classeur&nbsp;:<br>
    <tt>["chien", 4, "homme", 2, "pieuvre", 8]</tt>
    """,
    question="""Dis à Python d'afficher la somme
    du classeur contenant les nombres 0 et 1 et 2 au classeur
    contenant les nombres 0 et 1.""",
    tests=(
    print_required,
    space_required,
    apostrophe_rejected,
    plus_required,
    comma_required,
    number_of_is('[',2,
                 """Il doit y avoir 2 devants de couvertures de classeur
                 car on ajoute 2 classeurs"""),
    number_of_is(']',2,
                 """Il doit y avoir 2 derrières de couvertures de classeur
                 car on ajoute 2 classeurs"""),
    python_answer_good(str(list(range(3))+list(range(2)))+'\n'),
    ),    
    ) 
    
    


add(name="multiplication",
    required=['classeur:intro', 'texte:multiplication texte'],
    before = """Comme les nombres et les textes, les classeurs
    peuvent être multipliés par un nombre pour faire plein d'addition.
    <p>
    <tt>10 * [0]</tt> donne <tt>[0, 0, 0, 0, 0, 0, 0, 0, 0, 0]</tt>

    """,
    question = """Fais afficher <tt>[0, 1, 0, 1, 0, 1, 0, 1]</tt>
    en utilisant une multiplication.""",
    tests=(
    print_required,
    space_required,
    apostrophe_rejected,
    multiply_required,
    comma_required,
    square_bracket_required,
    require('4', 'Il y a 4 fois le classeur contenant les nombres 0 et 1'),
    python_answer_good(str(4*[0,1])+'\n'),
    ),    
    )

add(name="une page",
    required=["multiplication", "les entiers",
              "histoire:-er présent"],
    before="""Il est possible de regarder une page d'un classeur&nbsp;:
    Pour ce faire, il suffit d'indiquer après le classeur le numéro
    de la page entre crochets. <b>Attention, la première page
    porte le numéro <tt>0</tt></b>.
    <p>
    Quelques exemples&nbsp;:
    <table class=\"short\">
    <tr><th>Programme Python</th><th>Ce qu'il affiche</th></tr>
    <tr><td><tt>print ['do','ré','mi'][0]</tt></td><td><tt>do</tt></td></tr>
    <tr><td><tt>print ['do','ré','mi'][1]</tt></td><td><tt>ré</tt></td></tr>
    <tr><td><tt>print ['do','ré','mi'][2]</tt></td><td><tt>mi</tt></td></tr>
    <tr><td><tt>print range(4)[2]</tt></td><td><tt>2</tt></td></tr>
    <tr><td><tt>print ([2,3]+['x','y'])[2]</tt></td><td><tt>x</tt></td></tr>
    <tr><td><tt>print (range(3)+range(3))[5]</tt></td><td><tt>2</tt></td></tr>
    <tr><td><tt>print 'range(4)'[2]</tt></td><td><tt>n</tt></td></tr>
    <tr><td><tt>for i in range(4): print i, 'abcde'[i]</tt></td><td><pre>0 a
1 b
2 c
3 d</pre></td></tr>
    <tr><td><tt>for i in ['do','ré','mi']: print i[0] + '-' + i[1]</tt></td><td><pre>d-o
r-é
m-i</pre></td></tr>
</table>
    """,
    question="""Traduire le message secret contenu dans le classeur&nbsp;:
    <tt>[20,15,21,20,0,12,5,0,13,15,14,4,5,0,16,5,21,20,0,13,5,0,12,9,18,5]</tt>
    sachant que les nombres indiquent un numéro de page
    dans le classeur suivant&nbsp;: <tt>' ABCDEFGHIJKLMNOPQRSTUVWXY'</tt>
    <p>
    Pour que cela soit facile à lire, affiche toutes lettres
    du message sur la même ligne.

    """,
    nr_lines = 3,
    tests=(
    for_required,
    print_required,
    do_not_cheat(required="' ABCDEFGHIJKLMNOPQRSTUVWXY'"),
    do_not_cheat(required="[20,15,21,20,0,12,5,0,13,15,14,4,5,0,16,5,21,20,0,13,5,0,12,9,18,5]"),
    do_not_cheat(rejected="t o"),
    python_answer_good('T O U T   L E   M O N D E   P E U T   M E   L I R E\n'),
    ),
    indices = (
    """Le premier nombre du message est <tt>20</tt>,
    donc la première lettre est <tt>' ABCDEFGHIJKLMNOPQRSTUVWXY'[20]</tt>
    et si vous comptez bien, c'est <tt>'t'</tt>.""",
    """Pour chaque page du classeur contenant le message,
    il faut afficher la page de <tt>' ABCDEFGHIJKLMNOPQRSTUVWXY'</tt>
    dont le numéro correspond.""",
    """Pour chaque <tt>page</tt> du classeur contenant le message,
    il faut afficher <tt>' ABCDEFGHIJKLMNOPQRSTUVWXY'[page]</tt>
    """,
    ),
    
    )

# add(name="dernieres pages",
#     required=['une page'],
#     before="""
#     


