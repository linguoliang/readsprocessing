#!/usr/bin/env python3
# coding=utf-8
import sys
__author__ = 'Guoliang Lin'
Softwarename = 'filter_intron'
version = '0.0.1'
bugfixs = ''
__date__ = '2018/8/30'
if len(sys.argv)==3:
    iname=sys.argv[1]
    oname=sys.argv[2]
elif len(sys.argv)==2:
    iname=sys.argv[1]
    oname=iname+'.out'
else:
    print("Parameter error with {}".format(' '.join(sys.argv)))

with open(iname) as ifile:
    with open(oname,'w') as ofile:
        for item in ifile:
            itemlist=item.strip().split('\t')
            if abs(int(itemlist[2])-int(itemlist[1]))>50:
                ofile.write(item)