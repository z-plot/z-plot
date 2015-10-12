#! /usr/bin/env python
import os

# pull in zplot from parent directory
CODE_DIR = os.path.dirname(os.path.abspath(__file__))
os.sys.path.append(os.path.dirname(CODE_DIR))
from zplot import *

def main():
    # populate zplot table from data file
    t = table(os.path.join(CODE_DIR,'data','latency-breakdown.dat'))

    # create the postscript file we'll use as our canvas
    canvas = postscript('verticalbars.eps')

    # on the x-axis, we want categories, not numbers.  Thus, we
    # determine the number of categories by checking the max
    # "rownumber" (a field automatically added by zplot).  We want a
    # half bar width (0.5) to the left and right of the bar locations
    # so we don't overflow the drawable.
    d = drawable(canvas,
                 xrange=[-0.5,t.getmax('rownumber')+0.5],
                 yrange=[0,80])

    # xmanual is a list of the form [(label1,x1), (label2,x2), ...].
    # We want to use the "op" field from the data file as our labels
    # and use "rownumber" as our x coordinate.
    axis(d,
         xtitle='Operation', xmanual=t.query(select='op,rownumber'),
         ytitle='Latency (ms)', yauto=[0,80,20])

    # we are going to create several bars with similar arguments.  One
    # easy way to do this is to put all the arguments in a dict, and
    # use Python's special syntax ("**") for using the dict as named
    # args.  Then we can tweak the args between each call to
    # verticalbars.
    #
    # yfield determines the bar height, and stackfields determines
    # where the bottom of a bar starts.  This is useful for showing
    # several bar sections to indicate a breakdown.  After the first
    # bar, we append the previous yfield to stackfields to stack the
    # bars.
    p = plotter()
    leg = legend()
    barargs = {'drawable':d, 'table':t, 'xfield':'rownumber',
               'linewidth':0, 'fill':True, 'barwidth':0.8,
               'legend':leg, 'stackfields':[]}

    # compute bar
    barargs['yfield'] = 'compute'
    barargs['legendtext'] = 'CPU'
    barargs['fillcolor'] = 'red'
    p.verticalbars(**barargs)

    # network bar
    barargs['stackfields'].append(barargs['yfield'])
    barargs['yfield'] = 'network'
    barargs['legendtext'] = 'Net'
    barargs['fillcolor'] = 'green'
    p.verticalbars(**barargs)

    # storage bar
    barargs['stackfields'].append(barargs['yfield'])
    barargs['yfield'] = 'storage'
    barargs['legendtext'] = 'Disk'
    barargs['fillcolor'] = 'blue'
    p.verticalbars(**barargs)

    # we want legend entries to be all on one line.  Thus, we use
    # skipnext=1 to get one row.  We specify the horizontal space
    # between legend symbols (not considering text) with skipspace.
    leg.draw(canvas, coord=[d.left()+30, d.top()-5],
             skipnext=1, skipspace=40)
  
    canvas.render()

if __name__ == '__main__':
    main()
