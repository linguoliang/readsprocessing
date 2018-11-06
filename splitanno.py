#!/usr/bin/env python3
# coding=utf-8

__author__ = 'Guoliang Lin'
Softwarename = 'splitanno'
version = '0.0.1'
bugfixs = ''
__date__ = '2018/11/6'

import os
import sys
def splitanno(bedanno):
    tempname=""
    cwd=os.getcwd()
    with open(bedanno) as inputfile:
        with open('dirlist.txt','w') as dirlist:
            for item in inputfile:
                itemlist=item.strip().split('\t')
                if tempname!=itemlist[3]:
                    tempname=itemlist[3]
                    dirpath=cwd+'/'+tempname+'/'
                    if os.path.exists(cwd+'/'+tempname):
                        print("error!,dir {} exits already!".format(tempname))
                    else:
                        os.mkdir(dirpath)
                        dirlist.write(tempname+'\n')
                        try:
                            outputfile.close()
                        except:
                            pass
                        outputfile=open(dirpath+tempname+'_annotation.bed','w')
                outputfile.write(item)

if __name__=='__main__':
    splitanno(sys.argv[1])