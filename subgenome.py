#!/usr/bin/env python3
# coding=utf-8

__author__ = 'Guoliang Lin'
Softwarename = 'calssifysubgenome'
version = '0.0.1'
bugfixs = ''
__date__ = '18-7-2'
subgenomep=["chr4",
"chr8",
"chr3",
"chr23",
"chr17",
"chr41",
"chr46",
"chr33",
"chr9",
"chr30",
"chr35",
"chr39",
"chr27",
"chr6",
"chr25",
"chr24",
"chr12",
"chr11",
"chr1",
"chr22",
"chr44",
"chr43",
"chr21",
"chr20",
"chr15",]
scaffoldp={}
subgenomem=["chr40",
"chr47",
"chr2",
"chr26",
"chr18",
"chr37",
"chr49",
"chr42",
"chr5",
"chr36",
"chr28",
"chr45",
"chr34",
"chr7",
"chr32",
"chr29",
"chr19",
"chr13",
"chr10",
"chr31",
"chr48",
"chr38",
"chr14",
"chr50",
"chr16"]
scaffoldm={}
def getscafflodinformation(apgfile="Carassius.auratus.build.ScafInChr.last.agp"):
    with open(apgfile) as inputfile:
        # trim head
        inputfile.readline()
        for item in inputfile:
            itemlist=item.split()
            if itemlist[5]!="100":
                if itemlist[0] in subgenomep:
                    scaffoldp[itemlist[5]]=itemlist[0]
                elif itemlist[0] in subgenomem:
                    scaffoldm[itemlist[5]]=itemlist[0]


if __name__=='__main__':
    getscafflodinformation("Carassius.auratus.build.ScafInChr.last.agp")
    print(scaffoldm)