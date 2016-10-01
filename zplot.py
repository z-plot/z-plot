# Copyright (c) 2015, Remzi Arpaci-Dusseau
# All rights reserved.
# 
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
# 
# * Redistributions of source code must retain the above copyright notice, this
#   list of conditions and the following disclaimer.
# 
# * Redistributions in binary form must reproduce the above copyright notice,
#   this list of conditions and the following disclaimer in the documentation
#   and/or other materials provided with the distribution.
# 
# * Neither the name of zplot nor the names of its
#   contributors may be used to endorse or promote products derived from
#   this software without specific prior written permission.
# 
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

import time
import math
import os
import stat
import sys
import sqlite3
import re
import socket
import random
import types
import string

#
# UTILITY functions
#
# Used throughout.
#
def abortIfFalse(statement, msg):
    if statement == False:
        print 'ABORT:', msg
        exit(1)
    return

def abort(str):
    print 'Abort! Reason: (%s)' % str
    exit(1)


#
# class color
#
# Separate class just to map color names to RGB values.
# Not of general use.
#
class color:
    def __init__(self,
                 # no arguments
                 ):
        self.color_list = {
            'aliceblue'              :  '0.94 0.97 1.00',
            'antiquewhite'           :  '0.98 0.92 0.84',
            'aqua'                   :  '0.00 1.00 1.00',
            'aquamarine'             :  '0.50 1.00 0.83',
            'azure'                  :  '0.94 1.00 1.00',
            'beige'                  :  '0.96 0.96 0.86',
            'bisque'                 :  '1.00 0.89 0.77',
            'black'                  :  '0.00 0.00 0.00',
            'blanchedalmond'         :  '1.00 0.92 0.80',
            'blue'                   :  '0.00 0.00 1.00',
            'blueviolet'             :  '0.54 0.17 0.89',
            'brown'                  :  '0.65 0.16 0.16',
            'burlywood'              :  '0.87 0.72 0.53',
            'cadetblue'              :  '0.37 0.62 0.63',
            'chartreuse'             :  '0.50 1.00 0.00',
            'chocolate'              :  '0.82 0.41 0.12',
            'coral'                  :  '1.00 0.50 0.31',
            'cornflowerblue'         :  '0.39 0.58 0.93',
            'cornsilk'               :  '1.00 0.97 0.86',
            'crimson'                :  '0.86 0.08 0.24',
            'cyan'                   :  '0.00 1.00 1.00',
            'darkblue'               :  '0.00 0.00 0.55',
            'darkcyan'               :  '0.00 0.55 0.55',
            'darkgoldenrod'          :  '0.72 0.53 0.04',
            'darkgray'               :  '0.66 0.66 0.66',
            'darkgreen'              :  '0.00 0.39 0.00',
            'darkkhaki'              :  '0.74 0.72 0.42',
            'darkmagenta'            :  '0.55 0.00 0.55',
            'darkolivegreen'         :  '0.33 0.42 0.18',
            'darkorange'             :  '1.00 0.55 0.00',
            'darkorchid'             :  '0.60 0.20 0.80',
            'darkred'                :  '0.55 0.00 0.00',
            'darksalmon'             :  '0.91 0.59 0.48',
            'darkseagreen'           :  '0.55 0.74 0.56',
            'darkslateblue'          :  '0.28 0.24 0.55',
            'darkslategray'          :  '0.18 0.31 0.31',
            'darkturquoise'          :  '0.00 0.87 0.82',
            'darkviolet'             :  '0.58 0.00 0.83',
            'deeppink'               :  '1.00 0.08 0.58',
            'deepskyblue'            :  '0.00 0.75 1.00',
            'dimgray'                :  '0.41 0.41 0.41',
            'dodgerblue'             :  '0.12 0.56 1.00',
            'drabgreen'              :  '0.60 0.80 0.60',
            'dullyellow'             :  '1.00 0.90 0.60',
            'firebrick'              :  '0.70 0.13 0.13',
            'floralwhite'            :  '1.00 0.98 0.94',
            'forestgreen'            :  '0.13 0.55 0.13',
            'fuchsia'                :  '1.00 0.00 1.00',
            'gainsboro'              :  '0.86 0.86 0.86',
            'ghostwhite'             :  '0.97 0.97 1.00',
            'gold'                   :  '1.00 0.84 0.00',
            'goldenrod'              :  '0.85 0.65 0.13',
            'gray'                   :  '0.50 0.50 0.50',
            'green'                  :  '0.00 0.50 0.00',
            'greenyellow'            :  '0.68 1.00 0.18',
            'honeydew'               :  '0.94 1.00 0.94',
            'hotpink'                :  '1.00 0.41 0.71',
            'indianred'              :  '0.80 0.36 0.36',
            'indigo'                 :  '0.29 0.00 0.51',
            'ivory'                  :  '1.00 1.00 0.94',
            'khaki'                  :  '0.94 0.90 0.55',
            'lavender'               :  '0.90 0.90 0.98',
            'lavenderblush'          :  '1.00 0.94 0.96',
            'lawngreen'              :  '0.49 0.99 0.00',
            'lemonchiffon'           :  '1.00 0.98 0.80',
            'lightblue'              :  '0.68 0.85 0.90',
            'lightcoral'             :  '0.94 0.50 0.50',
            'lightcyan'              :  '0.88 1.00 1.00',
            'lightgoldenrodyellow'   :  '0.98 0.98 0.82',
            'lightgreen'             :  '0.56 0.93 0.56',
            'lightgrey'              :  '0.83 0.83 0.83',
            'lightpink'              :  '1.00 0.71 0.76',
            'lightsalmon'            :  '1.00 0.63 0.48',
            'lightseagreen'          :  '0.13 0.70 0.67',
            'lightskyblue'           :  '0.53 0.81 0.98',
            'lightslategray'         :  '0.47 0.53 0.60',
            'lightsteelblue'         :  '0.69 0.77 0.87',
            'lightyellow'            :  '1.00 1.00 0.88',
            'lime'                   :  '0.00 1.00 0.00',
            'limegreen'              :  '0.20 0.80 0.20',
            'linen'                  :  '0.98 0.94 0.90',
            'magenta'                :  '1.00 0.00 1.00',
            'maroon'                 :  '0.50 0.00 0.00',
            'mediumaquamarine'       :  '0.40 0.80 0.67',
            'mediumblue'             :  '0.00 0.00 0.80',
            'mediumorchid'           :  '0.73 0.33 0.83',
            'mediumpurple'           :  '0.58 0.44 0.86',
            'mediumseagreen'         :  '0.24 0.70 0.44',
            'mediumslateblue'        :  '0.48 0.41 0.93',
            'mediumspringgreen'      :  '0.00 0.98 0.60',
            'mediumturquoise'        :  '0.28 0.82 0.80',
            'mediumvioletred'        :  '0.78 0.08 0.52',
            'midnightblue'           :  '0.10 0.10 0.44',
            'mintcream'              :  '0.96 1.00 0.98',
            'mistyrose'              :  '1.00 0.89 0.88',
            'moccasin'               :  '1.00 0.89 0.71',
            'navajowhite'            :  '1.00 0.87 0.68',
            'navy'                   :  '0.00 0.00 0.50',
            'oldlace'                :  '0.99 0.96 0.90',
            'olivedrab'              :  '0.42 0.56 0.14',
            'orange'                 :  '1.00 0.65 0.00',
            'orangered'              :  '1.00 0.27 0.00',
            'orchid'                 :  '0.85 0.44 0.84',
            'palegoldenrod'          :  '0.93 0.91 0.67',
            'palegreen'              :  '0.60 0.98 0.60',
            'paleturquoise'          :  '0.69 0.93 0.93',
            'palevioletred'          :  '0.86 0.44 0.58',
            'papayawhip'             :  '1.00 0.94 0.84',
            'peachpuff'              :  '1.00 0.85 0.73',
            'peru'                   :  '0.80 0.52 0.25',
            'pink'                   :  '1.00 0.78 0.80',
            'plum'                   :  '0.87 0.63 0.87',
            'powderblue'             :  '0.69 0.88 0.90',
            'purple'                 :  '0.50 0.00 0.50',
            'red'                    :  '1.00 0.00 0.00',
            'rosybrown'              :  '0.74 0.56 0.56',
            'royalblue'              :  '0.25 0.41 0.88',
            'saddlebrown'            :  '0.55 0.27 0.07',
            'salmon'                 :  '0.98 0.50 0.45',
            'sandybrown'             :  '0.96 0.64 0.38',
            'seagreen'               :  '0.18 0.55 0.34',
            'seashell'               :  '1.00 0.96 0.93',
            'sienna'                 :  '0.63 0.32 0.18',
            'silver'                 :  '0.75 0.75 0.75',
            'skyblue'                :  '0.53 0.81 0.92',
            'slateblue'              :  '0.42 0.35 0.80',
            'snow'                   :  '1.00 0.98 0.98',
            'springgreen'            :  '0.00 1.00 0.50',
            'steelblue'              :  '0.27 0.51 0.71',
            'tan'                    :  '0.82 0.71 0.55',
            'teal'                   :  '0.00 0.50 0.50',
            'thistle'                :  '0.85 0.75 0.85',
            'tomato'                 :  '1.00 0.39 0.28',
            'turquoise'              :  '0.25 0.88 0.82',
            'violet'                 :  '0.93 0.51 0.93',
            'wheat'                  :  '0.96 0.87 0.70',
            'white'                  :  '1.00 1.00 1.00',
            'whitesmoke'             :  '0.96 0.96 0.96',
            'yellow'                 :  '1.00 1.00 0.00',
            'yellowgreen'            :  '0.60 0.80 0.20',
        }
        return

    # Just get the color
    def get(self, color):
        if color not in self.color_list:
            print 'color %s not valid; returning 0 0 0'
            return '0 0 0'
        return self.color_list[color]

    # converts floating point value (from 0->1) to
    # proper RGB hex value (from 0x00 to 0xFF)
    def floatToRgb(self, value):
        outValue = int(float(value) * 255.0)
        if outValue < 16:
            return '0%x' % outValue
        else:
            return '%x' % outValue

    def getAsHex(self, color):
        if color[0] == '#':
            # assume this is hex value already; just return it
            return color
        tmp = color.split(',')
        if len(tmp) == 3:
            # this is just three rgb values, comma-separated
            r, g, b = tmp[0], tmp[1], tmp[2]
        else:
            # assume that it is a color name
            if color not in self.color_list:
                print 'color %s not valid; returning 0 0 0'
                r, g, b = 0.0, 0.0, 0.0
            else:
                r, g, b = self.color_list[color].split()
        return '#%s%s%s' % (self.floatToRgb(r),
                            self.floatToRgb(g),
                            self.floatToRgb(b))
# END: class color


#
# CLASS util
#
# Class util has a number of shared utility methods for use across
# all real canvas types; thus, each should inherit from here to use them.
#
class util:
    def __init__(self,
                 ):
        return

    #
    # convert()
    #
    # Used to convert from whatever into points
    #
    def convert(self, unitStr):
        u = unitStr.split('inches')
        if len(u) > 1:
            return float(u[0]) * 72.0
        u = unitStr.split('in')
        if len(u) > 1:
            return float(u[0]) * 72.0
        u = unitStr.split('i')
        if len(u) > 1:
            return float(u[0]) * 72.0
        return float(unitStr)

    #
    # stringWidth()
    #
    # This is a complete hack, and can be very wrong depending on the fontface
    # (which it should clearly be dependent upon). The problem, of course: only
    # the ps interpreter really knows how wide the string is: e.g., put the
    # string on the stack and call 'stringwidth'. But of course, we don't want
    # to have to invoke that to get the result (a pain). We could build in a
    # table that has all the answers for supported fonts (Helvetica, TimesRoman,
    # etc.) but that is a complete pain as well. So, for now, we just make a
    # rough guess based on the length of the string and the size of the font.
    # 
    def stringWidth(self, str, fontsize):
        length = len(str)
        total  = 0.0
        for i in range(0,length):
            c = str[i]
            if re.search(c, "ABCDEFGHJKLMNOPQRSTUVWXYZ234567890") != None:
                add = 0.69
            elif re.search(c, "abcdeghkmnopqrsuvwxyz1I") != None:
                add = 0.54
            elif re.search(c, ".fijlt") != None:
                add = 0.3
            elif re.search(c, "-") != None:
                add = 0.3
            else:
                # be conservative for all others
                add = 0.65
            total = total + add
        return (fontsize * total)

    #
    # shape()
    #
    # Use this to draw a shape on the plotting surface. Lots of possibilities,
    # including square, circle, triangle, utriangle, plusline, hline, vline,
    # hvline, xline, dline1, dline2, dline12, diamond, asterisk, ...
    #
    # Amazingly, this is all generic, just built on lines, boxes, circles, etc.
    # 
    def shape(self,
              style     = '',      # the possible shapes
              x         = '',      # x position of shape
              y         = '',      # y position of shape
              size      = 3.0,     # size of shape
              linecolor = 'black', # color of the line of the marker
              linewidth = 1.0,     # width of lines used to draw the marker
              linedash  = 0,       # dash pattern - 0 means no dashes
              fill      = False,   # for some shapes, filling makes sense;
                                   # if desired, mark this true
              fillcolor = 'black', # if filling, use this fill color
              fillstyle = 'solid', # if filling, which fill style to use
              fillsize  = 3.0,     #  size of object in pattern
              fillskip  = 4.0,     # space between object in pattern
              ):
        if style == 'square':
	    self.box(coord=[[x-size,y-size],[x+size,y+size]], 
                     linecolor=linecolor, linewidth=linewidth,  fill=fill,
                     fillcolor=fillcolor, fillstyle=fillstyle,
                     fillsize=fillsize, fillskip=fillskip) 
        elif style == 'circle':
	    self.circle(coord=[x,y], radius=size, linecolor=linecolor,
                        linewidth=linewidth, fill=fill, fillcolor=fillcolor,
                        fillstyle=fillstyle, fillsize=fillsize,
                        fillskip=fillskip) 
	elif style == 'triangle':
	    self.polygon(coord=[[x-size,y-size], [x,y+size], [x+size, y-size]],
                         linecolor=linecolor, linewidth=linewidth,
                         fill=fill, fillcolor=fillcolor, fillstyle=fillstyle,
                         fillsize=fillsize, fillskip=fillskip) 
	elif style == 'utriangle':
	    self.polygon(coord=[[x-size,y+size],[x,y-size],[x+size,y+size]],
                         linecolor=linecolor, linewidth=linewidth, fill=fill,
                         fillcolor=fillcolor, fillstyle=fillstyle,
                         fillsize=fillsize, fillskip=fillskip) 
	elif style == 'plusline':
	    self.line(coord=[[x-size,y],[x+size,y]], linecolor=linecolor,
                      linewidth=linewidth) 
	    self.line(coord=[[x,y+size],[x,y-size]], linecolor=linecolor,
                      linewidth=linewidth) 
	elif style == 'xline':
	    self.line(coord=[[x-size,y-size],[x+size,y+size]],
                      linecolor=linecolor, linewidth=linewidth) 
	    self.line(coord=[[x-size,y+size],[x+size,y-size]],
                      linecolor=linecolor, linewidth=linewidth) 
	elif style == 'dline1':
	    self.line(coord=[[x-size,y-size],[x+size,y+size]],
                      linecolor=linecolor, linewidth=linewidth) 
	elif style == 'dline2':
	    self.line(coord=[[x-size,y+size],[x+size,y-size]],
                      linecolor=linecolor, linewidth=linewidth) 
	elif style == 'dline12':
	    self.line(coord=[[x-size,y-size],[x+size,y+size]],
                      linecolor=linecolor, linewidth=linewidth) 
	    self.line(coord=[[x-size,y+size],[x+size,y-size]],
                      linecolor=linecolor, linewidth=linewidth) 
	elif style == 'hline': 
	    self.line(coord=[[x-size,y],[x+size,y]], linecolor=linecolor,
                      linewidth=linewidth, linedash=linedash)
	elif style == 'vline': 
	    self.line(coord=[[x,y+size],[x,y-size]], linecolor=linecolor,
                      linewidth=linewidth)
        elif style == 'hvline':
	    self.line(coord=[[x-size,y],[x+size,y]], linecolor=linecolor,
                      linewidth=linewidth) 
	    self.line(coord=[[x,y+size],[x,y-size]], linecolor=linecolor,
                      linewidth=linewidth)
	elif style == 'diamond':
	    self.polygon(coord=[[x-size,y],[x,y+size],[x+size,y],[x,y-size]], 
                         linecolor=linecolor, linewidth=linewidth, fill=fill,
                         fillcolor=fillcolor, fillstyle=fillstyle,
                         fillsize=fillsize, fillskip=fillskip) 
	elif style == 'star':
            s2 = size / 2.0
            xp  = s2 * math.cos(math.radians(18.0))
            yp  = s2 * math.sin(math.radians(18.0))
            xp2 = s2 * math.cos(math.radians(54.0))
            yp2 = s2 * math.sin(math.radians(54.0))
	    self.polygon(coord=[[x,y+s2],[x+xp2,y-yp2],[x-xp,y+yp],[x+xp,y+yp],
                                [x-xp2,y-yp2],[x,y+s2]],
                         linecolor=linecolor, linewidth=linewidth,
                         fill=fill, fillcolor=fillcolor, fillstyle=fillstyle,
                         fillsize=fillsize, fillskip=fillskip) 
        elif style == 'asterisk':
	    self.line(coord=[[x-size,y-size],[x+size,y+size]],
                      linecolor=linecolor, linewidth=linewidth) 
	    self.line(coord=[[x-size,y+size],[x+size,y-size]],
                      linecolor=linecolor, linewidth=linewidth)
            self.line(coord=[[x-size,y],[x+size,y]], linecolor=linecolor,
                      linewidth=linewidth) 
	    self.line(coord=[[x,y+size],[x,y-size]], linecolor=linecolor,
                      linewidth=linewidth)
        else:
            abort('bad choice of point style: ' + style)
        return
    # END: shape()

    #
    # utility routines for recording steps and then output'ing at end
    #

    # add a new command
    def out(self, outStr):
        self.commands.append(outStr)
        return

    # add a command to the previously added line
    def outnl(self, outStr):
        assert(len(self.commands) > 0)
        idx = len(self.commands) - 1
        self.commands[idx] = self.commands[idx] + outStr
        return

    # output the commands
    def dump(self, outfile):
        if outfile == 'stdout':
            for line in self.commands:
                print line
        else:
            fd = open(outfile, 'w')
            for line in self.commands:
                fd.write(line + '\n')
            fd.close()
        return
