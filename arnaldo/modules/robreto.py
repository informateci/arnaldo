from arnaldo.modules import Arnaldigno, comanda
from random import shuffle


class Robreto(Arnaldigno):

    @comanda('(.*robreto.*)')
    def robreto(self, e, match):
        words = [list(m) for m in match.split() if len(m) > 3 and m != 'robreto']
        for w in range(0, len(words)):
            shuffle(words[w], lambda: 0.10)

        self.r(e, ' '.join([''.join(w) for w in words]))

        return True
