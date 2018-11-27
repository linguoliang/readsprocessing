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
sam="{0}_gsnap2012_fix_srt_rmdup.bam"
bai="{0}_gsnap2012_fix_srt_rmdup.bam.bai"
bam1="{0} {1}".format(prefixdata.format(SRR3192396)+sam.format(SRR3192396),sam.format(SRR3192396))
bai1="{0} {1}".format(prefixdata.format(SRR3192396)+bai.format(SRR3192396),bai.format(SRR3192396))
bam2="{0} {1}".format(prefixdata.format(SRR3192397)+sam.format(SRR3192397),sam.format(SRR3192397))
bai2="{0} {1}".format(prefixdata.format(SRR3192397)+bai.format(SRR3192397),bai.format(SRR3192397))
countsfile="./{2}/{0}_gsnap2012_fix_srt_rmdup.results.noExEx.peak.sam.recursive_counts.txt{1}"
matrixfile="./{2}/{0}_gsnap2012_fix_srt_rmdup.results.noExEx.peak.sam.recursive_matrix.txt{1}"


ln="ln -s {0};ln -s {1};ln -s {2};ln -s {3}".format(bam1,bam2,bai1,bai2)
strand=""

def produceresults(inputfile):
    with open(inputfile) as infile:
        for item in infile:
            item=item.strip()
            print("Porcessing {}".format(item))
            os.system("cat run.sh | sed 's/LINGENE\/LINGENE/{0}\/{0}/g'> ./{0}/run.sh".format(item))
            os.system("cd {0};{3};sh run.sh {1} {2}".format(item,sam.format(SRR3192396),sam.format(SRR3192397),ln))


def filters(item,Keywords="No"):
    # assert isinstance(item,str)
    if item.find(Keywords)==-1:
        return True
    else:
        return False

def decodedata(samplename,strand,dir,RSdict=None):
    if RSdict==None:
        RSdict={}
        with open(countsfile.format(samplename,strand,dir)) as RSfile:
            for item in RSfile:
                item=item.strip().split('\t')
                if filters(item[0]):
                    RSdict[item[0]]=[int(item[1])]
    else:
        with open(countsfile.format(samplename,strand,dir)) as RSfile:
            for item in RSfile:
                item=item.strip().split('\t')
                if filters(item[0]):
                    if item[0] in RSdict:
                        RSdict[item[0]].append(int(item[1]))
                    else:
                        RSdict[item[0]]=[int(item[1])]
    return RSdict

def PatternDec(RSpart:list):
    if filters(RSpart[0],"ex"):
        if filters(RSpart[1],'ex'):
            x= 0
        else:
            x= 1
    else:
        if filters(RSpart[1],'ex'):
            x= 2
        else:
            x= 3
    donor=RSpart[0].split('-')[0]
    acceptor=RSpart[1].split('-')[0]
    return (donor,acceptor,x)




def getresults(inputfile,outputfile):
    with open(inputfile) as infile:
        with open(outputfile,'w') as output:
            for item in infile:
                item=item.strip()
                print("Porcessing {}".format(item))
                with open("./{0}/{0}_annotation.bed".format(item)) as testfile:
                    strand=""
                    chrom=''
                    # for signals in testfile:
                    signals=testfile.readline()
                    signals=signals.strip()
                    signals=signals.split('\t')
                    if signals[-1]=="-":
                        strand='.strand'
                    chrom=signals[0]
                RSdict=decodedata(SRR3192396,strand,item)
                RSdict=decodedata(SRR3192397,strand,item,RSdict)
                for RS in RSdict:
                    RSpart=RS.split("__")
                    P=PatternDec(RSpart)
                    output.write('\t'.join((chrom,item,RS,P[0],P[1],str(abs(int(P[0])-int(P[1]))),str(P[2]),str(len(RSdict[RS])),str(max(RSdict[RS])),str(min(RSdict[RS])),','.join([str(x) for x in  RSdict[RS]])))+'\n')

if __name__ == '__main__':
    printinformations()
    options = _parse_args()
    # your code here!
    # produceresults(options.input)
    getresults(options.input,options.output)
    programends()