# END: canvas

#
# CLASS svg
#
# Use this to make an SVG drawing surface
#
class svg(util): 
    #
    # __init__()
    #
    def __init__(self, 
                 # name of the output file
                 title='default.svg',

                 # size of the drawing surface
                 dimensions=['3in','2in'],

                 # default font for text
                 font='Helvetica',

                 # whether to add more info into output file
                 verbose=False,

                 # name of the file calling into zplot;
                 # recorded in header of output file
                 script=__file__,
                 ):
        self.comments = ''
        self.commands = []
        
        self.program = 'zplot'
        self.version = 'python version 1.0'

        # SHOULD INCLUDE SOME INFO IN HEADER (in html comment form)
        self.__comment('Creator: %s version %s script: %s host: %s' % \
                 (self.program, self.version, os.path.abspath(script),
                  socket.gethostname()))

        self.default = font
        self.verbose = verbose

        self.date    = str(time.strftime('%X %x %Z'))
        self.title   = title

        if len(dimensions) != 2:
            print 'bad dimensions (should have two elements):', dimensions
            return
        self.width  = self.convert(str(dimensions[0]))
        self.height = self.convert(str(dimensions[1]))

        self.colors = color()

        #
        # init svg output header
        #
        # This is taken from http://tutorials.jenkov.com/svg
        #
        self.out('<svg xmlns="http://www.w3.org/2000/svg"\n' + \
                 'xmlns:xlink="http://www.w3.org/1999/xlink">')
        return

    # 
    # render()
    # 
    # Use this routine to print out all the postscript commands you've been
    # queueing up to a file or 'stdout' (default).
    # 
    def render(self):
        self.out('</svg>')
        self.dump(self.title)
        return

    #
    # line()
    #
    # Use this to draw a line on the canvas.
    # 
    def line(self,
             coord           = [[0,0],[0,0]],
             linecolor       = 'black',
             linewidth       = 1,
             linejoin        = 0,
             linecap         = 0,
             linedash        = 0,
             closepath       = False,
             arrow           = False,
             arrowheadlength = 4,
             arrowheadwidth  = 3,
             arrowlinecolor  = 'black',
             arrowlinewidth  = 0.5,
             arrowfill       = True,
             arrowfillcolor  = 'black', 
             arrowstyle      = 'normal'
            ):
        # ARROW NOT IMPLEMENTED (YET)
        assert(arrow == False)
        assert(linecap == 0)
        assert(closepath == False)
        
        linecolor = self.__getcolor(linecolor)
        point = coord[0]
        self.__startpath()
        self.__moveto(point[0], point[1])
        for i in range(1, len(coord)):
            point = coord[i]
            self.__lineto(point[0], point[1])
        self.__endpoints()
        self.__startstyle()
        self.outnl('stroke="%s" ' % linecolor)
        self.outnl('stroke-width="%.2fpx" ' % linewidth)
        if linedash != 0:
            self.outnl('stroke-dasharray="%s" ' % \
                                self.__getdash(linedash))
            
        self.outnl('fill="none"')
        self.__endstyle()
        self.__endpath()
        return
        # END: line()

    # 
    # INTERNAL HELPER FUNCTIONS
    #

    def __comment(self, msg):
        self.out('<!--')
        self.outnl(msg)
        self.outnl('-->')

    def __startpath(self):
        self.out('<path d="')
        return

    def __endpath(self):
        self.outnl('></path>')
        return

    def __endpoints(self):
        self.outnl('"')
        return

    def __startstyle(self):
        self.outnl(' ')
        return
    
    def __endstyle(self):
        return
    
    def __moveto(self, p1, p2):
        self.outnl('M %.2f,%.2f ' % (p1, self.__converty(p2)))
        return

    def __lineto(self, p1, p2):
        self.outnl('L %.2f,%.2f ' % (p1, self.__converty(p2)))
        return

    def __converty(self, y):
        return self.height - y

    def __getcolor(self, value):
        return self.colors.getAsHex(value)

    def __getdash(self, linedash):
        outdash = ''
        for e in linedash:
            if outdash == '':
                outdash = str(e)
            else:
                outdash = outdash + ',' + str(e)
        return outdash
        
    # text()
    # 
    # Use this routine to place text on the canvas. Most options are obvious
    # (the expected coordinate pair, color, text, font, size - the size of the
    # font, rotation - which way the text should be rotated, but the anchor can
    # be a bit confusing. Basically, the anchor determines where, relative to
    # the coordinate pair (x,y), the text should be placed. Simple anchoring
    # includes left (l), center (c), or right (r), which determines whether the
    # text starts at the x position specified (left), ends at x (right), or is
    # centered on the x (center). Adding a second anchor (xanchor,yanchor)
    # specifies a y position anchoring as well. The three options there are low
    # (l), which is the default if none is specified, high (h), and middle (m),
    # again all determining the placement of the text relative to the y
    # coordinate specified.
    # 
    def text(self,
             coord    = [0,0],
             text     = 'text',
             font     = 'default',
             color    = 'black',
             size     = 16,
             rotate   = 0,
             anchor   = 'c',
             bgcolor  = '',
             bgborder = 1,
             ):
        color = self.__getcolor(color)
        if font == 'default':
            font = 'Helvetica'

        tmp = anchor.split(',')
        # first can be l,c,r   left,center,right
        # second can be l,c,h  low,center,high
        if len(tmp) == 1:
            left = anchor
            right = 'c'
        elif len(tmp) == 2:
            left = tmp[0]
            right = tmp[1]
        else:
            abort('bad anchor ' + anchor)

        if left == 'c':
            anchor = 'middle'
        elif left == 'l':
            anchor = 'start'
        elif left == 'r':
            anchor = 'end'
        else:
            abort('bad anchor ' + anchor)

        if right == 'l':
            yshift = 0
        elif right == 'c':
            # XXX hackish adjustment of text height: +2
            yshift = -size/2.0 + 2
        elif right == 'h':
            # XXX hackish adjustment of text height: +2
            yshift = -size + 2
        else:
            abort('bad anchor ' + anchor)

        x, y = coord[0], self.__converty(coord[1] + yshift)
        self.out('<text x="%.2f" y="%.2f" ' % (x, y))
        if rotate != 0:
            self.outnl('transform="rotate(%.2f %.2f,%.2f)" ' %
                                (float(-rotate), x, y))
        self.outnl('style="')
        self.outnl('font-family: %s; ' % font)
        self.outnl('font-size: %d; ' % size)
        self.outnl('fill: %s; ' % color)
        self.outnl('text-anchor: %s; ' % anchor)
        self.outnl('"> ')
        self.outnl(text)
        self.outnl('</text>')
            
        return

    # 
    # box()
    #
    # Makes a box at coords specifying the bottom-left and upper-right corners
    # Options:
    # - Can change the surrounding line (linewidth=0 removes it)
    # - Can fill with solid or pattern
    # When filling with non-solid pattern, can add a background color so
    # as not to be see-through.
    # 
    def box(self,
            coord       = [[0,0],[0,0]],
            linecolor   = 'black',
            linewidth   = 1,
            linedash    = 0,
            linecap     = 0,
            fill        = False,
            fillcolor   = 'black',
            fillstyle   = 'solid',
            fillsize    = 3,
            fillskip    = 4,
            rotate      = 0,
            bgcolor     = '',
            ):
        # DOES NOT YET SUPPORT OTHER FILLS
        assert(fillstyle == 'solid')
        
        x1, y1 = coord[0][0], self.__converty(coord[0][1])
        x2, y2 = coord[1][0], self.__converty(coord[1][1])
        if x1 > x2:
            x = x2
            w = x1 - x2
        else:
            x = x1
            w = x2 - x1
        if y1 > y2:
            y = y2
            h = y1 - y2
        else:
            y = y1
            h = y2 - y1
        self.out('<rect x="%.2f" y="%.2f" ' % (x, y))
        self.outnl('height="%.2f" width="%.2f" ' % (h, w))
        if linewidth > 0:
            self.outnl('stroke="%s" ' % self.__getcolor(linecolor))
            self.outnl('stroke-width="%s" ' % linewidth)
        if linedash != 0:
            self.outnl('stroke-dasharray="%s" ' % self.__getdash(linedash))
        if fill:
            self.outnl('fill="%s" ' % fillcolor)
        self.outnl('></rect>')
        return


    #
    # arc()
    #
    # Can make circles, or partial circles (arcs), with this.
    #
    def arc(self,
            coord     = [],
            angle     = [0.0,360.0],
            radius    = 1,
            linecolor = 'black',
            linewidth = 1,
            linedash  = 0,
            ):
        # DOES NOT WORK NOW
        assert(0 == 1)
        return

    # circle()
    #
    # Can just make circles with this. Filled or not.
    #
    def circle(self,
               coord     = [0,0],
               radius    = 1,
               scale     = [1,1],
               linecolor = 'black',
               linewidth = 1,
               linedash  = 0,
               fill      = False,
               fillcolor = 'black',
               fillstyle = 'solid',
               fillsize  = 3,
               fillskip  = 4,
               bgcolor   = ''
               ):
        # DOES NOT YET SUPPORT OTHER FILL STYLES
        assert(fillstyle == 'solid')
        x, y = coord[0], self.__converty(coord[1])
        self.out('<circle cx="%.2f" cy="%.2f" r="%.2f" ' % (x, y, radius))
        self.outnl('stroke="%s" ' % self.__getcolor(linecolor))
        self.outnl('stroke-width="%s" ' % linewidth)
        if linedash != 0:
            self.outnl('stroke-dasharray="%s" ' % self.__getdash(linedash))
        if fill:
            self.outnl('fill="%s" ' % fillcolor)
        self.outnl('></circle>')
        return
    # END: circle

    #
    # polygon()
    #
    def polygon(self,
                coord      = [],
                linecolor  = 'black',
                linewidth  = 1,
                linecap    = 0,
                linedash   = 0,
                fill       = False,
                fillcolor  = 'black',
                fillstyle  = 'solid',
                fillsize   = 3,
                fillskip   = 4,
                bgcolor    = '',
                ):
        abort('POLYGON not implemented in SVG yet')
        return
    # END: polygon


# END: class svg

