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

def get_parameter(class_fd, line, comments):
    # FORMAT of this line is:
    #   PARAMETER = DEFAULT ,

    parameter = line.split('=')[0].strip()
    print '  parameter [%s]' % parameter

    if len(line.split('=')) == 1:
        return
    else:
        default = remove_until_last(line.split('=')[1], ',').strip()


    class_fd.write('<tr>')
    class_fd.write('<td style="width:150px"><b>%s</b></td>' % parameter)
    class_fd.write('<td style="width:10px"></td>')
    class_fd.write('<td style="width:150px">default: %s</td>' % default)
    class_fd.write('<td style="width:10px"></td><td>')
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
    return        


fd = open('../zplot.py')

in_class  = False
in_init   = False
in_method = False

for line in fd:
    # print 'debug', line
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

    if len(tmp) == 3 and tmp[0] == '#' and tmp[1] == '--method--':
        method_name = tmp[2]
        print 'class %s: method %s()' % (class_name, method_name)
        class_fd.write('\n')
        class_fd.write('<h3> Method %s</h3>' % method_name)
        class_fd.write('<table>\n')
        in_method = True

    if in_init or in_method:
        # inside __init__
        # gather needed info about arguments
        if tmp[0] == 'def':
            # this means we are done with the comments
            class_fd.write('\n')
            class_fd.write('<p>')
            for c in comments:
                class_fd.write(' %s' % c)
            class_fd.write('</p>')
            class_fd.write('\n')
            
        if tmp[0] == '#':
            potential_comment = line.strip()[2:]
            if len(tmp) > 1 and tmp[1] != '--method--':
                comments.append(potential_comment)
            if len(tmp) == 1:
                comments.append('\n')
        if tmp[0] != '#' and tmp[0] != '):':
            get_parameter(class_fd, line, comments)
            comments = []
        if tmp[0] == '):':
            in_init, in_method = False, False
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


