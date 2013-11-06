#! /usr/bin/env python
# vim: set fileencoding=utf-8:

from __future__ import unicode_literals
import irc.bot
import irc.strings
from irc.client import ip_numstr_to_quad, ip_quad_to_numstr
import cStringIO
from random import choice, randint
import json
import re
import urllib
import urllib2
import time
import sys, traceback
import bleach
from BeautifulSoup import BeautifulSoup
import random
import signal
import sys
import os.path
import os
import time
import redis
import hashlib
from blinker import signal as lasigna
import datetime

from utieffa import *
from vedetta import Vedetta
import quote

print "meglio una raspa di una ruspa"

dimme = lasigna('dimmelo')

SECONDIANNO=31556926 #num secondi in un anno youdontsay.png

try:
    brain = redis.Redis("localhost")
except:
    sys.exit("Insane in the membrane!!!")

MULTILINE_TOUT = 0.5

traceback_template = '''Tracefazza (most recent call last):
    File "%(filename)s", line %(lineno)s, in %(name)s
    %(type)s: %(message)s\n'''

URL_RE = re.compile(ur'(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:\'".,<>?\xab\xbb\u201c\u201d\u2018\u2019]))')

def pritaicsa(text):
    icsa=""
    for row in range(int(brain.get("asciitable:rows"))):
        for c in text:
            icsa=str(icsa)+str(brain.lindex("asciitable:%s"%c,row))
        icsa=icsa+'\n'
    icsa=icsa+'\n'
    return icsa


class Brain():
    def __init__(self,brain):
        self.b=brain

    def choicefromlist(self,name):
        i=random.randint(0,self.b.llen(name)-1)
        return self.b.lindex(name, i)

    def getCitta(self):
        return self.choicefromlist("CITTA")

    def getNomecen(self):
        return self.choicefromlist("NOMICEN")

    def getAttardi(self):
        return self.choicefromlist("ATTARDI")

    def getProverbiUno(self):
        return self.choicefromlist("PROV1")

    def getProverbiDue(self):
        return self.choicefromlist("PROV2")

    def getProverbioandid(self):
        i1=random.randint(0,self.b.llen("PROV1")-1)
        i2=random.randint(0,self.b.llen("PROV2")-2)
        if i2 >= i1:
            i2 += 1
        p=u"%s %s"%(self.b.lindex("PROV1", i1).decode('utf8'),self.b.lindex("PROV2", i2).decode('utf8'))
        return (p, "%dP%d"%(i1,i2))

    def getProverbiobyid(self,idp):
        try:
            p=idp.split('P')
            return u"%s %s"%(self.b.lindex("PROV1", int(p[0])).decode('utf8'),self.b.lindex("PROV2", int(p[1])).decode('utf8'))
        except:
                return "macche'"

class Sproloquio():
    def __init__(self):
        self.brain = Brain(brain)

    def attardati(self):
        return u"Stefano %s Attardi" % self.brain.getAttardi().decode('utf8')

    def ANAL(self):
        return u"%s ANAL %s" % (self.brain.getCitta().decode('utf8'), self.brain.getNomecen().decode('utf8'))

    def proverbia(self):
        #return u"%s %s" % (self.brain.getProverbiUno().decode('utf8'), self.brain.getProverbiDue().decode('utf8'))
        return self.proverbiaandid()[0]

    def proverbiaandid(self):
        return self.brain.getProverbioandid()

    def proverbiabyid(self,idp):
        return self.brain.getProverbiobyid(idp)

    def beuta(self):
        cocktail_id = random.randint(1, 4750)
        data = urllib2.urlopen("http://www.cocktaildb.com/recipe_detail?id=%d" % cocktail_id)
        soup = BeautifulSoup(data.read())
        directions = soup.findAll("div", { "class" : "recipeDirection" })
        measures = soup.findAll("div", { "class" : "recipeMeasure" })

        ret = []
        ret += [u"== %s ==\n" % (soup.find("h2").text)]

        for m in measures:
            ret += [u' '.join([x.strip() for x in m.findAll(text=True)])]

        ret += [u'']

        for d in directions:
            ret += [u' '.join([x.strip() for x in d.findAll(text=True)])]

        ret += [u'enjoy']
        return ret

    def boobs(self):
        urlo = "http://imgur.com/r/boobies/new/day/page/%d/hit?scrolled"
        response = urllib2.urlopen(urlo % random.randint(1, 50)).read()
        soup = BeautifulSoup(response)
        l = soup.findAll("div", {"class": "post"})
        i = choice(l)
        return "http://i.imgur.com/%s.jpg" % i.get("id")

