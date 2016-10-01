#! /usr/bin/env python

def remove_char(str, c):
    s = str.split(c)
    if len(s) > 1:
        return s[0]
    return str

def remove_until_last(str, c):
    s = str.split(c)
    if len(s) == 1:
        return s
    else:
        r = s[0]
        for x in range(1, len(s)-1):
            r += ',' + s[x]
        return r

def end_class(fd):
    fd.write('</html>\n')
    fd.close()
    return

fd = open('../zplot.py')

in_class = False
in_init  = False

for line in fd:
    tmp = line.split()
    if len(tmp) == 0:
        continue
    if tmp[0] == 'class':
        if in_class:
            end_class(class_fd)
        in_class = True
        class_name = remove_char(tmp[1], '(')
        class_name = remove_char(class_name, ':')
        print '\nclass', class_name

        # nothing fancy write now - style files, etc.
        # just simple HTML to begin.
        class_fd = open(class_name + '.html', 'w')
        class_fd.write('<html>\n')
        class_fd.write('\n')
        class_fd.write('<h2> Class %s</h2>' % class_name)
        class_fd.write('\n')

    if in_init:
        # inside __init__
        # gather needed info about arguments
        if tmp[0] == '#':
            comments.append(line.strip()[2:])
        if tmp[0] != '#' and tmp[0] != '):':

            # FORMAT of this line is:
            # PARAMETER = DEFAULT ,
            print 'debug', line
            parameter = line.split('=')[0].strip()
            default = remove_until_last(line.split('=')[1], ',').strip()

            print 'parameter [%s]' % parameter

            class_fd.write('<tr>')
            class_fd.write('<td><b>%s</b></td> <td>-</td>' % parameter)
            class_fd.write('<td>default: %s</td>' % default)
            class_fd.write('<td>-</td><td>')
            comment_len = 0
            for c in comments:
                class_fd.write(' %s' % c)
                comment_len += len(c)
                if comment_len > 40:
                    comment_len = 0
                    class_fd.write('</td></tr>')
                    class_fd.write('<tr><td></td><td></td><td></td><td></td><td>')
                    
            class_fd.write('</td>')
            class_fd.write(' </tr>\n')
            
            comments = []
        if tmp[0] == '):':
            in_init = False
            class_fd.write('</table>\n')
            class_fd.write('</p>\n')
            print ''

    if in_class:
        if tmp[0] == 'def':
            # looking for __init__
            func_name = remove_char(tmp[1], '(')
            if func_name == '__init__':
                class_fd.write('<p>\n')
                class_fd.write('<b> Initialize class with following parameters:</b>\n')
                class_fd.write('<table>\n')
                in_init = True
                comments = []

# close up last class file
if in_class:
    end_class(class_fd)

fd.close()


