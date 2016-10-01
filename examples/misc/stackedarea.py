#! /usr/bin/env python

from zplot import *

t = table('stackedarea.data', separator=':')
# c1 eastern   c2 central   c3 mountain   c4 pacific
# orange powderblue drabyellow drabgreen
t.addcolumns(['c1_sum', 'c2_sum', 'c3_sum', 'c4_sum'])
t.update(set='c1_sum = c1')
t.update(set='c2_sum = c1 + c2')
t.update(set='c3_sum = c1 + c2 + c3')
t.update(set='c4_sum = c1 + c2 + c3 + c4')
c = postscript(title='stackedarea.eps', dimensions=['4.5in','3in'])
d = drawable(canvas=c, dimensions=['3.5in','2.0in'], coord=['0.5in','0.5in'],
             xrange=[0,9], yrange=[0,200])
p = plotter()

plot_list = [('c4', 'drabgreen', 'pacific'),
             ('c3', 'dullyellow', 'mountain'),
             ('c2', 'powderblue', 'central'),
             ('c1', 'orange', 'eastern')]

L = legend()

for yfield, color, text in plot_list:
    p.verticalfill(drawable=d, table=t, xfield='rownumber',
                   yfield='%s_sum' % yfield, fillcolor=color,
                   legend=L, legendtext=text)

axis(drawable=d, xmanual=t.getaxislabels(column='c0'), xlabelrotate=90,
     xlabelfontsize=7, xlabelanchor='r,c', yauto=[0,200,50], ylabelfontsize=7)

L.draw(canvas=c, coord=d.map([0.5,235]), skipnext=1, skipspace=60.0)

c.render()


