#! /usr/bin/env python

from zplot import *

c = postscript(title='lineplot20.eps', dimensions=['5.5in','4.75in'])
t = table(file='lineplot20.data')
tlo = table(table=t, where='cast(x as decimal) < 8')
thi = table(table=t, where='cast(x as decimal) > 8')

d = {}
x = 0
y = 0
for i in range(8):
    x, y = (i % 2) * 2.5, i / 2
    d[i] = drawable(canvas=c, xrange=[0,17], yrange=[0,25],
                    dimensions=['2.0in','0.9in'],
                    coord=['%.2fin' % (x + 0.5), '%.2fin' % (y + 0.5)])
    c.box(coord=d[i].map([[0,0],[17,25]]), fill=True, fillcolor='lightgrey',
          linewidth=0.0)


p = plotter()

for i in range(8):
    if i / 2 == 0:
        stairstep, filled = False, True
    elif i / 2 == 1:
        stairstep, filled = True, True
    elif i / 2 == 2:
        stairstep, filled = False, False
    elif i / 2 == 3:
        stairstep, filled = True, False

    skip = False
    if i % 2 == 1:
        skip = True

    if skip:
        for ttmp in [tlo, thi]:
            if filled:
                p.verticalfill(drawable=d[i], table=ttmp, xfield='x', yfield='y',
                               fillcolor='pink', stairstep=stairstep)
            p.line(drawable=d[i], table=ttmp, xfield='x', yfield='y',
                   linecolor='red', stairstep=stairstep)
    else:
        if filled:
            p.verticalfill(drawable=d[i], table=t, xfield='x', yfield='y',
                           fillcolor='pink', stairstep=stairstep)
        p.line(drawable=d[i], table=t, xfield='x', yfield='y',
               linecolor='red', stairstep=stairstep)

c.text(coord=d[6].map([8.5,28]), text='no gap', size=8.0)
c.text(coord=d[7].map([8.5,28]), text='gap', size=8.0)

c.text(coord=d[6].map([-1,13]), text='stairstep', size=8.0, rotate=90,
       anchor='c,c')
c.text(coord=d[2].map([-1,13]), text='stairstep', size=8.0, rotate=90,
       anchor='c,c')

c.text(coord=d[3].map([18,13]), text='filled', size=8.0, rotate=90,
       anchor='c,c')
c.text(coord=d[1].map([18,13]), text='filled', size=8.0, rotate=90,
       anchor='c,c')


c.render()

