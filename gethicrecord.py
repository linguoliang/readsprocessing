#!/usr/bin/env python3
import copy
import re
import sys

import numpy as np

import getchimericreads

count = 0
prevois = ""
data = {}
read1 = 0


def getdistancematrix(read1, read2):
    assert isinstance(read1, list)
    assert isinstance(read2, list)
    length1 = len(read1)
    length2 = len(read2)
    x = np.zeros((length1, length2))
    for i in range(length1):
        for j in range(length2):
            if read1[i][2] == read2[j][2]:
                extra = 0
            else:
                extra = 1000000000
            x[i, j] = abs(int(read1[i][3]) - int(read2[j][3])) + extra
    return x


def isread1(reads):
    for item in reads:
        assert isinstance(item, list)
        pattern = getchimericreads.splitpatten(item[5])
        x = caculateM(pattern)
        if x < 85:
            return False
    return True


def caculateM(pattern):
    match = 0
    for i in range(len(pattern)):
        if pattern[i] == 'M':
            match += int(int(pattern[i - 1]))
    return match


def reversecomp(string):
    string = string[::-1].replace("A", "P").replace("T", "A").replace("P", 'T').replace("G", "P").replace("C",
                                                                                                          "G").replace(
        "P", 'C')
    return string


def issame(pattern1, pattern2, sameside):
    R2 = getchimericreads.splitpatten(pattern1)
    R22 = getchimericreads.splitpatten(pattern2)
    if abs(caculateM(R2) - caculateM(R22)) > 5:
        return False
    else:
        string1 = re.sub("\d+", '', pattern1)
        string1 = re.sub('H', 'S', string1)
        string2 = re.sub("\d+", '', pattern2)
        string2 = re.sub('H', 'S', string2)
        string1 = re.sub('DM', '', string1)
        string1 = re.sub('IM', '', string1)
        string2 = re.sub('DM', '', string2)
        string2 = re.sub('IM', '', string2)
        if not sameside:
            string2 = string2[::-1]
        if string1 == string2:
            return True
        else:
            return False


def getseq(reads):
    readseq = "*"
    readqual = "*"
    for read in reads:
        print(read)
        if (int(read[1]) & 256 == 0) and ('H' not in read[5]):
            if int(read[1]) & 16:
                readseq = reversecomp(read[9])
                readqual = reversecomp(read[10])
            else:
                readseq = read[9]
                readqual = read[10]
    return readseq, readqual


def converseq(seq, qual, pattern):
    if pattern[1] == 'H' and pattern[-1] == 'H':
        readseq = seq[int(pattern[0]) - 1:len(seq) - int(pattern[-2])]
        readqual = qual[int(pattern[0]) - 1:len(seq) - int(pattern[-2])]
    elif pattern[1] == 'H':
        readseq = seq[int(pattern[0]) - 1:]
        readqual = qual[int(pattern[0]) - 1:]
    else:
        readseq = seq[:len(seq) - int(pattern[-2])]
        readqual = qual[:len(seq) - int(pattern[-2])]
    return readseq, readqual


def writetodisk(read1, read2, read22, filehindle, string=""):
    read1 = copy.deepcopy(read1)
    read2 = copy.deepcopy(read2)
    read22 = copy.deepcopy(read22)
    read1[0] = read1[0] + string + '/1'
    read2[0] = read2[0] + string + '/2'
    read22[0] = read22[0] + string + '/2'
    if not issame(read2[5], read22[5], (int(read2[1]) & 16) == (int(read22[1]) & 16)):
        filehindle.write(' '.join(read1) + '\n')
        filehindle.write(' '.join(read2) + '\n')
        filehindle.write(' '.join(read22) + '\n')


