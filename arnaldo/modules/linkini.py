# vim: set fileencoding=utf-8:

from arnaldo.modules import Arnaldigno, comanda
import arnaldo.brain

#

from collections import defaultdict
import urllib2
import datetime

#

URL_RE = re.compile(ur'(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:\'".,<>?\xab\xbb\u201c\u201d\u2018\u2019]))')

def check_SI(p):
    mapping = [(-24, ('y', 'yocto' )),
               (-21, ('z', 'zepto' )),
               (-18, ('a', 'atto'  )),
               (-15, ('f', 'femto' )),
               (-12, ('p', 'pico'  )),
               ( -9, ('n', 'nano'  )),
               ( -6, ('u', 'micro' )),
               ( -3, ('m', 'mili'  )),
               ( -2, ('c', 'centi' )),
               ( -1, ('d', 'deci'  )),
               (  3, ('k', 'kilo'  )),
               (  6, ('M', 'mega'  )),
               (  9, ('G', 'giga'  )),
               ( 12, ('T', 'tera'  )),
               ( 15, ('P', 'peta'  )),
               ( 18, ('E', 'exa'   )),
               ( 21, ('Z', 'zetta' )),
               ( 24, ('Y', 'yotta' ))]

    for check, value in mapping:
        if p <= check:
            return value

def request_oembed(self, url):
    query = urllib.urlencode((('url', url),))
    data = urllib2.urlopen('http://noembed.com/embed?' + query)
    respa = json.loads(data.read()) #meglio una raspa d'una ruspa
    return respa

class Linkini(Arnaldigno):
    def __init__(self, *args):
        super(Accolli, self).__init__(*args)
        self.contabrazze = defaultdict(list)

    @comanda('.')
    def oembeddalo(self, e, match):
        allurls = URL_RE.findall(e.arguments[0])
        if len(allurls) != 1:
            return True

        #tipo goto ma peggio
        try:    respa = self.request_oembed(allurls[0][0])
        except: pass

        thaurlhash= hashlib.md5(allurls[0][0]).hexdigest()
        hashish=brain.brain.get("urlo:%s"%thaurlhash)

        try:
            if hashish == None: #NO FUMO NO FUTURE
                ts=time.time()
                nic=e.source.nick
                brain.brain.set("urlo:%s"%thaurlhash,"%f:%s:%d"%(ts,nic,1))
                self.reply(e, respa['title'])
            else:
                SECONDIANNO=31556926 #num secondi in un anno youdontsay.png
                ts,nic,v=hashish.split(':')
                ts=float(ts)
                delta=time.time() -ts
                v=int(v)+1
                brain.brain.set("urlo:%s"%thaurlhash,"%f:%s:%d"%(ts,nic,v))
                manti,expo=map(float,("%e"%(delta/SECONDIANNO)).split("e"))
                symb,todo=check_SI(expo*v)
                dignene="%.2f %sGaggo [postato da %s il %s]"%(manti+v,symb,nic,datetime.datetime.fromtimestamp(ts).strftime('%d/%m/%y %H:%M:%S'))
                self.reply(e, dignene)

        except:
            pass

        return True

