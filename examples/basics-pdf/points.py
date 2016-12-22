#! /usr/bin/env python

from zplot import *

# populate zplot table from data file
t = table('points.data')

# create the postscript file we'll use as our canvas
canvas = pdf('points.pdf')

# a drawable is a region of a canvas, and is used to convert data
# coordinates to raw pixel coordinates on the canvas, based on
# xrange and yrange.
d = drawable(canvas, xrange=[0,15], yrange=[0,25])

# create an axis for our drawable.  Specify axis labels with
# [START,END,STEP] via xauto and yauto.
axis(d, xtitle='Cost ($)', xauto=[0,15,3],
     ytitle='Latency (ms)', yauto=[0,25,5])

# a plotter fetches coordinates from the table, querying for the
# specified xfield and yfield.  These are converted to pixel
# coordinates using the drawable.  The pixel coordinates are then
# used to draw the points on the canvas.
p = plotter()
p.points(d, t, xfield='cost', yfield='latency',
         style='circle', fill=True, fillcolor='red',
         size=3, linewidth=0.5)
  
# save to eps file
canvas.render()