with open(sys.argv[1]) as inputfile:
    with open(sys.argv[2], 'w') as outputfile:
        for item in inputfile:
            itemlist = item.strip()
            itemlist = itemlist.split()
            names = itemlist[0].split("/")
            itemlist[0] = names[0]
            if names[0] == prevois:
                count += 1
                if names[1] in data:
                    data[names[1]].append(itemlist)
                else:
                    data[names[1]] = [itemlist]
                if names[1] == '1':
                    read1 += 1
            else:
                if '1' in data and '2' in data:
                    flag1 = isread1(data["1"])
                    flag2 = isread1(data['2'])
                else:
                    flag1 = False
                    flag2 = False
                if flag2:
                    data["2"], data['1'] = data["1"], data['2']
                    read1 = count - read1
                if (flag1 or flag2) and len(data['1']) == 2:
                    read1seq, read1qual = getseq(data['1'])
                    read2seq, read2qual = getseq(data['2'])
                    for i in range(len(data['1'])):
                        if int(data['1'][i][1]) & 256:
                            if "H" not in data['1'][i][5]:
                                if int(data['1'][i][1]) & 16:
                                    temseq = reversecomp(read1seq)
                                    temqual = reversecomp(read1qual)
                                else:
                                    temseq = read1seq
                                    temqual = read1qual
                                data['1'][i][9] = temseq
                                data['1'][i][10] = temqual
                            else:
                                # 存有疑问
                                pattern = getchimericreads.splitpatten(data['1'][i][5])
                                if int(data['1'][i][1]) & 16:
                                    temseq = reversecomp(read1seq)
                                    temqual = reversecomp(read1qual)
                                else:
                                    temseq = read1seq
                                    temqual = read1qual
                                data['1'][i][9], data['1'][i][10] = converseq(temseq, temqual, pattern)

                    for i in range(len(data['2'])):
                        if int(data['2'][i][1]) & 256:
                            if "H" not in data['2'][i][5]:
                                if int(data['2'][i][1]) & 16:
                                    temseq = reversecomp(read1seq)
                                    temqual = reversecomp(read1qual)
                                else:
                                    temseq = read1seq
                                    temqual = read1qual
                                data['2'][i][9] = temseq
                                data['2'][i][10] = temqual
                            else:
                                # 存有疑问
                                pattern = getchimericreads.splitpatten(data['2'][i][5])
                                if int(data['2'][i][1]) & 16:
                                    temseq = reversecomp(read1seq)
                                    temqual = reversecomp(read1qual)
                                else:
                                    temseq = read1seq
                                    temqual = read1qual
                                data['2'][i][9], data['2'][i][10] = converseq(temseq, temqual, pattern)

                    distanc = getdistancematrix(data["1"], data['2'])
                    if distanc.min() <= 1000:
                        if count == 4:
                            index = distanc.argmin()
                            i = index // (count - 2)
                            j = index % (count - 2)
                            writetodisk(data['1'][i], data['2'][0], data['2'][1], outputfile)
                            # data['1'][i][0]=data['1'][i][0]+'/1reversecomp('
                            # data['2'][0][0]=data['2'][0][0]+'/2'
                            # data['2'][1][0]=data['2'][1][0]+'/2'
                            # outputfile.write(' '.join(data['1'][i])+'\n')
                            # outputfile.write(' '.join(data['2'][0])+'\n')
                            # outputfile.write(' '.join(data['2'][1])+'\n')
                        elif count == 5:
                            index = distanc.argmin(1)
                            if index[0] != index[1]:
                                if distanc[0, 3 - index[0] - index[1]] >= 1000000000 and distanc[
                                    1, 3 - index[0] - index[1]] >= 1000000000:
                                    if distanc[0, index[0]] < 1000:
                                        writetodisk(data['1'][0], data['2'][index[0]],
                                                    data['2'][3 - index[0] - index[1]], outputfile)
                                        # data['1'][0][0]=data['1'][0][0]+'/1'
                                        # data['2'][index[0]][0]=data['2'][index[0]][0]+'/2'
                                        # data['2'][3-index[0]-index[1]][0]=data['2'][3-index[0]-index[1]][0]+'/2'
                                        # outputfile.write(' '.join(data['1'][0])+'\n')
                                        # outputfile.write(' '.join(data['2'][index[0]])+'\n')
                                        # outputfile.write(' '.join(data['2'][3-index[0]-index[1]])+'\n')
                                    if distanc[1, index[1]] < 1000:
                                        writetodisk(data['1'][1], data['2'][index[1]],
                                                    data['2'][3 - index[0] - index[1]], outputfile, "lin1")
                                        # data['1'][1][0]=data['1'][1][0]+'lin1/1'
                                        # data['2'][index[1]][0]=data['2'][index[1]][0]+'lin1/2'
                                        # data['2'][3-index[0]-index[1]][0]=data['2'][3-index[0]-index[1]][0]+'lin1/2'
                                        # outputfile.write(' '.join(data['1'][1])+'\n')
                                        # outputfile.write(' '.join(data['2'][index[1]])+'\n')
                                        # outputfile.write(' '.join(data['2'][3-index[0]-index[1]])+'\n')
                                else:
                                    if distanc[0, index[0]] < 1000 and distanc[0, 3 - index[0] - index[1]] < 1000:
                                        writetodisk(data['1'][0], data['2'][index[0]],
                                                    data['2'][3 - index[0] - index[1]], outputfile)
                                        # data['1'][0][0]=data['1'][0][0]+'/1'
                                        # data['2'][index[0]][0]=data['2'][index[0]][0]+'/2'
                                        # data['2'][3-index[0]-index[1]][0]=data['2'][3-index[0]-index[1]][0]+'/2'
                                        # outputfile.write(' '.join(data['1'][0])+'\n')
                                        # outputfile.write(' '.join(data['2'][index[0]])+'\n')
                                        # outputfile.write(' '.join(data['2'][3-index[0]-index[1]])+'\n')
                                    if distanc[1, index[1]] < 1000 and distanc[1, 3 - index[0] - index[1]] < 1000:
                                        writetodisk(data['1'][1], data['2'][index[1]],
                                                    data['2'][3 - index[0] - index[1]], outputfile, "lin1")
                                        #
                                        # data['1'][1][0]=data['1'][1][0]+'lin1/1'
                                        # data['2'][index[1]][0]=data['2'][index[1]][0]+'lin1/2'
                                        # data['2'][3-index[0]-index[1]][0]=data['2'][3-index[0]-index[1]][0]+'lin1/2'
                                        # outputfile.write(' '.join(data['1'][1])+'\n')
                                        # outputfile.write(' '.join(data['2'][index[1]])+'\n')
                                        # outputfile.write(' '.join(data['2'][3-index[0]-index[1]])+'\n')
                prevois = names[0]
                data = {}
                data[names[1]] = [itemlist]
                count = 1
                if names[1] == '1':
                    read1 += 1
                else:
                    read1 = 0
