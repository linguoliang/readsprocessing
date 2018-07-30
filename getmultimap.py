#!/usr/bin/env python3
import sys

count=0
prevois=""
data=[]
read1=0
with open(sys.argv[1]) as inputfile:
    with open(sys.argv[2],'w') as outputfile:
        for item in inputfile:
            itemlist=item.strip()
            itemlist=itemlist.split()
            names=itemlist[0].split("/")
            if names[0]==prevois:
                count+=1
                data.append(item)
                if names[1]=='1':
                    read1+=1
            else:
                if prevois=="E00511:135:HJN5YALXX:1:1101:10003:10415":
                    print("hello")
                if (3<count<7) and (abs(count-2*read1)<3):
                    for x in data:
                        outputfile.write(x)
                prevois=names[0]
                data=[item]
                count=1
                if names[1]=='1':
                    read1+=1
                else:
                    read1=0