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

import collections
import os
import colorsys
import time
import cgi

from . import questions
from . import utilities
from . import student
from . import configuration
import types

_stats = None

def select(value, mean, coef):
    i = -2
    for c in coef:
        if value < c*mean :
            break
        i += 1
    return i

class QuestionStat:
    time_searching = 0
    time_after = 0
    given = 0
    view = 0
    bad = 0
    good = 0
    indice = 0
    nr_comment = 0
    def __init__(self, question):
        self.question = question
        self.good_time = [] # Times to give a good answer
        self.indices = [0] * len(question.indices)

class Stats:
    def __init__(self):
        self.last_time = 0
        self.ttl = 1
        
    def update(self):
        """Compute statistics about questions and students"""
        t = time.time()
        if t - self.last_time < self.ttl:
            return
        self.last_time = t

        if student.students:
            self.all_students = tuple(student.students.values())
        else:
            self.all_students = student.all_students()

        for question in questions.questions.values():
            question.NS = QuestionStat(question)

        self.nr_good_answers = 0
        self.nr_bad_answers = 0
        self.nr_bad_answers_normed = 0
        self.nr_given_indices = 0
        self.nr_given_indices_normed = 0
        self.nr_given_comment = 0
        self.time_after = 0
        self.time_after_normed = 0

        normed_count = 0
        for s in self.all_students:
            s.the_number_of_good_answers    = s.number_of_good_answers()
            s.the_number_of_given_questions = s.number_of_given_questions()
            s.the_number_of_bad_answers     = s.number_of_bad_answers()
            s.the_number_of_given_indices   = s.number_of_given_indices()
            s.the_number_of_comment         = s.number_of_comment()
            s.the_time_searching            = s.time_searching()
            s.the_time_after                = s.time_after()
            s.the_time_first                = s.time_first()
            s.the_time_last                 = s.time_last()
            s.the_time_variance             = s.time_variance()

            if s.the_number_of_good_answers:
                normed_count += 1
                s.the_number_of_bad_answers_normed = s.the_number_of_bad_answers / float(s.the_number_of_good_answers)
                s.the_number_of_given_indices_normed = s.the_number_of_given_indices / float(s.the_number_of_good_answers)
                s.the_time_after_normed = s.the_time_after / float(s.the_number_of_good_answers)
            else:
                s.the_number_of_bad_answers_normed = None
                s.the_number_of_given_indices_normed = None
                s.the_time_after_normed = None

            self.nr_good_answers  += s.the_number_of_good_answers
            self.nr_bad_answers   += s.the_number_of_bad_answers
            self.nr_given_indices += s.the_number_of_given_indices
            self.nr_given_comment += s.the_number_of_comment
            self.time_after       += s.the_time_after

            if s.the_number_of_good_answers:
                self.nr_bad_answers_normed += s.the_number_of_bad_answers_normed
                self.nr_given_indices_normed += s.the_number_of_given_indices_normed
                self.time_after_normed += s.the_time_after_normed
                
            
            for answer in s.answers.values():
                try:
                    q = questions.questions[answer.question]
                except KeyError:
                    continue
                if answer.nr_asked == 0:
                    continue
                q.NS.given += 1
                q.NS.view += answer.nr_asked
                q.NS.bad += answer.nr_bad_answer
                q.NS.indice += answer.indice + 1
                if answer.indice >= 0:
                    try:
                        for i in range(answer.indice+1):                    
                            q.NS.indices[i] += 1
                    except IndexError:
                        import sys
                        sys.stderr.write("""Problem indice overflow
question: %s
student: %s
""" % (q, s.filename))
                if answer.nr_good_answer:
                    q.NS.time_searching += (answer.time_searching
                                            / answer.nr_good_answer)
                else:
                    q.NS.time_searching += answer.time_searching
                q.NS.time_after += answer.time_after
                q.NS.good       += answer.nr_good_answer != 0
                q.NS.nr_comment += len(answer.comments)
                if answer.good_answer_times:
                    q.NS.good_time.append(max(answer.good_answer_times))
                    # q.NS.good_time += answer.good_answer_times

        for q in questions.questions.values():
            q.student_time = q.NS.time_searching + q.NS.time_after
            nr_good_times = len(q.NS.good_time)
            if nr_good_times > 5:
                q.perfect_time = max(
                    sorted(q.NS.good_time)[nr_good_times//2],
                    q.perfect_time)
            q.stats = q.NS

        # Recompute the number of perfect time answer
        for s in self.all_students:
            for answer in s.answers.values():
                q = questions.questions.get(answer.question, None)
                if q is None:
                    continue
                answer.nr_perfect_answer = len(tuple(
                    x
                    for x in answer.good_answer_times
                    if x < q.perfect_time))

        # Search correct response time within a time window
        t = []
        for s in self.all_students:
            s.nr_answer_same_time = collections.defaultdict(lambda: [0,0])
            for answer in s.answers.values():
                if answer.answered:
                    t.append( (answer.question, answer.answer_times[-1], id(s), s) )
        t.sort()
        for i in range(len(t)):
            current_time = t[i][1]
            current_question = t[i][0]
            j = i - 1
            while ( j >= 0
                    and current_time - t[j][1] < 60
                    and current_question == t[j][0]
                    ) :
                # i copied on j
                t[i][3].nr_answer_same_time[t[j][3].name][0] += 1
                # j was copied by i
                t[j][3].nr_answer_same_time[t[i][3].name][1] += 1
                j -= 1
        for s in self.all_students:
            s.nr_of_same_time = sum(sum(list(s.nr_answer_same_time.values()),
                                        []))
            if s.the_number_of_given_questions:
                s.nr_of_same_time_normed = (
                    s.nr_of_same_time
                    / float(s.the_number_of_given_questions) )
            else:
                s.nr_of_same_time_normed = 0



        # Compute the list of students by number of good answers
        t = [(s.the_number_of_good_answers, id(s), s)
             for s in self.all_students]
        t.sort()
        t.reverse()
        self.sorted_students = [c for a, b, c in t]

        if normed_count:
            # Compute some means
            self.nr_good_answers         /= float(len(self.all_students))
            self.nr_bad_answers          /= float(len(self.all_students))
            self.nr_given_indices        /= float(len(self.all_students))
            self.nr_given_comment        /= float(len(self.all_students))
            self.time_after              /= float(len(self.all_students))
            self.nr_given_indices_normed /= float(normed_count)
            self.nr_bad_answers_normed   /= float(normed_count)
            self.time_after_normed       /= float(normed_count)
                                               
        # Warning
        # 2 : very good
        # 1 : good
        # 0 : nothing to say
        # -1 : bad
        # -2 : very bad
        for s in self.all_students:
            if (s.the_number_of_good_answers == 0
                or self.nr_good_answers < 10):
                s.warning_nr_good_answers = 0
                s.warning_nr_bad_answers = 0
                s.warning_nr_given_indices = 0
                s.warning_time_after = 0
                continue

            s.warning_nr_good_answers = select(
                s.the_number_of_good_answers,
                self.nr_good_answers,
                (0.7, 0.8, 1.3, 1.5)
                )

            s.warning_nr_bad_answers = - select(
                s.the_number_of_bad_answers_normed,
                self.nr_bad_answers_normed,
                (0.5, 0.6, 1.5, 2)
                )

            s.warning_nr_given_indices = - select(
                s.the_number_of_given_indices_normed,
                self.nr_given_indices_normed,
                (0.5, 0.6, 1.5, 2)
                )

            s.warning_time_after = - select(
                s.the_time_after_normed,
                self.time_after_normed,
                (0.4, 0.6, 1.6, 1.8)
                )
        if self.all_students:
            self.max_good_answers  = max(s.the_number_of_good_answers
                                         for s in self.all_students)
            self.max_bad_answers   = max(s.the_number_of_bad_answers
                                         for s in self.all_students)
            self.max_given_indices = max(s.the_number_of_given_indices
                                         for s in self.all_students)
        else:
            self.max_good_answers  = 0
            self.max_bad_answers  = 0
            self.max_given_indices  = 0

        # Compute statistics a percentage of the time
        # If we compute statistics in one second and we want
        # to allocate 1% of time to statistics computing.
        # then we must compute statistics every 100 seconds.
        self.ttl = (101-configuration.statistics_cpu_allocation)*(time.time() - self.last_time)




_stats = Stats()


def histogram_level():
    histogram = []
    for q in questions.sorted_questions:
        while q.level >= len(histogram):
            histogram.append(0)
        histogram[q.level] += 1
    return histogram

@utilities.add_a_lock
def question_stats():
    _stats.update()
    return _stats

def forget_stats():
    _stats.last_time = 0

def translate_dot_(name):
    return cgi.escape(name.translate(utilities.flat).replace('\\', 'BS')).replace(':',' ').replace('"',' ').replace(' ', '\\n')

def translate_dot(name):
    return '"' + translate_dot_(name) + '"'


def graph_dot(show_stats=False):
    stats = question_stats()

    f = open("HTML/xxx_graphe.dot", "w")
    f.write("""
    digraph "questions" {
    node[shape=none,margin="0",height="0.01",style="filled"];
    edge[arrowhead=empty, arrowsize="0.5",norm_width="0.5"];
    graph[dpi=70,nodesep="0.1",ranksep="0.2",charset="UTF-8", orientation="P",mclimit="10",nslimit="10"];
    """)
    nb = float(len(questions.worlds()))
    rvb = {}
    i = 0
    for w in questions.worlds():
        c = colorsys.hls_to_rgb(i/nb, 0.8, 0.99)
        rvb[w] = '"#%02x%02x%02x"' % (int(c[0]*256), int(c[1]*256),
                                      int(c[2]*256))
        i += 1
    n = float(len(stats.all_students))
    for q in questions.questions.values():
        name = q.name.translate(utilities.flat)
        color = rvb[ q.name.split(":")[0] ]
        if q.stats.given == 0:
            q.stats.given = 1 # forked, so it is allowed
        if show_stats:
            f.write("""%s [ href="%s",label=<<TABLE BORDER="0" CELLPADDING="0"><TR><TD COLSPAN="3" BGCOLOR="blue" HEIGHT="%d"></TD></TR><TR><TD BGCOLOR="red" WIDTH="%d"></TD><TD BGCOLOR=%s>%s</TD><TD BGCOLOR="green" WIDTH="%d"></TD></TR><TR><TD COLSPAN="3" BGCOLOR="black" HEIGHT="%d"></TD></TR></TABLE>>] ;\n""" % (
                translate_dot(q.name),
                q.url(),
                int(50*q.stats.indice/q.stats.given),
                int(50*q.stats.bad/n),
                color,
                translate_dot_(q.name).replace("\\n", "<BR/>"),
                int(50*q.stats.good/n),
                int(q.student_time/q.stats.given/10),
                )
                    )
        else:
            f.write("""%s [ fillcolor=%s,label="%s" ] ;\n""" % (
                translate_dot(q.name),
                color,
                translate_dot_(q.name).replace("\\n", " "),
                )
                    )

    for q in questions.questions.values():
        for qq in q.required.requireds:
            if qq.name not in questions.questions:
                print("%s est requis par %s" % (qq.name, q))
                raise ValueError
            if qq.unrequired:
                style = "[ style=dotted ]"
            elif qq.hidden:
                style = "[ style=dashed ]"
            else:
                style = ""
            f.write("%s -> %s%s;\n" % (translate_dot(qq.name),
                                       translate_dot(q.name),
                                       style
                                     ))

    f.write("}\n")
    f.close()

    os.system("""

    (
    dot -oHTML/xxx_graphe.png -Tpng HTML/xxx_graphe.dot
    dot -oHTML/xxx_graphe.svg -Tsvg HTML/xxx_graphe.dot
    ) &


    """)

graph_dot_minimal = graph_dot

def graph2_dot():
    stats = question_stats()
    nb = float(len(questions.worlds()))
    n = float(len(stats.all_students))
    if n == 0:
        return

    f = open("HTML/xxx_graphe2.dot", "w")
    f.write("""
    digraph "questions" {
    node[shape=none];
    graph[charset="UTF-8", size="11.50,7.5", orientation="L"];
    """)
    for w in questions.worlds():
        f.write("""subgraph cluster_%s {
     label="%s";
     """ % (w, w))
        for q in questions.questions.values():
            if not q.name.startswith(w + ":"):
                continue
            name = q.name.translate(utilities.flat)
            if q.stats.given == 0:
                q.stats.given = 1
            f.write("""%s [ label=<<TABLE BORDER="0" CELLPADDING="0"><TR><TD COLSPAN="3" BGCOLOR="blue" HEIGHT="%d"></TD></TR><TR><TD BGCOLOR="red" WIDTH="%d"></TD><TD>%s</TD><TD BGCOLOR="green" WIDTH="%d"></TD></TR><TR><TD COLSPAN="3" BGCOLOR="black" HEIGHT="%d"></TD></TR></TABLE>>] ;\n""" % (
                translate_dot(q.name),
                int(50*q.stats.indice/q.stats.given),
                int(50*q.stats.bad/n),
                translate_dot_(q.name).replace("\\n", "<BR/>"),
                int(50*q.stats.good/n),
                int(q.student_time/q.stats.given/10),
                )
                    )
        f.write("}\n")

    for q in questions.questions.values():
        for qq in q.required.names():
            if qq not in questions.questions:
                print("%s est requis par %s" % (qq, q))
                raise ValueError
            f.write("%s -> %s ;\n" % (translate_dot(qq), translate_dot(q.name)))

    f.write("}\n")
    f.close()

    os.system("dot -oHTML/xxx_graphe2.ps -Tps HTML/xxx_graphe2.dot &")




def troncate_question(q):
    if True:
        q = q.split('<br>')[0]
        q = q[:min(len(q),90)]
        q = cgi.escape(q)
    else:
        q = cgi.escape(q)
            
    return q

def html_simple(state):
    """display an HTML table with all the questions name
    and the start of the question itself.

    Function called when running: 'main.py session plot'
    """
    all = list(questions.questions)
    all.sort()
    t = ['<table><colgroup><col width="*"><col width="5*"></colgroup><tbody>']
    w = ''
    for q in all:
        q = questions.questions[q]
        if q.world != w:
            t.append( '<tr><th colspan="2">' + q.world + '</th></tr>')
            w = q.world
        t.append('<tr><td>' + q.short_name + '</td><td><p>' +
                 troncate_question(q.question(state)) + '</td></tr>')
    t.append('</tbody></table>')
           
    return '\n'.join(t)

def display_no_more_valid_answers():
    """Displays student answers that where validated as good in the past.
    But no more now.

    Function called when running: 'main.py session problems'
    """
    import sys
    class X:
        pass
    X = X()
    stats = question_stats()
    messages = {}
    print()
    
    for s in stats.all_students:
        sys.stdout.write('*')
        sys.stdout.flush()
        for answer in s.answers.values():
            try:
                q = questions.questions[answer.question]
            except KeyError:
                continue
            if not answer.answered:
                continue
            X.question = q
            X.student = s
            ok, comment = s.check_answer(answer.answered, X)
            if not ok:
                if answer.question not in messages:
                    messages[answer.question] = {}
                messages[answer.question][answer.answered] = True
    print()
    print("Answers no more accepted:")
    for m in messages:
        print(m)
        for v in messages[m]:
            print('\t' + v)

