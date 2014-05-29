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

square_star = """*****
*****
*****
*****
*****

"""

add(name='carré étoilé',
    required=['texte:multiplication texte', 'texte:\xe0 la ligne'],
    before="Le carré étoilé :<pre>" + square_star + "</pre>",
    question="""Pour afficher un carré étoilé, dis à Python
    d'afficher 5 fois le texte : ***** suivies d'un retour à la ligne.""",
    tests=(
    print_required,
    space_required,
    apostrophe_required,
    multiply_required,
    comma_rejected,
    lf_required,
    python_answer_good(square_star),
    require('*****', 'Je ne trouve pas les ***** que tu dois afficher'),
    ),    
    )


add(name='rectangle étoilé',
    required=['dessin:carr\xe9 \xe9toil\xe9', 'intro:ordre des calculs', 'texte:addition texte'],
    before="""Pour faire le carré étoilé, tu as fait
    <tt>print 5 * '*****\\n'</tt>
    <p>
    Mais si au lieu de mettre 5 étoiles tu en veux 40,
    vas-tu les compter&nbsp;? Ou laisser le Python travailler&nbsp;?
    """,
    question="""Dis à Python d'afficher 5 fois&nbsp;:
    <ul>
    <li> l'addition de 40 fois le caractère '*'
    <li> le texte lui disant de revenir à la ligne
    </ul>    
    """,
    tests=(
    print_required,
    space_required,
    apostrophe_required,
    multiply_required,
    plus_required,
    bracket_required,
    comma_rejected,
    lf_required,
    require('40', "Tu ne dois pas compter les '*', tu multiplies par 70"),
    require('5', "Tu dois afficher 5 fois la ligne de *"),
    python_answer_good(5*(40*'*'+'\n')+'\n'),
    ),    
    )



t = 10
square_top = 'a' + t*'H' + 'b\n'
square_bottom = 'c' + t*'B' + 'd\n'
square_middle = 'G' + t*' ' + 'D\n'

square = square_top + t*square_middle + square_bottom


add(name='carré haut',
    required=['texte:addition texte', 'texte:multiplication texte'],
    question="""Dis à Python d'afficher 'a' plus %d fois 'H' plus 'b'&nbsp;:
    <pre>%s</pre>""" % (t, square_top),
    tests=(
    print_required,
    space_required,
    apostrophe_required,
    multiply_required,
    plus_required,
    comma_rejected,
    python_answer_good(square_top),
    ),    
    )



add(name='carré bas',
    required=['texte:addition texte', 'texte:multiplication texte'],
    question="""Dis à Python d'afficher 'c' plus %d fois 'B' plus 'd'&nbsp;:
    <pre>%s</pre>""" % (t, square_bottom),
    tests=(
    print_required,
    space_required,
    apostrophe_required,
    multiply_required,
    plus_required,
    comma_rejected,
    python_answer_good(square_bottom),
    ),    
    )
    


add(name='carré milieu',
    required=['texte:addition texte', 'texte:multiplication texte'],
    question="""Dis à Python d'afficher 'G' plus %d fois '&nbsp;&nbsp;' (un espace) plus 'D'&nbsp;:
    <pre>%s</pre>""" % (t, square_middle),
    tests=(
    print_required,
    space_required,
    apostrophe_required,
    multiply_required,
    plus_required,
    comma_rejected,
    python_answer_good(square_middle),
    ),    
    )
    



add(name='carré',
    required=['dessin:carr\xe9 haut', 'dessin:carr\xe9 milieu', 'dessin:carr\xe9 bas', 'texte:\xe0 la ligne', 'intro:ordre des calculs'],
    before="Le carré :<pre>" + square + "</pre>",
    question="""Pour afficher le carré, dis à Python
    d'afficher&nbsp;:
    <ul>
    <li> la ligne du haut plus un retour à la ligne
    <li> plus %d fois : la ligne du milieu plus un retour à la ligne
    <li> plus la ligne du bas
    </ul>
    """ % t,
    tests=(
    print_required,
    space_required,
    apostrophe_required,
    multiply_required,
    plus_required,
    comma_rejected,
    lf_required,
    bracket_required,
    number_of_is('\\n', 2, "N'oublie pas les 2 retours à la ligne"),
    number_of_is('*', 4, "Il doit y avoir 4 multiplications"),
    number_of_is('10', 4, "Il doit y avoir 4 multiplications par 10"),
    python_answer_good(square),
    ),    
    )



triangle = '\n'.join([ i * "*" for i in range(8) ]) + '\n'

