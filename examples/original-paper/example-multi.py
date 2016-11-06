#! /usr/bin/env python

from zplot import *

# describe the drawing surface
import sys
ctype = 'eps' if len(sys.argv) < 2 else sys.argv[1]
c = make_canvas(ctype, title='example-multi', dimensions=[300,210])

t = table(file='example-multi.data')
t.addcolumns(columns=['ylower','yhigher'])
t.update(set='ylower=ylo-1')
t.update(set='yhigher=yhi+1')

# lines
d1 = drawable(canvas=c, xrange=[0,11], yrange=[0,10], coord=[10,10], dimensions=[60,40])
axis(drawable=d1, title='Lines', domajortics=False, dolabels=False)
p = plotter()
p.line(drawable=d1, table=t, xfield='x', yfield='y', linewidth=0.5)

# points
d23 = drawable(canvas=c, xrange=[0,11], yrange=[0,10], coord=[80,10], dimensions=[60,40])
axis(drawable=d23, title='Points', domajortics=False, dolabels=False)
p.points(drawable=d23, table=t, xfield='x', yfield='y', style='xline', linewidth=0.5)

# linespoints
d2 = drawable(canvas=c, xrange=[0,11], yrange=[0,10], coord=[150,10], dimensions=[60,40])
axis(drawable=d2, title='Lines + Points', domajortics=False, dolabels=False)
p.line(drawable=d2, table=t, xfield='x', yfield='y', linewidth=0.5)
p.points(drawable=d2, table=t, xfield='x', yfield='y', style='xline', linewidth=0.5)

# filled 
d3 = drawable(canvas=c, xrange=[0,11], yrange=[0,10], coord=[220,10], dimensions=[60,40])
axis(drawable=d3, title='Filled', domajortics=False, dolabels=False)
p.verticalfill(drawable=d3, table=t, xfield='x', yfield='y')
p.line(drawable=d3, table=t, xfield='x', yfield='y', linewidth=0.5)

# error bars
da = drawable(canvas=c, xrange=[0,11], yrange=[0,10], coord=[10,80], dimensions=[60,40])
axis(drawable=da, title='Error Bars', domajortics=False, dolabels=False)
p.verticalintervals(drawable=da, table=t, xfield='x', ylofield='ylo', yhifield='yhi', devwidth=4, linewidth=0.5)
p.points(drawable=da, table=t, xfield='x', yfield='y', style='circle', linewidth=0.5, size=0.5)

# box plots
db = drawable(canvas=c, xrange=[0,11], yrange=[0,10], coord=[80,80], dimensions=[60,40])
axis(drawable=db, title='Box Plots', domajortics=False, dolabels=False)
p.verticalintervals(drawable=db, table=t, xfield='x', ylofield='ylower', yhifield='yhigher', devwidth=4, linewidth=0.5)
p.verticalbars(drawable=db, table=t, xfield='x', ylofield='ylo', yfield='yhi', fill=True, fillcolor='lightgrey', linewidth=0.5, barwidth=0.8)
p.points(drawable=db, table=t, xfield='x', yfield='y', style='circle', linewidth=0.5, size=0.5)

# hintervals
dc = drawable(canvas=c, xrange=[0,11], yrange=[0,10], coord=[150,80], dimensions=[60,40])
axis(drawable=dc, title='Intervals', domajortics=False, dolabels=False)
p.horizontalintervals(drawable=dc, table=t, yfield='x', xlofield='ylo', xhifield='yhi', linewidth=0.5, devwidth=4)

# functions
dd = drawable(canvas=c, xrange=[0,11], yrange=[0,10], coord=[220,80], dimensions=[60,40])
axis(drawable=dd, title='Functions', domajortics=False, dolabels=False)
p.function(drawable=dd, function=lambda x: x, xrange=[0,10], step=0.1, linewidth=0.5)
p.function(drawable=dd, function=lambda x: x * x, xrange=[0,3.16], step=0.01, linewidth=0.5)
p.function(drawable=dd, function=lambda x: 2 * x, xrange=[0,5], step=0.1, linewidth=0.5)
c.text(coord=dd.map([1.5,9]), text='y=x*x', size=6)
c.text(coord=dd.map([5.5,8]), text='y=x', size=6)
c.text(coord=dd.map([7.5,5]), text='y=2x', size=6)

# bars
d5 = drawable(canvas=c, xrange=[0,11], yrange=[0,10], coord=[10,150], dimensions=[60,40])
axis(drawable=d5, title='Vertical Bars', domajortics=False, dolabels=False)
p.verticalbars(drawable=d5, table=t, xfield='x', yfield='y', barwidth=0.8, fillcolor='lightgrey', linewidth=0, fill=True)

# stacked bars
d55 = drawable(canvas=c, xrange=[0,11], yrange=[0,10], coord=[80,150], dimensions=[60,40])
axis(drawable=d55, title='Stacked Bars', domajortics=False, dolabels=False)
p.verticalbars(drawable=d55, table=t, xfield='x', yfield='y', barwidth=0.8, fillcolor='lightgrey', linewidth=0, fill=True)
p.verticalbars(drawable=d55, table=t, xfield='x', yfield='ylo', barwidth=0.8, fillcolor='darkgray', linewidth=0, fill=True)

# bars
d6 = drawable(canvas=c, xrange=[0,11], yrange=[0,10], coord=[150,150], dimensions=[60,40])
axis(drawable=d6, title='Horizontal Bars', domajortics=False, dolabels=False)
p.horizontalbars(drawable=d6, table=t, xfield='x', yfield='y', barwidth=0.8, fillcolor='lightgrey', linewidth=0, fill=True)

# heat
#Table -table h -file "file.heat"
h = table(file='example-multi.heat')
d7 = drawable(canvas=c, xrange=[0,6], yrange=[0,6], coord=[220,150], dimensions=[60,40])
p.heat(drawable=d7, table=h, xfield='c0', yfield='c1', hfield='c2', divisor=4.0)
axis(drawable=d7, title='Heat', domajortics=False, dolabels=False)

# finally, output the graph to a file
c.render()
