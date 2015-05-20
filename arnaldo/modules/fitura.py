from arnaldo.brain import redox
from arnaldo.modules import Arnaldigno, comanda


class Fitura(Arnaldigno):

    @comanda('^RFC:\s*(.*)')
    def fituriquest(self, e, match):
        redox.rpush('__RFC', match.groups()[0])
        self.r(e, 'Noted.')

    @comanda('^RFC ([\d]+)')
    def dammifitur(self, e, match):
        self.r(e, redox.lindex('__RFC', int(match.groups()[0])).decode('utf8'))

    @comanda('^RFC\?')
    def quantefitur(self, e, match):
        self.r(e, 'Ci sono %d RFC' % (redox.llen('__RFC'), ))