#
# CLASS postscript
# 
# use this to make a postscript drawing surface
#
class postscript(util):
    def comment(self, comments):
        self.comments += comments

    def __addfont(self, font):
        if font == 'default':
            font = self.default
        
        found = 0
        for efont in self.allfonts:
            if font == efont:
                found = 1
                break
        if found == 0:
            abort('Bad font: ' + font)

        if self.fontlist.count(font) == 0:
            self.fontlist.append(font)
            
    def __setfont(self, face, size):
        if face == 'default':
            face = self.default
        self.out('(' + face + ') findfont ' + str(size) +
                 ' scalefont setfont')

    def __gsave(self):
        self.out('gs')
        self.gsaveCnt = self.gsaveCnt + 1
        
    def __grestore(self):
        self.out('gr')
        self.grestoreCnt = self.grestoreCnt + 1

    def __newpath(self):
        self.out('np')

    def __moveto(self, p1, p2):
        self.out(str(float(p1)) + ' ' + str(float(p2)) + ' m')

    def __rmoveto(self, p1, p2):
        self.out(str(float(p1)) + ' ' + str(float(p2)) + ' mr')

    def __lineto(self, p1, p2):
        self.out(str(float(p1)) + ' ' + str(float(p2)) + ' l')

    def __rlineto(self, p1, p2):
        self.out(str(float(p1)) + ' ' + str(float(p2)) + ' lr')

    def __rotate(self, angle):
        self.out(str(angle) + ' rotate')
        
    def __show(self, text, anchor):
        if anchor == 'c':
            self.out('('+text+') cshow')
	elif anchor == 'l':
            self.out('('+text+') lshow')
        elif anchor == 'r':
            self.out('('+text+') rshow')
        else:
	    abort('bad anchor: ' + anchor)

    def __closepath(self):
        self.out('cp')

    def __setcolor(self, value):
        tmp = value.split(',')
        if len(tmp) > 1:
            c = '%s %s %s' % (tmp[0], tmp[1], tmp[2])
        else:
            c = self.colors.get(value)
        self.out(c + ' sc')
        return

    def __setlinewidth(self, linewidth):
        self.out(str(float(linewidth)) + ' slw')

    def __setlinecap(self, linecap):
        self.out(str(float(linecap)) + ' slc')

    def __setlinejoin(self, linejoin):
        self.out(str(float(linejoin)) + ' slj')

    def __setlinedash(self, linedash):
        self.out('[ ')
        for seg in linedash:
            self.outnl(str(seg) + ' ')
        self.outnl('] 0 sd')

    def __fill(self):
        self.out('fl')

    def __rectangle(self, x1, y1, x2, y2):
        self.__moveto(x1, y1)
        self.__lineto(x1, y2)
        self.__lineto(x2, y2)
        self.__lineto(x2, y1)

    def __scale(self, x, y):
        self.out(str(x) + ' ' + str(y) + ' scale')

    def __arc(self, x, y, radius, start, end):
        self.out(str(x) + ' ' + str(y) + ' ' + str(radius) + ' ' + \
                   str(start) + ' ' + str(end) + ' arc')

    def __clip(self):
        self.out('clip')

    def __clipbox(self, x1, y1, x2, y2):
        self.__newpath()
        self.__rectangle(x1, y1, x2, y2)
        self.__closepath()
        self.__clip()

    # Use this to fill a rectangular region with one of many specified patterns
    def __makepattern(self,
                      coord     = [],
                      fillcolor = 'black',
                      fillstyle = 'solid',
                      fillsize  = 3,
                      fillskip  = 4,
                      ):

        # bound box
        assert(len(coord) == 2)
        assert(len(coord[0]) == 2)
        assert(len(coord[1]) == 2)
        x1 = float(coord[0][0])
        y1 = float(coord[0][1])
        x2 = float(coord[1][0])
        y2 = float(coord[1][1])

        fillsize = float(fillsize)
        fillskip = float(fillskip)

        if fillstyle == 'solid':
            self.__newpath()
            self.__rectangle(x1, y1, x2, y2)
	    self.__closepath()
	    self.__setcolor(fillcolor)
	    self.__fill()
            return
            
        # XXX - needs to update these values
        # self.__makeboxbigger(x1, y1, x2, y2, 10.0)
        delta = 10
        if x2 > x1:
            x1 = x1 - delta
            x2 = x2 + delta
        else:
            nx1 = x2 - delta
            nx2 = x1 + delta
            x1  = nx1
            x2  = nx2

        if y2 > y1:
            y1 = y1 - delta
            y2 = y2 + delta
        else:
            ny1 = y2 - delta
            ny2 = y1 + delta
            y1  = ny1
            y2  = ny2

        # this is done for all except the solid ...
        self.__setcolor(fillcolor)
        styleList = ''

        if fillstyle == 'hline':
            styleList += 'hline '
	    self.__setlinewidth(fillsize)
            cy = y1
            while cy <= y2:
		self.__newpath()
		self.__rectangle(x1, cy, x2, cy + fillsize)
		self.__closepath()
		self.__fill()
		self.__stroke()
                cy = cy + fillsize + fillskip
	elif fillstyle == 'vline':
            styleList += 'vline '
	    self.__setlinewidth(fillsize)
            cx = x1
            while cx <= x2:
		self.__newpath()
		self.__moveto(cx, y1)
		self.__lineto(cx, y2)
		self.__stroke()
                cx = cx + fillsize + fillskip
        elif fillstyle == 'hvline':
            styleList += 'hvline '
	    self.__setlinewidth(fillsize)
            cy = y1
            while cy <= y2:
		self.__newpath()
		self.__rectangle(x1, cy, x2, cy + fillsize)
		self.__closepath()
		self.__fill()
		self.__stroke()
                cy = cy + fillsize + fillskip
            cx = x1
            while cx <= x2:
		self.__newpath()
		self.__moveto(cx, y1)
		self.__lineto(cx, y2)
		self.__stroke()
                cx = cx + fillsize + fillskip
	elif fillstyle == 'dline1':
            styleList += 'dline1 '
	    self.__setlinewidth(fillsize)
            cy = y1
            while cy <= y2:
		self.__newpath()
		self.__moveto(x1, cy)
		self.__lineto(x2, (x2-x1)+cy)
		self.__stroke()
                cy = cy + fillskip + fillsize
            cx = x1
            while cx <= x2:
		self.__newpath()
		self.__moveto(cx, y1)
		self.__lineto(cx+(y2-y1), y2)
		self.__stroke()
                cx = cx + fillskip + fillsize
	elif fillstyle == 'dline2':
            styleList += 'dline2 '
	    self.__setlinewidth(fillsize)
            cy = y1
            while cy <= y2:
		self.__newpath()
		self.__moveto(x2, cy)
		self.__lineto(x1, (x2-x1)+cy)
		self.__stroke()
                cy = cy + fillskip + fillsize
            cx = x2
            while cx >= x1:
		self.__newpath()
		self.__moveto(cx, y1)
		self.__lineto(cx-(y2-y1), y2)
		self.__stroke()
                cx = cx - (fillskip + fillsize)
	elif fillstyle == 'dline12':
            styleList += 'dline12 '
	    self.__setlinewidth(fillsize)
            cy = y1
            while cy <= y2:
		self.__newpath()
		self.__moveto(x1, cy)
		self.__lineto(x2, (x2-x1)+cy)
		self.__stroke()
                cy = cy + fillskip + fillsize
            cx = x1
            while cx <= x2:
		self.__newpath()
		self.__moveto(cx, y1)
		self.__lineto(cx+(y2-y1), y2)
		self.__stroke()
                cx = cx + fillskip + fillsize
            cy = y1
            while cy <= y2:
		self.__newpath()
		self.__moveto(x2, cy)
		self.__lineto(x1, (x2-x1)+cy)
		self.__stroke()
                cy = cy + fillskip + fillsize
            cx = x2
            while cx >= x1:
		self.__newpath()
		self.__moveto(cx, y1)
		self.__lineto(cx-(y2-y1), y2)
		self.__stroke()
                cx = cx - (fillskip + fillsize)
	elif fillstyle == 'circle':
            styleList += 'circle '
            cx = x1
            while cx <= x2:
                cy = y1
                while cy <= y2:
                    self.__newpath()
		    self.__arc(cx, cy, fillsize, 0, 360)
		    self.__fill()
		    self.__stroke()
                    cy = cy + fillskip + fillsize
                cx = cx + fillsize + fillskip
	elif fillstyle == 'square':
            styleList += 'square '
            cx = x1
            while cx <= x2:
                cy = y1
                while cy <= y2:
		    self.__newpath()
		    self.__rectangle(cx, cy, cx+fillsize, cy+fillsize)
		    self.__fill()
		    self.__stroke()
                    cy = cy + fillskip + fillsize
                cx = cx + fillsize + fillskip
	elif fillstyle == 'triangle':
            styleList += 'triangle '
            cx = x1
            while cx <= x2:
                cy = y1
                while cy <= y2:
		    self.__newpath()
		    self.__moveto(cx-fillsize/2.0, cy)
		    self.__lineto(cx+fillsize/2.0, cy)
		    self.__lineto(cx, cy+fillsize)
		    self.__closepath()
		    self.__fill()
		    self.__stroke()
                    cy = cy + fillskip + fillsize
                cx = cx + fillsize + fillskip
        elif fillstyle == 'utriangle':
            styleList += 'utriangle '
            cx = x1
            while cx <= x2:
                cy = y1
                while cy <= y2:
		    self.__newpath()
		    self.__moveto(cx-fillsize/2.0, cy+fillsize)
		    self.__lineto(cx+fillsize/2.0, cy+fillsize)
		    self.__lineto(cx, cy)
		    self.__closepath()
		    self.__fill()
		    self.__stroke()
                    cy = cy + fillsize + fillsize
                cx = cx + fillsize + fillskip
	else:
            print 'Bad fill style: ', fillstyle
	    abort('Should be one of %s' % styleList)
        # END: makepattern()

    def raw(self,
            str):
        self.out(str)

    def __stroke(self):
        self.out('st')

    #
    # __init__ routine
    # 
    # initialize everything for this particular canvas
    # (one drawing surface per PS canvas, saved to exactly one file, of course)
    # 
    def __init__(self,
                 # name of the output file
                 title='default.eps',

                 # size of the drawing surface
                 dimensions=['3in','2in'],

                 # default font for text
                 font='Helvetica',
                 
                 # whether to add more info into output file
                 verbose=False,

                 # name of the file calling into zplot;
                 # recorded in header of output file
                 script=__file__,
                 ):
        self.comments = ''
        self.commands = []
        
        self.program = 'zplot'
        self.version = 'python version 1.0'
        self.default = font

        self.date    = str(time.strftime('%X %x %Z'))

        # fonts in this document
        self.fontlist = []
        self.fontlist.append(self.default)

        # list of all fonts 
        self.allfonts = ['Helvetica', 'Helvetica-Bold', 'Helvetica-Italic',
                         'TimesRoman', 'TimesRoman-Bold', 'TimesRoman-Italic',
                         'Courier', 'Courier-Bold', 'Courier-Italic',
                         'URWPalladioL-Roma', 'ICQPMD+NimbusSanL-Regu']
        
        self.gsaveCnt    = 0
        self.grestoreCnt = 0

        self.colors = color()

        self.title = title
        # print 'generating %s' % title
        
        assert(len(dimensions) == 2)
        self.width  = self.convert(str(dimensions[0]))
        self.height = self.convert(str(dimensions[1]))

        # generic eps header
        self.out('%!PS-Adobe-2.0 EPSF-2.0')
        self.out('%%Title: ' + str(self.title))
        self.out('%%Creator: '+ str(self.program) + ' version:' + \
                 str(self.version) + ' script:' + os.path.abspath(script) + \
                 ' host:'+socket.gethostname())
        self.out('%%CreationDate: ' + str(self.date))
        self.out('%%DocumentFonts: (atend)')
        self.out('%%BoundingBox: 0 0 ' + str(self.width) + ' ' + \
                 str(self.height))
        self.out('%%Orientation: Portrait')
        self.out('%%EndComments')

        # zdraw dictionary
        self.out('% zdraw dictionary')
        self.out('/zdict 256 dict def')
        self.out('zdict begin')
        self.out('/cpx 0 def')
        self.out('/cpy 0 def')
        self.out('/recordcp {currentpoint /cpy exch def /cpx exch def} bind def')
        self.out('/m {moveto} bind def')
        self.out('/l {lineto} bind def')
        self.out('/mr {rmoveto} bind def')
        self.out('/lr {rlineto} bind def')
        self.out('/np {newpath} bind def')
        self.out('/cp {closepath} bind def')
        self.out('/st {stroke} bind def')
        self.out('/fl {fill} bind def')
        self.out('/gs {gsave} bind def')
        self.out('/gr {grestore} bind def')
        self.out('/slw {setlinewidth} bind def')
        self.out('/slc {setlinecap} bind def')
        self.out('/slj {setlinejoin} bind def')
        self.out('/sc  {setrgbcolor} bind def')
        self.out('/sd  {setdash} bind def')
        # XXX -- triangle not implemented (yet) -- expects x y size on stack
        # self.out('/triangle {pop pop pop} bind def')  
        self.out('/lshow {show recordcp} def')
        self.out('/rshow {dup stringwidth pop neg 0 mr show recordcp} def')
        self.out('/cshow {dup stringwidth pop -2 div 0 mr show recordcp} def')
        self.out('end')
        self.out('zdict begin')

        # END: __init

    # 
    # render()
    # 
    # Use this routine to print out all the postscript commands you've been
    # queueing up to a file or 'stdout' (default).
    # 
    def render(self):
        # do some checks
        if self.gsaveCnt != self.grestoreCnt:
            print self.gsaveCnt
            print self.grestoreCnt
            print 'INTERNAL ERROR: gsavecnt != grestorecnt (bad ps possible)'
            exit(1)

        # generic eps trailer
        for ln in self.comments.split('\n'):
            self.out('% '+ln)
        self.out('% zdraw epilogue')
        self.out('end')
        self.out('showpage')
        self.out('%%Trailer')

        # make font list
        flist = self.fontlist[0]
        for i in range(1,len(self.fontlist)):
            flist = flist + ' ' + self.fontlist[i]
        self.out('%%DocumentFonts: ' + flist)

        self.dump(self.title)
        # END: render()

    # 
    #
    # line()
    #
    # Use this to draw a line on the canvas.
    # 
    def line(self,
             coord           = [[0,0],[0,0]],
             linecolor       = 'black',
             linewidth       = 1,
             linejoin        = 0,
             linecap         = 0,
             linedash        = 0,
             closepath       = False,
             arrow           = False,
             arrowheadlength = 4,
             arrowheadwidth  = 3,
             arrowlinecolor  = 'black',
             arrowlinewidth  = 0.5,
             arrowfill       = True,
             arrowfillcolor  = 'black', 
             arrowstyle      = 'normal'
            ):

        # save the context to begin
        self.__gsave()

        # first, draw the line, one component at a time
        self.__newpath()
        point = coord[0]
        self.__moveto(point[0], point[1])
        for i in range(1, len(coord)):
            point = coord[i]
            self.__lineto(point[0], point[1])

        # now check for optional other things ...
        if closepath == True:
            self.__closepath()
        if linecolor != 'black':
            self.__setcolor(linecolor)
        if linewidth != 1:
            self.__setlinewidth(linewidth)
        if linecap != 0:
            self.__setlinecap(linecap)
        if linejoin != 0:
            self.__setlinejoin(linejoin)
        if linedash != 0:
            self.__setlinedash(linedash)

        # all done, so stroke and restore
        self.__stroke()

        # ARROW?
        # now, do the arrow 
        if arrow == True:
            count = len(coord)
            sx = coord[count-2][0]
            sy = coord[count-2][1]
            ex = coord[count-1][0]
            ey = coord[count-1][1]
            # use the last line segment to compute the orthogonal vectors
            vx = ex - sx
            vy = ey - sy
            hypot = math.hypot(vx,vy)
            # get angle of last line segment
            svx = vx / hypot
            svy = vy / hypot

            if svx > 0 and svy >= 0:
                angle = math.atan(abs(svy)/abs(svx))
            elif svx > 0 and svy < 0:
                angle = math.radians(360.0) - math.atan(abs(svy)/abs(svx))
            elif svx < 0 and svy >= 0:
                angle = math.radians(180.0) - math.atan(abs(svy)/abs(svx))
            elif svx < 0 and svy < 0:
                angle = math.radians(180.0) + math.atan(abs(svy)/abs(svx))
            elif svx == 0 and svy < 0:
                angle = math.radians(270.0)
            elif svx == 0 and svy > 0:
                angle = math.radians(90.0)
            else:
                abort('arrow feature clearly broken')

            angle = math.degrees(angle)

            aw = arrowheadwidth/2.0
            al = arrowheadlength

            for i in range(0,2):
                self.__gsave()
                self.__newpath()
                self.__moveto(ex, ey)
                self.__rotate(angle)
                self.__rlineto(0, aw)
                self.__rlineto(al, -aw)
                self.__rlineto(-al, -aw)
                self.__closepath()
                if i == 1:
                    self.__setcolor(arrowlinecolor)
                    self.__setlinewidth(arrowlinewidth)
                    self.__stroke()
                else:
                    self.__setcolor(arrowfillcolor)
                    self.__fill()
                self.__grestore()

        self.__grestore()
        return
        # END: line()

    # 
    # text()
    # 
    # Use this routine to place text on the canvas. Most options are obvious
    # (the expected coordinate pair, color, text, font, size - the size of the
    # font, rotation - which way the text should be rotated, but the anchor can
    # be a bit confusing. Basically, the anchor determines where, relative to
    # the coordinate pair (x,y), the text should be placed. Simple anchoring
    # includes left (l), center (c), or right (r), which determines whether the
    # text starts at the x position specified (left), ends at x (right), or is
    # centered on the x (center). Adding a second anchor (xanchor,yanchor)
    # specifies a y position anchoring as well. The three options there are low
    # (l), which is the default if none is specified, high (h), and middle (m),
    # again all determining the placement of the text relative to the y
    # coordinate specified.
    # 
    def text(self,
             coord    = [0,0],
             text     = 'text',
             font     = 'default',
             color    = 'black',
             size     = 10,
             rotate   = 0,
             anchor   = 'c',
             bgcolor  = '',
             bgborder = 1,
             ):

        self.__addfont(font)

        assert (len(coord) == 2)
        x = float(coord[0])
        y = float(coord[1])

        a = anchor.split(',')
        if len(a) == 1:
            # just one anchor, assume it is the x anchor
            xanchor = a[0]
            yanchor = 'l'
        elif len(a) == 2:
            # two anchors
            xanchor = a[0]
            yanchor = a[1]
        else:
            abort('Bad anchor: ' + str(anchor))

        self.__gsave()

        # XXX - this is just a bit ugly and messy, sorry postscript
        if bgcolor != '':
            self.__newpath()
            self.__setcolor(bgcolor)
            self.__setfont(font, size)
            self.__moveto(x, y)
            if rotate != 0:
                self.__gsave()
                self.__rotate(rotate)
            # now, adjust based on yanchor
            if yanchor == 'c':
                self.__rmoveto(0, -0.36 * size)
            elif yanchor == 'h':
                self.__rmoveto(0, -0.72 * size) 

            # now, adjust based on xanchor
            if xanchor == 'l':
                self.out('('+ text +') stringwidth pop dup')
            elif xanchor == 'c':
                self.out('('+ text +') stringwidth pop dup -2 div 0 ' + \
                           'rmoveto dup')
            elif xanchor == 'r':
                self.out('('+ text +') stringwidth pop dup -1 div 0 ' + \
                           'rmoveto dup')
            else:
                abort('xanchor should be: l, c, or r')

            # now get width of string and draw the box
            # move to left-bottom including borders
            self.out('-' + str(bgborder) + ' -' + str(bgborder) + ' rmoveto')
            # add border*2 to the width (on the stack) and move over
            self.out(str(2 * bgborder) + ' add 0 rlineto')
            # move a line up by the height of characters + border
            self.out('0 ' + str((0.72 * size) + (2 * bgborder)) + ' rlineto')
            # move back down and closepath to finish
            self.out('neg ' + str(-2 * bgborder) + ' add 0 rlineto')
            self.__closepath()
            self.__fill()
            if rotate != 0:
                self.__grestore()
        # END: if bgcolor != '':

        # now, just draw the text
        self.__newpath()
        self.__setcolor(color)
	self.__setfont(font, size)
        self.__moveto(x, y)
        if rotate != 0:
            self.__gsave()
            self.__rotate(rotate)

        # 0.36: a magic adjustment to center text in y direction. Based on years
        # of postscript experience, only change if you actually know something
        # about how this works, unlike me. BTW: if just 'l', do nothing ...
        if yanchor == 'c':
            self.__rmoveto(0, -0.36 * float(size))
        elif yanchor == 'h':
            self.__rmoveto(0, -0.72 * float(size))
        elif yanchor == 'l':
            nop = 0
        else:
            abort('yanchor should be: l, c, or h')

        # TODO: missing text feature.
        # Need to mark parens specially in postscript (as they are normally
        # used to mark strings).
        # Something like this?
        #   set text [string map { ( \\( ) \\) } $use(text)]
        # For now, user can deal with it themselves.
        self.__show(str(text),xanchor)
        if rotate != 0:
            self.__grestore()
        self.__stroke()
        self.__grestore()
        return
        # END: text()

    # 
    # box()
    #
    # Makes a box at coords specifying the bottom-left and upper-right corners
    # Options:
    # - Can change the surrounding line (linewidth=0 removes it)
    # - Can fill with solid or pattern
    # When filling with non-solid pattern, can add a background color so
    # as not to be see-through.
    # 
    def box(self,
            coord       = [[0,0],[0,0]],
            linecolor   = 'black',
            linewidth   = 1,
            linedash    = 0,
            linecap     = 0,
            fill        = False,
            fillcolor   = 'black',
            fillstyle   = 'solid',
            fillsize    = 3,
            fillskip    = 4,
            rotate      = 0,
            bgcolor     = '',
            ):

        # pull out each element of the path
        assert(len(coord) == 2)
        x1 = float(coord[0][0])
        y1 = float(coord[0][1])
        x2 = float(coord[1][0])
        y2 = float(coord[1][1])

        # the code assumes y2 is bigger than y1, so switch them if need be
        if y1 > y2:
            tmp = y2
            y2 = y1
            y1 = tmp

        # if the background should be filled, do that here
        if bgcolor != '':
            self.__gsave()
            self.__makepattern(coord=[[x1,y1],[x2,y2]], fillcolor=bgcolor,
                               fillstyle='solid')
            self.__grestore()

        # do filled one first
        if fill == True:
            self.__gsave()
            self.__clipbox(x1, y1, x2, y2)
            self.__makepattern(coord=[[x1,y1],[x2,y2]], fillcolor=fillcolor,
                               fillstyle=fillstyle, fillsize=fillsize,
                               fillskip=fillskip)
            self.__grestore()

        # draw outline box
        if float(linewidth) > 0.0:
            self.__gsave()
            self.__newpath()
            self.__rectangle(x1, y1, x2, y2)
            self.__closepath()
            self.__setcolor(linecolor)
            self.__setlinewidth(linewidth)
            if linedash != 0:
                self.__setlinedash(linedash)
            if linecap != 0:
                self.__setlinecap(linecap)
            self.__stroke()
            self.__grestore()
        return
        # END: box()

    # 
    # box3()
    #
    # Makes a box at coords specifying the bottom-left and upper-right corners
    # Options:
    # - Can change the surrounding line (linewidth=0 removes it)
    # - Can fill with solid or pattern
    # When filling with non-solid pattern, can add a background color so
    # as not to be see-through.
    # 
    def box3(self,
             coord       = [0,0],
             xwidth      = 10,
             ywidth      = 10,
             center      = 'l,l',
             linecolor   = 'black',
             linewidth   = 1,
             linedash    = 0,
             linecap     = 0,
             fill        = False,
             fillcolor   = 'black',
             fillstyle   = 'solid',
             fillsize    = 3,
             fillskip    = 4,
             rotate      = 0,
             bgcolor     = '',
            ):

        # pull out each element of the path
        assert(len(coord) == 2)
        x1 = float(coord[0])
        y1 = float(coord[1])
        x2 = x1 + (xwidth * math.cos(math.radians(rotate)))
        y2 = y1 + (xwidth * math.sin(math.radians(rotate)))
        x3 = x2 - (ywidth * math.cos(math.radians(90.0 - rotate)))
        y3 = y2 + (ywidth * math.sin(math.radians(90.0 - rotate)))
        x4 = x1 - (ywidth * math.cos(math.radians(90.0 - rotate)))
        y4 = y1 + (ywidth * math.sin(math.radians(90.0 - rotate)))
        self.polygon(coord=[[x1,y1],[x2,y2],[x3,y3],[x4,y4]],
                     linecolor=linecolor, linewidth=linewidth,
                     linedash=linedash, linecap=linecap, fill=fill,
                     fillcolor=fillcolor, fillstyle=fillstyle,
                     fillsize=fillsize, fillskip=fillskip)
        return
    # END: box3()

    #
    # arc()
    #
    # Can make circles, or partial circles (arcs), with this.
    #
    def arc(self,
            coord     = [],
            angle     = [0.0,360.0],
            radius    = 1,
            linecolor = 'black',
            linewidth = 1,
            linedash  = 0,
            ):
        
        # pull out each element of the path
        assert(len(angle) == 2)
        assert(len(coord) == 2)
        x = float(coord[0])
        y = float(coord[1])
        radius = float(radius)

        self.__gsave()
        self.__newpath()
        self.__arc(x, y, radius, angle[0], angle[1])
        self.__setcolor(linecolor)
        self.__setlinewidth(linewidth)
        if linedash != 0:
            self.__setlinedash(linedash)
        self.__stroke()
        self.__grestore()
        return
    # END: arc

    #
    # circle()
    #
    # Can just make circles with this. Filled or not.
    #
    def circle(self,
               coord     = [0,0],
               radius    = 1,
               scale     = [1,1],
               linecolor = 'black',
               linewidth = 1,
               linedash  = 0,
               fill      = False,
               fillcolor = 'black',
               fillstyle = 'solid',
               fillsize  = 3,
               fillskip  = 4,
               bgcolor   = ''
               ):
        # pull out each element of the path
        assert(len(coord) == 2)
        x = float(coord[0])
        y = float(coord[1])
        radius = float(radius)

        doScale = False
        if scale[0] != 1:
            x = x / scale[0]
            doScale = True
        if scale[1] != 1:
            y = y / scale[1]
            doScale = True

        # if the background should be filled, do that here
        if bgcolor != '':
            self.__gsave()
            self.__newpath()
            if doScale == True:
                self.__scale(scale[0],scale[1])
            self.__arc(x, y, radius, 0, 360)
            self.__setcolor(bgcolor)
            self.__fill()
            self.__grestore()

        # do fill first
        if fill == True:
            self.__gsave()
            self.__newpath()
            if doScale == True:
                self.__scale(scale[0],scale[1])
            self.__arc(x, y, radius, 0, 360)
            self.__closepath()
            self.__clip()
            r = float(radius)
            self.__makepattern(coord=[[x-radius,y-radius],[x+radius,y+radius]],
                               fillcolor=fillcolor, fillstyle=fillstyle,
                               fillsize=fillsize, fillskip=fillskip)
            self.__grestore()

        # make the circle outline now
        if linewidth > 0.0:
            self.__gsave()
            self.__newpath()
            if doScale == True:
                self.__scale(scale[0],scale[1])
            self.__arc(x, y, radius, 0, 360)
            self.__setcolor(linecolor)
            self.__setlinewidth(linewidth)
            if linedash != 0:
                self.__setlinedash(linedash)
            self.__stroke()
            self.__grestore()
        return
        # END: circle()

    def polygon(self,
                coord      = [],
                linecolor  = 'black',
                linewidth  = 1,
                linecap    = 0,
                linedash   = 0,
                fill       = False,
                fillcolor  = 'black',
                fillstyle  = 'solid',
                fillsize   = 3,
                fillskip   = 4,
                bgcolor    = '',
                ):
        # find minx,miny and maxx,maxy
        xmin = coord[0][0]
        ymin = coord[0][1]
        xmax = xmin
        ymax = ymin
        for p in range(1,len(coord)):
            if coord[p][0] < xmin:
                xmin = coord[p][0]
            if coord[p][1] < ymin:
                ymin = coord[p][1]
            if coord[p][0] > xmax:
                xmax = coord[p][0]
            if coord[p][1] > ymax:
                ymax = coord[p][1]

        # if the background should be filled, do that here
        if bgcolor != '':
            self.__gsave()
            self.__moveto(coord[0][0], coord[0][1]) 
            for p in range(1,len(coord)):
                self.__lineto(coord[p][0], coord[p][1])
            self.__closepath()
            self.__setcolor(bgcolor)
            self.__fill()
            self.__grestore()

        # do filled one first
        if fill == True:
            # need to draw proper path to then clip it
            self.__gsave()
            self.__moveto(coord[0][0], coord[0][1]) 
            for p in range(1,len(coord)):
                self.__lineto(coord[p][0], coord[p][1])
            self.__closepath()
            self.__clip()
            # use minimal x,y pair and max x.y pair to determine patternbox
            self.__makepattern(coord=[[xmin,ymin],[xmax,ymax]],
                               fillcolor=fillcolor, fillstyle=fillstyle,
                               fillsize=fillsize, fillskip=fillskip)
            self.__grestore()

        # now draw outline of polygon
        if linewidth > 0.0:
            self.__gsave()
            self.__moveto(coord[0][0], coord[0][1])
            for p in range(1,len(coord)):
                self.__lineto(coord[p][0], coord[p][1])
            self.__closepath()
            self.__setcolor(linecolor)
            self.__setlinewidth(linewidth)
            if linecap != 0:
                self.__setlinecap(linecap)
            if linedash != 0:
	        self.__setlinedash(linedash)
            self.__stroke()
            self.__grestore()

        return
        # END: polygon
    # END: class postscript

