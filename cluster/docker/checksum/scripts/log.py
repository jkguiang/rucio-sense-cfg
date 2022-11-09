import time,os,pwd,socket

class log(object):
    def __init__(self):
        self._dir = os.path.dirname(os.path.abspath(__file__))
    def write(self,entries):
        t = time.localtime()
        timestamp = time.strftime('%Y-%m-%d %H:%M:%S',t)
        day       = time.strftime('%Y-%m-%d'         ,t)
        try    : user = pwd.getpwuid(os.getuid())[0]
        except : user = 'unknown'
        try    : host = socket.gethostname()
        except : host = 'unknown'
        LOGPATH = os.path.join(self._dir,'adler_'+day+'.log')
        Entries = [['time',timestamp],['user',user],['host',host]]+[[entry[0],entry[1].replace('=',':').replace(',',' ')] for entry in entries]
        logline = ', '.join(['='.join(entry) for entry in Entries])
        os.system('echo "'+logline+'" >> '+LOGPATH)
        return self

if __name__=='__main__':
    lf = log()
    lf.write([])
