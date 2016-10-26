#! /usr/bin/env python

from zplot import *

def make_pattern(xlo, xhi, step, ylo, yhi):
    rlist = []
    x = xlo
    rlist.append([x, ylo])
    counter = 0
    for x in range(xlo + step, xhi, step):
        if counter == 0:
            rlist.append([x, ylo])
            rlist.append([x, yhi])
        else:
            rlist.append([x, yhi])
            rlist.append([x, ylo])
        counter = 1 - counter
    if counter == 0:
        rlist.append([xhi, ylo])
    else:
        rlist.append([xhi, yhi])
    return rlist
        
c = postscript(title='example-psline.eps', dimensions=[90, 90])

c.text(coord=[17.5,15], text='linecap=0', size=7)
c.line(coord=make_pattern(5, 30, 5, 5, 10), linecolor='black')

c.text(coord=[17.5,45], text='linecap=1', size=7)
c.line(coord=make_pattern(5, 30, 5, 35, 40), linecap=1, linecolor='black')

c.text(coord=[17.5,75], text='linecap=2', size=7)
c.line(coord=make_pattern(5, 30, 5, 65, 70), linecap=2, linecolor='black')

c.text(coord=[67.5,15], text='linejoin=0', size=7)
c.line(coord=make_pattern(55, 80, 5, 5, 10), linecolor='black')

c.text(coord=[67.5,45], text='linejoin=1', size=7)
c.line(coord=make_pattern(55, 80, 5, 35, 40), linecolor='black', linejoin=1)

c.text(coord=[67.5,75], text='linejoin=2', size=7)
c.line(coord=make_pattern(55, 80, 5, 65, 70), linecolor='black', linejoin=2)

c.render()