#
# class drawable
# 
# Creates a drawable region onto which graphs can be drawn. Must define the
# xrange and yrange, which are each min,max pairs, so that the drawable can
# translate data in table into points on the graph. Also, must select which
# type of scale each axis is, e.g., linear, log10, and so forth. If unspecified,
# coordinates (the x,y location of the lower left of the drawable) and
# dimensions (the width, height of the drawable) will be guessed at; specifying
# these allows control over where and how big the drawable is. Other options do
# things like place a background color behind the entire drawable or make an
# outline around it.
# 
class drawable:
    def __init__(self,
                 # Canvas object upon which to draw.
                 canvas     = '',

                 # Dimensions of the drawable surface; e.g., ['1in','1in']
                 # if left as empty list, will make a guess as to size.
                 dimensions = [],

                 # Lower-left corner of drawable should be placed at this
                 # location on the canvas. If left as empty, will make a guess.
                 coord      = [],

                 # X range of the drawable.
                 xrange     = [],

                 # Y range of the drawable
                 yrange     = [],

                 # Scale to use ('linear' or 'log2' or 'log10' or 'logX')
                 # for x range; currently, no other types of scales supported.
                 xscale     = 'linear',

                 # Scale to use ('linear' or 'log2' or 'log10' or 'logX')
                 # for y range; currently, no other types of scales supported.
                 yscale     = 'linear',
                 ):
        # record canvas of this drawable...
        assert(canvas != '')
        self.canvas = canvas
        
        # check if x and y have been specified
        if coord == []:
            coord = ['0.5in', '0.5in']
        assert(len(coord) == 2)
        coord[0] = str(coord[0])
        coord[1] = str(coord[1])
        self.offset = [canvas.convert(coord[0]), canvas.convert(coord[1])]

        # now, check if height and width have been specified
        if dimensions == []:
            dimensions = [canvas.width-float(self.offset[0])-15,
                          canvas.height-float(self.offset[1])-15]
        assert(len(dimensions) == 2)
        dimensions[0] = str(dimensions[0])
        dimensions[1] = str(dimensions[1])
        self.dimensions = [canvas.convert(dimensions[0]),
                           canvas.convert(dimensions[1])]

        self.scaletype = ['blank', 'blank']
        self.logbase = [0, 0]
        self.linearMin = [0, 0]
        self.linearMax = [0, 0]
        self.virtualMin = [0, 0]
        self.virtualMax = [0, 0]
        self.linearRange = [0, 0]

        for axis in ['x', 'y']:
            if axis == 'x':
                axisnum = 0
                gscale = xscale
                grange = xrange
            else:
                axisnum = 1
                gscale = yscale
                grange = yrange

            if gscale == 'linear':
                self.scaletype[axisnum]  = 'linear'
		self.linearMin[axisnum]  = float(grange[0])
		self.linearMax[axisnum]  = float(grange[1])
		self.virtualMin[axisnum] = float(grange[0])
		self.virtualMax[axisnum] = float(grange[1])

            else:
                idx = gscale.find('log')
                if idx == -1:
                    abort('must be a linear or log scale')
                tmp = gscale.split('log')
                assert(len(tmp) == 2)
                self.logbase[axisnum] = float(tmp[1])

                self.scaletype[axisnum]  = 'log'

                assert(float(grange[0]) > 0)
                assert(float(grange[1]) > 0)
                
		self.linearMin[axisnum]  = math.log(float(grange[0]),
                                                    self.logbase[axisnum])
		self.linearMax[axisnum]  = math.log(float(grange[1]),
                                                    self.logbase[axisnum])
		self.virtualMin[axisnum] = float(grange[0])
		self.virtualMax[axisnum] = float(grange[1])

            # and record the linear range (for use in scaling)
            self.linearRange[axisnum] = self.linearMax[axisnum] - \
                                        self.linearMin[axisnum]

        self.axismap = {'x': 0, 'y': 1}
        return
    # END: __init__

    # helper functions
    def __axisindex(self, axis):
        return self.axismap[axis]

    #
    # VALUES have three possible types
    #   Virtual    : what they are in the specifed scale type (log, linear)
    #   Linear     : what they are once the mapping has been applied
    #                (log(virtual), etc.)
    #   Scaled     : in Postscript points, scaled as if the drawable is at 0,0
    #   Translated : in Postscript points, scaled + offset of drawable
    #
    # How to go from one to the other?
    #   to translate from Virtual -> Linear, call [Map]
    #   to translate from Linear  -> Scaled, call [Scale]
    #   to translate from Scaled  -> Translated, call [Translate]
    # 
    def getscaletype(self, axis):
        axisnum = self.axismap[axis]
        return self.scaletype[axisnum]

    # Map: take value, map it onto a linear value scale
    def dmapNum(self, axisnum, value):
        scale = self.scaletype[axisnum]

        if scale == 'linear':
            return value
        elif scale == 'log':
            return math.log(value, self.logbase[axisnum])
        else:
            abort('unknown mapping scale')

    def scaleNum(self, axisnum, value):
        width  = self.dimensions[axisnum]
        lrange = self.linearRange[axisnum]
        result = float(value) * (width / lrange)
        return result
        
    # Scale: scale a linear value onto the drawable's range
    def scale(self, axis, value):
        return self.scaleNum(self.__axisindex(axis), value)

    # Translate: scale and then add the offset 
    def translate(self, axis, value):
        # need two linear values: then subtract, scale, and add offset
        anum  = self.__axisindex(axis)
        lmin  = self.linearMin[anum]
        value = self.dmapNum(anum, float(value))

        # offset + scaled difference = what we want
        result = self.offset[anum] + self.scaleNum(anum, value - lmin)
        return result

    # accessor function
    def virtualmin(self, axis):
        axisnum = self.axismap[axis]
        return self.virtualMin[axisnum]

    # accessor function
    def virtualmax(self, axis):
        axisnum = self.axismap[axis]
        return self.virtualMax[axisnum]

    def rangeiterator(self, axis, min, max, step):
        tlist = []
        axisnum = self.axismap[axis]
        scale = self.scaletype[axisnum]
        if scale == 'linear':
            i = min
            while i <= max:
		tlist.append(i)
                i = i + step
        elif scale == 'log':
            i = min
            while i <= max:
                tlist.append(i)
                i = i * step
        return tlist

    # useful for extracting canvas
    def canvas(self):
        return self.canvas

    #
    def map(self, coord):
        if type(coord) == types.ListType:
            # need to figure out: is this a simple list, or a list of lists?
            first = coord[0]
            if type(first) == types.ListType:
                return self.translatecoord(coord)
            else:
                return self.translatecoordsingle(coord)
        else:
            abort('map: needs to be passed a list')

    # useful for calling basic ps functions ...
    def translatecoord(self, coord):
        assert(coord != '')
        assert(len(coord) > 0)
        ucoord = []
        ucoord.append([self.translate('x', float(coord[0][0])),
                       self.translate('y', float(coord[0][1]))])
        for i in range(1,len(coord)):
            ucoord.append([self.translate('x', float(coord[i][0])),
                           self.translate('y', float(coord[i][1]))])
        return ucoord

    # useful for calling basic ps functions ...
    def translatecoordsingle(self, coord):
        assert(coord != '')
        assert(len(coord) > 0)
        ucoord = [self.translate('x', float(coord[0])),
                  self.translate('y', float(coord[1]))]
        return ucoord

    def getsize(self, axis):
        axisnum = self.axismap[axis]
        return self.dimensions[axisnum]

    def bottom(self):
        return self.offset[1]

    def top(self):
        return self.offset[1] + self.dimensions[1]

    def left(self):
        return self.offset[0]

    def right(self):
        return self.offset[0] + self.dimensions[0]
    # END: class drawable

#
# class table
#
# Tables store data to be plotted, and provide a thin layer over SQLite to
# select subsets of the data to plot.
#
class table:
    def __init__(self,
                 # File name where table should be populated from;
                 # file should have fixed number of columns of data.
                 file  = '',

                 # If file name is not specified (as above), can populate
                 # a table with data from another table (this makes a copy).
                 table = '',

                 # When initializing a table from another table, use the
                 # 'where' option to perform a selection of which data you want.
                 # For example, 'where=c0 > 10' populates the new table with
                 # all rows where the first value in the row (i.e., c0) is
                 # greater than 10.
                 where = '',

                 # When reading from a file, use the 'separator' to split each
                 # line and thus decide the different entries for that line.
                 # Default is to use whitespace; a colon is a common one too.
                 separator = '',
                 ):
        self.file = file
        self.cnames = []

        data = []

        if table != '':
            rows = table.query(where)
            self.cnames  = table.cnames
            self.columns = table.columns
            self.file    = table.file

            for r in rows:
                element = []
                count = 0
                for i in r:
                    if count > 0:
                        element.append(i)
                    count = count + 1
                data.append(element)
            
            # generate unique name - undoubtedly not the way to do this.
            self.dbname = 'tmp' + str(random.randint(0,9999999))
        elif self.file != '':
            # first, look for schema
            fd = open(self.file, 'r')
            line = fd.readline().strip()
            if separator == '':
                separator = None
            tmp = line.split(separator)
            if (len(tmp) > 0) and (tmp[0] == '#'):
                # there is a schema, decode it
                self.columns = len(tmp)
                self.cnames.append('rownumber')
                for i in range(1, self.columns):
                    self.cnames.append(tmp[i].strip())
            else:
                # no schema: just assign column names c0, c1, etc.
                self.columns = len(tmp) + 1
                self.cnames.append('rownumber')
                for i in range(0, self.columns):
                    self.cnames.append('c'+str(i))
            fd.close()

            # open again for reading ...
            fd = open(self.file, 'r')
            for line in fd:
                line = line.strip()
                tmp = line.split(separator)
                if (len(tmp) > 0) and (tmp[0] != '') and (tmp[0][0] != '#'):
                    curlen = len(tmp)
                    if curlen != (self.columns - 1):
                        abort('Bad input row! (%s)' % line)
                    ntmp = []
                    for d in tmp:
                        ntmp.append(d.strip())
                    data.append(ntmp)
            fd.close()

            # extract unique number from file, somehow
            self.dbname = 'tmp' + str(random.randint(0,9999999))
        else:
            self.cnames  = ['rownumber']
            self.columns = 1
            self.file    = ''
            self.dbname = 'tmp' + str(random.randint(0,9999999))
        # END: if ...

        # make an in-memory database
        self.fd     = sqlite3.connect(':memory:')
        self.cursor = self.fd.cursor()

        # calling each column cXXX where XXX is the row number
        create = 'create table %s (' % self.dbname
        for i in range(0, self.columns):
            if i != 0:
                create += ', '
            create += '%s text' % self.cnames[i]
        create += ')'

        # create reverse index of column names
        self.rindex  = {}
        for i in range(0, self.columns):
            self.rindex[self.cnames[i]] = i
        self.cursor.execute(create)
        self.fd.commit()

        # now, insert values
        insert = 'insert into %s values (' % self.dbname
        for i in range(0, self.columns-1):
            insert = insert + '?, '
        insert = insert + '?)'

        count = 0
        for row in data:
            row.insert(0, count)
            count = count + 1
            self.cursor.execute(insert, row)
        return

    def __cnames(self):
        return self.cnames
    
    def getaxislabels(self,
                      column=''):
        self.cursor.execute('select * from %s' % (self.dbname))
        rindex = self.getrindex()
        idx    = rindex[column]
        cnt = 0
        rlist = []
        for row in self.cursor:
            tmp = []
            tmp.append(row[idx])
            tmp.append(cnt)
            rlist.append(tmp)
            cnt = cnt + 1
        return rlist
   
    def dump(self, title='', canvas=None):
        s = ''
        if title:
            s += title + '\n'
        s += '*DUMP* '
        for name in self.cnames:
            s += name + ' '
        s += '\n'
        self.cursor.execute('select * from %s' % (self.dbname))
        for row in self.cursor:
            s += '*DUMP* ' + str(row) + '\n'
        if canvas:
            canvas.comment(s)
        else:
            print s
        return

    # INSERT INTO table_name
    # SET column1=value, column2=value2,...
    # WHERE some_column=some_value
    def insert(self,keyValues={}):
        keys = sorted(keyValues.keys())
        values = ["'%s'" % keyValues[x] for x in keys]
        rownumber = self.cursor.execute('select count(*) from %s' % self.dbname)
        rownumber = rownumber.fetchone()[0] + 1
        query = ('insert into %s (rownumber, %s)'
                 'values (%d, %s)' % (
                self.dbname,
                ', '.join(keys),
                rownumber,
                ', '.join(values)))
        self.cursor.execute(query)
        return

    # UPDATE table_name
    # SET column1=value, column2=value2,...
    # WHERE some_column=some_value
    def update(self,
               set='',
               where=''):
        assert(set != '')
        if where == '':
            self.cursor.execute('update %s set %s' % (self.dbname, set))
        else:
            self.cursor.execute('update %s set %s where %s' % (self.dbname, set,
                                                               where))

    def getmax(self, column, cmax=''):
        self.cursor.execute('select * from %s' % (self.dbname))
        rindex = self.getrindex()
        idx    = rindex[column]
        # print column, idx
        for row in self.cursor:
            value = float(row[idx])
            if cmax == '':
                cmax = value
            elif value > cmax:
                cmax = value
        return cmax

    def getvalues(self, column, cmax=''):
        self.cursor.execute('select * from %s' % (self.dbname))
        rindex = self.getrindex()
        idx    = rindex[column]
        # print column, idx
        return_values = []
        for row in self.cursor:
            return_values.append(row[idx])
        return return_values

    def getmin(self, column, cmin=''):
        self.cursor.execute('select * from %s' % (self.dbname))
        rindex = self.getrindex()
        idx    = rindex[column]
        for row in self.cursor:
            value = float(row[idx])
            if cmin == '':
                cmin = value
            if value < cmin:
                cmin = value
        return cmin

    def getavg(self, column, where=''):
        if where == '':
            self.cursor.execute('select * from %s' % self.dbname)
        else:
            self.cursor.execute('select * from %s where %s' % (self.dbname,
                                                               where))

        rindex = self.getrindex()
        idx    = rindex[column]
        currsum = 0.0
        count   = 0
        for row in self.cursor:
            value   = float(row[idx])
            currsum = currsum + value
            count = count + 1
        if count > 0:
            return currsum / count
        else:
            return 0

    def getrange(self, column, crange):
        if crange != '':
            return [self.getmin(column, crange[0]),
                    self.getmax(column, crange[1])]
        else:
            return [self.getmin(column, ''), self.getmax(column, '')]

    def getrindex(self):
        return self.rindex

    def getname(self):
        return self.dbname

    def query(self, where='', order='', select='*', group=''):
        q = 'select %s from %s' % (select, self.dbname)
        if where != '':
            q += ' where %s' % where
        if order != '':
            q += ' order by %s' % order
        if group != '':
            q += ' group by %s' % group

        self.cursor.execute(q)

        # key: adding 'rownumber' as the first element of each row 
        results = []
        counter = 0
        for row in self.cursor:
            results.append(row)
            counter = counter + 1
        return results

    def addcolumns(self, *args):
        for cn in args:
            self.addcolumn(cn)
        return self

    def addcolumn(self,
                  column='',
                  value='',
                  ):
        assert(column != '')
        self.cursor.execute('alter table %s add column %s text' % (self.dbname,
                                                                   column))
        self.cnames.append(column)
        self.rindex[column] = self.columns
        self.columns = self.columns + 1
        if value == '':
            value = 0
        self.cursor.execute('update %s set %s=\'%s\'' % (self.dbname, column,
                                                         value))
        return
