#!/usr/bin/env python3
# coding=utf-8
import optparse
import time
import os

__author__ = 'Guoliang Lin'
Softwarename = 'massproduce'
version = '0.0.1'
bugfixs = ''
__date__ = '2018/11/24'


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
prefix="/home/luoj/data/GM12878RNA/SRR3192396/anno/"
prefixdata="/home/luoj/data/GM12878RNA/{0}/"
SRR3192396="SRR3192396"
SRR3192397="SRR3192397"
sam="{0}_gsnap2012_sort.bam"
bai="{0}_gsnap2012_sort.bam.bai"
bam1="{0} {1}".format(prefixdata.format(SRR3192396)+sam.format(SRR3192396),sam.format(SRR3192396))
bai1="{0} {1}".format(prefixdata.format(SRR3192396)+bai.format(SRR3192396),bai.format(SRR3192396))
bam2="{0} {1}".format(prefixdata.format(SRR3192397)+sam.format(SRR3192397),sam.format(SRR3192397))
bai2="{0} {1}".format(prefixdata.format(SRR3192397)+bai.format(SRR3192397),bai.format(SRR3192397))

ln="ln -s {0};ln -s {1};ln -s {2};ln -s {3}".format(bam1,bam2,bai1,bai2)


if __name__ == '__main__':
    printinformations()
    options = _parse_args()
    # your code here!
    with open(options.input) as infile:
        for item in infile:
            item=item.strip()
            os.system("cat run.sh | sed 's/LINGENE\/LINGENE/{0}\/{0}/g'> ./{0}/test_run.sh".format(item))
            os.system("cd {0};{3};sh test_run.sh {1} {2} 1 >logs.out 2>logs.err".format(item,sam.format(SRR3192396),sam.format(SRR3192397),ln))
    programends()