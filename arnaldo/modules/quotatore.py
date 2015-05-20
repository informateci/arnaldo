# vim: set fileencoding=utf-8:
import pickle
import time
from random import choice
import re
import arnaldo.brain as b

from arnaldo.modules import Arnaldigno, comanda


class Quotatore(Arnaldigno):

    @comanda('^%s[:, \\t]*addquote (.*)')
    def add_quote(self, e, match):
        author = e.source.nick
        quote = match.groups()[0]
        maxa = max([int(x.decode('utf8').split(':')[1]) for x in b.brain.data.keys('quote:*')] + [-1])
        q = {"author": author,
             "date": str(time.time()),
             "id": str(maxa + 1),
             "quote": quote}
        # Si può usare pure json, come ve pare
        b.brain.data.set("quote:%d" % (maxa + 1), pickle.dumps(q))
        self.r(e, "vai agile [#%d]"%(maxa+1))

    @comanda('^%s[:, \\t]*quote$')
    def random_quote(self, e, match):
        q = b.brain.data.get(choice(b.brain.data.keys("quote:*")))
        if q is None:
            self.r(e, 'NOPE.WAV')
            return
        # Si può usare pure json, come ve pare
        q = pickle.loads(q)
        self.r(e, '#%s: %s' % (q['id'], q['quote']))

    @comanda('^%s[:, \\t]*quote ([^#]*)$')
    def search_quote(self, e, match):
        pattern = match.groups()[0]

        regex = re.compile(".*(%s).*" % pattern)

        # <PAZO>
        k = b.brain.data.keys("quote:*")
        if len(k) > 0:
            listo = [pickle.loads(l) for l in b.brain.data.mget(*k)]
            resp = [r for r in listo if regex.search(r['quote'])]
        # </PAZO>

        respa = choice(resp) if len(resp) > 0 else None
        if respa is None:
            self.r(e, 'no such quote')
            return None
        self.r(e, '#%s: %s' % (respa['id'], respa['quote']))

if __name__ == '__main__':
    Quotatore.random_quote()
