#! /usr/bin/env python

import os

from zplot import *

# populate zplot table from data file
t = table('horizontalbars.data')

# create the postscript file we'll use as our canvas
canvas = postscript('horizontalbars.eps')

# on the y-axis, we want categories, not numbers.  Thus, we
# determine the number of categories by checking the max
# "rownumber" (a field automatically added by zplot).  We want a
# half bar width (0.5) to the left and right of the bar locations
# so we don't overflow the drawable.
d = drawable(canvas, xrange=[0,80], yrange=[-0.5,t.getmax('rownumber')+0.5])

# ymanual is a list of the form [(label1,y1), (label2,y2), ...].
# We want to use the "op" field from the data file as our labels
# and use "rownumber" as our y coordinate.
axis(d, xtitle='Latency (ms)', xauto=[0,80,20],
         ytitle='Operation', ymanual=t.query(select='op,rownumber'))

# we are going to create several bars with similar arguments.  One
# easy way to do this is to put all the arguments in a dict, and
# use Python's special syntax ("**") for using the dict as named
# args.  Then we can tweak the args between each call to horizontalbars.
#
# xfield determines the bar length, and stackfields determines
# where the base of a bar starts.  This is useful for showing
# several bar sections to indicate a breakdown.  After the first
# bar, we append the previous xfield to stackfields to stack the bars.
p = plotter()
L = legend()
barargs = {'drawable':d, 'table':t, 'yfield':'rownumber',
           'linewidth':0, 'fill':True, 'barwidth':0.8,
           'legend':L, 'stackfields':[]}

# compute bar
barargs['xfield'] = 'compute'
barargs['legendtext'] = 'CPU'
barargs['fillcolor'] = 'red'
p.horizontalbars(**barargs)

# network bar
barargs['stackfields'].append(barargs['xfield'])
barargs['xfield'] = 'network'
barargs['legendtext'] = 'Net'
barargs['fillcolor'] = 'green'
p.horizontalbars(**barargs)

# storage bar
barargs['stackfields'].append(barargs['xfield'])
barargs['xfield'] = 'storage'
barargs['legendtext'] = 'Disk'
barargs['fillcolor'] = 'blue'
p.horizontalbars(**barargs)

# we want legend entries to be all on one line.  Thus, we use
# skipnext=1 to get one row.  We specify the horizontal space
# between legend symbols (not considering text) with skipspace.
L.draw(canvas, coord=[d.left()+30, d.top()-5], skipnext=1, skipspace=40)
  
canvas.render()