# END: class table

# 
# class plotter
#
# Use this to draw some points on a drawable. There are some obvious parameters:
# which drawable, which table, which x and y columns from the table to use, the
# color of the point, its linewidth, and the size of the marker. 'style' is a
# more interesting parameter, allowing one to pick a box, circle, horizontal
# line (hline), and 'x' that marks the spot, and so forth. However, if you set
# 'style' to label, PlotPoints will instead use a column from the table (as
# specified by the 'label' flag) to plot an arbitrary label at each (x,y) point.
# Virtually all the rest of the flags pertain to these text labels: whether to
# rotate them, how to anchor them, how to place them, font, size, and color.
# 
class plotter:
    def __init__(self,
                 # The default drawable for this plotter. However, you can
                 # specify a different drawable when making specific graphs
                 # (which thus overrides this default).
                 drawable=''
                 ):
        self.drawable = drawable
        return

    #
    # points()
    #
    # Use this to draw points onto the drawing surface. Lots of options...
    #
    def points(self,
               drawable        = '',        # name of the drawable area
               table           = '',        # name of table to use
               where           = '',        # where clause: which rows to plot?
               xfield          = 'c0',      # table column with x data
               yfield          = 'c1',      # table column with y data
               shift           = [0,0],     # shift points in x,y direction
               size            = 2.0,       # overall size of marker;
                                            # used unless sizefield is specified
               style           = 'xline',   # label,hline,vline,plusline,xline,
                                            # dline1,dline2,dline12,square,
                                            # circle,triangle,utriangle,diamond,
                                            # star,asterisk
               sizefield       = '',        # if specified, table column with
                                            # sizes for each point
               sizediv         = '',        # if using sizefield, use sizediv to
                                            # scale each value (each sizefield
                                            # gets divided by sizediv)
               linecolor       = 'black',   # color of the line of the marker
               linewidth       = 1.0,       # width of lines used to draw marker
               fill            = False,     # for some shapes, filling makes
                                            # sense; if desired, mark this true
               fillcolor       = 'black',   # if filling, use this fill color
               fillstyle       = 'solid',   # if filling, which fill style 
               fillsize        = 3.0,       # size of object in pattern
               fillskip        = 4.0,       # space between object in pattern
               labelfield      = '',        # if specified, table column with
                                            # labels for each point
               labelformat     = '%s',      # if specified, table column with
                                            # labels for each point
               labelrotate     = 0,         # if using labels, rotate labels
               labelanchor     = 'c,c',     # if using labels, how to anchor 
               labelplace      = 'c',       # if using labels, place text:
                                            # (c) centered on point, (s) below
                                            # point, (n) above point, (w) west
                                            # of point, (e) east of point
               labelshift      = [0,0],     # shift text in x,y direction
               labelfont       = 'default', # if using labels, what font 
               labelsize       = 6.0,       # if using labels, font for label
               labelcolor      = 'black',   # if using labels, what color font
               labelbgcolor    = '',        # if using labels, put a background
                                            # color behind each
               legend          = '',        # which legend?
               legendtext      = '',        # text to add to legend
               stackfields     = [],        # fields to add to yfield to
                                            # determine y coord
               ):
        if drawable == '':
            drawable = self.drawable
        assert(drawable != '')
        canvas = drawable.canvas

        rindex = table.getrindex()
        xindex = rindex[xfield]
        yindex = rindex[yfield]
        if sizefield != '':
            sizeindex = rindex[sizefield]
        if labelfield != '':
            labelindex = rindex[labelfield]

        # iterate...
        for r in table.query(where):
            unscaledy = float(r[yindex])
            for stackfield in stackfields:
                unscaledy += float(r[rindex[stackfield]])

            x = drawable.translate('x', r[xindex])
            y = drawable.translate('y', unscaledy)

            if sizefield != '':
                # non-empty -> sizefield should be used (i.e., ignore use(size))
                size = float(r[sizeindex]) / float(sizediv)

            if style == 'label': 
                assert(labelfield != '')
                label = r[labelindex]
                if labelplace == 'c':
                    y = y + 0
                elif labelplace == 's':
                    y = y - labelsize
                elif labelplace == 'n':
                    y = y + labelsize
                elif labelplace == 'w':
                    x = x - size - 2.0
                elif labelplace == 'e':
                    x = x + size + 2.0
                else:
                    abort('bad place flag (%s); should be c, s, n, w, or e' % \
                          labelplace)
                text = labelformat % label
                canvas.text(coord=[x+labelshift[0],y+labelshift[1]], text=text,
                            anchor=labelanchor, rotate=labelrotate,
                            font=labelfont, size=labelsize, color=labelcolor,
                            bgcolor=labelbgcolor)
		
            else:
                canvas.shape(style=style, x=x+shift[0], y=y+shift[1], size=size,
                             linecolor=linecolor, linewidth=linewidth,
                             fill=fill, fillcolor=fillcolor,
                             fillstyle=fillstyle, fillsize=fillsize,
                             fillskip=fillskip)

        if legend != '':
            s = 'canvas.shape(style=\'' + style + \
                '\', x=$__Xx, y=$__Yy, size=$__M2, linecolor=\''+ \
                str(linecolor) + '\', linewidth=' + str(linewidth) + \
                ', fill=' + str(fill) + ', fillcolor=\'' + str(fillcolor) + \
                '\', fillstyle=\'' + str(fillstyle) + '\', fillsize=' + \
                str(fillsize) + ', fillskip=' + str(fillskip)+')'
            t = string.Template(s)
            legend.add(text=legendtext, picture=t)
        return
    # END: points()


    # 
    # horizontalbars()
    # 
    # Use this to plot horizontal bars. The options are quite similar to the
    # vertical cousin of this routine, except (somehow) less feature-filled
    # (hint: lazy programmer).
    # 
    def horizontalbars(self,
                       drawable    = '',
                       table       = '',
                       where       = '',
                       xfield      = 'c0',
                       yfield      = 'c1',

                       # if specified, table column with xlo data; use if bars
                       # don't start at the minimum of the range
                       xloval      = '',

                       # width of the bars
                       barwidth    = 1.0,

                       # color, width of lines
                       linecolor   = 'black',
                       linewidth   = 1.0,

                       # if filling, description of fill of bars
                       fill        = False,
                       fillcolor   = 'black',
                       fillstyle   = 'solid',
                       fillsize    = 3,
                       fillskip    = 4,

                       # background color for legend text, + other legend stuff
                       bgcolor     = '',
                       legend      = '',
                       legendtext  = '',

                       # fields to add to yfield to determine y coord
                       stackfields = [],       
                       ):
        if drawable == '':
            drawable = self.drawable
        assert(drawable != '')
        canvas = drawable.canvas
        assert(table != '')

        # construct query, adding fields as need be, and recording index values
        rindex = table.getrindex()
        xindex = rindex[xfield]
        yindex = rindex[yfield]

        for r in table.query(where):
            x = r[xindex]
            y = r[yindex]
            if xloval == '':
                # XXX: should be min of the yrange
                xlo = 0.0
            else:
                xlo = xloval

            if len(stackfields) > 0:
                xlo = 0
                for stackfield in stackfields:
                    inc = float(r[rindex[stackfield]])
                    xlo += inc
                    x = float(x)+inc

            bwidth = drawable.scale('y', barwidth)

            x1 = drawable.translate('x', xlo)
            y1 = drawable.translate('y', y) - (bwidth/2.0)
            x2 = drawable.translate('x', x)
            y2 = drawable.translate('y', y) + (bwidth/2.0)

            canvas.box(coord=[[x1,y1],[x2,y2]],
                       linecolor=linecolor, linewidth=linewidth, fill=fill,
                       fillcolor=fillcolor, fillstyle=fillstyle,
                       fillsize=fillsize, fillskip=fillskip, bgcolor=bgcolor)
        return
    # END: horizontalbars()

    #
    # helper function for vertical bars routine below
    # 
    def __getanchorplace(self, labelanchor, labelplace, y1, y2):
        if y2 < y1:
            # this is an upside down bar, so switch anchor and 'place'
            if labelplace == 'i':
                place = 3
            else:
                place = -3
        else:
            # normal bar (not upside down)
            if labelplace == 'i':
                place = -3
            else:
                place = 3

        if labelanchor == '':
            # autospecifying the anchor
            if place < 0:
                anchor = 'c,h'
            else:
                anchor = 'c,l'
        else:
            anchor = labelanchor
        return [anchor, place]

    #
    # verticalbars()
    #
    # Use this to plot vertical bars on a drawable. A basic plot will specify
    # the table, xfield, and yfield. Bars will be drawn from the minimum of the
    # range to the y value found in the table. If the bars should start at some
    # value other than the minimum of the range (for example, when the yaxis
    # extends below zero, or you are building a stacked bar chart), two options
    # are available: ylofield and yloval. ylofield specifies a column of a
    # table that has the low values for each bar, i.e., a bar will be drawn at
    # the value specifed by the xfield starting at the ylofield value and going
    # up to the yfield value. yloval can be used instead when there is just a
    # single low value to draw all bars down to. Some other interesting options:
    # labelfield, which lets you add a label to each bar by giving a column of
    # labels (use rotate, anchor, place, font, fontsize, and fontcolor flags to
    # control details of the labels); barwidth, which determines how wide each
    # bar is in the units of the x-axis; linecolor, which determines the color
    # of the line surrounding the box, and linewidth, which determines its
    # thickness (or 0 to not have one); and of course the color and fill of the
    # bar, as determined by fillcolor, fillstyle, and fillsize and fillskip.
    # 
    def verticalbars(self,
                     drawable      = '',
                     table         = '',
                     where         = '',
                     xfield        = 'c0',
                     yfield        = 'c1',

                     # if specified, table column with ylo data; use if bars
                     # don't start at the minimum of the range
                     ylofield      = '',        

                     # fields to add to yfield to determine y coord
                     stackfields     = [],

                     # if there is no ylofield, use this value to fill down to;
                     # if empty, just use min of yrange
                     yloval        = '',        

                     barwidth      = 1.0,       # bar width

                     # of the form n,m; thus, each x-axis data point actually
                     # will have 'm' bars plotted upon it; 'n' specifies which
                     # cluster of the 'm' this one is (from 0 to m-1); width of
                     # each bar is 'barwidth/m'; normal bar plots (without
                     # clusters) are just the default, '0,1'
                     cluster       = [0,1],

                     # color of the line surrounding each bar
                     linecolor     = 'black',

                     # width of the line; set to 0 if you don't want a
                     # surrounding line on the box
                     linewidth     = 0.25,

                     # fill the box or not 
                     fill          = False,

                     # fill color (if used)
                     fillcolor     = 'gray',

                     # solid, boxes, circles, ...
                     fillstyle     = 'solid',

                     # size of object in pattern
                     fillsize      = 3,

                     # space between object in pattern
                     fillskip      = 4,

                     # color background for the bar; empty means none (patterns
                     # may be see through)
                     bgcolor       = '',

                     # if specified, table column with labels for each bar
                     labelfield    = '',

                     # use this format for the labels; can prepend and postpend
                     # arbitrary text
                     labelformat   = '%s',

                     # rotate labels by this many degrees
                     labelrotate   = 0,

                     # text anchor if using a labelfield; empty means use a
                     # best guess
                     labelanchor   = '',

                     # place label (o) outside of bar or (i) inside of bar
                     labelplace    = 'o',

                     # shift text in x,y direction
                     labelshift    = [0.0,0.0],

                     # if using labels, what font should be used
                     labelfont     = 'default',

                     # if using labels, font for label
                     labelsize     = 10.0,

                     # if using labels, what color font should be used
                     labelcolor    = 'black',

                     # if specified, fill this color in behind each text item
                     labelbgcolor  = '',

                     # which legend?
                     legend        = '',

                     # text to add to legend
                     legendtext    = '',        
                     ):
        # start here
        if drawable == '':
            drawable = self.drawable
        assert(drawable != '')
        canvas = drawable.canvas

        assert(len(cluster) == 2)
        n        = float(cluster[0])
        clusters = float(cluster[1])
        assert(n >= 0)
        assert(n < clusters)

        barwidth  = drawable.scale('x', barwidth)
        ubarwidth = barwidth / clusters

        # construct query, adding fields as need be, and recording index values
        rindex = table.getrindex()
        xindex = rindex[xfield]
        yindex = rindex[yfield]
        if ylofield != '':
            yloindex = rindex[ylofield]
        if labelfield != '':
            labelindex = rindex[labelfield]

        # get data from table
        rows  = table.query(where)
        
        # if using loval (and not lofield)
        if yloval == '':
	    ylo = drawable.virtualmin('y')
        else:
	    ylo = yloval

        # print 'rows', rows

        for r in rows:
            # print 'plot', r
            x = r[xindex]
            y = r[yindex]
            if ylofield != '':
                ylo = r[yloindex]

            if len(stackfields) > 0:
                ylo = 0
                for stackfield in stackfields:
                    inc = float(r[rindex[stackfield]])
                    ylo += inc
                    y = float(y)+inc

            x1 = drawable.translate('x', x) - (barwidth/2.0) + (ubarwidth * n)
            y1 = drawable.translate('y', ylo)
            x2 = x1 + (barwidth/clusters)
            y2 = drawable.translate('y', y)

            # auto set anchor, etc.
            ap = self.__getanchorplace(labelanchor, labelplace, y1, y2)
            anchor = ap[0]
            place  = ap[1]

            # make the arg list and call the box routine
            canvas.box(coord=[[x1,y1],[x2,y2]],
                       linecolor=linecolor, linewidth=linewidth, fill=fill,
                       fillcolor=fillcolor, fillstyle=fillstyle,
                       fillsize=fillsize, fillskip=fillskip, bgcolor=bgcolor)

            if labelfield != '':
                label  = labelformat % r[labelindex]
                xlabel = x1 + (barwidth/2.0) + labelshift[0]
                ylabel = drawable.translate('y', y) + place + labelshift[1]
                canvas.text(coord=[xlabel,ylabel], text=label, anchor=anchor,
                            rotate=labelrotate, font=labelfont, size=labelsize,
                            color=labelcolor, bgcolor=labelbgcolor)

        if legend != '':
            if fillcolor=='white' and linewidth==0:
                linewidth=1
            s = 'canvas.box(coord=[[$__Xmm,$__Ymm],[$__Xpm,$__Ypm]], fill=' + \
                str(fill) + ', fillcolor=\'' + str(fillcolor) + \
                '\', fillstyle=\'' + str(fillstyle) + '\', fillsize=\'' + \
                str(fillsize) + '\', fillskip=\'' + str(fillskip) + \
                '\', linewidth=\'' + str(linewidth/2.0) + '\', linecolor=\'' + \
                str(linecolor) + '\')'
            t = string.Template(s)
            legend.add(text=legendtext, picture=t)
        return
    # END: verticalbars()

    #
    # line()
    # 
    # Use this function to plot lines. It is one of the simplest routines there
    # is -- basically, it takes the x and y fields and plots a line thru them.
    # It does NOT sort them, though, so you might need to do that first if you
    # want the line to look pretty. The usual line arguments can be used,
    # including color, width, and dash pattern.
    # 
    def line(self,
             drawable     = '',
             table        = '', 
             where        = '', 
             xfield       = 'c0', 
             yfield       = 'c1',

             # plot the data in a stairstep manner (e.g., CDF)
             stairstep    = False,   
             linecolor    = 'black', 
             linewidth    = 1.0,
             linejoin     = 0,
             linecap      = 0,

             # dash pattern - 0 means no dashes
             linedash     = 0,

             # if specified, table column with labels for each point in line.
             # Rest of label args spec things about the lables.
             labelfield   = '',      
             labelplace   = 'n',     
             labelfont    = 'default',
             labelsize    = 8.0,
             labelcolor   = 'black',
             labelanchor  = 'c',
             labelrotate  = 0,       
             labelshift   = [0,0],
             labelformat  = '%s',
             labelbgcolor = '',
             # if using labels, how much to offset from point by
             labeloffset  = 3.0,

             # legend info
             legend       = '',       
             legendtext   = '',       

             # if adding points as well - a convenience?
             # why not just use lines and points?
             symbstyle    = '',
             symbsize     = 2,
             symbfill     = False,
             ):

        if drawable == '':
            drawable = self.drawable
        assert(drawable != '')

        if symbstyle:
            self.points(drawable=drawable, table=table, style=symbstyle,
                        xfield=xfield, yfield=yfield, size=symbsize,
                        fill=symbfill, linecolor=linecolor, fillcolor=linecolor)

        # get some things straight before looping
        if labelplace == 'n':
            offset = labeloffset
        elif labelplace == 's':
            offset = -labeloffset

        assert(table != '')

        # construct query, adding fields as need be, and recording index values
        rindex = table.getrindex()
        xindex = rindex[xfield]
        yindex = rindex[yfield]
        if labelfield != '':
            labelindex = rindex[labelfield]

        # get data from table
        rows  = table.query(where)

        lastx = -1
        lasty = -1

        linelist = []

        canvas = drawable.canvas

        x = 0
        lastyt = 0

        for r in rows:
            x = r[xindex]
            y = r[yindex]

            if labelfield != '':
                label = r[labelindex]

            xt = drawable.translate('x', x)
            yt = drawable.translate('y', y)

            if len(linelist) > 0 and stairstep == True:
                linelist.append([xt, lastyt])
            linelist.append([xt, yt])
            lastyt = yt 

            if labelfield != '':
                label  = labelformat % r[labelindex]
                xlabel = xt + labelshift[0]
                ylabel = yt + labelshift[1] + offset
                canvas.text(coord=[xlabel,ylabel], text=label,
                            anchor=labelanchor, rotate=labelrotate,
                            font=labelfont, size=labelsize,
                            color=labelcolor, bgcolor=labelbgcolor)
        # end: for r in rows
        # if stairstep == True:
        # should this really just be one? what if each stairstep
        # is much bigger than that? what should it be then?
        # XXX
        # linelist.append([drawable.translate('x', float(x) + 1.0), lastyt])

        canvas.line(coord=linelist, linecolor=linecolor, linewidth=linewidth,
                    linedash=linedash, linecap=linecap, linejoin=linejoin)

        if legend != '':
            s = 'canvas.shape(style=\'hline\', x=$__Xx, y=$__Yy, size=$__M2,' \
                + 'linecolor=\'' + str(linecolor) + '\', linewidth=' + \
                str(linewidth) + ', linedash=' + str(linedash) + ')'
            t = string.Template(s)
            legend.add(text=legendtext, picture=t)

        return
    # END: line()

    #
    # function()
    #
    # Use function() to plot a function right onto a drawable. The function
    # should simply take one argument (e.g., x) and return the value of the
    # function (e.g., f(x)).
    # 
    def function(self,
                 drawable   = '',

                 # the function, such as 'x*x'
                 function   = '',
                 
                 # the x-range the function should be plotted over [xmin,xmax]
                 xrange     = [0,10],

                 # given the range of xmin to xmax, step determines at which x
                 # values the function is evaluated and a line is drawn to
                 step       = 1,

                 # if given, limit function to values between low/hi y values
                 ylimit     = ['',''],

                 # line width, color, and dash pattern
                 linewidth  = 1,      
                 linecolor  = 'black',
                 linedash   = 0,

                 # legend info
                 legend     = '',     
                 legendtext = '',     
                 ):
        if drawable == '':
            drawable = self.drawable
        assert(drawable != '')
        linelist = []
        x = xrange[0]
        while x <= xrange[1]:
            y = function(x)
            if ((ylimit[0] == '') or (ylimit[0] != '') and (y >= ylimit[0])) \
                   and ((ylimit[1] == '') or ((ylimit[1] != '') and \
                                              (y <= ylimit[1]))):
                linelist.append([drawable.translate('x', x),
                                 drawable.translate('y', y)])
            x = x + step
            
        canvas = drawable.canvas
        canvas.line(coord=linelist, linecolor=linecolor, linewidth=linewidth,
                    linedash=linedash)

        if legend != '':
            s = 'canvas.line(coord=[[$__Xmw,$__Yy],[$__Xpw,$__Yy]], ' + \
                'linewidth=%s, linecolor=\'%s\', linedash=%s)' % \
                (linewidth, linecolor, linedash)
            t = string.Template(s)
            legend.add(text=legendtext, picture=t)

        return
    # END: function()

    # 
    # horizontalintervals()
    #
    # Use this to plot interval markers in the x direction. The y column has
    # the y value for each interval, and draws the interval between the ylo and
    # yhi column values. The marker can take on many forms, as specified by
    # the 'align' flag. Note the 'b' type in particular, which can be used to
    # assemble box plots.
    #
    def horizontalintervals(self,
                            drawable  = '', # name of the drawable area
                            table     = '', # name of table to use
                            where     = '', # select a subset of the table?
                            yfield    = '', # table column with y data
                            xlofield  = '', # table column with xlo data
                            xhifield  = '', # table column with xhi data
                            align     = 'c', # c-center u-upper l-lower n-none
                            linecolor = 'black', # color of the line
                            linewidth = 1,  # width of all lines
                            devwidth  = 3,  # width of interval marker on top
                            ):
        if drawable == '':
            drawable = self.drawable
        assert(drawable != '')
        canvas = drawable.canvas

        rindex   = table.getrindex()
        yindex   = rindex[yfield]
        xloindex = rindex[xlofield]
        xhiindex = rindex[xhifield]

        # get data from table
        rows  = table.query(where)

        for r in rows:
            y   = r[yindex]
            xlo = r[xloindex]
            xhi = r[xhiindex]

            yp   = drawable.translate('y', y)
            xlop = drawable.translate('x', xlo)
            xhip = drawable.translate('x', xhi)

            dw   = devwidth / 2.0
            hlw  = linewidth / 2.0
            
            if align == 'c':
		canvas.line(coord=[[xlop,yp],[xhip,yp]], linecolor=linecolor,
                            linewidth=linewidth)
            elif align == 'l':
		canvas.line(coord=[[xlop,yp-dw+hlw],[xhip,yp-dw+hlw]],
                            linecolor=linecolor, linewidth=linewidth)
            elif align == 'u':
		canvas.line(coord=[[xlop,yp+dw-hlw],[xhip,yp+dw-hlw]],
                            linecolor=linecolor, linewidth=linewidth)
            elif align != 'n':
                abort('Bad alignment: %s; should be c, l, or r' % align)

            # vertical line between two end marks
            canvas.line(coord=[[xhip,yp-dw],[xhip,yp+dw]], linecolor=linecolor,
                        linewidth=linewidth)
            canvas.line(coord=[[xlop,yp-dw],[xlop,yp+dw]], linecolor=linecolor,
                        linewidth=linewidth)
        return
    # END: horizontalintervals()

    # 
    # verticalintervals()
    # 
    # Use this to plot interval markers in the y direction. The x column has
    # the x value for each interval, and draws the interval between the ylo and
    # yhi column values. The marker can take on many forms, as specified by
    # the 'align' flag. Note the 'b' type in particular, which can be used to
    # assemble box plots. 
    # 
    def verticalintervals(self,
                          drawable    = '',   # name of the drawable area
                          table       = '',   # name of table to use
                          where       = '',   # where clause?
                          xfield      = 'c0', # table column with x data
                          ylofield    = 'c1', # table column with ylo data
                          yhifield    = 'c2', # table column with yhi data
                          align       = 'c',  # c-center l-left r-right n-none
                          linecolor   = 'black', # color of the line
                          linewidth   = 1,    # width of all lines
                          devwidth    = 3,    # width of interval marker on top
                          ):
        if drawable == '':
            drawable = self.drawable
        assert(drawable != '')
        canvas = drawable.canvas

        # construct query, adding fields as need be, and recording index values
        rindex   = table.getrindex()
        xindex   = rindex[xfield]
        yloindex = rindex[ylofield]
        yhiindex = rindex[yhifield]

        # get data from table
        rows  = table.query(where)

        for r in rows:
            x   = r[xindex]
            ylo = r[yloindex]
            yhi = r[yhiindex]

            xp   = drawable.translate('x', x)
            ylop = drawable.translate('y', ylo)
            yhip = drawable.translate('y', yhi)

            dw   = devwidth / 2.0
            hlw  = linewidth / 2.0

            if align == 'c':
		canvas.line(coord=[[xp,ylop],[xp,yhip]], linecolor=linecolor,
                            linewidth=linewidth)
            elif align == 'l':
		canvas.line(coord=[[xp-dw+hlw,ylop],[xp-dw+hlw,yhip]],
                            linecolor=linecolor, linewidth=linewidth)
            elif align == 'r':
		canvas.line(coord=[[xp+dw-hlw,ylop],[xp+dw-hlw,yhip]],
                            linecolor=linecolor, linewidth=linewidth)
	    elif align != 'n':
                # n is the only other reasonable choice...
		abort('Bad alignment (%s): should be c, l, r, or n' % align)

            # vertical line between two end marks
            canvas.line(coord=[[xp-dw,yhip],[xp+dw,yhip]], linecolor=linecolor,
                        linewidth=linewidth)
            canvas.line(coord=[[xp-dw,ylop],[xp+dw,ylop]], linecolor=linecolor,
                        linewidth=linewidth)
        return
    # END: verticalintervals()

    #
    # METHOD verticalfill()
    #
    # Use this function to fill a vertical region between either the values in
    # yfield and the minimum of the y-range (default), the yfield values and
    # the values in the ylofield, or the yfield values and a single yloval.
    # Any pattern and color combination can be used to fill the filled space.
    # 
    def verticalfill(self,
                     drawable   = '',  # name of the drawable area
                     table      = '',  # name of table to use
                     where      = '',  # where clause?
                     xfield     = '',  # table column with x data
                     yfield     = '',  # table column with y data
                     ylofield   = '',  # if not empty, use this table column
                                       # to fill down to this value
                     yloval     = '',  # if no ylofield, use this value to fill
                                       # down to; if empty, use min of y-range
                     stairstep  = False, # use stairsteps in making fill
                     fillcolor  = 'lightgrey', #  fill color (if used)
                     fillstyle  = 'solid',     # solid, boxes, circles, ...
                     fillsize   = 3,   # size of object in pattern
                     fillskip   = 4,   # space between object in pattern
                     legend     = '',  # which legend object?
                     legendtext = '',  # text to add to legend
                     ):
        if drawable == '':
            drawable = self.drawable
        assert(drawable != '')

        # get rindex
        rindex   = table.getrindex()
        xindex   = rindex[xfield]
        yindex   = rindex[yfield]
        if ylofield != '':
            yloindex = rindex[ylofield]
        else:
            if yloval == '':
                ylo = drawable.translate('y', 0.0)
            else:
                ylo = drawable.translate('y', yloval)

        canvas = drawable.canvas

        first = 0
        for r in table.query(where):
            # get first point
            x = drawable.translate('x', r[xindex])
            y = drawable.translate('y', r[yindex])
            if ylofield != '':
                ylo = drawable.translate('y', r[yloindex])

            if first == 0:
                xlast   = x
                ylast   = y
                ylolast = ylo
                first   = 1
            else:
                xcurr   = x
                ycurr   = y
                ylocurr = ylo

                # draw the polygon between the last pair of points and
                # the current points if stairstep is in action
                if stairstep:
                    ycurr_use   = ylast
                    ylocurr_use = ylolast
                else:
                    ycurr_use   = ycurr
                    ylocurr_use = ylocurr

                canvas.polygon(coord=[[xlast,ylolast],[xlast,ylast],
                                      [xcurr,ycurr_use],[xcurr,ylocurr_use]],
                               fill=True, fillcolor=fillcolor,
                               fillstyle=fillstyle, fillsize=fillsize,
                               fillskip=fillskip, linewidth=0.1,
                               linecolor=fillcolor)
                # future: 
                # make a little bit of linewidth so as to overlap
                # neighboring regions. The alternate is worse: having to draw
                # one huge polygon (though maybe not that bad...)

                # move last points to current points
                xlast   = xcurr
                ylast   = ycurr
                ylolast = ylocurr
        # END: for ...

        if legend != '':
            s = 'canvas.shape(style=\'' + 'square' + \
                '\', x=$__Xx, y=$__Yy, size=$__M2, linecolor=\''+ \
                'black' + '\', linewidth=' + str(0.5) + \
                ', fill=' + str(True) + ', fillcolor=\'' + str(fillcolor) + \
                '\', fillstyle=\'' + str(fillstyle) + '\', fillsize=' + \
                str(fillsize) + ', fillskip=' + str(fillskip)+')'
            t = string.Template(s)
            legend.add(text=legendtext, picture=t)
        return
    # END: verticalfill()
