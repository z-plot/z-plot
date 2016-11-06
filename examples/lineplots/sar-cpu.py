#! /usr/bin/env python

from zplot import *
import sys

ctype = 'eps' if len(sys.argv) < 2 else sys.argv[1]
c = make_canvas(ctype, title='sar-cpu', dimensions=['7in','4in'])
t = table(file='sar-cpu.data')

# convert time into just seconds for easy plotting
# (plotters don't understand time natively)
t.addcolumn('ntime')
t.update(set='ntime = strftime(\'%H\', time) * 3600' + \
         '+ strftime(\'%M\', time) * 60' + \
         '+ strftime(\'%S\', time)')
         
d = drawable(canvas=c, xrange=[0,75000], yrange=[0,100],
             dimensions=['6in','3in'], coord=['0.5in', '0.4in'])

seconds = 0
hour    = 0
xlabels = []
while seconds < 70000:
    if hour % 24 >= 12:
        ampm = 'pm'
    else:
        ampm = 'am'

    if hour % 12 == 0:
        xlabels.append(['%d %s' % (12, ampm), seconds])
    else:
        xlabels.append(['%d %s' % (hour % 12, ampm), seconds])
    hour += 2
    seconds += 7200
    
axis(drawable=d, style='xy', ticstyle='out', dominortics=True,
     xminorticcnt=2, doxminortics=False, yminorticcnt=3,
     title='% CPU Utilization', titlefont='Courier-Bold',
     xtitle='', ytitle='', linewidth=0.5,
     xmanual=xlabels, yauto=[0,100,10])

p = plotter()
L = legend()
p.line(drawable=d, table=t, xfield='ntime', yfield='wio', linecolor='blue',
       linewidth=0.5, legend=L, legendtext='wio')
p.line(drawable=d, table=t, xfield='ntime', yfield='sys', linecolor='red',
       linewidth=0.5, legend=L, legendtext='sys')
p.line(drawable=d, table=t, xfield='ntime', yfield='usr', linecolor='green',
       linewidth=0.5, legend=L, legendtext='usr')
    
# legend
L.draw(canvas=c, coord=d.map([50000,90]), fontsize=8)

# all done
c.render()






