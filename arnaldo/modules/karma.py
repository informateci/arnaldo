# -*- coding: utf-8 -*-

from arnaldo.brain import redox
from arnaldo.conf import NICK
from arnaldo.modules import Arnaldigno, comanda


class Karmelo(Arnaldigno):

    @comanda(r'^([^\s]+)\+\+')
    def karmelone(self, e, match):
        icche = match.groups()[0]
        indove = u'__karma_%s' % (icche.lower(),)
        k = redox.get(indove)
        redox.set(indove, 1 + (int(k) if k else 0))
        self.r(e, 'vabbé')

    @comanda(r'^([^\s]+)\-\-')
    def karmelino(self, e, match):
        icche = match.groups()[0]
        indove = u'__karma_%s' % (icche.lower(),)
        k = redox.get(indove)
        redox.set(indove, (int(k) if k else 0) - 1)
        self.r(e, 'vabbé')

    @comanda(r'^%s\s*[:,]\s*(.*)\?' % (NICK, ))
    def karma(self, e, match):
        icche = match.groups()[0]
        indove = u'__karma_%s' % (icche.lower(),)
        k = redox.get(indove)
        if k:
            self.r(e, u'karma %s: %d' % (icche, int(k)))
        else:
            self.r(e, u'%s chi?' % (icche, ))
