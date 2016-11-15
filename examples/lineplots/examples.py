#! /usr/bin/env python

#
# A fun example of a number of different point styles to use.
#

from zplot import *

ctype = 'eps' if len(sys.argv) < 2 else sys.argv[1]
c = make_canvas(ctype, 'examples', dimensions=['3.5in','2.95in'])

t = table(file='examples.data')

d = drawable(canvas=c, xrange=[0,7], yrange=[0,20],
             dimensions=['2.8in','2in'])

styles = [
    ['orange',        'square',   True],
    ['lightblue',     'circle',   True],
    ['darkblue',      'triangle', True],
    ['olivedrab',     'utriangle',True],
    ['mediumpurple',  'diamond',  True],
    ['green',         'star',     True],
    ['lightsalmon',   'xline',    False],
    ['rosybrown',     'plusline', False],
    ['mistyrose',     'hline',    False],
    ['slateblue',     'vline',    False],
    ['lightcoral',    'asterisk', False],
    ['red',           'square',   False],
    ['green',         'circle',   False],
    ['brown',         'triangle', False],
    ['black',         'utriangle',False],
    ['gray',          'diamond',  False],
    ['darkcyan',      'dline1',   False],
    ['darkgoldenrod', 'dline2',   False],
]

a = axis(drawable=d, style='box', ticstyle='centered', dominortics=True,
         xminorticcnt=2, doxminortics=False, yminorticcnt=3,
         title='Example of Lines and Points', xtitle='X title', ytitle='Y title',
         linewidth=0.5, xauto=[0,7,1], yauto=[0,20,5])

p = plotter()

L = legend()

for i in range(0,len(styles)):
    color = styles[i][0]
    style = styles[i][1]
    fill  = styles[i][2]

    p.line(drawable=d, table=t, xfield='x', yfield='y', linecolor=color,
           linewidth=0.5)
    
    if fill == True:
	p.points(drawable=d, table=t, xfield='x', yfield='y', linecolor=color,
                 linewidth=0.5, style=style, fill=True, fillcolor=color,
                 legend=L, legendtext=style)
    else:
	p.points(drawable=d, table=t, xfield='x', yfield='y', linecolor=color,
                 linewidth=0.5, style=style, legend=L, legendtext=style)

    # update column y to be higher, to plot next line in a different spot...
    t.update(set='y=y+0.75')

L.draw(canvas=c, coord=d.map([0.2,19]), width=5, height=5, fontsize=8, skipnext=5, skipspace=45)

c.render()






