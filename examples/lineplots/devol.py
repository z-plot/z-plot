#! /usr/bin/env python

from zplot import *
import sys

import sys
ctype = 'eps' if len(sys.argv) < 2 else sys.argv[1]
c = canvas(ctype, title='devol', dimensions=['400','340'])

t = table(file='devol.data')
t.addcolumns(['month','year'])
t.update(set='month = substr(date, 1, 2)')
t.update(set='year = substr(date, 4, 2)')

d = drawable(canvas=c, xrange=[-1,t.getmax(column='rownumber') + 1],
             yrange=[0,2000], coord=[40,40], dimensions=[350,270])

grid(drawable=d, ystep=200, xstep=1, linecolor='lightgrey')

axis(drawable=d, style='y', yauto=['','',200])
axis(drawable=d, style='x', xmanual=t.getaxislabels(column='month'),
     xlabelrotate=90, xlabelanchor='r,c', xlabelfontsize=7,
     title='Number of Inquiries Per Month', titlesize=8,
     titlefont='Courier-Bold', xtitle='Year and Month',
     xtitleshift=[0,-15])

# Just pick out the unique years that show up and use them to label the axis
years, xlabels = [], []
for label in t.getaxislabels(column='year'):
    if label[0] not in years:
        years.append(label[0])
        xlabels.append(label)
axis(drawable=d, style='x', xmanual=xlabels, linewidth=0, xlabelshift=[5,-15],
     xlabelrotate=0, xlabelanchor='r,c', xlabelfontsize=7, xlabelformat='\'%s')

p = plotter()
p.line(drawable=d, table=t, xfield='rownumber', yfield='value', stairstep=True,
       linecolor='purple', labelfield='value', labelsize=7, labelcolor='purple',
       labelshift=[6,0], labelrotate=90, labelanchor='l,c')

c.circle(coord=d.map([10.5,463]), radius=20, linecolor='red')

c.render()
