# -*- coding: latin-1 -*-
#    QUENLIG: Questionnaire en ligne (Online interactive tutorial)
#    Copyright (C) 2011 Thierry EXCOFFIER, Universite Claude Bernard
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
from check import C

add(name="variables",
    required = ['intro:intro'],
    before="""En programmation, on manipule des <b>données</b>.
    <p>
    Ces données peuvent être des nombres, des chaînes de caractères ou
    des structures de données.
    <p>
    Pour pouvoir être manipulées, ces données doivent être "stockées"
    dans la mémoire de l'ordinateur.
    Pour que le programmeur puisse utiliser ces données,
    on va leur associer un <b>nom</b>&nbsp;: c'est ce que l'on appelle
    une <b>variable</b>.
    <p>
    En d'autres termes une <b>variable</b> est un nom que l'on associe
    à une zone mémoire dans laquelle sera codée une information
    """,  
    question="""Énumérez les noms des différents types de données du
    langage C (en français&nbsp;: caractère, entier, flottant, grand flottant).""",
    tests = (
        Good(Contain("int") & Contain("float") & Contain("double")
             & Contain("char")),
        Bad(Comment(Contain("main"),
                    """<tt>main</tt> n'est pas un mot clé du langage
                    mais le nom de la fonction principale""")),
        ),
    )

add(name="nom de variable",
    required = ['variables'],
    before="""Les noms de variables sont constitués d'une chaine de caractères.
    Mais attention, toutes les chaines de caractères ne sont pas valides. 
    Une chaine de caratère valide doit répondre aux critères suivants :
    <ul>
    <li>Ne pas contenir de caractères accentués
    <li>Ne pas contenir d'<tt>espace blanc</tt>.
    <small>caractère blanc, tabulation, fin de ligne</small>
    <li>Ne pas commencer par un chiffre
    <li>Ne pas contenir un <tt>caractère graphique</tt>.
    <small>tout caractère du clavier ne représentant ni une lettre
    de l'alphabet latin, ni un chiffre.
    hormis le 'tiret de soulignement' : <b>_</b></small>
    <li>Ne pas porter le même nom qu'un :
    <ul>
    <li> <b>mot clé</b> du langage (i.e un mot réservé au langage) ;
    <li> qu'une fonction existante ;
    <li> qu'une autre variable visible.
    </ul>
    </ul>
    On peut le dire autrement : un nom de variable peut être composé uniquement
    de caractères non accentués de l'alphabet latin, de chiffres et de tirets
    de soulignement; un nom de variable ne doit pas commencer par un chiffre.
    """,
    question="""Dans le programme suivant,
    listez les noms de variables qui ne sont pas valides.
    <small>Vous pouvez le vérifier en copiant ce programme dans un fichier
    et en le compilant.</small>
    <pre>int main(int argc, char **argv)
{
  int a_2 ;
  int 2b, c@d ;
  char _d ;
  float ?x ;
  double y2 ;
 
  return 0 ;
}</pre>
    """, 
    tests = (
        Bad(Comment(Contain('a_2'),
                    "Le souligné est autorisé dans les noms de variable")),
        Bad(Comment(Contain('y2'),
                    "Les chiffres sont autorisés dans les noms de variable")),
        Good(Contain("2b") & Contain("c@d") & Contain("?x")),
        Bad(Comment(Contain(''), "Il en manque")),
        ),
    )

add(name="casse variable",
    before="""En langage C,
    on différencie les caractères écrits en majuscules ou en minuscules.
    <p>
    Ainsi deux variables peuvent porter le même nom si la casse
    utilisée est différente.
    <p>
    Par exemple, la déclaration suivante est valide&nbsp;:
    <pre>int toto, TOTO, ToTo ;</pre>
    Pour le langage C, les trois variables précédentes portent des noms
    différents.
    <p>
    <b>Remarque</b> : Tous les mots clés du langage C sont écrits en caractères
    minuscules. 
    """,  
    question="""Dans le programme suivant,
    les déclarations de variables sont-elles correctes&nbsp;?
    <small>Répondez par oui ou non</small>
    <pre>
int main(int argc, char **argv)
{
  int INT;
  float FLOAT;
  double argv;
  
  return 0 ;
}</pre>
    """, 
   nr_lines=1,     
    tests = (
    Good(Comment(No(),
         """Les déclarations des variables <tt>INT</tt> et <tt>FLOAT</tt>
         sont correctes (car ces noms sont différents de <tt>int</tt>
         et <tt>float</tt> pour le langage).
         <p>Mais la déclaration <tt>double argv;</tt> est <b>incorrecte</b>,
         car le nom <tt>argv</tt> a déjà été utilisé plus haut dans une
         autre déclaration."""),
         ),
        ),
    )
