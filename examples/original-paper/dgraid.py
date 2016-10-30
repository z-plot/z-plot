#! /usr/bin/env python

from zplot import *
import sys

ctype = 'eps'
if len(sys.argv) == 2:
    ctype = sys.argv[1]
c = make_canvas(canvas=ctype, title='dgraid', dimensions=[400,290])

p = plotter()

tcopy = table(file='dgraid.copy.data')
tnocopy = table(file='dgraid.nocopy.data')


# do major copy graph
copy = drawable(canvas=c, coord=[35,30], dimensions=[350,110], xrange=[0,4500], yrange=[0,8000])

p.points(drawable=copy, table=tcopy, style='xline', linewidth=0.25)
p.line(drawable=copy, table=tcopy, linewidth=0.25)
axis(drawable=copy, xtitle='Time (s)', xauto=['','',500], yauto=['','',2000], ylabeltimes=0.001, ylabelformat='%d')
 
# do closeups of copy graph
copyc1 = drawable(canvas=c, coord=[135,90], dimensions=[40,40], xrange=[700,720], yrange=[0,6000])
tcopyc1 = table(table=tcopy, where='(cast(c0 as decimal) > 700) and (cast(c0 as decimal) <= 720)')
axis(drawable=copyc1, ticmajorsize=2, xauto=['','',10], yauto=['','',2000], ylabeltimes=0.001,
     ylabelformat='%d', linecolor='darkgray', xlabelfontsize=6, ylabelfontsize=6)
p.line(drawable=copyc1, table=tcopyc1, linewidth=0.25)

copyc2 = drawable(canvas=c, coord=[325,70], dimensions=[40,40], xrange=[3280,3330], yrange=[0,6000])
tcopyc2 = table(table=tcopy, where='(cast(c0 as decimal) > 3280) and (cast(c0 as decimal) <= 3310)')
axis(drawable=copyc2, ticmajorsize=2, xauto=['','',20], yauto=['','',2000], ylabeltimes=0.001,
     ylabelformat='%d', linecolor='darkgray', xlabelfontsize=6, ylabelfontsize=6)
p.line(drawable=copyc2, table=tcopyc2, linewidth=0.25)

# finally, do nocopy graph
nocopy = drawable(canvas=c, coord=[35,160], dimensions=[350,110], xrange=[0,4500], yrange=[0,8000])
p.points(drawable=nocopy, table=tnocopy, style='plusline', linewidth=0.25)
p.line(drawable=nocopy, table=tnocopy, linewidth=0.25)
axis(drawable=nocopy, xauto=['','',500], yauto=['','',2000], ylabeltimes=0.001, ylabelformat='%d')
 
# a few labels
c.text(coord=nocopy.map([2250,8300]), text='DGRAID: Measuring Imperfect Placement', size=10)
c.text(coord=[13,150], text='Number of Misplaced Blocks (Thousands)', rotate=90, size=10)
 
# boxes around the closeup regions (though not really needed)
c.box(coord=copy.map([[650,-400],[770,6000]]), linedash=[2,2], linewidth=0.25, linecolor='black', fill=False)
c.box(coord=copy.map([[3200,-400],[3400,1000]]), linedash=[2,2], linewidth=0.25, linecolor='black', fill=False)
c.line(coord=copy.map([[780,3000],[1100,4000]]), linedash=[2,2], linewidth=0.25, linecolor='black')
c.line(coord=copy.map([[3400,1000],[3600,2000]]), linedash=[2,2], linewidth=0.25, linecolor='black')

c.render()




