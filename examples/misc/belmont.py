#! /usr/bin/env python

from zplot import *

# define the canvas
import sys
ctype = 'eps' if len(sys.argv) < 2 else sys.argv[1]
c = canvas(ctype, title='belmont', dimensions=['8.5in', '3.6in'])

colors = {}
colors['runavg'] = 'forestgreen'
colors['best']   = 'orange'

# read in the file into a table called bar1
t = table(file='belmont.data', separator=':')
t.addcolumns(columns=['zero'])

# get last value from table, add something to it
maxyear = t.getmax(column='year')

# this defines one particular drawing area
d1 = drawable(canvas=c, xrange=[1925,2010], yrange=[138,156], coord=[40,30],
              dimensions=['7.7in','2.9in'])
d2 = drawable(canvas=c, xrange=[1925,2010], yrange=[0,1], coord=[40,30],
              dimensions=['7.7in','2.9in'])

mean = 149.19
stddev = 1.78357
c.box(coord=d1.map([[1926,mean-stddev],[2007,mean+stddev]]), linewidth=0,
      fill=True, fillcolor='lightgrey')

# make colored backgrounds
for y in range(1925,2011,2):
    c.box(coord=d1.map([[y,138],[y+1,156]]), linewidth=0, fill=True,
          fillcolor='lavender')

# should calculate this!
c.line(coord=d1.map([[1926.5,mean],[2007.5,mean]]), linewidth=0.5, linedash=[2,2])

# labels
c.text(coord=d1.map([1935.5,mean-3]), text='Overall Average' + \
       '(%.2f +/- %.2f)' % (mean, stddev), size=7, anchor='l,c')
c.line(coord=d1.map([[1935,mean-3],[1930,mean-0.6]]), arrow=True, linewidth=0.5)

c.text(coord=d1.map([1946.5,154]), text='Running Average', size=7, anchor='l,c',
       color=colors['runavg'])
c.line(coord=d1.map([[1946,154],[1938,152]]), arrow=True, linewidth=0.5,
       linecolor=colors['runavg'], arrowfillcolor=colors['runavg'],
       arrowlinecolor=colors['runavg'])

axis(drawable=d1, xtitle='Year', ytitle='Time (Seconds)', title='Belmont',
     yauto=[138,156,2], xauto=[1930,2010,10])

p = plotter()
p.line(drawable=d1, table=t, xfield='year', yfield='time', linecolor='black',
       linewidth=0.5, stairstep=True)

t.update(set='year=year+0.5')
p.line(drawable=d2, table=t, xfield='year', yfield='zero', labelfield='horse',
       labelrotate=90.0, labelsize=6, labelanchor='l,c')
p.line(drawable=d1, table=t, xfield='year', yfield='runavg', linewidth=0.5,
       linecolor=colors['runavg'])
c.line(coord=d1.map([[2007,148.74],[2008,148.74]]), linewidth=0.5)

c.text(coord=d1.map([1977,144]), text='Why we remember Secretariat',
       anchor='l,c', color=colors['best'], size=7)
coords = d2.map([1973.5,0])
c.text(coord=[coords[0], coords[1]+3], anchor='l,c', rotate=90.0,
       text='Secretariat', size=6, color=colors['best'], 
       bgcolor='lavender')

c.line(coord=d1.map([[1976.5,144],[1975,144]]), arrow=True, linewidth=0.5,
       arrowfillcolor=colors['best'], arrowfill=colors['best'],
       linecolor=colors['best'], arrowlinecolor=colors['best'])

c.render()


