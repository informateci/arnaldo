# vim: set fileencoding=utf-8:
from arnaldo.modules import Arnaldigno, comanda
import arnaldo.brain as b

class Icsah(Arnaldigno):

    def pritaicsa(self, text):
        icsa = ""
        for row in range(int(b.brain.get("asciitable:rows"))):
            for c in text:
                icsa = str(icsa) + str(b.brain.lindex("asciitable:%s" % c, row))
            icsa += '\n'
        icsa += '\n'
        return icsa

    @comanda('^icsah (.+)')
    def icsah(self, e, match):
        try:
            ggallin = match.groups()[0]
        except:
            ggallin = None
        if not ggallin:
            return
        try:
            icsa = self.pritaicsa(ggallin)
            self.r(e, icsa)
        except:
            pass

    @comanda('^bamba$')
    def rosa(self, e, match):
        icsa = self.pritaicsa("rosa")
        self.r(e, icsa)
