#!/usr/bin/env python
# -*- coding: latin-1 -*-
#    QUENLIG: Questionnaire en ligne (Online interactive tutorial)
#    Copyright (C) 2007 Thierry EXCOFFIER, Universite Claude Bernard
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

"""Display an SVG graphic of the session with all the questions and statistics.
This graphic is very slow to display so it is unusable."""

import statistics
import questions
import configuration
import types
import cgi

container = 'analyse'
link_to_self = True
priority_execute = '-question_answer'
acls = { 'Teacher': ('executable',) }

##############################################################################

import server

class Svg:
    def __init__(self, text_height, bar_text_height, border_width,
                 width, height, url_base=''):
        self.url_base = url_base

        self.content = '''<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<!-- <?xml-stylesheet href="/%ssvg.css" type="text/css"?> -->
<!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 20010904//EN" 
  "http://www.w3.org/TR/2001/REC-SVG-20010904/DTD/svg10.dtd">
<svg
   xmlns:dc="http://purl.org/dc/elements/1.1/"
   xmlns:cc="http://web.resource.org/cc/"
   xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"
   xmlns:svg="http://www.w3.org/2000/svg"
   xmlns="http://www.w3.org/2000/svg"
   xmlns:xlink="http://www.w3.org/1999/xlink"
   width="%d"
   height="%d"
   >
<script xlink:href="/%ssvg.js"/>
<defs>
    <style type="text/css"><![CDATA[
      text.title { font-size:%dpx;}
      text.title_m { font-size:%dpx; text-anchor: middle;}
      text.bar { font-size:%dpx; }
      rect.back { stroke-width: %dpx; }
      %s
    ]]></style>
  </defs>
     ''' % (configuration.prefix, width, height,configuration.prefix,text_height,text_height, bar_text_height, border_width, server.get_file('svg.css').content)

    def end(self):
        return self.content + '''</svg>'''
    def rect(self, x, y, w, h, svg_class="", style=""):
        if svg_class:
            svg_class = 'class="' + svg_class + '" '
        self.content += '''<rect %sx="%g" y="%g" width="%g" height="%g" style="%s" />\n''' % (svg_class,x,y,w,h,style)
    def text(self, x,y, text, svg_class="", style=""):
        if svg_class:
            svg_class = ' class="' + svg_class + '"'
        if style:
            style = ' style="' + style + '"'
        self.content += '''<text%s%s><tspan x="%d" y="%d">%s</tspan></text>\n''' % (svg_class, style, x,y,cgi.escape(text))
    def g_start(self, x, y):
        self.content += """<g onclick=\"mouseclick(this);\" transform=\"translate(%d,%d)\">\n""" % (x, y)
    def g_end(self):
        self.content += """</g>\n"""

def split_text(text):
    middle = len(text)/2
    for i in xrange(middle):
        if text[middle+i] == ' ':
            return [text[0:middle+i], text[middle+i+1:]]
        if text[middle-i] == ' ':
            return [text[0:middle-i], text[middle-i+1:]]
    return [text, '']

