import os, json, urllib3, pathlib
import base64 as b64
import requests as req
import requests_toolbelt as reqt
import colorama as cr
cr.init()
from lib import misc
from typing import Any

class InvalidClientException(Exception):
    def __init__(self, msg: str = 'Invalid Client!') -> None:
        self.msg: str = msg

    def __str__(self) -> str:
        return 'InvalidClientException: {}'.format(self.msg)

class Client(object):
    def __init__(self, host: str = 'localhost', port: int = '4800') -> None:
        self.host: str = host
        self.port: int = port
        self.path: str = '/'
        self.sess: req.Session = req.Session()
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        if not self.__conn_work():
            raise InvalidClientException('"{}" did not respond properly ... '.format(self.hoststr()))

    def __conn_work(self) -> bool:
        try:
            return bool(self.hostinfo())
        except Exception:
            return False

    def __benc(self, p: str) -> str:
        return b64.b64encode(p.encode()).decode()

    def __bdec(self, p: str) -> str:
        return b64.b64decode(p).decode()

    def __isdir(self, d: str) -> bool:
        try:
            res = self.sess.get(self.url()+'fs/'+self.__benc(d), verify=False)
            if res.status_code != 200:
                return False
            res = json.loads(res.text)
            return 'success' in res.keys() and res['success']
        except Exception:
            return False

    def __isfile(self, file: str) -> bool:
        d = os.path.dirname(file)
        if not self.__isdir(d):
            return False
        for f in self.ls(d):
            if f['name'] == os.path.basename(file) and f['type'] != 'dir':
                return True
        return False

    def __resolve(self, p: str) -> str:
        return os.path.abspath(p).replace(os.getcwd(), '') or '/'

    def hostinfo(self) -> Any:
        res = self.sess.get(self.url()+'host', verify=False)
        if res.status_code != 200:
            return None
        return json.loads(res.text)

    def hoststr(self, hname: str = '') -> str:
        return '{}:{}'.format(hname if hname else self.host, self.port)

    def url(self) -> str:
        return 'https://{}/'.format(self.hoststr())

    def prompt(self) -> str:
        hosti = self.hostinfo()
        return '{}{}{}{}@{}{}{};{}{}{}{}'.format(cr.Style.BRIGHT, cr.Fore.LIGHTGREEN_EX, hosti['username'], cr.Fore.LIGHTBLACK_EX, 
            cr.Fore.LIGHTBLUE_EX, self.hoststr(hosti['hostname']), cr.Fore.LIGHTBLACK_EX, cr.Fore.LIGHTRED_EX, self.path, cr.Fore.RESET, 
            cr.Style.RESET_ALL)

    def wprompt(self) -> str:
        hosti = self.hostinfo()
        return '{}@{};{}$ '.format(hosti['username'], self.hoststr(hosti['hostname']), self.path)

    def ls(self, d: str = '') -> Any:
        if not d:
            d = self.path
        res = self.sess.get(self.url()+'fs/'+self.__benc(d), verify=False)
        if res.status_code != 200:
            return None
        res = json.loads(res.text)
        if 'success' not in res.keys() or not res['success']:
            return None
        return res['dir']

    def dl(self, fpath: str, dlpath: str = '') -> Any:
        if not os.path.isabs(fpath):
            fpath = os.path.join(self.path, fpath)
        if not dlpath:
            dlpath = os.getcwd()
        res = self.sess.get(self.url()+'f/'+self.__benc(fpath), stream=True, verify=False)
        if res.status_code != 200:
            return ''
        fname = list(os.path.splitext(os.path.join(dlpath, os.path.basename(fpath))))
        if os.path.isfile(''.join(fname)):
            i = 1
            while os.path.isfile(fname[0]+'_'+str(i)+fname[1]):
                i += 1
            fname[0] = fname[0]+'_'+str(i)
        pb = misc.ProgressBar(int(res.headers['Content-length']), 'Downloading "{}" ... '.format(os.path.basename(fpath)))
        with open(''.join(fname), 'wb') as f:
            for c in res:
                pb.inc(len(c))
                f.write(c)
        pb.ensure_end()
        return os.path.abspath(''.join(fname))

    def ul(self, fpath: str, tpath: str = '') -> str:
        if not os.path.isabs(fpath):
            fpath = os.path.join(os.getcwd(), fpath)
        if not tpath:
            tpath = os.path.basename(fpath)
        if not os.path.isfile(fpath):
            return ''
        tpath = os.path.join(self.path, tpath)
        fname = list(os.path.splitext(tpath))
        if self.__isfile(''.join(fname)):
            i = 1
            while self.__isfile(fname[0]+'_'+str(i)+fname[1]):
                i += 1
            fname[0] = fname[0]+'_'+str(i)
        pb = misc.ProgressBar(os.path.getsize(fpath), title='Uploading "{}"'.format(os.path.basename(fpath)))
        e = reqt.MultipartEncoder(fields=dict(file=(os.path.basename(''.join(fname)), open(fpath, 'rb'),)))
        def up(mon: reqt.MultipartEncoderMonitor) -> None:
            pb.update(mon.bytes_read)
        m = reqt.MultipartEncoderMonitor(e, up)
        res = self.sess.post(self.url()+'u/'+self.__benc(''.join(fname)), data=m, headers={'Content-Type': m.content_type,})
        if res.status_code != 200:
            return ''
        return ''.join(fname)

    def cd(self, d: str) -> str:
        nd = self.__resolve(os.path.join(self.path, d))
        if not self.__isdir(nd):
            return ''
        self.path = nd
        return nd

    def mkdir(self, d: str) -> str:
        td = os.path.join(self.path, d)
        if self.__isdir(td):
            return ''
        res = self.sess.post(self.url()+'mk/'+self.__benc(td))
        if res.status_code != 200:
            return ''
        return td

    def pwd(self) -> str:
        return '{} {}[{}]{}'.format(self.path, cr.Fore.LIGHTBLACK_EX, b64.b64encode(self.path.encode()).decode(), cr.Fore.RESET)