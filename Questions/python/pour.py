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



add(name="feuilleter un classeur",
    required=['classeur:les entiers', 'classeur:dans classeur', 'classeur:addition'],
    before="""Le python sait feuilleter un classeur page par page.
    Pour chaque page, il fait ce que tu lui demandes.
    <p>
    En français on dirait&nbsp;:<br>
    <em>Pour chaque <tt>page</tt> dans le classeur <tt>['Un', 'grand', 'chien']</tt> : dis-moi '(' et <tt>page</tt> et ')'</em><br>
    <ul>
    <li> «<em>Pour chaque</em>» se dit <tt>for</tt> en Python.
    <li> «<em>dans le classeur</em>» se dit <tt>in</tt> en Python.
    <li> «<em>:</em>» se dit <tt>:</tt> en Python.
    </ul>
    <p>
    La phrase traduite en Python devient&nbsp;:<br>
    <tt>for page in ['Un', 'grand', 'chien']: print '(', page, ')'</tt>
    <p>
    Le Python affichera&nbsp;:
    <pre>( Un )
( grand )
( chien )</pre>""",
    question="Fais afficher les nombres de 0 à 9 un par ligne.",
    tests=(
    print_required,
    space_required,
    apostrophe_rejected,
    for_required,
    range_required(10),
    python_answer_good('0\n1\n2\n3\n4\n5\n6\n7\n8\n9\n'),
    ),    
    )


add(name='un dé',
    required=['classeur:un dé', 'feuilleter un classeur'],
    question="""Fais afficher les chiffres indiqués par un dé,
    en en mettant un par ligne.""",
    tests=(
    print_required,
    space_required,
    for_required,
    range_required(),
    python_answer_good('1\n2\n3\n4\n5\n6\n'),
    ),
    )

add(name="compter de 2 en 2",
    required=['pour:feuilleter un classeur', 'nombre:multiplication',
              'dis:formule et résultat'],
    before="""Pour compter de 2 en 2 c'est simple,
    on compte de 1 en 1 et on dit le double&nbsp;:
    <ul>
    <li> 0*2 : 0
    <li> 1*2 : 2
    <li> 2*2 : 4
    <li> 3*2 : 6
    <li> 4*2 : 8
    <li> 5*2 : 10
    <li> ...
    <li> 10*2 : 20
    </ul>""",
    question="Fais afficher les nombres paires de 0 à 20.",
    tests=(
    print_required,
    space_required,
    apostrophe_rejected,
    for_required,
    range_required(11),
    python_answer_good('0\n2\n4\n6\n8\n10\n12\n14\n16\n18\n20\n'),
    ),    
    )

add(name="décompter",
    required=['compter de 2 en 2', 'nombre:soustraction'],
    question="""Fais afficher les nombres de 9 à 0&nbsp;:
    <tt>9 8 7 6 5 4 3 2 1 0</tt>""",
    tests=(
    print_required,
    space_required,
    apostrophe_rejected,
    for_required,
    range_required(10),
    do_not_cheat(rejected='5'),
    python_answer_good('9876543210',remove_spaces=True, remove_newline=True),
    ),
    indices=(
    """Il suffit de parcourir les entiers de 0 à 9 en faisant un petit
    calcul&nbsp;:
<pre>9 - 0 donne 9
9 - 1 donne 8
9 - 2 donne 7
...
9 - 8 donne 1
9 - 9 donne 0</pre>
""",
    ),
    )
    

