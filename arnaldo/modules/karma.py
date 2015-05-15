# -*- coding: utf-8 -*-

from arnaldo.brain import brain
from arnaldo.conf import NICK
from arnaldo.modules import Arnaldigno, comanda


class Karmelo(Arnaldigno):

    @comanda('(.*)\+\+')
    def karmelone(self, e, match):
        icche = match.groups()[0].lower()
        indove = u'__karma_%s'.encode('utf-8') % (icche,)
        k = brain.get(indove)
        brain.set(indove, 1 + (int(k) if k else 0))
        self.r(e, 'vabbé'.decode('utf-8'))

    @comanda('(.*)\-\-')
    def karmelino(self, e, match):
        icche = match.groups()[0].lower()
        indove = u'__karma_%s'.encode('utf-8') % (icche,)
        k = brain.get(indove)
        brain.set(indove, (int(k) if k else 0) - 1)

    @comanda('^%s\s*[:,]\s*(.*)\?' % (NICK, ))
    def karma(self, e, match):
        icche = match.groups()[0].lower()
        indove = u'__karma_%s'.encode('utf-8') % (icche,)
        k = brain.get(indove)
        if k:
            self.r(e, u'karma %s: %d'.encode('utf-8') % (icche, int(k)))
        else:
            self.r(e, u'%s chi?'.encode('utf-8') % (icche, ))