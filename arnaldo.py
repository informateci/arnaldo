from minibot import MiniBot
import pycurl
import cStringIO
from random import choice, randint
import urllib2
import json


class GourmetBot(MiniBot):

    def __init__(self):
        self.cy = file('SUB-EST2011-01.csv', 'r').read()
        self.nn = file('nounlist.txt', 'r').read()
        MiniBot.__init__(self, 'chat.freenode.net', 6666, '#informateci', 'Illuvatar594')
        opener = urllib2.build_opener()
        opener.addheaders = [('User-agent', 'Mozilla/5.0')]

    def _on_message(self, author, content, private):
        if ("ANAL" in content):
            print "Say it!"
            sayit=self._doit()
            self.write_message(sayit)
        else
	    nrand = randint(0, 2000)
            if nrand <= 2:
                print "Say it!"
                sayit=self._doit()
                self.write_message(sayit)
            elif nrand <= 4:
                print "Say it!"
                infile = opener.open('http://it.wikipedia.org/w/api.php?action=query&list=random&rnnamespace=0&rnlimit=1&format=json')
                sayit="Parliamo di " + json.loads(infile.read())['query']['random'][0]['title']
                self.write_message(sayit)
            
    def _doit(self):
        citta=choice([[a.split(',')[1] for a in (self.cy).split(",,,,")[6:-11]]][0])
        citta=citta.upper()
        citta=citta.replace("(BALANCE)",'').replace("CITY",'')
        if citta[-1:]==" ":
            citta=citta[:-1]
        nome=choice(self.nn.split('\n')).upper()
        return "%s ANAL %s"%(citta,nome)
    def _tipo(self,n,a,p,d):
            print "Say it!"
            sayit=self._doit()
            self.write_message(sayit)
            return True

if __name__ == "__main__":
    print "Starting GourmetBot 1.0"
    bot = GourmetBot()
    bot.register_command("tipo?", bot._tipo)
    bot.start()
