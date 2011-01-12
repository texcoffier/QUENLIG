#!/usr/bin/python
# -*- coding: latin-1 -*-
#    QUENLIG: Questionnaire en ligne (Online interactive tutorial)
#    Copyright (C) 2008 Thierry EXCOFFIER, Olivier GLÜCK, Universite de Lyon
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

import sys
import os

def generate(name):
    sys.path.append(os.path.join(os.getcwd()))

    import statistics
    import configuration
    import main
    import questions
    import cgi
    
    configuration.session = main.Session(name)
    configuration.root = os.getcwd()
    configuration.version = os.path.basename(os.getcwd())
    configuration.session.init()
    os.chdir(configuration.session.dir)

    statistics.update_stats()
    stats = statistics.question_stats()

    ba = []
    filename = 'xxx-' + name + '.html'
    print '\nGenerate', os.path.join(os.getcwd(), filename)
    f = open(filename, 'w')
    f.write('''
<body onclick="compute();">
<style>
pre { margin: 0.1em }
td { vertical-align:top }
#rank { position: fixed ; right:0px; top: 0px; }
#rank TD { font-size: 80% }
TD.radio { white-space: nowrap ; }
table.top > TBODY > TR > TD { border-top: 1px solid black ; border-left: 1px solid black ; }
table.top { border-spacing: 0px ; border: 1px solid black; }
@media print { #rank { position: inherit ; } #rank TD { font-size: 100% ;} }
table.points { text-align: center ; }
</style>
''')

    students = list(stats.all_students)
    students.sort(lambda x,y: cmp(x.name, y.name))


    f.write("""<script>
var win ;
    
function compute()
{
if ( win == undefined || win.closed )
   {
   win = window.open() ;
   if ( ! win )
      return;
   win.document.open('text/html') ;
   win.document.write('Total:<div id="top"></div>');
   win.document.close() ;
   }

t = document.getElementsByTagName('input') ;
students = [] ;
for(i in t)
   {
   if ( t[i].checked )
       {
       name = t[i].name.split('/')[0] ;
       if ( students[name] != undefined )
           students[name] = Number(students[name]) + Number(t[i].value) ;
       else
           students[name] = Number(t[i].value) ;
       }
   }
s = '<table border class="top">' ;
for(i in students)
   s += '<tr><td>' + i + '</td><td>' + students[i] + '</td></tr>' ;
s += '</table>' ;
win.document.getElementById('top').innerHTML = s ;
}

var note_pas = 1 ;
var note_nb = 5 ;

function radio(name, question, answer)
{
document.write('<tr><td class="radio"><table class="points"><tr>') ;
for(var i=0; i<note_nb; i++)
   document.write('<td>' + i*note_pas + '</td>') ;
document.write('</tr><tr>') ;
for(var i=0; i<note_nb; i++)
   document.write('<td><input type="radio" name="' + name + '/' + question + '" value="' + i*note_pas + '"></td>') ;
document.write('</tr></table></td><td>' + name +
               '</td><td>' + answer + '</td></tr>') ;

}


</script>
""")
    for q in questions.sorted_questions:
        q = q.name
        f.write('<h1>' + q + '</h1>\n')
        f.write('<p>' + questions.questions[q].question('') + '</p>\n')
        f.write('<table class="top">\n')
        t = []
        for s in students:
            for a in s.answers.values():
                if a.question == q and a.answered:
                    t.append( (s.name, q,
                               cgi.escape(a.answered)
                               .replace('\r\n','\n')
                               .replace('\n','<br>')
                               .replace('\\','\\\\')
                               .replace('"', '\\"')) )
                    break
        t.sort(key=lambda x: x[2].strip().lower())
        for tt in t:
            f.write('<script>radio("%s","%s","%s");</script>\n' % tt)
        f.write('</table>')
    f.close()





if __name__ == "__main__":
    if len(sys.argv) == 1:
        sys.stderr.write('Give a list of session names')
        sys.exit(1)
    
    
    current_directory = os.getcwd()
    for i in sys.argv[1:]:
        print i
        generate(i)
        os.chdir(current_directory)
        import statistics
        statistics.forget_stats()
