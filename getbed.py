#!/usr/bin/env python3
# coding=utf-8
import sys
Length=10
depth=3

scallfold=""
firstPos=0
previousPos=0
count=1
with open(sys.argv[1]) as inputfile:
    with open(sys.argv[2],'w') as outfile:
        for x in inputfile:
            x=x.strip()
            itemlist=x.split()
            if itemlist[0]!=scallfold:
                if count >=Length:
                    outfile.write('\t'.join([scallfold,str(firstPos),str(previousPos)])+'\n')
                if int(itemlist[2])>=depth:
                    scallfold=itemlist[0]
                    firstPos=int(itemlist[1])
                    previousPos=firstPos
                count=1
            elif int(itemlist[1])-previousPos==1:
                if int(itemlist[2])>=depth:
                    previousPos=int(itemlist[1])
                    count+=1
                else:
                    if count >=Length:
                        outfile.write('\t'.join([scallfold,str(firstPos),str(previousPos)])+'\n')
                    count=1
            else:
                if count >=Length:
                    outfile.write('\t'.join([scallfold,str(firstPos),str(previousPos)])+'\n')
                if int(itemlist[2])>=depth:
                    firstPos=int(itemlist[1])
                    previousPos=firstPos
                count=1
        if count >=Length:
            outfile.write('\t'.join([scallfold,str(firstPos),str(previousPos)])+'\n')