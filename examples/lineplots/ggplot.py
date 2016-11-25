#! /usr/bin/env python

from zplot import *

ctype = 'eps' if len(sys.argv) < 2 else sys.argv[1]
c = make_canvas(ctype, 'ggplot', dimensions=['3.75in','4.75in'])

t1 = table(file='ggplot.1.data')
t2 = table(file='ggplot.2.data')

xmin, xmax = 0.0025, 0.9
ymin, ymax = 0.3, 1.1
d = drawable(canvas=c, xrange=[xmin,xmax], xscale='log10',
             yrange=[ymin,ymax], yscale='log10',
             dimensions=['3.0in','4in'],
             coord=['.5in','.5in'])

c.box(coord=d.map([[xmin,ymin],[xmax,ymax]]),
      fill=True, fillcolor='lightgrey', linewidth=0)

p = plotter()

# L = legend()

axis(drawable=d, ytitle='Scaled Temperature', xtitle='Radius',
     linewidth=0, linecolor='lightgrey',
     xmanual=[['0.01', 0.01], ['0.1', 0.1]],
     ymanual=[['1', 1]], xlabelfontsize=8, ylabelfontsize=8)

grid(drawable=d, xrange=[0.01,0.1], xstep=10,
     yrange=[0.1,1], ystep=10,
     linecolor='white')
grid(drawable=d, xrange=[0.03,0.3], xstep=10,
     yrange=[0.1,1], ystep=10,
     linecolor='white', linewidth=0.2)

p.verticalfill(drawable=d, table=t1, xfield='Radius',
               yfield='up', ylofield='lo', fillcolor='lightblue')
p.verticalfill(drawable=d, table=t2, xfield='Radius',
               yfield='up', ylofield='lo', fillcolor='salmon')

p.line(drawable=d, table=t1, xfield='Radius', yfield='scaledkt',
       linecolor='black', linewidth=0.5, linedash=[2,2])
p.line(drawable=d, table=t2, xfield='Radius', yfield='scaledkt',
       linecolor='black', linewidth=1.0)

# this adds blue outlines so as to make the cross-over region clearer
p.line(drawable=d, table=t1, xfield='Radius', yfield='lo',
       linecolor='lightblue', linewidth=0.5)
p.line(drawable=d, table=t1, xfield='Radius', yfield='up',
       linecolor='lightblue', linewidth=0.5)

# 
    
# L.draw(canvas=c, coord=d.map([0.2,19]), width=5, height=5, fontsize=8, skipnext=5, skipspace=45)

c.render()