class BarPlot:
    def __init__(self, svg, width, height, nr_bars, text_height):
        self.svg = svg
        self.width = width
        self.height = height
        self.nr_bars = nr_bars
        self.bar_height = height / nr_bars
        self.text_height = text_height
        self.half_width = width / 2

    def background(self, border_width):
        self.svg.rect(-border_width/2., -border_width/2.,
                 self.width + border_width, self.height + border_width,
                 svg_class='back', style=self.opacity)

    def bar(self, nr, value, max, svg_class, pixel=False):
        if isinstance(value, types.ListType):
            if not value:
                return
            dy = self.bar_height / float(len(value))
            for i in range(len(value)):
                self.svg.rect(0, self.bar_height * nr + i * dy,
                              self.width * (value[i]/float(max)), dy, 
                              svg_class=svg_class + str(i),
                              style=self.opacity)
            self.svg.text(1,
                          self.bar_height * nr + (self.text_height + self.bar_height)/2.,
                          str(value),
                          style=self.opacity,
                          svg_class='bar s',
                          )
            return

        if pixel:
            n = int(value/max)
            for i in range(n):
                self.svg.rect(0, self.bar_height * nr + i*pixel,
                              self.width, pixel, 
                              svg_class=svg_class,
                              style=self.opacity)
            self.svg.rect(0, self.bar_height * nr + n*pixel,
                          self.width * (value % max) / float(max), pixel, 
                          svg_class=svg_class,
                          style=self.opacity)
            comment = '%g' % value
        else:
            self.svg.rect(0, self.bar_height * nr,
                          self.width * (value/float(max)), self.bar_height, 
                          svg_class=svg_class,
                          style=self.opacity)
            comment = '%g / %g' % (value, max)

        self.svg.text(1,
                      self.bar_height * nr + (self.text_height + self.bar_height)/2.,
                      comment,
                      style=self.opacity,
                      svg_class='bar',
                      )

    def nr_comments(self, nr):
        self.svg.text(self.width, self.height/2,
                      str(nr),
                      style=self.opacity,
                      svg_class='nr_comments e',
                      )
        
    def textes(self, textes, line_decal, svg_class='title_m', align='m',
               opacity=None, url=None):
        if opacity == None:
            opacity = self.opacity
        if align == 'm':
            x = self.half_width
        elif align == 's':
            x = self.width + self.text_height
        else:
            x = -self.text_height

        if url:
            self.svg.content += '<a xlink:href="%s%s">' % (
                self.svg.url_base, url.replace('&','&amp;'))
        
        for i in range(len(textes)):
            if textes[i]:
                self.svg.text(x, line_decal*(i+1),
                              textes[i].encode('utf-8'),
                              style=opacity,
                              svg_class=svg_class
                              )
        if url:
            self.svg.content += '</a>'
        
def plot_svg(url_base):
    width = 55
    height = 24
    text_height = 6
    bar_text_height = text_height / 2
    x_spacing = 3
    y_spacing = 3
    line_spacing = (height - 3*text_height)/4
    line_decal = text_height + line_spacing
    border_width = 1
    x_margin = width * 1.5
    x_margin += 2*width # Name of required and used_by list of questions
    y_margin = height * 1.4

    stats = statistics.question_stats()

    h = statistics.histogram_level()
    h.sort()
    
    svg = Svg(text_height, bar_text_height, border_width,
              h[-1] * (width + x_spacing) + 2*x_margin,
              (2+questions.sorted_questions[-1].level) * (height + y_spacing) + 2 * y_margin,
              url_base
              )
    barplot = BarPlot(svg, width, height, 4, bar_text_height)

    level = -1
    y = y_margin
    for q in questions.sorted_questions:
        if q.level != level:
            x = x_margin
            y += height + y_spacing
            level = q.level

        opacity = (q.student_given+1.) / (len(stats.all_students)+1)
        barplot.opacity = "opacity:%5.3f;fill-opacity:%5.3f;" % (
            opacity, opacity)

        svg.g_start(x, y)
        barplot.background(border_width)

        if q.student_given:
            barplot.bar(0,q.student_good, q.student_given, svg_class='good')
            barplot.bar(1,q.student_bad, q.student_given, svg_class='bad', pixel=2)
            barplot.bar(2,q.student_indices, q.student_given, svg_class='indice')
            barplot.bar(3,int(q.student_time_searching/q.student_given),300,svg_class='time', pixel=2)

        if q.student_nr_comment:
            barplot.nr_comments(q.student_nr_comment)
            
        t = [q.world] + split_text(q.short_name)
        barplot.textes(t, line_decal, url=q.url())

        t = q.required.names()
        barplot.textes(t, bar_text_height, opacity='fill-opacity:0;', align='e', svg_class='bar e')

        t = q.used_by
        barplot.textes(t, bar_text_height, opacity='fill-opacity:0;', align='s', svg_class='bar s')
        
        x += width + x_spacing
        svg.g_end()

    return svg.end()



def execute(state, plugin, argument):
    if argument == None:
        return ''
    return 'image/svg+xml', plot_svg(state.url_base_full)










