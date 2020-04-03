import os, json, urllib3, pathlib
import base64 as b64
import requests as req
import colorama as cr
cr.init()

class InvalidClientException(Exception):
    def __init__(self, msg='Invalid Client!'):
        self.msg = msg

    def __str__(self):
        return 'InvalidClientException: {}'.format(self.msg)

class Client(object):
    def __init__(self, host='localhost', port='4800'):
        self.host = host
        self.port = port
        self.path = '/'
        self.sess = req.Session()
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        if not self.__conn_work():
            raise InvalidClientException('"{}" did not respond properly ... '.format(self.hoststr()))

    def __conn_work(self):
        try:
            return bool(self.hostinfo())
        except Exception:
            return False

    def __benc(self, p):
        return b64.b64encode(p.encode()).decode()

    def __bdec(self, p):
        return b64.b64decode(p).decode()

    def __isdir(self, d):
        try:
            res = req.get(self.url()+'fs/'+self.__benc(d), verify=False)
            if res.status_code != 200:
                return False
            res = json.loads(res.text)
            return 'success' in res.keys() and res['success']
        except Exception:
            return False

    def __isfile(self, file):
        d = os.path.dirname(file)
        if not self.__isdir(d):
            return False
        for f in self.ls(d):
            if f['name'] == os.path.basename(file) and f['type'] != 'dir':
                return True
        return False

    def __resolve(self, p):
        return os.path.abspath(p).replace(os.getcwd(), '') or '/'

    def hostinfo(self):
        res = req.get(self.url()+'host', verify=False)
        if res.status_code != 200:
            return None
        return json.loads(res.text)

    def hoststr(self, hname=None):
        return '{}:{}'.format(hname if hname else self.host, self.port)

    def url(self):
        return 'https://{}/'.format(self.hoststr())

    def prompt(self):
        hosti = self.hostinfo()
        return '{}{}{}{}@{}{}{};{}{}{}{}$ '.format(cr.Style.BRIGHT, cr.Fore.LIGHTGREEN_EX, hosti['username'], cr.Fore.LIGHTBLACK_EX, 
            cr.Fore.LIGHTBLUE_EX, self.hoststr(hosti['hostname']), cr.Fore.LIGHTBLACK_EX, cr.Fore.LIGHTRED_EX, self.path, cr.Fore.RESET, 
            cr.Style.RESET_ALL)

    def ls(self, d=None):
        if not d:
            d = self.path
        res = req.get(self.url()+'fs/'+self.__benc(d), verify=False)
        if res.status_code != 200:
            return None
        res = json.loads(res.text)
        if 'success' not in res.keys() or not res['success']:
            return None
        return res['dir']

    def dl(self, fpath, dlpath=None):
        if not os.path.isabs(fpath):
            fpath = os.path.join(self.path, fpath)
        if not dlpath:
            dlpath = os.getcwd()
        res = req.get(self.url()+'f/'+self.__benc(fpath), stream=True, verify=False)
        if res.status_code != 200:
            return None
        fname = os.path.splitext(os.path.join(dlpath, os.path.basename(fpath)))
        if os.path.isfile(''.join(fname)):
            i = 1
            while os.path.isfile(fname[0]+'_'+str(i)+fname[1]):
                i += 1
            fname[0] = fname[0]+'_'+str(i)
        with open(''.join(fname), 'wb') as f:
            for c in res:
                f.write(c)
        return os.path.abspath(''.join(fname))

    def cd(self, d):
        nd = self.__resolve(os.path.join(self.path, d))
        if not self.__isdir(nd):
            return None
        self.path = nd
        return nd

    def pwd(self):
        return '{} {}[{}]{}'.format(self.path, cr.Fore.LIGHTBLACK_EX, b64.b64encode(self.path.encode()).decode(), cr.Fore.RESET)