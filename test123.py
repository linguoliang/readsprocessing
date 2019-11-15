import optparse
import time
import gzip

# add your options here!
def _parse_args():
    """Parse the command line for options."""
    usage = 'usage: %prog -i INPUT -o OUTPUT'
    parser = optparse.OptionParser(usage)
    parser.add_option('-1',
                      '--R1', dest='R1', type='string',
                      help='paired end read 1')
    parser.add_option('-2',
                      '--R2', dest='R2', type='string',
                      help='paired end read 2')
    parser.add_option('-g','--gz',
                      action='store_true', dest='gz',
                      help='Is a gzip file? default=False')
    #    parser.add_option('-f','--fpkm',dest='fpkm_file',type='string',help='input fpkm file')
    #    parser.add_option('-v','--variation', dest='variation', type='string', help='input variation information file')
    #    parser.add_option('-g', '--gff3', dest='gff', help='gff3 file')
    #    parser.add_option('-o', '--output', dest='output', type='string', help='output file')
    options, args = parser.parse_args()
    # positional arguments are ignored
    return options


if __name__ == '__main__':
    options = _parse_args()
    # your code here!
    string="hell o.gz"
    print(string.replace(".gz",""))
    print(string)
    if options.gz:
        print("yes")