add(name='triangle étoilé',
    required=['pour:feuilleter un classeur', 'texte:multiplication texte', 'texte:0 * texte'],
    question="Fais afficher le triangle suivant&nbsp;<pre>" + \
    triangle.replace('\n','&nbsp;\n') + '</pre>',
    tests=(
    print_required,
    space_required,
    apostrophe_required,
    for_required,
    range_required(8),
    python_answer_good(triangle),
    ),
    indices = (
    "Pour chaque nombre, tu fais afficher le nombre multiplié par '*'",
    ),
    )

lettre_E = '\n'.join(['*'*i for i in [4,1,3,1,4]]) + '\n'

add(name='lettre E',
    required=['triangle étoilé'],
    question="""Faire afficher la lettre E avec des '*' comme ceci&nbsp;:
    <pre>""" + lettre_E + """</pre>
    Pour le faire, il suffit de faire comme pour le triangle,
    mais au lieu de parcourir le classeur contenant les nombres,
    tu fais parcourir le classeur contenant le nombre d'étoiles
    à afficher sur chaque ligne.""",
    tests=(
    print_required,
    space_required,
    apostrophe_required,
    for_required,
    square_bracket_required,
    python_answer_good(lettre_E),
    ),
    indices=(
    """Le classeur à utiliser est <tt>[4,1,3,1,4]</tt> car cela
    défini pour chaque ligne le nombre d'étoiles à afficher.""",
    ),
   )

table = """1 2 3 4 5 6 7 8 9 10
2 4 6 8 10 12 14 16 18 20
3 6 9 12 15 18 21 24 27 30
4 8 12 16 20 24 28 32 36 40
5 10 15 20 25 30 35 40 45 50
6 12 18 24 30 36 42 48 54 60
7 14 21 28 35 42 49 56 63 70
8 16 24 32 40 48 56 64 72 80
9 18 27 36 45 54 63 72 81 90
10 20 30 40 50 60 70 80 90 100"""

add(name="multiplication",
    required=["pour:imbriqués", "dis:même ligne", "dis:rien"],
    question="""Faire afficher la table de multiplication&nbsp;:
<pre>%s</pre>""" % table,
    nr_lines = 4,
    tests=(
    print_required,
    space_required,
    apostrophe_rejected,
    for_required,
    number_of_is('for', 2, "Il faut 2 <tt>for</tt> pour cet exercice"),
    range_required(),
    python_answer_good(table + '\n'),
    ),
    indices = (
    """Les nombres de la table sont les produits de nombres
    compris entre 1 et 10, il faut donc utiliser des <tt>range(1,11)</tt>.""",
    """La première boucle contient la boucle affichant
    tous les nombres d'une ligne ainsi que la commande permettant
    de revenir à gauche.""",
    ),
    )

def jtable():
    s = ''
    for i in range(1,11):
        for j in range(1,11):
            s += '%2d ' % (i*j)
        s = s[:-1] + '\n'
    return s



add(name='jolie table',
    required=['multiplication', 'si:multi lignes', 'dis:espace'],
    default_answer="""for i in range(1,11):
 for j in range(1,11):
  print i*j,
 print""",
    before="""La table de multiplication n'est pas très jolie
    car certains produits sont inférieurs à 10 et d'autre non.
    C'est pour cela qu'il n'y a pas de jolies colonnes.""",
    question="""Modifies le programme Python pour afficher un espace
    avant les produits qui sont plus petits que 10,
    il suffit d'ajouter un <em>si</em> et d'afficher un espace
    avant d'afficher le produit.""",
    nr_lines = 6,
    tests=(
    print_required,
    space_required,
    apostrophe_required,
    for_required,
    less_than_required,
    require('10',
            "Il faut afficher un espace si le produit est inférieur à 10"),
    number_of_is('for', 2, "Il faut 2 <tt>for</tt> pour cet exercice"),
    range_required(),
    python_answer_good(jtable()),
    ),
    )

def coords():
    s = ''
    for y in range(6):
        for x in range(6):
            s += '(x= %d y= %d ) ' % (x,y)
        s = s[:-1] + '\n'
    return s

