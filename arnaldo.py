#! /usr/bin/env python

import irc.bot
import irc.strings
from irc.client import ip_numstr_to_quad, ip_quad_to_numstr
import cStringIO
from random import choice, randint
import json
import re
import urllib
import urllib2
from html2text import HTML2Text
import time
import sys, traceback
import bleach
from BeautifulSoup import BeautifulSoup

traceback_template = '''Tracefazza (most recent call last):
  File "%(filename)s", line %(lineno)s, in %(name)s
  %(type)s: %(message)s\n'''



def tdecode(bytes):
    try:
        text = bytes.decode('utf-8')
    except UnicodeDecodeError:
        try:
            text = bytes.decode('iso-8859-1')
        except UnicodeDecodeError:
            text = bytes.decode('cp1252')
    return text


def tencode(bytes):
    try:
        text = bytes.encode('utf-8')
    except UnicodeEncodeError:
        try:
            text = bytes.encode('iso-8859-1')
        except UnicodeEncodeError:
            text = bytes.encode('cp1252')
    return text


class TestBot(irc.bot.SingleServerIRCBot):
    def __init__(self, channel, nickname, server, port=6667):
        irc.bot.SingleServerIRCBot.__init__(self, [(server, port)], nickname, nickname)
        self.channel = channel
        self.commands = []

        self.cy = file('SUB-EST2011-01.csv', 'r').read()
        self.nn = file('nounlist.txt', 'r').read()

        self.parliamo_summary = None

        self.register_command('ANAL', self.anal)
        self.register_command('e allora\\?$', self.eallora)
        self.register_command('^allivello\\?', self.allivello)
        self.register_command('parliamo di', self.allivello)
        self.register_command('parliamone', self.checcazzo)

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
        for r, callback in self.commands:
            match = r.search(e.arguments[0])
            if match:
                try:
                    callback(e, match)
                    return True
                except Exception as ex:
                    excfazza="Error in"
                    for frame in traceback.extract_tb(sys.exc_info()[2]):
                        fname,lineno,fn,text = frame
                        excfazza=excfazza+ "%s on line %d; " % (fname, lineno)    
                    self.reply(e, excfazza+'      Exception: ' + str(ex).replace('\n', ' - '))
                    continue
   
    def reply(self, e, m):
        target = e.source.nick if e.target == self.connection.get_nickname() else e.target
        self.connection.privmsg(target, m)

    def anal(self, e, match):
        self.reply(e, self.ANAL())

    def allivello(self, e, match):
        self.reply(e, self.parliamo2())

    def eallora(self, e, match):
        self.reply(e, "e allora le foibe?")

    def ANAL(self):
        citta=choice([[a.split(',')[1] for a in (self.cy).split(",,,,")[6:-11]]][0])
        citta=citta.upper()
        citta=citta.replace("(BALANCE)",'').replace("CITY",'')
        if citta[-1:]==" ":
            citta=citta[:-1]
        nome=choice(self.nn.split('\n')).upper()
        return "%s ANAL %s"%(citta,nome)

    def parliamo(self):
        request = urllib2.Request('http://it.wikipedia.org/w/api.php?action=query&list=random&rnnamespace=0&rnlimit=1&format=json')
        request.add_header('User-Agent', 'Mozilla/5.0')

        respa = urllib2.build_opener().open(request).read()

        msgg=reduce(dict.get,['query','random'], json.loads(respa))
        if msgg is not None and len(msgg)>0 and msgg[0].get('title',None) is not None:
            troiaio=tdecode(msgg[0].get('title',None))
            return (u"Parliamo di " +(tencode(troiaio))).encode('ascii','replace')

        return ''

    def parliamo2(self):
        wikipedia_url = 'http://it.wikipedia.org/wiki/Speciale:PaginaCasuale#'
        wikipedia_url += str(time.time())
        query = urllib.urlencode((('url', wikipedia_url),))
        data = urllib2.urlopen('http://noembed.com/embed?' + query)
        respa = json.loads(data.read()) #meglio una raspa d'una ruspa
        soup = BeautifulSoup(respa['html'])
        if soup.p:
            text=bleach.clean(soup.p,tags=[], strip=True)
        else:
            text="macche'"
        #text = parser.handle(respa['html'])
        self.parliamo_summary = ' '.join(text.split('\n'))
        return u'Parliamo di ' + respa['title']

    def checcazzo(self, e, match):
        if self.parliamo_summary:
            self.reply(e, self.parliamo_summary[:430])
        
def main():
    import sys
    if len(sys.argv) != 4:
        print "Usage: testbot <server[:port]> <channel> <nickname>"
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

    bot = TestBot(channel, nickname, server, port)
    bot.start()

if __name__ == "__main__":
    main()
