#!/usr/bin/env python3
# coding=utf-8
'''
This code in only for SRR data
'''
__author__ = 'Guoliang Lin'
Softwarename = 'paired_end_trim'
version = '0.0.1'
bugfixs = ''
__date__ = '2018/6/27'
import optparse
import time


def printinformations():
    print("%s software version is %s in %s" % (Softwarename, version, __date__))
    print(bugfixs)
    print('Starts at :' + time.strftime('%Y-%m-%d %H:%M:%S'))


def programends():
    print('Ends at :' + time.strftime('%Y-%m-%d %H:%M:%S'))


# add your options here!
def _parse_args():
    """Parse the command line for options."""
    usage = 'usage: %prog -i INPUT -o OUTPUT'
    parser = optparse.OptionParser(usage)
    parser.add_option('-1',
                      '--R1', dest='R1', type='string',
                      help='paired end read 1')
    parser.add_option('-2',
                      '--R2', dest='R2', type='string',
                      help='paired end read 2')
    #    parser.add_option('-f','--fpkm',dest='fpkm_file',type='string',help='input fpkm file')
    #    parser.add_option('-v','--variation', dest='variation', type='string', help='input variation information file')
    #    parser.add_option('-g', '--gff3', dest='gff', help='gff3 file')
    #    parser.add_option('-o', '--output', dest='output', type='string', help='output file')
    options, args = parser.parse_args()
    # positional arguments are ignored
    return options


def returnreadsname(name):
    name = int(name.strip().split()[1])
    return name


def getnameset(fastqfile, nameset):
    print('Getting read name from {}'.format(fastqfile))
    with open(fastqfile) as read1:
        while read1:
            name = read1.readline()
            if name:
                readname = returnreadsname(name)
                if readname in nameset:
                    print("duplictes name in {} file,bye!".format(fastqfile))
                else:
                    nameset.add((readname,None))
                read1.readline()
                read1.readline()
                read1.readline()
            else:
                break
    return nameset


def writeonereads(filehandle, name1, seq, name2, q):
    filehandle.write(name1)
    filehandle.write(seq)
    filehandle.write(name2)
    filehandle.write(q)


def writetodisk(fastqfile, intersectset,dictintersectset):
    count = 0
    length=len(intersectset)
    stack = {}
    print('Write to disk as {}.pe'.format(fastqfile))
    with open(fastqfile) as reads:
        with open("{}.pe".format(fastqfile), 'w') as pe:
            with open("{}.se".format(fastqfile), 'w') as se:
                while reads:
                    name1 = reads.readline()
                    if name1:
                        readname = returnreadsname(name1)
                        seq = reads.readline()
                        name2 = reads.readline()
                        q = reads.readline()
                        if readname in dictintersectset:
                            if readname == intersectset[count][0]:
                                writeonereads(pe, name1, seq, name2, q)
                                count += 1
                                while count<length and (intersectset[count][0] in stack):
                                    writeonereads(pe, stack[intersectset[count][0]][0], stack[intersectset[count][0]][1],
                                                  stack[intersectset[count][0]][2], stack[intersectset[count][0]][3])
                                    stack.pop(intersectset[count][0])
                                    count += 1
                            else:
                                stack[readname] = [name1, seq, name2, q]
                        else:
                            writeonereads(se, name1, seq, name2, q)
                    else:
                        while count<length and (intersectset[count][0] in stack):
                            writeonereads(pe, stack[intersectset[count][0]][0], stack[intersectset[count][0]][1],
                                          stack[intersectset[count][0]][2], stack[intersectset[count][0]][3])
                            stack.pop(intersectset[count][0])
                            count += 1
                        break


# define your functions here!
def paired_end_trim(R1, R2):
    nameset1 = set()
    nameset2 = set()
    nameset1 = getnameset(R1, nameset1)
    nameset2 = getnameset(R2, nameset2)
    intersectset = nameset1 & nameset2
    # covert to list
    intersectset = list(intersectset)
    intersectset.sort(key=lambda x:x[0])
    dictintersectset=dict(intersectset)
    # print(intersectset)
    # print(dictintersectset)
    writetodisk(R1, intersectset,dictintersectset)
    writetodisk(R2, intersectset,dictintersectset)


if __name__ == '__main__':
    printinformations()
    options = _parse_args()
    # your code here!
    paired_end_trim(options.R1, options.R2)
    programends()
