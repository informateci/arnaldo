# -*- coding: utf-8 -*-

from arnaldo.brain import brain
from arnaldo.conf import NICK, CHAN
from arnaldo.modules import Arnaldigno, comanda


class Karmelo(Arnaldigno):

    @comanda('(.*)\+\+')
    def karmelone(self, e, match):
        u = self.arnaldo.channels[CHAN].users()
        icche = '__karma_%s' % (match.groups()[0],)
        if match.groups()[0] in u:
            k = brain.get(icche)
            brain.set(icche, 1 + (int(k) if k else 0))
            self.r(e, 'vabbé'.decode('utf-8'))
        else:
            self.r(e, 'nenti sacciu e nenti vitti')

    @comanda('(.*)\-\-')
    def karmelino(self, e, match):
        u = self.arnaldo.channels[CHAN].users()
        icche = '__karma_%s' % (match.groups()[0],)
        if match.groups()[0] in u:
            k = brain.get(icche)
            brain.set(icche, (int(k) if k else 0) - 1)
            self.r(e, 'vabbé'.decode('utf-8'))
        else:
            self.r(e, 'nenti sacciu e nenti vitti')

    @comanda('^%s\s*[:,]\s*(.*)\?' % (NICK, ))
    def karma(self, e, match):
        icche = '__karma_%s' % (match.groups()[0],)
        k = brain.get(icche)
        if k:
            self.r(e, 'karma %s: %d' % (match.groups()[0], int(k)))
        else:
            self.r(e, '%s chi?' % (match.groups()[0], ))