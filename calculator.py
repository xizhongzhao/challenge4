#!/usr/bin/env python3

import sys
from multiprocessing import Queue,Process

class Config(object):
    def __init__(self,configfile):
        self._configfile = configfile

    @property
    def config(self):
        config = {}
        with open(self._configfile,'r') as file:
            for line in file:
                s = line.split('=')
                fkey = s[0].strip()
                fvalue = s[1].strip()
                config[fkey] = float(fvalue)
        return config 


class UserData(object):
    def __init__(self,userdatafile):
        self._userdatafile = userdatafile
    
    @property 
    def userdata(self):
        userdata = {}
        with open(self._userdatafile) as file:
            for line in file:
                s = line.split(',')
                fkey = s[0].strip()
                fvalue = s[1].strip()
                userdata[fkey] = int(fvalue)
        return userdata
    
      

class Salary(object):
    #bftax is salary before the pitax
    #soinsurp is socail insur pecentage
    #basel is the lowest base
    #baseh is the hightest base
    def __init__(self,bftax,soinsurp,basel,baseh):
        self._bftax = bftax
        self._soinsurp = soinsurp
        self._basel = basel
        self._baseh = baseh
    @property 
    def soinsur(self):
        if self._bftax <= self._basel:
            return self._basel * self._soinsurp
        elif self._bftax >= self._baseh:
            return self._baseh * self._soinsurp
        else:
            return self._bftax * self._soinsurp
    
    @property
    def pitax(self):
        taxbase = self._bftax - self.soinsur - 3500
        if taxbase <= 0:
            return 0
        elif taxbase > 0 and taxbase <= 1500:
            return taxbase * 0.03
        elif taxbase > 1500 and taxbase <= 4500:
            return (taxbase * 0.1 - 105)
        elif taxbase > 4500 and taxbase <= 9000:
            return (taxbase * 0.2 - 555)
        elif taxbase > 9000 and taxbase <= 35000:
            return (taxbase * 0.25 - 1005)
        elif taxbase > 35000 and taxbase <= 55000:
            return (taxbase * 0.3 - 2755)
        elif taxbase > 55000 and taxbase <= 80000:
            return (taxbase * 0.35 - 5505)
        else:
            return (taxbase * 0.45 - 13505)
    @property
    def aftax(self):
        return self._bftax - self.soinsur - self.pitax                          
class Argument(object):
    def __init__(self,arg):
        self._arg = arg
    @property
    def ne_arg(self):
        arglist = sys.argv[1:]
        arg_index =arglist.index(self._arg)
        return arglist[arg_index + 1]

que1 = Queue()
que2 = Queue()

def putdata(arg):
     _argument = Argument(arg)
     quelist =[(k,v) for k, v in\
     UserData(_argument.ne_arg).\
     userdata.items()]
     que1.put(quelist)

def comp_func(soinsurp,basel,baseh,lock):
    bftaxlist = que1.get()
    g = (bftaxlist)
    for i in g:
         bftax = i[1]
         with lock:
              salary = Salary(bftax,soinsurp,basel,baseh)
              sal_list = [i[0],salary._bftax,salary.soinsur,salary.pitax,\
                        salary.aftax]
              que2.put(sal_list)

def outfile(arg):
    sal_list = que2.get() 
    _argument = Argument(arg)
    with open(_argument.ne_arg,'a') as file:
         file.write(sal_list[0])
         for i in sal_list[1:]:
             file.write(','+'{:.2f}'.format(i)) 
if __name__ == '__main__': 
    try:
        arglist = sys.argv[1:]
        if len(arglist) ==6 and '-c' in arglist and\
        '-d' in arglist and '-o'in arglist
            argc = Argument('-c')
            config_argc = Config(argc.ne_arg)
            soinsurp = config_argc.config['ShengYu']\ 
               + config_argc.config['YangLao'] \
               + config_argc.config['YiLiao'] \
               + config_argc.config['GongJiJin']\  
               + config_argc.config['GongShang'] \
               + config_argc.config['ShiYe']
            basel = config_argc.config['JiShuL']
            baseh = config_argc.config['JiShuH']
            lock = Lock()
            Process(target=putdata,arg=('-d',)).start()
            Process(target=comp_func,arg=(soinsur,basel,baseh,lock)).start()
            Process(target=outfile,arg=('-o')).start()
        else:  
            raise "Parameter Error"
    except:
        print("Parameter Error")
   
        
   

 
