from arnaldo.modules import Arnaldigno, comanda
import arnaldo.brain as b

class Fitura(Arnaldigno):

    @comanda('^RFC:\s*(.*)')
    def fituriquest(self, e, match):
        b.brain.data.rpush('__RFC', match.groups()[0])
        self.r(e, 'Noted.')

    @comanda('^RFC ([\d]+)')
    def dammifitur(self, e, match):
        self.r(e, b.brain.data.lindex('__RFC', int(match.groups()[0])).decode('utf8'))

    @comanda('^RFC\?')
    def quantefitur(self, e, match):
        self.r(e, 'Ci sono %d RFC' % (b.brain.data.llen('__RFC'), ))