# END: class plotter

#
# class axis
#
# Use this to draw some axes. It is supposed to be simpler and easier to use
# than the older package. We will see about that.
# 
class axis:
    def __init__(self,
                 drawable      = '',

                 # The color of axis line.
                 linecolor     = 'black',

                 # The width of axis line.
                 linewidth     = 1.0,       

                 # dash parameters; will make axes dashed, but not tic marks.
                 # 0 means no dashes; otherwise use a list to specify the
                 # dash pattern (e.g., [2,2], or [2,3,2], etc.).
                 linedash      = 0,

                 # Which axes to draw: 'xy', 'x', 'y', 'box' are the options.
                 style         = 'xy',

                 # Labels 'in' or 'out'? for xaxis, 'out' means below and
                 # 'in' above; for yaxis,'out' means left/'in' right
                 labelstyle    = 'out',

                 # Are tics 'in', 'out', or 'centered'? (inside the axes,
                 # outside them, or centered upon the axes)
                 ticstyle      = 'out',

                 # Whether to draw the actual axes or not; useful if you just
                 # want to draw the tic marks, for example.
                 doaxis        = True,

                 # Whether to put labels on or not.
                 dolabels      = True,

                 # Whether to put majortics on axes or not.
                 domajortics   = True,

                 # Whether to put major tics on x-axis.
                 doxmajortics  = True,

                 # Whether to put major tics on y-axis.
                 doymajortics  = True,

                 # Whether to put minortics on axes or not.
                 dominortics   = False,

                 # Whether to put major tics on x-axis.
                 doxminortics  = True,

                 # Whether to put major tics on y-axis.
                 doyminortics  = True,

                 # Whether to put labels on x-axis.
                 doxlabels     = True,

                 # Whether to put labels on y-axis.
                 doylabels     = True,      

                 # The min/max values to draw xaxis between; empty (default)
                 # means the whole range.
                 xaxisrange    = '',

                 # The min/max values to draw yaxis between; empty (default)
                 # means the whole range.
                 yaxisrange    = '',

                 # The y value that the x-axis is located at; empty gives you
                 # the min; ignored by 'box'.
                 xaxisposition = '',

                 # The x value that the y-axis is located at; empty gives you
                 # the min; ignored by 'box'.
                 yaxisposition = '',        

                 # [x1,x2,step] will put labels and major tics from 'x1' to 'x2'
                 # with 'step' between each; can leave any of these empty ('')
                 # and the method will fill in a guess (either the min or max 
                 # of range, or a guess for the step), e.g., [0,'',2] means
                 # start at 0, fill in the max of the xrange for a max value,
                 # and set the step to 2. The default is to guess these values.
                 xauto         = ['','',''],

                 # Specify labels/majortics by hand with a list of form:
                 # [['label1', x1], ['label2', x2]...]. Can also be filled in
                 # from a table column with method table.getaxislabels(column=).
                 xmanual       = '',        

                 # Similar to xauto, but for the y-axis.
                 yauto         = ['','',''],

                 # Similar to xmanual, but for y-axis.
                 ymanual       = '',        

                 # Size of the major tics.
                 ticmajorsize  = 4.0,

                 # Size of the minor tics.
                 ticminorsize  = 2.5,       

                 # how many minor tics between each major tic (x axis)
                 xminorticcnt  = 1,

                 # how many minor tics between each major tic (y axis)
                 yminorticcnt  = 1,         

                 # Font to use for x labels.
                 xlabelfont      = 'default',

                 # font size of labels for x labels.
                 xlabelfontsize  = 10.0,

                 # font color for x labels.
                 xlabelfontcolor = 'black',

                 # Rotation for x labels, in degrees. If not 0, 90 is common.
                 xlabelrotate   = 0,          

                 # If non-empty, put a background colored square behind xlabels.
                 xlabelbgcolor = '',
                 
                 # Text anchor for labels along the x axis; empty means guess.
                 xlabelanchor   = '',

                 # Format string for xlabels; e.g., %d for ints; empty (default)
                 # implies best guess; can also use this to add decoration to
                 # the label, e.g., '%i %%' will add a percent sign to each
                 # integer label, and so forth.
                 xlabelformat   = '',         

                 # Font to use for y labels.
                 ylabelfont      = 'default',

                 # font size of labels for y labels.
                 ylabelfontsize  = 10.0,

                 # font color for y labels.
                 ylabelfontcolor = 'black',

                 # Rotation for x labels, in degrees. If not 0, 90 is common.
                 ylabelrotate   = 0,          

                 # If non-empty, put a background colored square behind ylabels.
                 ylabelbgcolor = '',
                 
                 # Text anchor for labels along the x axis; empty means guess.
                 ylabelanchor   = '',

                 # Format string for y labels; see xlabelformat for details.
                 ylabelformat   = '',         

                 # What to multiply xlabel values by; e.g., if 10, 1 becomes 10,
                 # 2 becomes 20, and so forth.
                 xlabeltimes   = 1,
                 
                 # Similar to xlabeltimes, but for y label values.
                 ylabeltimes   = 1,           

                 # Shift xlabels left/right, up/down (+4,-3 -> right 4, down 3)
                 xlabelshift   = [0,0],
                 
                 # Similar to xshift, but for ylabels.
                 ylabelshift   = [0,0],       

                 # Title along the X axis.
                 xtitle        = '',

                 # Font to use for x title.
                 xtitlefont    = 'default',

                 # Font size for x title.
                 xtitlesize    = 10,

                 # Font color for xtitle.
                 xtitlecolor   = 'black',

                 # General placement of xtitle:
                 # 'c' for center, 'l' for left, 'r' for right.
                 xtitleplace   = 'c',

                 # Coordinates of title; if empty, guess (you can always
                 # adjust final placement with -xtitleshift).
                 xtitlecoord   = '',          

                 # Use this to adjust title place left/right, up/down.
                 xtitleshift   = [0,0],

                 # How much (in degrees) to rotate the title.
                 xtitlerotate  = 0,

                 # How to anchor text; empty means best guess.
                 xtitleanchor  = '',

                 # If not-empty, color behind title.
                 xtitlebgcolor = '',          

                 # Same as with xtitle, but for ytitle.
                 ytitle        = '',          

                 # Same as with xtitle, but for ytitle.
                 ytitlefont    = 'default',   

                 # Same as with xtitle, but for ytitle.
                 ytitlesize    = 10,          

                 # Same as with xtitle, but for ytitle.
                 ytitlecolor   = 'black',     

                 # Same as with xtitle, but for ytitle.
                 ytitleplace   = 'c',         

                 # Same as with xtitle, but for ytitle.
                 ytitlecoord   = '',          

                 # Same as with xtitle, but for ytitle.
                 ytitleshift   = [0,0],       

                 # Same as with xtitle, but for ytitle (default is different).
                 ytitlerotate  = 90.0,        

                 # Same as with xtitle, but for ytitle.
                 ytitleanchor  = '',          

                 # Same as with xtitle, but for ytitle.
                 ytitlebgcolor = '',          

                 # Main title of the graph.
                 title         = '',          

                 # Same as with xtitle, but for main title.
                 titlefont     = 'default',   

                 # Same as with xtitle, but for main title.
                 titlesize     = 10.0,        

                 # Same as with xtitle, but for main title.
                 titlecolor    = 'black',     

                 # Same as with xtitle, but for main title.
                 titleplace    = 'c',         

                 # Same as with xtitle, but for main title.
                 titleshift    = [0,0],       

                 # Same as with xtitle, but for main title.
                 titlerotate   = 0,           

                 # Same as with xtitle, but for main title.
                 titleanchor   = '',          

                 # Same as with xtitle, but for main title.
                 titlebgcolor  = '',          
                 ):
        assert(drawable != '')

        values = {} # empty dict
        values['xrange,min'] = drawable.virtualmin('x')
        values['xrange,max'] = drawable.virtualmax('x')
        values['yrange,min'] = drawable.virtualmin('y')
        values['yrange,max'] = drawable.virtualmax('y')

        # figure out where axes will go
        if xaxisposition != '':
            values['xaxis,ypos'] = xaxisposition
        else:
            values['xaxis,ypos'] = values['yrange,min']

        if yaxisposition != '':
            values['yaxis,xpos'] = yaxisposition
        else:
            values['yaxis,xpos'] = values['xrange,min']

        # find out ranges of each axis
        if xaxisrange != '':
            assert(len(xaxisrange) == 2)
            values['xaxis,min'] = xaxisrange[0]
            values['xaxis,max'] = xaxisrange[1]
        else:
            values['xaxis,min'] = values['xrange,min']
            values['xaxis,max'] = values['xrange,max']

        if yaxisrange != '':
            assert(len(yaxisrange) == 2)
            values['yaxis,min'] = yaxisrange[0]
            values['yaxis,max'] = yaxisrange[1]
        else:
            values['yaxis,min'] = values['yrange,min']
            values['yaxis,max'] = values['yrange,max']

        # translate each of these values into points
        tvalues = {}
        for v in ['xaxis,min', 'xaxis,max', 'xrange,min', 'xrange,max',
                  'yaxis,xpos']:
            tvalues[v] = drawable.translate('x', values[v])
        for v in ['yaxis,min', 'yaxis,max', 'yrange,min', 'yrange,max',
                  'xaxis,ypos']:
            tvalues[v] = drawable.translate('y', values[v])

        # adjust for linewidths
        half = float(linewidth) / 2.0

        assert(style == 'x' or style == 'y' or style == 'xy' or style == 'box')

        assert(drawable != '')
        canvas = drawable.canvas

        if doaxis == True:
            if style == 'x' or style == 'xy':
		canvas.line(coord=[[tvalues['xaxis,min']-half,
                                    tvalues['xaxis,ypos']],
                                   [tvalues['xaxis,max']+half,
                                    tvalues['xaxis,ypos']]],
                            linecolor=linecolor, linewidth=linewidth,
                            linedash=linedash)
            if style == 'y' or style == 'xy':
		canvas.line(coord=[[tvalues['yaxis,xpos'],
                                    tvalues['yaxis,min']-half],
                                   [tvalues['yaxis,xpos'],
                                    tvalues['yaxis,max']+half]],
                            linecolor=linecolor, linewidth=linewidth,
                            linedash=linedash)

            if style == 'box':
		canvas.line(coord=[[tvalues['xaxis,min']-half,
                                    tvalues['yrange,min']],
                                   [tvalues['xaxis,max']+half,
                                    tvalues['yrange,min']]],
                            linecolor=linecolor, linewidth=linewidth,
                            linedash=linedash)
		canvas.line(coord=[[tvalues['xrange,min'],
                                    tvalues['yaxis,min']-half],
                                   [tvalues['xrange,min'],
                                    tvalues['yaxis,max']+half]],
                            linecolor=linecolor, linewidth=linewidth,
                            linedash=linedash)
		canvas.line(coord=[[tvalues['xaxis,min']-half,
                                    tvalues['yrange,max']],
                                   [tvalues['xaxis,max']+half,
                                    tvalues['yrange,max']]],
                            linecolor=linecolor, linewidth=linewidth,
                            linedash=linedash)
		canvas.line(coord=[[tvalues['xrange,max'],
                                    tvalues['yaxis,min']-half],
                                   [tvalues['xrange,max'],
                                    tvalues['yaxis,max']+half]],
                            linecolor=linecolor, linewidth=linewidth,
                            linedash=linedash)

        # unpack the (complex) args and put useful things into labels and
        # values arrays
        xlabels = []
        ylabels = []
        self.__unpackargs(drawable, axis='x', values=values, labels=xlabels,
                          manual=xmanual, auto=xauto,
                          labelformat=xlabelformat, labeltimes=xlabeltimes)
        self.__unpackargs(drawable, axis='y', values=values, labels=ylabels,
                          manual=ymanual, auto=yauto,
                          labelformat=ylabelformat, labeltimes=ylabeltimes)

        if domajortics == True:
            if doxmajortics and (style == 'x' or style == 'xy'):
                self.__maketics(drawable=drawable, axis='x',
                                axispos=tvalues['xaxis,ypos'], labels=xlabels,
                                ticstyle=ticstyle, ticsize=ticmajorsize,
                                linecolor=linecolor, linewidth=linewidth)
            if doymajortics and (style == 'y' or style == 'xy'):
                self.__maketics(drawable=drawable, axis='y',
                                axispos=tvalues['yaxis,xpos'], labels=ylabels,
                                ticstyle=ticstyle, ticsize=ticmajorsize,
                                linecolor=linecolor, linewidth=linewidth)
            if style == 'box':
                if doxmajortics:
                    self.__maketics(drawable=drawable, axis='x',
                                    axispos=tvalues['yaxis,min'],
                                    labels=xlabels, ticstyle=ticstyle,
                                    ticsize=ticmajorsize, linecolor=linecolor,
                                    linewidth=linewidth)
                    self.__maketics(drawable=drawable, axis='x',
                                    axispos=tvalues['yaxis,max'],
                                    labels=xlabels,
                                    ticstyle=self.__toggle(ticstyle),
                                    ticsize=ticmajorsize,
                                    linecolor=linecolor, linewidth=linewidth)
                if doymajortics:
                    self.__maketics(drawable=drawable, axis='y',
                                    axispos=tvalues['xaxis,min'],
                                    labels=ylabels, ticstyle=ticstyle,
                                    ticsize=ticmajorsize, linecolor=linecolor,
                                    linewidth=linewidth)
                    self.__maketics(drawable=drawable, axis='y',
                                    axispos=tvalues['xaxis,max'],
                                    labels=ylabels,
                                    ticstyle=self.__toggle(ticstyle),
                                    ticsize=ticmajorsize,
                                    linecolor=linecolor, linewidth=linewidth)
                
        if dolabels == True:
            if (style == 'x' or style == 'xy' or style == 'box') and \
                   doxlabels == True:
                self.__makelabels(drawable=drawable, values=values, 
                                  axis='x', axispos=tvalues['xaxis,ypos'],
                                  labels=xlabels, labelstyle=labelstyle,
                                  ticstyle=ticstyle, ticmajorsize=ticmajorsize,
                                  font=xlabelfont, fontsize=xlabelfontsize,
                                  fontcolor=xlabelfontcolor,
                                  labelanchor=xlabelanchor,
                                  labelrotate=xlabelrotate,
                                  labelshift=xlabelshift,
                                  labelbgcolor=xlabelbgcolor)
            if (style == 'y' or style == 'xy' or style == 'box') and \
                   doylabels == True:
                self.__makelabels(drawable=drawable, values=values,
                                  axis='y', axispos=tvalues['yaxis,xpos'],
                                  labels=ylabels, labelstyle=labelstyle,
                                  ticstyle=ticstyle, ticmajorsize=ticmajorsize,
                                  font=ylabelfont, fontsize=ylabelfontsize,
                                  fontcolor=ylabelfontcolor,
                                  labelanchor=ylabelanchor,
                                  labelrotate=ylabelrotate,
                                  labelshift=ylabelshift,
                                  labelbgcolor=ylabelbgcolor)

        self.__maketitle(drawable=drawable, values=values, tvalues=tvalues,
                         # label info ...
                         dolabels=dolabels, doxlabels=doxlabels,
                         doylabels=doylabels, labelstyle=labelstyle,
                         # describing title...
                         title=title, titleshift=titleshift,
                         titlefont=titlefont, titlecolor=titlecolor,
                         titlerotate=titlerotate, titlesize=titlesize,
                         titlebgcolor=titlebgcolor, titleanchor=titleanchor,
                         titleplace=titleplace,
                         # describing xtitle...
                         xtitle=xtitle, xtitleshift=xtitleshift,
                         xtitlefont=xtitlefont, xtitlecolor=xtitlecolor,
                         xtitlerotate=xtitlerotate, xtitlesize=xtitlesize,
                         xtitlebgcolor=xtitlebgcolor, xtitleanchor=xtitleanchor,
                         xtitleplace=xtitleplace,
                         # describing ytitle...
                         ytitle=ytitle, ytitleshift=ytitleshift,
                         ytitlefont=ytitlefont, ytitlecolor=ytitlecolor,
                         ytitlerotate=ytitlerotate, ytitlesize=ytitlesize,
                         ytitlebgcolor=ytitlebgcolor, ytitleanchor=ytitleanchor,
                         ytitleplace=ytitleplace)

        # minortics
        if dominortics == True:
            nxlabels = []
            nylabels = []
            self.__makeminorlabels(nxlabels, xlabels, xminorticcnt)
            self.__makeminorlabels(nylabels, ylabels, yminorticcnt)
            
            if doxminortics and (style == 'x' or style == 'xy'):
                self.__maketics(drawable=drawable, axis='x',
                                axispos=tvalues['xaxis,ypos'], labels=nxlabels,
                                ticstyle=ticstyle, ticsize=ticminorsize,
                                linecolor=linecolor, linewidth=linewidth)
            if doyminortics and (style == 'y' or style == 'xy'):
                self.__maketics(drawable=drawable, axis='y',
                                axispos=tvalues['yaxis,xpos'], labels=nylabels,
                                ticstyle=ticstyle, ticsize=ticminorsize,
                                linecolor=linecolor, linewidth=linewidth)
            if style == 'box':
                if doxminortics:
                    self.__maketics(drawable=drawable, axis='x',
                                    axispos=tvalues['yaxis,min'],
                                    labels=nxlabels, ticstyle=ticstyle,
                                    ticsize=ticminorsize, linecolor=linecolor,
                                    linewidth=linewidth)
                    self.__maketics(drawable=drawable, axis='x',
                                    axispos=tvalues['yaxis,max'],
                                    labels=nxlabels,
                                    ticstyle=self.__toggle(ticstyle),
                                    ticsize=ticminorsize, linecolor=linecolor,
                                    linewidth=linewidth)
                if doyminortics:
                    self.__maketics(drawable=drawable, axis='y',
                                    axispos=tvalues['xaxis,min'],
                                    labels=nylabels, ticstyle=ticstyle,
                                    ticsize=ticminorsize, linecolor=linecolor,
                                    linewidth=linewidth)
                    self.__maketics(drawable=drawable, axis='y',
                                    axispos=tvalues['xaxis,max'],
                                    labels=nylabels,
                                    ticstyle=self.__toggle(ticstyle),
                                    ticsize=ticminorsize, linecolor=linecolor,
                                    linewidth=linewidth)
        return
    #END: __init__()

    def __recordlabel(self,
                      drawable,
                      values,
                      axis,
                      x, y,
                      label,
                      font, fontsize, anchor, rotate):
        # height and width
        height = fontsize
        canvas = drawable.canvas
        width  = canvas.stringWidth(label, fontsize)

        # get anchors
        a = anchor.split(',')
        if len(a) == 2:
            xanchor = a[0]
            yanchor = a[1]
        elif len(a) == 1:
            xanchor = a[0]
            yanchor = 'l'
        else:
            abort('rbad anchor: '+ anchor)

        # XXX deal with rotation XXX
    
        # now, find bounding box 
        if xanchor == 'l':
            xlo = x
        elif xanchor == 'c':
            xlo = x - (width/2.0)
        elif xanchor == 'r':
            xlo = x - width 

        if yanchor == 'l':
            ylo = y
        elif yanchor == 'c':
            ylo = y - (height/2.0)
        elif yanchor == 'h':
            ylo = y - height 

        xhi = xlo + width
        yhi = ylo + height

        if (('labelbox,'+axis+',xlo' in values) == False) or \
               (xlo < values['labelbox,'+axis+',xlo']):
            values['labelbox,'+axis+',xlo'] = xlo
        if (('labelbox,'+axis+',ylo' in values) == False) or \
               (ylo < values['labelbox,'+axis+',ylo']):
            values['labelbox,'+axis+',ylo'] = ylo
        if (('labelbox,'+axis+',xhi' in values) == False) or \
               (xhi > values['labelbox,'+axis+',xhi']):
            values['labelbox,'+axis+',xhi'] = xhi
        if (('labelbox,'+axis+',yhi' in values) == False) or \
               (yhi > values['labelbox,'+axis+',yhi']):
            values['labelbox,'+axis+',yhi'] = yhi
        return
    #END: __recordlabel()

    def __makelabels(self,
                     drawable,
                     values,
                     axis,
                     axispos,
                     labels,
                     labelstyle,
                     ticstyle,
                     ticmajorsize,
                     font,
                     fontsize,
                     fontcolor,
                     labelanchor,
                     labelrotate,
                     labelshift,
                     labelbgcolor,
                     ):
        # how much space between fonts and tics, basically
        offset = 3.0 

        # set fixpos to the place where labels should be drawn
        #   for yaxis, this is the x position of the labels
        #   for xaxis, this is the y position of the labels
        # fixpos thus does not change and is used to draw each of the labels
        if labelstyle == 'out':
            if axis == 'x':
                anchor = 'c,h'
            else:
                anchor = 'r,c'

            if ticstyle == 'in':
                fixpos = axispos - offset
            elif ticstyle == 'out':
                fixpos = axispos - ticmajorsize - offset 
            elif ticstyle == 'centered':
                fixpos = axispos - (ticmajorsize/2.0) - offset
            else:
                abort('bad ticstyle: ' + ticstyle)

        if labelstyle == 'in':
            if axis == 'x':
                anchor = 'c,l'
            else:
                anchor = 'l,c'

            if ticstyle == 'in':
                fixpos = axispos + ticmajorsize + offset
            elif ticstyle == 'out':
                fixpos = axispos + offset
            elif ticstyle == 'centered':
                fixpos = axispos + (ticmajorsize/2.0) + offset
            else:
                abort('bad ticstyle: ' + ticstyle)

        # allow intelligent override, otherwise provide solid guess as to
        # label placement
        if labelanchor != '':
            anchor = labelanchor

        assert(drawable != '')
        canvas = drawable.canvas

        # draw the labels
        for i in range(0, len(labels)):
            label  = labels[i][0]
            value  = labels[i][1]
            movpos = drawable.translate(axis, value)
            if axis == 'x':
		x = movpos + labelshift[0]
		y = fixpos + labelshift[1]
		canvas.text(coord=[x,y], text=label, font=font, size=fontsize,
                            color=fontcolor, anchor=anchor, rotate=labelrotate,
                            bgcolor=labelbgcolor)
	    elif axis == 'y':
		x = fixpos + labelshift[0]
		y = movpos + labelshift[1]
		canvas.text(coord=[x,y], text=label, font=font, size=fontsize,
                            color=fontcolor, anchor=anchor, rotate=labelrotate,
                            bgcolor=labelbgcolor)
            else:
                abort('bad axis: ' + axis)
            # record where text is s.t. later title pos are properly placed 
            self.__recordlabel(drawable=drawable, values=values, axis=axis, x=x,
                               y=y, label=label, font=font, fontsize=fontsize,
                               anchor=anchor, rotate=labelrotate)
        return

    def __maketics(self,
                   drawable,
                   axis,
                   axispos,
                   labels,
                   ticstyle,
                   ticsize,
                   linecolor,
                   linewidth):
        if ticstyle == 'in':
	    hipos = axispos + ticsize
	    lopos = axispos
        elif ticstyle == 'out':
	    hipos = axispos
	    lopos = axispos - ticsize
        elif ticstyle == 'centered':
	    hipos = axispos + (ticsize/2.0)
	    lopos = axispos - (ticsize/2.0)
        else:
            abort('bad tic style: ' + ticstyle)

        canvas = drawable.canvas

        # draw the tic marks AT EACH LABEL in labels array
        for i in range(0, len(labels)):
            label  = labels[i][0]
            value  = labels[i][1]
            tvalue = drawable.translate(axis, value)
            if axis == 'x':
		canvas.line(coord=[[tvalue,lopos],[tvalue,hipos]],
                            linecolor=linecolor, linewidth=linewidth)
            elif axis == 'y':
		canvas.line(coord=[[lopos,tvalue],[hipos,tvalue]],
                            linecolor=linecolor, linewidth=linewidth)
        return
    # END: maketics()
    
    def __findmajorstep(self,
                        drawable,
                        axis,
                        vmin,
                        vmax):
        # XXX 3.5 is pretty random
        ticsperinch = 3.5 
        width = drawable.getsize(axis) / 72.0
        tics  = width * ticsperinch
        step  = 1 + int((vmax - vmin) / tics)
        return step
    # END: findmajorstep()

    def __unpackargs(self,
                     drawable,
                     axis,
                     values,
                     labels,
                     manual,
                     auto,
                     labelformat,
                     labeltimes, 
                     ):
        assert(axis == 'x' or axis == 'y')
        rangemin = values[axis+'range,min']
        rangemax = values[axis+'range,max'] 

        # now, unpack label and tic info
        if manual != '':
            # if manual is not empty, use it (override auto)
            for m in manual:
                if labelformat == '':
                    labelformat = '%s'
                assert(len(m) == 2)
                name     = m[0]
                location = m[1]
                labels.append([labelformat % name, location])
        else:
            assert(len(auto) == 3)
            if auto[0] == '':
                values[axis+',min'] = rangemin
            else:
                values[axis+',min'] = auto[0]

            if auto[0] == '':
                values[axis+',max'] = rangemax
            else:
                values[axis+',max'] = auto[1]

            if auto[2] == '':
                # This assumes that rangemin, max are linear values, whereas
                # they MIGHT NOT BE. More proper to: take virtual values, map
                # them to linear, figure out what to do then 
                # values[axis+',step'] =
                #   int((float(rangemax) - float(rangemin)) / 10.0)
                values[axis+',step'] = self.__findmajorstep(drawable=drawable,
                                                            axis=axis,
                                                            vmin=rangemin,
                                                            vmax=rangemax)
            else:
                values[axis+',step'] = auto[2]

            if values[axis+',step'] <= 0:
                values[axis+',step'] = 1

            # now, set the format properly, if needed
            if labelformat == '':
                if drawable.getscaletype(axis) == 'category':
                    labelformat = '%s'
                else:
                    notInt = 0
                    for i in [',min', ',max', ',step']:
                        if values[axis+i] != int(values[axis+i]):
                            notInt = notInt + 1
                    if notInt > 0:
                        labelformat = '%.1f'
                    else:
                        labelformat = '%d'

            # now, fill in labels array with positions of each label
            init = values[axis+',min']
            assert(values[axis+',min'] < values[axis+',max'])
            assert(values[axis+',step'] > 0)
            # print 'AUTO', auto
            while init <= values[axis+',max']:
                if labeltimes != 1:
                    labels.append([labelformat % (init * labeltimes), init])
                else:
                    labels.append([labelformat % init, init])
                init = init + values[axis+',step']
        return
    # END: __unpackargs()

    def __maketitle(self, drawable, values, tvalues, dolabels, doxlabels,
                    doylabels, title, titleshift, titlefont, titlecolor,
                    titlerotate, titlesize, titlebgcolor, titleanchor,
                    titleplace, xtitle, xtitleshift, xtitlefont, xtitlecolor,
                    xtitlerotate, xtitlesize, xtitlebgcolor, xtitleanchor,
                    xtitleplace, ytitle, ytitleshift, ytitlefont, ytitlecolor,
                    ytitlerotate, ytitlesize, ytitlebgcolor, ytitleanchor,
                    ytitleplace, labelstyle):                    
        # some space between titles and the nearest text to them;
        # 3 is randomly chosen
        offset = 3.0
        canvas = drawable.canvas

        if title != '':
            values['title,y'] = tvalues['yrange,max'] + (2.5 * offset)
            if titleplace == 'c':
		values['title,x']      = (tvalues['xrange,min'] + \
                                          tvalues['xrange,max']) / 2.0
		values['title,anchor'] = 'c,l'
            elif titleplace == 'l':
		values['title,x']      = tvalues['xrange,min'] + offset
		values['title,anchor'] = 'l,l'
            elif titleplace == 'r':
		values['title,x']      = tvalues['xrange,max'] - offset
		values['title,anchor'] = 'r,l'
            else:
                abort('bad titleanchor: Must be c, l, or r')

            # allow user override of this option, of course
            if titleanchor != '':
                values['title,anchor'] = titleanchor
        # END: if title != ''
                
        if ytitle != '':
            if labelstyle == 'in':
		values['ytitle,x']  = tvalues['yaxis,xpos'] + offset
		yanchor             = 'h'
            elif labelstyle == 'out':
		values['ytitle,x']  = tvalues['yaxis,xpos'] - offset
		yanchor             = 'l'
            else:
                abort('bad labelstyle')
	
            if ytitleplace == 'c':
		values['ytitle,y']  = (tvalues['yrange,max'] + \
                                       tvalues['yrange,min']) / 2.0
		xanchor             = 'c'
            elif ytitleplace == 'l':
		values['ytitle,y']  = tvalues['yrange,min'] + offset
		xanchor             = 'l'
            elif ytitleplace == 'u':
		values['ytitle,y']  = tvalues['yrange,max'] - offset
		xanchor             = 'r'
            else:
                abort('Bad titleanchor: Must be c, l, or u')

            # allow user override of this option, of course
            if ytitleanchor != '':
                values['ytitle,anchor'] = ytitleanchor
            else:
                values['ytitle,anchor'] = xanchor + ',' + yanchor

            # try to move ytitle based on labelbox(y,*)
            if dolabels == True:
                if doylabels == True:
                    if labelstyle == 'out':
                        if values['ytitle,x'] >= values['labelbox,y,xlo']:
                            values['ytitle,x'] = values['labelbox,y,xlo'] - \
                                                 offset
                    if labelstyle == 'in':
                        if values['ytitle,x'] <= values['labelbox,y,xhi']:
                            values['ytitle,x'] = values['labelbox,y,xhi'] + \
                                                 offset
        # END: if ytitle != ''

        if xtitle != '':
            if labelstyle == 'in':
                values['xtitle,y']   = tvalues['xaxis,ypos'] + offset
                yanchor              = 'l'
            elif labelstyle == 'out':
                values['xtitle,y']   = tvalues['xaxis,ypos'] - offset
                yanchor              = 'h'
            else:
                abort('bad labelstyle')

            if xtitleplace == 'c':
                values['xtitle,x']   = (tvalues['xrange,min'] + \
                                        tvalues['xrange,max']) / 2.0
                xanchor              = 'c'
            elif xtitleplace == 'l':
                values['xtitle,x']   = tvalues['xrange,min'] + offset
                xanchor              = 'l'
            elif xtitleplace == 'r':
                values['xtitle,x']   = tvalues['xrange,max'] - offset
                xanchor              = 'r'
            else:
                abort('Bad titleanchor: Must be c, l, or r')

            # allow user override of this option, of course
            if xtitleanchor != '':
                values['xtitle,anchor'] = xtitleanchor
            else:
                values['xtitle,anchor'] = xanchor + ',' + yanchor

            # move xtitle if there are xlabels in the way
            if dolabels == True:
                if doxlabels == True:
                    if values['xtitle,y'] >= values['labelbox,x,ylo']:
                        values['xtitle,y'] = values['labelbox,x,ylo'] - offset
        # END: if xtitle != ''

        # finish up
        if title != '':
            canvas.text(coord=[titleshift[0]+values['title,x'],
                               titleshift[1]+values['title,y']],
                        text=title, font=titlefont, size=titlesize,
                        color=titlecolor, anchor=values['title,anchor'],
                        bgcolor=titlebgcolor, rotate=titlerotate)

        if xtitle != '':
            canvas.text(coord=[xtitleshift[0]+values['xtitle,x'],
                               xtitleshift[1]+values['xtitle,y']],
                        text=xtitle, font=xtitlefont, size=xtitlesize,
                        color=xtitlecolor, anchor=values['xtitle,anchor'],
                        bgcolor=xtitlebgcolor, rotate=xtitlerotate)

        if ytitle != '':
            canvas.text(coord=[ytitleshift[0]+values['ytitle,x'],
                               ytitleshift[1]+values['ytitle,y']],
                        text=ytitle, font=ytitlefont, size=ytitlesize,
                        color=ytitlecolor, anchor=values['ytitle,anchor'],
                        bgcolor=ytitlebgcolor, rotate=ytitlerotate)
    # END: __maketitle()

    def __toggle(self,
                 style):
        if style == 'in':
            return 'out'
        elif style == 'out':
            return 'in'
        return 'centered'

    def __makeminorlabels(self, nlabels, labels, minorticcnt):
        for i in range(0, len(labels) - 1):
            curr   = labels[i]
            next   = labels[i+1]
            clabel = curr[0]
            cvalue = curr[1]
            nlabel = next[0]
            nvalue = next[1]
            diff   = (nvalue - cvalue) / (minorticcnt + 1.0)

            nlabels.append(curr)
            for j in range(0, minorticcnt):
                cvalue = cvalue + diff
                nlabels.append(['', cvalue])
        return
    # END: __makeminorlabels
