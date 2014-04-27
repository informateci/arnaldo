# vim: set fileencoding=utf-8:

from arnaldo.modules import Arnaldigno, comanda
from arnaldo.modules.linkini import request_oembed

from BeautifulSoup import BeautifulSoup
import time
import bleach

class Parliamo(Arnaldigno):
    def __init__(self, *args):
        super(Parliamo, self).__init__(*args)
        self.parliamo_summary = None

    @comanda('e allora\\?$')
    def eallora(self, e, match):
        self.reply(e, "e allora le foibe?")

    @comanda('(^allivello\\?)|(parliamo di)')
    def allivello(self, e, match):
        wikipedia_url = 'http://it.wikipedia.org/wiki/Speciale:PaginaCasuale#'
        wikipedia_url += str(time.time())
        respa = request_oembed(wikipedia_url)
        corpo = respa.get('html',None)
        text="macche'"
        if corpo != None:
            soup = BeautifulSoup(respa['html'])
            if soup.p:
                text=bleach.clean(soup.p, tags=[], strip=True)

        self.parliamo_summary = ' '.join(text.split('\n'))
        self.r(e, u'Parliamo di ' + respa.get('title',"macche'"))

    @comanda('parliamone')
    def parliamone(self, e, match):
        if self.parliamo_summary:
            self.reply(e, self.parliamo_summary[:430])
            self.parliamo_summary = None

    @comanda('anche no')
    def ancheno(self, e, match):
        if self.parliamo_summary:
            self.reply(e, u'ಥ_ಥ  ockay')
            self.parliamo_summary = u'┌∩┐(◕_◕)┌∩┐'

