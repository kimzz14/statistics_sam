################################################################################################
last_modified = '2024-11-24'
version = '0.0.1'
print('Last Modified:', last_modified, 'Version:', version)
################################################################################################
import gzip
from optparse import OptionParser
import sys

#option parser
parser = OptionParser(usage="""Run annotation.py \n Usage: %prog [options]""")
parser.add_option("-i","--input",action = 'store',type = 'string',dest = 'input',help = "")
parser.add_option("-o","--output",action = 'store',type = 'string',dest = 'output',help = "")
(opt, args) = parser.parse_args()
if opt.input == None or opt.output == None:
    print('Basic usage')
    print('')
    print('     python depthofcoverage.py -i test.genomecov.gz -o test.genomecov.coverage')
    print('')
    sys.exit()

#prepare
maxDepth = 200
covbase_LIST = [0] * (maxDepth + 1)

#Read file
fin = gzip.open(opt.input, 'rt')
for line in fin:
    seq, sPos, ePos, depth = line.rstrip('\n').split('\t')
    sPos = int(sPos) + 1
    ePos = int(ePos)
    depth = int(depth)

    length = ePos - sPos + 1
    for depthIDX in range(0, min(depth, maxDepth) + 1):
        covbase_LIST[depthIDX] += length
fin.close()

#write Result
fout = open(opt.output, 'w')
totalbase = covbase_LIST[0]
for depthIDX, covbase in enumerate(covbase_LIST):
    fout.write('\t'.join(map(str, [depthIDX, covbase/totalbase, covbase, totalbase])) + '\n')
fout.close()