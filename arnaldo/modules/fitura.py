from arnaldo.modules import Arnaldigno, comanda
from arnaldo import brain


class Fitura(Arnaldigno):
    @comanda(r"^RFC:\s*(.*)")
    def fituriquest(self, e, match):
        brain.rpush("__RFC", match.groups()[0])
        self.r(e, "Noted.")

    @comanda(r"^RFC ([\d]+)")
    def dammifitur(self, e, match):
        self.r(e, brain.lindex("__RFC", int(match.groups()[0])).decode("utf8"))

    @comanda(r"^RFC\?")
    def quantefitur(self, e, match):
        self.r(e, "Ci sono %d RFC" % (brain.llen("__RFC"),))
