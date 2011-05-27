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

add(name = "affectation",
    required = ['variable:casse variable', 'types:entier flottant'],
    before = """Une fois déclarées, les variables vont pouvoir recevoir une
    valeur, c'est ce que l'on appelle une <b>affectation</b>.
    <p>
    Pour réaliser une affectation, on utilise l'opérateur <b>=</b>
    (comme en mathématiques).
    <p>
    Exemple, on pourra stocker un entier dans une variable de type
    <tt>int</tt>, un réel dans une variable de type <tt>float</tt>
    ou <tt>double</tt>,<br> un caractère dans une variable de
    type <tt>char</tt>.
    <p>
    On peux aussi réaliser des affectations de variables de même type,
    exemple : <tt>titi = toto</tt> signifie que l'on recopie le contenu
    de la variable <tt>toto</tt> dans le contenu de la variable <tt>titi</tt>.
    <p>
    Dans le programme suivant, après avoir déclarées des variables,
    nous les avons <b>initialisées</b> en leur affectant une valeur
    ou une variable.   
    <pre>int main(void)
{
  int toto, titi ;
  char caract ;
  float nombre ;
  double autre ;

  toto   = 10    ;
  caract = 'e'   ;
  nombre = 10.1  ;
  autre  = 1e-60 ;
  titi   = toto  ;
 
  return 0 ;
}</pre> """,
   question="""Après l'exécution du programme ci-dessus, que vaudra la variable <tt>titi</tt>?""",   
    tests = (
        Bad(Comment(UpperCase(Contain("toto")),
                    """La variable <tt>titi</tt> a effectivement reçu
                    le contenu de la variable <tt>toto</tt>,
                    par conséquent, que vaut <tt>titi</tt>&nbsp;?""")),
        Good(Comment(Int(10),
                     """Vous remarquerez que pour l'affectation d'un caractère
                     dans une variable de type <tt>char</tt>,
                     on met des quotes autour du caractère&nbsp;:
                     <tt>caract = 'e'</tt>
                     <p>
                     Vous noterez également qu'il y a deux façons de déclarer
                     une variable de type réelle en utilisant <tt>float</tt>
                     ou <tt>double</tt>,
                     nous expliquerons plus loin dans ce cours la différence
                     entre les deux, en attendant nous utiliserons uniquement
                     le type <tt>float</tt>""")),
        ),
    )

prog1 = r'''int main(void)
{
  float titi ;
  int toto ;
  char tutu ;

  titi = 5 ;
  toto = 10.4 ;
  tutu = 'x' ;
 
  return 0 ;
}'''

  
add(name = "bon type",
    before = """Une fois déclarées, les variables ne pourront recevoir
    que des données de même type que la variable.""",
    question = """Le programme suivant comporte un type erroné,
    corrigez-le et envoyez votre réponse.<pre>%s</pre>""" % prog1,
    nr_lines = 13,
    default_answer = prog1,
    tests = (
     Good(C(Equal(r'''int main(void)
{
  float titi ;
  float toto ;
  char tutu ;

  titi = 5 ;
  toto = 10.4 ;
  tutu = 'x' ;
 
  return 0 ;
}'''))),
        ),
    )

add(name = "addition",
    required = ["affectation"],
    before = """En langage C, on peut effectuer des additions en utilisant
    l'opérateur <b>+</b>
    <p>
    Comme en mathématique, on ne peut additioner que des objets
    de même nature.
    On peut additioner des nombres ou bien des variables contenant
    des nombres.""",
    question = """Regardez le programme ci-dessous,
    il illustre ce qui vient d'être expliqué.
    <p>
    À la fin du programme,
    quelle est la valeur de la variable nommée <tt>titi</tt>&nbsp;?
   <PRE>int main(void)
{
  int toto, titi ;
  
  toto = 10 ;     
  toto = toto + 5 ;
  titi = toto + 2 + 3 ;
 
  return 0 ;
}</PRE>""",
    tests = (
        Good(Int(20)),
        ),
    indices=(
        """Vous avez remarqué que l'expression <b>toto = toto+5</b>
        n'a pas de sens en mathématique. Mais en programmation,
        cela a un sens et signifie que l'expression qui se trouve à droite
        du signe <b>=</b> est évaluée et le résultat est stocké dans
        la variable qui se trouve à gauche du signe <b>=</b>.
        <p>
        En d'autres terme, cela signifie que l'on prend le contenu de la
        variable <tt>toto</tt>, on lui ajoute la valeur <tt>5</tt> et
        on stocke le résultat dans la variable <tt>toto</tt>.
        <p>
        À l'issue de cette instruction la variable <tt>toto</tt>
        prendra la valeur 15.""",
        ), 
    )

    


add(name = "4 opérations",
    required = ["addition"],
    before = """De même que l'addition, on peut effectuer les 3
    autres opérations de base : soustraction, multiplication, division
    en utilisant les signes mathématiques : <b>-</b>, <b>*</b> et
    <b>/</b>.
    <p>
    Les règles de priorité entre les opérateurs sont les mêmes
    qu'en mathématique&nbsp;: les opérateurs de multiplication
    et de division sont prioritaires sur les opérateurs d'addition
    et de soustraction.
    <p>
    Pour qu'un calcul soit prioritaire sur un autre,
    on peut utiliser des parenthèses.""",
    question="""Dans l'exemple ci-dessous,
    vous trouverez un exemple de calcul qui peut être effectué. <br>
    En fin de calcul, quelle est la valeur de la variable <tt>x</tt> ?
    <pre>
int main(void)
{
  float x, y ;

  y = 10 ;
  x = (y + 10) / 2 ;
  x =  y*3 - x ;

  return 0 ;
} </pre>""",
    tests = (
     Good(Int(20)),),
    )

add(name = "division entière",
    required = ["4 opérations"],
    before = """ATTENTION en langage C quand on divise deux entiers
    le résultat est un nombre entier.
    <tt>7/4</tt> donne 1 et <tt>7/-4</tt> donne -1.
    Ce n'est pas l'entier le plus proche.""",
    question = """Que contiendra la variable <tt>a</tt>&nbsp;?
    <pre>
int main(void)
{
  float a ;

  a = (10 * 3) / 3   -   (10 / 3) * 3 ;

  return 0 ;
} </pre>""",
    tests = (
        Good(Int(1)),
        ),
    ),
