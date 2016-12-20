#! /usr/bin/env python

from zplot import *

c = pdf(title='simple.pdf', dimensions=[300,300])

c.line(coord=[[10,10],[290,290]])
c.line(coord=[[10,290],[290,10]])

c.line(coord=[[50,50],[50,100],[100,100],[100,50]],
       linewidth=3,
       linecolor='orange',
       linejoin=1,
       closepath=True)

c.box(coord=[[150,150],[250,250]],
      fill=True,
      fillcolor='lightblue',
      linewidth=2,
      linecolor='navy')

c.render()


