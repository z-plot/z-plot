#! /usr/bin/env python

from zplot import *

c = postscript(title='scatter10.eps', dimensions=['3.5in', '3.5in'])

t = table(file='scatter10.data')
for col in ['ylo', 'yhi', 'xlo', 'xhi']:
    t.addcolumn(column=col)

d = drawable(canvas=c, xrange=[0.5,5.0], yrange=[0,70],
             dimensions=['2.5in', '2.5in'])

axis(drawable=d, yauto=['','',10], xauto=['','',0.5])

t.update(set='yhi=yval+yse')
t.update(set='ylo=yval-yse')
t.update(set='xhi=xval+xse')
t.update(set='xlo=xval-xse')

p = plotter()
p.verticalintervals(drawable=d, table=t, xfield='xval', ylofield='ylo',
                    yhifield='yhi', linecolor='orange', linewidth=0.25,
                    devwidth=2)
p.horizontalintervals(drawable=d, table=t, yfield='yval', xlofield='xlo',
                      xhifield='xhi', linecolor='orange', linewidth=0.25,
                      devwidth=2)
p.points(drawable=d, table=t, xfield='xval', yfield='yval', style='circle',
         linewidth=0, fill=True, fillcolor='blue', size=1.5)

# add a single red line for the function y = 10.9x - 3.50
p.function(drawable=d, function=lambda x: (10.9 * x) - 3.50, xrange=[0.75,5],
           step=4.25, linecolor='red', linewidth=0.5)
c.text(anchor='l', coord=d.translatecoordsingle([3.25,28]),
       text='y = 10.9x - 3.50', color='red', size=6.0, rotate=35.5)

c.render()







