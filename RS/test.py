import gzip
import os.path

def file_extension(path):
    return os.path.splitext(path)[1]
string="Homo_sapiens.GRCh37.87.chr.gtf.gz"
# string="../Homo_sapiens.GRCh38.92.chr.gtf"
if file_extension(string)==".gz":

    linopen=gzip.open
else:
    linopen=open

with linopen(string,'rt') as ifile:
    for x in ifile:
        print(x)
# import pandas as pd
# datalist =pd.read_excel("../hg19data.xlsx")
# print(datalist["name"].values)