#! /usr/bin/env python

from zplot import *

t = table(file='propbars2.data')

# make cumulative across columns with simple SQL updates
t.addcolumns('USA_2', 'Britain_2', 'USSR_2', 'France_2', 'Other_2')
t.update(set='USA_2 = USA')
t.update(set='Britain_2 = USA_2 + Britain')
t.update(set='USSR_2 = Britain_2 + USSR')
t.update(set='France_2 = USSR_2 + France')
t.update(set='Other_2 = France_2 + Other')

c = postscript(dimensions=[100, 200], title='propbars2.eps')
d = drawable(canvas=c, xrange=[-0.6,0.6], yrange=[0,100], coord=[4,4],
             dimensions=[92,180])

p = plotter()

for country, color in [('Other', 'mediumpurple'), ('France', 'pink'),
                    ('USSR', 'salmon'), ('Britain', 'yellowgreen'),
                    ('USA', 'lightblue')]:
    p.verticalbars(drawable=d, table=t, xfield='rownumber',
                   yfield=country + '_2', linewidth=0, fill=True,
                   fillcolor=color, labelfield=country, labelplace='i',
                   labelformat=country + ' %s%%')

c.text(coord=d.map([0,102]), text='Arms Exporters', font='Courier-Bold')

c.render()




