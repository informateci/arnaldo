# -*- coding: utf-8 -*-

from arnaldo.brain import brain
from arnaldo.conf import NICK, CHAN
from arnaldo.modules import Arnaldigno, comanda


class Karmelo(Arnaldigno):

    @comanda('(.*)\+\+')
    def karmelone(self, e, match):
        icche = match.groups()[0].lower()
        print self.arnaldo.channels[CHAN].users()
        if icche in self.arnaldo.channels[CHAN].users():
            indove = u'__karma_%s'.encode('utf-8') % (icche,)
            k = (lambda x: int(x) if x is not None else 0)(brain.get(indove)) + 1
            brain.set(indove, k)
            self.r(e, u'%s: %d'.encode('utf-8') % (icche, k))

    @comanda('(.*)\-\-')
    def karmelino(self, e, match):
        icche = match.groups()[0].lower()
        if icche in self.arnaldo.channels[CHAN].users():
            indove = u'__karma_%s'.encode('utf-8') % (icche,)
            k = (lambda x: int(x) if x is not None else 0)(brain.get(indove)) - 1
            brain.set(indove, k)

    @comanda('^%s\s*[:,]\s*(.*)\?' % (NICK, ))
    def karma(self, e, match):
        icche = match.groups()[0].lower()
        indove = u'__karma_%s'.encode('utf-8') % (icche,)
        k = brain.get(indove)
        if k:
            self.r(e, u'karma %s: %d'.encode('utf-8') % (icche, int(k)))
        else:
            self.r(e, u'%s chi?'.encode('utf-8') % (icche, ))
