#!/usr/bin/env python3
# coding=utf-8
# for hic get genome size
import optparse
import time

__author__ = 'Guoliang Lin'
Softwarename = 'getsize'
version = '0.0.1'
bugfixs = ''
__date__ = '2018/11/12'


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
    parser.add_option('-i',
                      '--input', dest='input', type='string',
                      help='input file!')
    #    parser.add_option('-f','--fpkm',dest='fpkm_file',type='string',help='input fpkm file')
    #    parser.add_option('-v','--variation', dest='variation', type='string', help='input variation information file')
    #    parser.add_option('-g', '--gff3', dest='gff', help='gff3 file')
    parser.add_option('-o', '--output', dest='output', type='string', help='output file')
    options, args = parser.parse_args()
    # positional arguments are ignored
    return options


# define your functions here!


if __name__ == '__main__':
    printinformations()
    options = _parse_args()
    # your code here!
    with open(options.input) as infile:
        with open(options.output,'w') as ofile:
            previous=""
            count=0
            for item in infile:
                item=item.strip()
                if item.find('>')!=-1:
                    ofile.write('\t'.join((previous,str(count)))+'\n')
                    previous=item[1:]
                    count=0
                else:
                    count+=len(item)
            ofile.write('\t'.join((previous,str(count)))+'\n')

    programends()