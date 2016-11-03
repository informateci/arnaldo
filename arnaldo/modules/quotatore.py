# vim: set fileencoding=utf-8:

from arnaldo.modules import Arnaldigno, comanda
from arnaldo.brain import brain

import time
from random import choice
import re


class Quotatore(Arnaldigno):

    @comanda('^%s[:, \\t]*addquote (.*)')
    def add_quote(self, e, match):
        try:
            author = e.source.nick
            quote = match.groups()[0]
            maxa = max([int(x.split(':')[1]) for x in brain.keys('quote:*')])
            q = {"author": author,
                 "date": str(time.time()),
                 "id": str(maxa + 1),
                 "quote": quote}
            brain.set(u"quote:%d" % (maxa + 1), q)
            self.r(e, "vai agile [#%d]"%(maxa+1))
        except:
            self.r(e, "macche'")

    # prima che qualche faccia di merda si lamenti
    # e' l'eval per ritrasformare il tostring di un
    # dizionario (di stringhe per giunta) di nuovo
    # nel dizionario originale.
    # vale la regola, se riuscite a romperlo bravi/lode/avete ragione
    # altrimenti ANDATE IN CULO.

    @comanda('^%s[:, \\t]*quote$')
    def random_quote(self, e, match):
        q = brain.get(choice(brain.keys("quote:*")))

        if q is None:
            return

        q = eval(q)
        self.r(e, '#%s: %s' % (q['id'], q['quote']))

    @comanda('^%s[:, \\t]*quote #(\d+)$')
    def get_quote(self, e, match):

        if match is None:
            return

        q = brain.get("quote:%s" % match.groups()[0])

        if q is None:
            return

        q = eval(q)
        self.r(e, '#%s: %s' % (q['id'], q['quote']))

    @comanda('^%s[:, \\t]*quote ([^#]*)$')
    def search_quote(self, e, match):
        pattern = match.groups()[0]

        regex = re.compile(".*(%s).*" % pattern)

        # <PAZO>
        k = brain.keys("quote:*")
        if len(k) > 0:
            listo = [eval(l) for l in brain.mget(*k)]
            resp = [r for r in listo if regex.search(r['quote'])]
        # </PAZO>

        respa = choice(resp) if len(resp) > 0 else None
        if respa is None:
            self.r(e, 'no such quote')
            return None
        self.r(e, '#%s: %s' % (respa['id'], respa['quote']))

if __name__ == '__main__':
    Quotatore.random_quote()