#END: class axis

#
# class grid
#
# Just a simple way to draw grids onto graphs.
# While we generally don't like grids, some people do.
#
class grid:
    def __init__(self,
                 # The relevant drawable upon which to place this grid.
                 drawable  = '',

                 # The color of grid lines.
                 linecolor = 'black',

                 # The width of grid lines.
                 linewidth = 0.5,          

                 # Make grid lines dashed as per usual patterns. Examples:
                 # 0 for no dashes, [2,2] for length 2 lines with length 2
                 # spaces, etc.
                 linedash  = 0,
                 
                 # Specify false to turn off grid in x direction
                 # (False means no vertical lines).
                 x         = True,

                 # Specify false to turn off grid in y direction
                 # (False means no horizontal lines).
                 y         = True,

                 # Empty means whole range, otherwise a [y1,y2] as beginning
                 # and end of the range to draw vertical lines upon.
                 xrange    = '',

                 # How much space to skip between each x. grid line. 
                 # If log scale, this will be used in a multiplicative manner.
                 xstep     = '',

                 # Empty means whole range, otherwise a [x1,x2] as beginning
                 # and end of the range to draw horizontal lines upon.
                 yrange    = '',

                 # How much space to skip between each y grid line.
                 # if log scale, this will be used in a multiplicative manner.
                 ystep     = '',           
                 ):

        if x == True:
            self.__dogrid(drawable=drawable, axis='x', step=xstep,
                          range=xrange, linecolor=linecolor,
                          linewidth=linewidth, linedash=linedash)
        if y == True:
            self.__dogrid(drawable=drawable, axis='y', step=ystep,
                          range=yrange, linecolor=linecolor,
                          linewidth=linewidth, linedash=linedash)
    # END __init__

    def __dogrid(self,
                 drawable,
                 axis,
                 step,
                 range,
                 linecolor, linewidth, linedash):
        assert(step != '')
        if axis == 'x':
            otheraxis = 'y'
        elif axis == 'y':
            otheraxis = 'x'

        urange = []
        if range == '':
            # THIS SHOULD BE TRANSLATABLE
            urange.append(drawable.virtualmin(axis))
            urange.append(drawable.virtualmax(axis))
        else:
            urange = range
            assert(len(urange) == 2)

        # THIS SHOULD BE TRANSLATABLE
        othermin = drawable.virtualmin(otheraxis)
        othermax = drawable.virtualmax(otheraxis)

        # iterate over the range
        canvas = drawable.canvas
        for v in drawable.rangeiterator(axis, urange[0], urange[1], step):
            if axis == 'x':
                canvas.line(coord=drawable.map([[v,othermin],[v,othermax]]),
                            linecolor=linecolor, linewidth=linewidth,
                            linedash=linedash)
            if axis == 'y':
		canvas.line(coord=drawable.map([[othermin,v],[othermax,v]]),
                            linecolor=linecolor, linewidth=linewidth,
                            linedash=linedash)
    # END __dogrid()
    
