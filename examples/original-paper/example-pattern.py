#! /usr/bin/env python

from zplot import *

c = postscript(title='example-pattern.eps', dimensions=[335, 40])

x = 15
y = 15

w = 20
s = 10

size, skip = 2, 4

for t in ['solid', 'hline', 'vline', 'hvline', 'dline1', 'dline2', 'dline12',
          'circle', 'square', 'triangle', 'utriangle']:
    c.text(coord=[x,y-4], text=t, size=8, anchor='c,h')

    if x > 280:
        size, skip = 4, 3
    c.box(coord=[[x-w/2.0,y],[x+w/2.0,y+w]], fill=True, fillstyle=t,
          linewidth=0.25, fillsize=size, fillskip=skip)
    x = x + w + s

c.render()




