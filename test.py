def name(infile):
    while True:
        p=infile.tell()
        x=infile.readline()
        if x.find("werqwer")==-1:
            pass
        else:
            print("in name is {}".format(x))
            infile.seek(p)
            break
with open("test.txt") as infile:
    name(infile)
    m=infile.readline()
    print("out name is {}".format(m))