add(name='coordonnées',
    required = ['multiplication'],
    before="""Les coordonnées sont la série de nombres permettant
    de connaître la position d'un objet dans l'espace.
    <p>
    Si tu connais ta latitude et ta longitude, tu sais où
    tu te trouve sur terre.
    """,
    question = """Modifie le programme qui affiche la table de multiplication
    et affiche <tt>'(x=',x,'y=',y,')',</tt> à la place du produit.
<p>N'oublie pas la virgule à la fin du <tt>print</tt>""",
    nr_lines = 5,
    default_answer = """for y in range(6):
    for x in range(6):
        print x*y,
    print""",
    tests=(
    print_required,
    space_required,
    apostrophe_required,
    for_required,
    number_of_is('for', 2, "Il faut 2 <tt>for</tt> pour cet exercice"),
    range_required(),
    python_answer_good(coords()),
    ),
    good_answer = """Chaque case entre parenthèse du tableau,
    contient ses coordonnées <em>x</em> et <em>y</em>.
    <ul>
    <li> L'origine (point de coordonnées (x=0,y=0) est haut à gauche,</li>
    <li> La distance indiquée par <em>x</em> est horizontale et vers la droite.</li>
    <li> La distance indiquée par <em>y</em> est vertical, vers le bas.</li>
    </ul>
    """,
    )
    
    

def disque():
    s = ''
    for i in range(20):
        for j in range(20):
            if (i-10)*(i-10) + (j-10)*(j-10) < 8*8:
                s += '# '
            else:
                s += '. '
        s = s[:-1] + '\n'
    return s


add(name='disque',
    required=['pour:imbriqués', 'si:sinon', 'dis:même ligne', 'coordonnées'],
    before = """Géométrie&nbsp;: Un disque est composé des points
    dont la distance au centre du disque est
    plus petite que le rayon du disque.
    """,
    question = """<table><tr><td nowrap>Traduis en Python l'algorithme suivant&nbsp;:<br>
<em><big>
pour x dans les nombres entre 0 et 19 inclu:<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;pour y dans les nombres entre 0 et 19 inclu:<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;si (x-10)*(x-10) + (y-10)*(y-10) < 8*8 alors<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;affiche '#' sans revenir à la ligne<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;sinon affiche '.' sans revenir à la ligne<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;reviens à la ligne<br>
</big></em></td><td>Python devrait écrire&nbsp;&nbsp;:<small><pre>%s</pre></td></tr></table>""" % disque(),
    nr_lines = 8,
    tests=(
    print_required,
    space_required,
    apostrophe_required,
    for_required,
    less_than_required,
    range_required(),
    comma_required,
    require(("'#'", "'.'"), "Il manque le <tt>'#'</tt> ou le <tt>'.'</tt>"),
    require('20', """Il faut les nombres entre 0 et 19 inclu,
    on doit indiquer 20 à <tt>range</tt>"""),
    number_of_is('for', 2, "Il faut 2 <tt>for</tt> pour cet exercice"),
    python_answer_good(disque()),
    ),
    )

def dessine_point(coords):
    s = ''
    for i in range(10):
        for j in range(10):
            if [j,i] in coords:
                s += '# '
            else:
                s += '. '
        s = s[:-1] + '\n'
    return s

p = [[3,3],[4,3],[3,4],[5,4],[3,5],[4,5],[3,6],[3,7]]

add(name='dessine points',
    required=['pour:imbriqués', 'si:sinon', 'dis:même ligne', 'coordonnées'],
    before = """On veut afficher un rectangle avec des caractères <tt>'.'</tt>
    sauf à des endroits définis par leur coordonnées.
    Par exemple, si on met des <tt>'#'</tt> aux coordonnées
    <tt>[[0,0], [1,1], [2,2], [3,3], [4,3], [5,3], [5,2]]</tt>.
    On obtient&nbsp;:
    <pre># . . . . . . 
. # . . . . . 
. . # . . # . 
. . . # # # . 
. . . . . . .</pre>
    """,
    question = """Afficher des <tt>'#'</tt> aux coordonnées&nbsp;:
    <tt>""" + str(p) + """</tt>

    <p>
    Pour cela, tu peux traduire en Python l'algorithme suivant&nbsp;:<br>
<em><big>
pour y dans les nombres entre 0 et 9 inclu:<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;pour x dans les nombres entre 0 et 9 inclu:<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;si [x,y] est dans la liste des coordonnées alors<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;affiche '#' sans revenir à la ligne<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;sinon affiche '.' sans revenir à la ligne<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;reviens à la ligne<br>
</big></em>
""",
    nr_lines = 8,
    tests=(
    print_required,
    space_required,
    apostrophe_required,
    for_required,
    in_required,
    range_required(),
    comma_required,
    require(("'#'", "'.'"), "Il manque le <tt>'#'</tt> ou le <tt>'.'</tt>"),
    require('10', """Il faut les nombres entre 0 et 9 inclu,
    on doit indiquer 10 à <tt>range</tt>"""),
    number_of_is('for', 2, "Il faut 2 <tt>for</tt> pour cet exercice"),
    python_answer_good(dessine_point(p)),
    ),
    )


    
