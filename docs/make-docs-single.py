#! /usr/bin/env python

#
# make-docs-single
#
# A pretty ugly little program to strip comments
# out of the zplot.py file and make some rudimentary
# documentation.
#

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
    return

def output_comments_para(class_fd, comments):
    class_fd.write('\n')
    class_fd.write('<p>')
    for c in comments:
        class_fd.write(' %s' % c)
    class_fd.write('</p>')
    class_fd.write('\n')
    return

# FORMAT of this line is:
#   PARAMETER = DEFAULT ,
def get_parameter(class_fd, line, comments):
    global ignore_class
    
    parameter = line.split('=')[0].strip()
    print '  parameter [%s]' % parameter

    if len(line.split('=')) == 1:
        return
    else:
        default = remove_until_last(line.split('=')[1], ',').strip()

    if ignore_class:
        return

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


fd = open('../zplot/zplot.py')

class_fd = open('./in.docs.html', 'w')

in_class     = False
in_init      = False
in_method    = False
ignore_class = False

comments = []

for line in fd:
    # print 'debug', line
    tmp = line.split()
    if len(tmp) == 0:
        continue

    if tmp[0] == '#':
        potential_comment = line.strip()[2:]
        comments.append(potential_comment)

    if tmp[0] == '#' and len(tmp) > 1 and \
           (tmp[1] == '--class--' or tmp[1] == '--method--'):
        ignore_class = False
        if len(tmp) > 3 and tmp[3] == 'IGNORE':
            ignore_class = True
            print 'ignore', line
        comments = []

    # look for actual beginning of "class" 
    if tmp[0] == 'class':
        if in_class:
            end_class(class_fd)
        in_class = True

        class_name = remove_char(tmp[1], '(')
        class_name = remove_char(class_name, ':')
        print '\nclass', class_name

        # nothing fancy write now - style files, etc.
        # just simple HTML to begin.
        # class_fd = open(class_name + '.html', 'w')
        # class_fd.write('<html>\n')
        if ignore_class == False:
            class_fd.write('\n')
            class_fd.write('<h2 id=%s> </h2><p>.</p>' % class_name)
            class_fd.write('<h2> Class %s</h2>' % class_name)
            class_fd.write('\n')
            output_comments_para(class_fd, comments)

    if len(tmp) == 3 and tmp[0] == '#' and tmp[1] == '--method--':
        method_name = tmp[2]
        print 'class %s: method %s()' % (class_name, method_name)
        if ignore_class == False:
            class_fd.write('\n')
            class_fd.write('<h3 id=%s_%s> %s.%s()</h3>' % (class_name, method_name,
                                                           class_name, method_name))
            class_fd.write('<table>\n')
        in_method = True

    if in_init or in_method:
        # inside __init__
        # gather needed info about arguments
        if tmp[0] == 'def':
            # seeing 'def' means we are done with the comments
            if ignore_class == False:
                output_comments_para(class_fd, comments)
        if tmp[0] != '#' and tmp[0] != '):':
            get_parameter(class_fd, line, comments)
            comments = []
        if tmp[0] == '):':
            in_init, in_method = False, False
            if ignore_class == False:
                class_fd.write('</table>\n')
                class_fd.write('</p>\n')
            print ''

    if in_class:
        if tmp[0] == 'def':
            comments = []
            # looking for __init__
            func_name = remove_char(tmp[1], '(')
            if func_name == '__init__':
                if ignore_class == False:
                    class_fd.write('<p>\n')
                    class_fd.write('<b>Initialize with following parameters:</b>\n')
                    class_fd.write('<table>\n')
                in_init = True
                comments = []

# close up last class file
if in_class:
    end_class(class_fd)

fd.close()




