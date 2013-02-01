from minibot import MiniBot
import pycurl
import cStringIO
from random import choice, randint
import requests
import json


class GourmetBot(MiniBot):

    def __init__(self, nick='Illuvatar594'):
        self.nick = nick
        self.cy = file('SUB-EST2011-01.csv', 'r').read()
        self.nn = file('nounlist.txt', 'r').read()
        MiniBot.__init__(self, 'chat.freenode.net', 6666, '#informateci', self.nick)

    def _on_message(self, author, content, private):
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

if __name__ == "__main__":
    print "Starting GourmetBot 1.0"
    bot = GourmetBot()
    bot.register_command("tipo?", bot._tipo)
    bot.register_command("allivello?", bot._allivello)
    bot.start()

