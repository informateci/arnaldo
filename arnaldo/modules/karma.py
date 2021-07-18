# -*- coding: utf-8 -*-

from arnaldo.brain import brain
from arnaldo.conf import NICK, CHAN
from arnaldo.modules import Arnaldigno, comanda


class Karmelo(Arnaldigno):
    @comanda(r"(.*)\+\+")
    def karmelone(self, e, match):
        icche = match.groups()[0].lower()
        if icche in self.arnaldo.channels[CHAN].users():
            indove = f"__karma_{icche}".encode("utf-8")
            k = (lambda x: int(x) if x is not None else 0)(brain.get(indove)) + 1
            brain.set(indove, k)
            self.r(e, f"{icche}: {k}")

    @comanda(r"(.*)\-\-")
    def karmelino(self, e, match):
        icche = match.groups()[0].lower()
        if icche in self.arnaldo.channels[CHAN].users():
            indove = f"__karma_{icche}".encode("utf-8")
            k = (lambda x: int(x) if x is not None else 0)(brain.get(indove)) - 1
            brain.set(indove, k)
            self.r(e, f"{icche}: {k}")

    @comanda(r"^%s\s*[:,]\s*(.*)\?" % (NICK,))
    def karma(self, e, match):
        icche = match.groups()[0].lower()
        indove = f"__karma_{icche}".encode("utf-8")
        k = brain.get(indove)
        if k:
            self.r(e, f"karma {icche}: {k}")
        else:
            self.r(e, f"{icche} chi?")