add(name="multi lignes",
    required=['intro:multi lignes'],
    before="""Quand on écrit le <tt>for</tt> sur plusieurs lignes
    ce qui est à droite du <tt>:</tt> est mis sur la ligne suivante.
    Les lignes qui sont à répéter sont décalées à droite du
    même nombre d'espace.
    <pre>print 'avant'
for nombre in range(10):
    print nombre
    print '------'
print 'après'</pre>
    <p>
    Dans l'exemple précédent seules les deux lignes après le <tt>for</tt>
    sont répétés.
""",
    question="""Pour tous les nombres de 0 à 4 fait afficher
    le nombre sur une ligne et son double sur la ligne suivante""",
    nr_lines=3,
    tests=(
    print_required,
    space_required,
    apostrophe_rejected,
    for_required,
    do_not_cheat(rejected='3'),
    range_required(5),
    number_of_is('print', 2,
                 "Il doit y avoir 2 <tt>print</tt> dans la phrase Python"),
    python_answer_good(''.join([str(i) + '\n' + str(2*i) + '\n' for i in range(5)])),
    ),    
    )

add(name='cherche 72',
    required=['multi lignes', 'booleen:recherche 72', 'si:multi lignes'],
    question="""Fais afficher le nombre qui multiplié par 8 donne 72.""",
    nr_lines=3,
    tests=(
    print_required,
    space_required,
    apostrophe_rejected,
    for_required,
    if_required,
    range_required(),
    python_answer_good('9\n'),
    ),
    indices=(
    """En français la phrase serait&nbsp;:
    <em>pour chaque nombre du classeur contenant les nombres entre 0 et 20 :
    si le nombre * 8 est égale à 72 alors afficher le nombre</em>""",
    ),
    )

def dd():
    s = ''
    for d1 in range(1,7):
        for d2 in range(1,7):
            s += "%d + %d = %d\n" % (d1,d2,d1+d2)
    return s.replace(' ','')

add(name='imbriqués',
    required=['multi lignes', 'un dé'],
    before="""Dans un «<em>pour</em>» on peut tout mettre, on peut donc mettre
    un autre «<em>pour</em>».
    On appelle cela des boucles imbriquées.""",
    question="""On lance 2 dés, fait afficher tous les tirages
    et pour chaque tirage la somme des 2 dés.
    <p>
    Voici ce que tu dois lui faire afficher :
    <pre>
    1 + 1 = 2
    1 + 2 = 3
    1 + 3 = 4
    1 + 4 = 5
    1 + 5 = 6
    2 + 1 = 3
    2 + 2 = 4
    2 + 3 = 5
    ...
    ...
    6 + 6 = 12
    </pre>""",
    nr_lines=3,
    tests=(
    print_required,
    space_required,
    apostrophe_required,
    for_required,
    number_of_is('for', 2, "Il faut 2 <tt>for</tt> pour cet exercice"),
    range_required(),
    require(('1','7'), "Il faut utiliser 2 <tt>range</tt> entre 1 et 7"),
    python_answer_good(dd(), remove_spaces=True),
    ),
    indices=(
    """Un exemple :
    <pre>for carnivore in ['lion', 'loup']:
    for herbivore in ['éléphant', 'lapin']:
        print 'Le', carnivore, 'mange un', herbivore + '.'</pre>
    Affiche&nbsp;:
    <pre>Le lion mange un éléphant.
Le lion mange un lapin.
Le loup mange un éléphant.
Le loup mange un lapin.</pre>""",
    ),
    )    

def dd7():
    s = ''
    for d1 in range(1,7):
        for d2 in range(1,7):
            if d1 + d2 == 7: s += "%d + %d = %d\n" % (d1,d2,d1+d2)
    return s.replace(' ','')

add(name="dé + dé = 7",
    required=['cherche 72', 'imbriqués'],
    question="""Trouver toutes les sommes de deux dés qui donnent 7.
    Il suffit d'ajouter un «<em>si</em>» au programme Python
    affichant toutes les sommes.
    """,
    nr_lines=5,
    default_answer = """for d1 in range(1,7):
    for d2 in range(1,7):
        print d1, '+', d2, '=', d1+d2""",
    tests=(
    print_required,
    space_required,
    apostrophe_required,
    for_required,
    number_of_is('for', 2, "Il faut 2 <tt>for</tt> pour cet exercice"),
    range_required(),
    python_answer_good(dd7(), remove_spaces=True),
    ),
    )


# , "pour:décompter", palindrome

