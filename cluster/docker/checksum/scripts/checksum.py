#
#   Computes the Adler32 checksum of input path.
#
#   Saul Youssef, 2021
#
BLOCKSIZE=2*1024*1024
from zlib import adler32

def checksum(path):
    val = 1
    f = open(path,'r')
    while True:
        data = f.read(BLOCKSIZE)
        if not data: break
        val = adler32(data,val)
    if val<0: val += 2**32
    f.close()
    return hex(val)[2:10].zfill(8).lower()

if __name__=='__main__':
    print checksum('./checksum.py')
