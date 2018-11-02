# def name(infile):
#     while True:
#         p=infile.tell()
#         x=infile.readline()
#         if x.find("werqwer")==-1:
#             pass
#         else:
#             print("in name is {}".format(x))
#             infile.seek(p)
#             break
# with open("test.txt") as infile:
#     name(infile)
#     m=infile.readline()
#     print("out name is {}".format(m))
m=[[22,33],[44,55]]
def x(x,c,v,b):
    print([x,c,v,b])
x(**m)