#!/usr/bin/env python3
# coding=utf-8
import optparse
import time
import subgenome
# import caculatebedlength

__author__ = 'Guoliang Lin'
Softwarename = 'calssifysubgenome'
version = '0.0.1'
bugfixs = ''
__date__ = '18-7-2'


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
lengthm=0
lengthp=0
subgenome.getscafflodinformation()

def caculatebedlength():
    with open("merged.bed") as inputfile:
        lengthm=0
        lengthp=0
        for item in inputfile:
            item=item.strip()
            itemlist=item.split("\t")
            if itemlist[0] in subgenome.scaffoldm:
                lengthm += (int(itemlist[2])-int(itemlist[1])+1)
            elif itemlist[0] in subgenome.scaffoldp:
                lengthp += (int(itemlist[2])-int(itemlist[1])+1)
    return lengthm,lengthp

def caculateratio(file,lm,lp):
    coverage=3
    tag=3
    snvdcitp={}
    snvdcitm={}
    with open(file) as inputfile:
        for item in inputfile:
            item=item.strip()
            itemlist=item.split("\t")
            tempPosition='\t'.join(itemlist[0:tag])
            if (itemlist[0] in subgenome.scaffoldm) and int(itemlist[4])>=coverage:
                if tempPosition in snvdcitm:
                    if itemlist[tag] not in snvdcitm[tempPosition]:
                        snvdcitm[tempPosition].append(itemlist[tag])
                else: snvdcitm[tempPosition]=[itemlist[tag]]
            elif itemlist[0] in subgenome.scaffoldp and int(itemlist[4])>=coverage :
                if tempPosition in snvdcitp:
                    if itemlist[tag] not in snvdcitp[tempPosition]:
                        snvdcitp[tempPosition].append(itemlist[tag])
                else: snvdcitp[tempPosition]=[itemlist[tag]]
    print("the subgenome one ratio is {}, subgenome two ratio is {}".format(len(snvdcitm)/lm,len(snvdcitp)/lp))

printinformations()
options = _parse_args()
# your code here!
lengthm,lengthp=caculatebedlength()
print("Caculate the ratio of triploid")
caculateratio("8952-gan-merged.snv",lengthm,lengthp)
print("Caculate the ratio of diploid")
caculateratio("16001-gan-merged.snv",lengthm,lengthp)

programends()