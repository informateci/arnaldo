from minibot import MiniBot
import cStringIO
from random import choice, randint
import json
import re
import urllib2

class GourmetBot(MiniBot):

    def __init__(self, nick='Illuvatar594'):
        self.nick = nick
        self.cy = file('SUB-EST2011-01.csv', 'r').read()
        self.nn = file('nounlist.txt', 'r').read()
        MiniBot.__init__(self, 'chat.freenode.net', 6666, '#informateci', self.nick)

        self.register_command('ANAL', self.anal)
        self.register_command('^allivello\\?', self.allivello)
        self.register_command('e allora\\?$', self.eallora)
        self.register_command('peso', self.peso)

    def anal(self, match):
        print " -- NEW ANAL --"
        self.write_message(self.ANAL())

    def allivello(self, match):
        print " -- NEW ALLIVELLO --"
        self.write_message(self.parliamo())

    def eallora(self, match):
        self.write_message("e allora le foibe?")

    def peso(self, match):
        self.write_message("PESO")

    def OLD_on_message(self, author, content, private):
        nrand = randint(0, 2000)
        if nrand <= 2:
            print "Say it!"
            sayit=self.ANAL()
            self.write_message(sayit)
        elif nrand <= 4:
            print "Say it!"
            sayit=self.parliamo()
            self.write_message(sayit)

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
            return "Parliamo di " + (msgg[0].get('title',None)).encode("utf-8")

        return ''

if __name__ == "__main__":
    bot = GourmetBot()
    bot.start()

