import sys
with open(sys.argv[0]) as inputfile:
    with open("exon.bed") as output:
        for x in range(5):
            inputfile.readline()
        for item in inputfile:
            item=item.split('\t')
            if item[2]=="exon":
                output.write('\t'.join([item[0],item[3],item[4]])+'\n')