sproloquio = Sproloquio()


def check_SI(p):
    mapping = [(-24,('y','yocto')),(-21,('z','zepto')),(-18,('a','atto')),(-15,('f','femto')),(-12,('p','pico')),
               (-9, ('n','nano')),(-6, ('u','micro')),(-3, ('m','mili')),(-2, ('c','centi')),(-1, ('d','deci')),
               (3,  ('k','kilo')),(6,  ('M','mega')),(9,  ('G','giga')),(12, ('T','tera')),(15, ('P','peta')),
               (18, ('E','exa')),(21, ('Z','zetta')),(24, ('Y','yotta'))]

    for check, value in mapping:
        if p <= check:
            return value

class Arnaldo(irc.bot.SingleServerIRCBot):

    def __init__(self, channel, nickname, server, port=6667):
        irc.client.ServerConnection.buffer_class = BambaRosaNasaBuffer
        irc.bot.SingleServerIRCBot.__init__(self, [(server, port)], nickname, nickname)
        self.channel = channel
        self.commands = []

        self.brain = Brain(brain)

        self.parliamo_summary = None
        self.BAM = None

        self.register_command('ANAL', self.anal)
        self.register_command('e allora\\?$', self.eallora)
        self.register_command('^allivello\\?', self.allivello)
        self.register_command('parliamo di', self.allivello)
        self.register_command('parliamone', self.checcazzo)
        self.register_command('anche no', self.ancheno)
        self.register_command('beuta', self.beuta)
        self.register_command('^facci (.+)', self.accollo)
        self.register_command('boobs please', self.boobs)
        self.register_command('^icsah (.+)', self.icsah)
        self.register_command('^arnaldo hai visto (.+)\\?', self.chilhavisto)


        self.contabrazze = {}
        self.register_command('^brazzami (.+)', self.brazzafazza)
        self.register_command('proverbia', self.proverbia)
        self.register_command('attardati', self.attardati)
        self.register_command('^markoviami(.*)', self.markoviami)

        self.register_command('^%s[:, \\t]*addquote (.*)' % nickname, self.add_quote)
        self.register_command('^%s[:, \\t]*quote$' % nickname, self.random_quote)
        self.register_command('^%s[:, \\t]*quote (.*)$' % nickname, self.search_quote)
        
        self.register_command('^bamba$', self.rosa)
        dimme.connect(self.dimmeame)        

    def dimmeame(self,msg):
        conn= self.connection

        if type(msg) == type(()):
           conn.privmsg(self.channel, '<%s>: %s' % msg)
        else:
           conn.privmsg(self.channel, '* %s' % msg)

    def attardati(self, e, match):
        self.reply(e, sproloquio.attardati())

    def add_quote(self, e, match):
        quote.add_quote(e.source.nick, match.groups()[0])

    def random_quote(self, e, match):
        self.reply(e, '#%s: %s' % quote.random_quote())
    
    def search_quote(self, e, match):
        q = quote.search_quote(match.groups()[0])
        if q is None:
            self.reply(e, 'no such quote')
        else:
            self.reply(e, '#%s: %s' % q)

    def proverbia(self, e, match):
        self.reply(e, sproloquio.proverbia())

    def on_muori(self,a,b):
        msg=None
        author=None
        message=None
        if os.path.isfile('arnaldo.commit'):
            try:
                f=open('arnaldo.commit',"r")
                allo=f.readline()
                f.close()
                allo=allo.split(':')
                author=allo[0]
                message=":".join(allo[1:])
            except:
                pass
        if author!=None and message!=None:
            message='[%s ha committato "%s"]'%(author, message)
        self.connection.privmsg(self.channel, message if message !=None else "speriamo venga la guerra!" )
        self.connection.disconnect("mi levo di 'ulo.")
        sys.exit(0)

    def on_nicknameinuse(self, c, e):
        c.nick(c.get_nickname() + "_")

    def on_welcome(self, c, e):
        c.join(self.channel)

    def on_privmsg(self, c, e):
        self.do_command(e)

    def on_pubmsg(self, c, e):
        self.do_command(e)

    def register_command(self, regexp, handler, admin=False):
        self.commands.append((re.compile(regexp), handler))

    def do_command(self, e):
        notmatch=True
        for r, callback in self.commands:
            match = r.search(e.arguments[0])
            if match:
                try:
                    callback(e, match)
                    notmatch=False
                    return True
                except Exception as ex:
                    excfazza="Error in"
                    for frame in traceback.extract_tb(sys.exc_info()[2]):
                        fname,lineno,fn,text = frame
                        excfazza=excfazza+ "%s on line %d; " % (fname, lineno)
                    self.reply(e, excfazza+'      Exception: ' + str(ex).replace('\n', ' - '))
                    continue
        if notmatch:
            self.BAMBAM(e)

        self.oembed_link(e)
    
    def boobs(self, e, match):
        self.reply(e, sproloquio.boobs())

    def reply(self, e, m):
        target = e.source.nick if e.target == self.connection.get_nickname() else e.target
        if '\n' in m:
            ll=m.split('\n')
            if len(ll)>12:
                self.connection.privmsg(target, "flodda tu ma'")
            else:
                for l in ll:
                  self.connection.privmsg(target, l)
                  time.sleep(MULTILINE_TOUT)
        else:
            self.connection.privmsg(target, m)



    def icsah(self,e,match):
        try:
            ggallin=None;
            try:
                ggallin=match.groups()[0]
            except:
                pass

            if ggallin:
                icsa= pritaicsa(ggallin)
                self.reply(e,icsa)
        except:
            pass

    def rosa(self, e, match):
        icsa=ritaicsa("rosa")
        self.reply(e,icsa)

    def anal(self, e, match):
        self.reply(e, "%s ANAL %s"%(self.brain.getCitta(),self.brain.getNomecen()))

    def allivello(self, e, match):
        self.reply(e, self.parliamo())

    def eallora(self, e, match):
        self.reply(e, "e allora le foibe?")

    def chilhavisto(self, e, match):
        try:
            ggallin=None;
            try:
                ggallin=match.groups()[0]
            except:
                pass
            if ggallin:
                ts=brain.get(ggallin)
                if ts:
                    response = "chiaro il %s" % datetime.datetime.fromtimestamp(float(ts)).strftime('%d/%m/%y %H:%M:%S')
                else:
                    response = "macche'"
                self.reply(e, response)
        except:
            pass


    def markoviami(self, e, match):
      request = "?"
      ids = match.groups()[0].strip().split()
      print ids
      if (len(ids) > 0):
        for id in ids:
          request = request + "tweetid=" + id.strip() + "&"
      else:
        request = request + "tweetid=Pontifex_it"
      response = urllib2.urlopen("http://markoviami.appspot.com/"+request).read().decode('utf8')
      self.reply(e, response) 

    def brazzafazza(self, e, match):
      h = e.source.host
      if not self.contabrazze.has_key(h):
          self.contabrazze[h] = []

      d = datetime.datetime.now()
      self.contabrazze[h] = filter(lambda x: (d-x).total_seconds() < 60*30, self.contabrazze[h])
      l = self.contabrazze[h]

      if len(l) == 0 or ((d-l[0]).total_seconds() < 60*30 and len(l) < 3):
          self.contabrazze[h].append(d)
          urlo = match.groups()[0]
          response = urllib2.urlopen("http://brazzifier.ueuo.com/index.php?urlz="+urlo).read()
          self.reply(e, response)
      else:
        self.reply(e, "hai rotto il cazzo.")

    def accollo(self, e, match):
        ggallin=None;
        try:
            ggallin=match.groups()[0]
        except:
            pass
        if ggallin:
            urlo="http://shell.appspot.com/shell.do"
            session="agVzaGVsbHITCxIHU2Vzc2lvbhjdlpXJnooGDA"
            response = urllib2.urlopen(urlo+"?&"+urllib.urlencode((("statement",ggallin.replace("@t","    ").replace("@n","\n")),("session",session)))).read()
        self.reply(e,response)
            
    def request_oembed(self, url):
        query = urllib.urlencode((('url', url),))
        data = urllib2.urlopen('http://noembed.com/embed?' + query)
        respa = json.loads(data.read()) #meglio una raspa d'una ruspa
        return respa

    def beuta(self, e, match):
        self.reply(e, '\n'.join(sproloquio.beuta()))

    def parliamo(self):
        wikipedia_url = 'http://it.wikipedia.org/wiki/Speciale:PaginaCasuale#'
        wikipedia_url += str(time.time())
        respa = self.request_oembed(wikipedia_url)
        corpo=respa.get('html',None)
        text="macche'"
        if corpo != None:
            soup = BeautifulSoup(respa['html'])
            if soup.p:
                text=bleach.clean(soup.p,tags=[], strip=True)
        self.parliamo_summary = ' '.join(text.split('\n'))
        return u'Parliamo di ' + respa.get('title',"macche'")

    def checcazzo(self, e, match):
        if self.parliamo_summary:
            self.reply(e, self.parliamo_summary[:430])
            self.parliamo_summary = None

    def oembed_link(self, e):
        allurls = URL_RE.findall(e.arguments[0])
        if len(allurls) != 1:
            pass

        try:
            try: #tipo goto ma peggio
                respa = self.request_oembed(allurls[0][0])
            except:
                pass 
            thaurlhash= hashlib.md5(allurls[0][0]).hexdigest()
            hashish=brain.get("urlo:%s"%thaurlhash)
            if hashish == None: #NO FUMO NO FUTURE
                ts=time.time()
                nic=e.source.nick
                brain.set("urlo:%s"%thaurlhash,"%f:%s:%d"%(ts,nic,1))
                self.reply(e, respa['title'])
            else:
                ts,nic,v=hashish.split(':')
                ts=float(ts)
                delta=time.time() -ts
                v=int(v)+1
                brain.set("urlo:%s"%thaurlhash,"%f:%s:%d"%(ts,nic,v))
                manti,expo=map(float,("%e"%(delta/SECONDIANNO)).split("e"))
                symb,todo=check_SI(expo*v)
                dignene="%.2f %sGaggo [postato da %s il %s]"%(manti+v,symb,nic,datetime.datetime.fromtimestamp(ts).strftime('%d/%m/%y %H:%M:%S'))
                self.reply(e, dignene)
        except:
            pass

    def BAMBAM(self, e):
        brain.set(e.source.nick, time.time())
        t = e.arguments[0]
        if self.BAM == t:
            self.reply(e, self.BAM)
            self.BAM = None
        else:
            try:
                if self.BAM.lower() == self.BAM and \
                        self.BAM.upper() == t:
                    marks = re.compile("([!?.;:]+)$")
                    m = marks.search(t)
                    if m:
                        m = m.groups()[0]
                        t = marks.sub('', t)
                    else:
                        m = ''
                    t = re.sub('i?[aeiou]$', '', t, flags=re.IGNORECASE)
                    self.reply(e, "%sISSIMO%s" % (t, m))
                    self.BAM = None
                else:
                    self.BAM = t
            except:
                self.BAM = t


    def ancheno(self, e, match):
        if self.parliamo_summary:
            self.reply(e, u'ಥ_ಥ  ockay')
            self.parliamo_summary = u'┌∩┐(◕_◕)┌∩┐'


def main():
    import sys
    if len(sys.argv) != 4:
        print "Usage: arnaldo <server[:port]> <channel> <nickname>"
        sys.exit(1)

    s = sys.argv[1].split(":", 1)
    server = s[0]
    if len(s) == 2:
        try:
            port = int(s[1])
        except ValueError:
            print "Error: Erroneous port."
            sys.exit(1)
    else:
        port = 6667
    channel = sys.argv[2]
    nickname = sys.argv[3]

    T800 = Vedetta()
    T800.start() #I'm a friend of Sarah Connor. I was told she was here. Could I see her please?

    bot = Arnaldo(channel, nickname, server, port)
    signal.signal(signal.SIGUSR1, bot.on_muori)
    bot.start()