# END: class grid

#
# class legend
#
# Minimal support for legends is provided.
# Initialize it first:
# L = Legend()
# Pass 'L' and other info to plotters.
# Then, call draw() to make it on the plot.
# 
class legend:
    def __init__(self
                 ):
        # 'info' field will track each picture and text in the legend
        # All the work is done later - when legend is drawn.
        self.info = []
    # END: __init__

    # 
    # legend()
    # Use this to draw a legend given the current entries in the legend.
    # Lots of options are available.
    # 
    def draw(self,
             canvas      = '',        

             # where to place the legend (lower left point)
             coord       = '',

             # which side to place the text on, right or left?
             style       = 'right',

             # width of the picture to be drawn in the legend
             width       = 10.0,

             # height of the picture to be drawn in the legend
             height      = 10.0,

             # number of points to skip when moving to next legend entry
             vskip       = 3.0,

             # space between pictures and text
             hspace      = 4.0,

             # go downward from starting spot when building the legend;
             # false goes upward
             down        = True,

             # if non-empty, how many rows of legend to print before
             # skipping to a new column
             skipnext    = '',

             # how much to move over if the 'skipnext' option is used to
             # start the next column
             skipspace   = 25.0,

             # which type face to use
             font        = 'default',

             # size of font of legend, and color
             fontsize    = 10,        
             fontcolor   = 'black',

             # can specify a specific legend order ...
             order       = [],
             ):

        if canvas == '':
            print 'error: must specify canvas when drawing legend', 
            print '(legend not drawn as result)'
            return
        assert(len(coord) == 2)
        x = coord[0]
        y = coord[1]
        w = width
        h = height

        if w < h:
            minval = w
        else:
            minval = h

        overcounter = 0
        for i in range(0, len(self.info)):
            if(len(order) > 0):
                i = order[i]

            if style == 'left':
		cx = x + hspace + (w/2.0)
		tx = x
            elif style == 'right':
		cx = x + (w/2.0)
		tx = x + w + hspace
            else:
                abort('bad style: ', style)

            # make replacements for coordinates in legend pictures
            legend = self.info[i]
            text   = legend[0]
            pic    = legend[1]

            mapped = pic.substitute(__Xx=cx, __Yy=y, __Ww=w, __Hh=h,
                                    __Mm=minval, __W2=(w/2.0), __H2=(h/2.0),
                                    __M2=(minval/2.0), __Xmm=(cx-(minval/2.0)),
                                    __Xpm=cx+(minval/2.0),
                                    __Ymm=(y-(minval/2.0)),
                                    __Ypm=(y+(minval/2.0)), __Xmw=cx-(w/2.0),
                                    __Xpw=(cx+(w/2.0)), __Ymh=(y-(h/2.0)),
                                    __Yph=(y+(h/2.0)))

            if style == 'left':
		canvas.text(coord=[tx,y], anchor='r,c', text=text, font=font,
                            color=fontcolor, size=fontsize)
		eval(mapped)
            elif style == 'right':
                for m in mapped.split(';'):
                    eval(m)
		canvas.text(coord=[tx,y], anchor='l,c', text=text, font=font,
                            color=fontcolor, size=fontsize)

            if down == True:
                y = y - height - vskip
            else:
                y = y + height + vskip

            if skipnext != '':
                overcounter = overcounter + 1
                if overcounter >= skipnext:
                    if type(skipspace) == list:
                        x += skipspace.pop(0)
                    else:
                        x = x + skipspace
                    y = coord[1]
                    overcounter = 0
        # END: for i in range...
        return
    # END: draw()

    # 
    # add()
    # 
    # command used to add some info about a legend to the legend list. If
    # 'entry' is specified, this will add the text (if any) to the existing
    # text in that spot, and also add the picture to the list of pictures to be
    # drawn for this entry. If 'entry' is not specified, simply use the current
    # counter and add this to the end of the list.
    # 
    def add(self,
            # text for the legend
            text    = '',  

            # code to add the picture to the legend: COORDX and COORDY should
            # be used to specify the lower-left point of the picture key;
            # WIDTH and HEIGHT should be used to specify the width and height
            # of the picture
            picture = '',

            # entry number: which legend entry this should be
            # (empty means auto-picked for you).
            entry   = '',   
            ):

        if entry == '':
            self.info.append([text, picture])
        else:
            self.info[entry] = [text, picture]
    # END: add()

#END: class legend
