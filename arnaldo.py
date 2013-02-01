from minibot import MiniBot
import pycurl
import cStringIO
from random import choice, randint
import requests
import json
import re

class GourmetBot(MiniBot):

    def __init__(self, nick='Illuvatar594'):
        self.nick = nick
        self.cy = file('SUB-EST2011-01.csv', 'r').read()
        self.nn = file('nounlist.txt', 'r').read()
        MiniBot.__init__(self, 'chat.freenode.net', 6666, '#informateci', self.nick)
        self.commands = [
            (re.compile('ANAL'), self.anal),
            (re.compile('^allivello\\?'), self.allivello)
        ]
        self.strip_name = re.compile('^\s*(' + self.nick + ')?[.:]?\s*')

    def _on_message(self, author, content, private):
        stripped_content = self.strip_name.sub('', content)
        for r, callback in self.commands:
            match = r.search(stripped_content)
            if match:
                callback(match)
                return

    def anal(self, match):
        print " -- NEW ANAL --"
        self.write_message(self.ANAL())

    def allivello(self, match):
        print " -- NEW ALLIVELLO --"
        self.write_message(self.parliamo())

    def OLD_on_message(self, author, content, private):
        if ("ANAL" in content):
            print "Say it!"
            sayit=self.ANAL()
            self.write_message(sayit)
        else:
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
        respa = requests.get('http://it.wikipedia.org/w/api.php?action=query&list=random&rnnamespace=0&rnlimit=1&format=json', headers={'User-Agent':'Mozilla/5.0'})
        if(respa.ok):
             msgg=reduce(dict.get,['query','random'], json.loads(respa.content))
             if msgg is not None and len(msgg)>0 and msgg[0].get('title',None) is not None:
                 return "Parliamo di " + (msgg[0].get('title',None)).encode("utf-8")
        return None


    def _tipo(self,n,a,p,d):
            print "Say it!"
            sayit=self.ANAL()
            self.write_message(sayit)
            return True

    def _allivello(self,n,a,p,d):
            print "Say it!"
            sayit=self.parliamo()
            self.write_message(sayit)
            return True

    def _eallora(self,n,a,p,d):
            print "Say it!"
            self.write_message("e allora le foibe?")
            return True

if __name__ == "__main__":
    print "Starting GourmetBot 1.0"
    bot = GourmetBot()
    bot.register_command("tipo?", bot._tipo)
    bot.register_command("allivello?", bot._allivello)
    bot.register_command("e allora?", bot._eallora)
    bot.start()

