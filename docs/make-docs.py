#! /usr/bin/env python

def remove_char(str, c):
    s = str.split(c)
    if len(s) > 1:
        return s[0]
    return str

fd = open('zplot.py')

in_class = False
in_init  = False

for line in fd:
    tmp = line.split()
    if len(tmp) == 0:
        continue
    if tmp[0] == 'class':
        in_class = True
        class_name = remove_char(tmp[1], '(')
        class_name = remove_char(class_name, ':')
        print '\nclass', class_name

    if in_init:
        # inside __init__
        # gather needed info about arguments
        if tmp[0] == '#':
            comments.append(line.strip()[2:])
        if tmp[0] != '#' and tmp[0] != '):':
            print line.strip(),
            for c in comments:
                print c,
            print ''
            comments = []
        if tmp[0] == '):':
            in_init = False
            print ''

    if in_class:
        if tmp[0] == 'def':
            # looking for __init__
            func_name = remove_char(tmp[1], '(')
            if func_name == '__init__':
                print func_name
                in_init = True
                comments = []

fd.close()


