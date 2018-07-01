#!/usr/bin/env python3
# coding=utf-8
import optparse
import re
import time

__author__ = 'Guoliang Lin'
Softwarename = 'getchimericreads'
version = '0.0.1'
bugfixs = ''
__date__ = '2018/6/29'



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
                      help='input sam format file!')
    #    parser.add_option('-f','--fpkm',dest='fpkm_file',type='string',help='input fpkm file')
    #    parser.add_option('-v','--variation', dest='variation', type='string', help='input variation information file')
    #    parser.add_option('-g', '--gff3', dest='gff', help='gff3 file')
    # parser.add_option('-o', '--output', dest='output',default="", type='string', help='')
    options, args = parser.parse_args()
    # positional arguments are ignored
    return options


# ===============================================================================================
#
# ===============================================================================================


def splitpatten(string: str) -> list:
    '''

    :param string: str
    :return:
    '''
    patten = re.split(r'(\d+)', string)[1:]
    return patten


def ischimeric(pattens: list) -> bool:
    '''

    :param pattens:
    :return:
    '''
    for patten in pattens:
        listpatten = splitpatten(patten)
        for i in range(len(listpatten)):
            if (listpatten[i] == "H" or listpatten[i] == "S") and int(listpatten[i - 1]) >= 25:
                return True
    return False


def writesamtodisk(pattens: list, readscontainer: list, outputfile):
    if ischimeric(pattens):
        for x in readscontainer:
            outputfile.write(x)


def trimhead(infile):
    '''
    Trim the sam head section.
    :return: string head sections
    '''
    headstring = ""
    while True:
        filepointer = infile.tell()
        x = infile.readline()
        if x.find("@") == 0:
            headstring += x
        else:
            infile.seek(filepointer)
            break
    return headstring


# define your functions here!
def getchimericreads(insam):
    with open(insam) as inputfile:
        with open(insam[:-4] + "_chimeric.sam", 'w') as outputfile:
            head = trimhead(inputfile)
            outputfile.write(head)
            readscontainer = []
            pattens = []
            readsname = ''
            for item in inputfile:
                tempitem = item.split('\t')
                tempname = tempitem[0]
                if tempname == readsname:
                    readscontainer.append(item)
                    if ("S" in tempitem[5]) or ("H" in tempitem[5]):
                        pattens.append(tempitem[5])
                else:
                    writesamtodisk(pattens, readscontainer, outputfile)
                    readscontainer = [item]
                    readsname = tempname
                    pattens = []
            writesamtodisk(pattens, readscontainer, outputfile)


if __name__ == '__main__':
    printinformations()
    options = _parse_args()
    # your code here!
    getchimericreads(options.input)
    programends()
