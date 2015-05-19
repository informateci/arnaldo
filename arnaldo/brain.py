#! /usr/bin/env python
# vim: set fileencoding=utf-8:

from random import randrange, shuffle
# ci fisto anche tutta la roba condivisibile,
# non condivisibile eticamente, condivisibile che si condivide
import urllib.parse
import urllib.request
import json
from blinker import signal as lasigna

dimme = lasigna('dimmelo')


def request_oembed(url):
    query = urllib.parse.urlencode((('url', url),))
    data = urllib.request.urlopen('http://noembed.com/embed?' + query)
    respa = json.loads(data.read().decode('utf-8'))  # meglio una raspa d'una ruspa
    return respa


class Redox:

    def __init__(self):
        try:
            import redis
            self._self = redis.Redis("localhost")
        except ImportError:
            print("")
            self._self = {}
        except ConnectionError:
            self._self = {}

    def __getattribute__(self, item):
        if item == '_self':
            return object.__getattribute__(self, item)

        try:
            import redis
            return getattr(self._self, item)
        except:
            return object.__getattribute__(self, item)

    def lrand(self, a):
        try:
            return self.lindex(a, randrange(self.llen(a)))
        except Exception:
            return 'NISBA'

    def set(self, a, b):
        self._self[a] = b

    def get(self, a):
        return self._self.get(a, None)

    def llen(self, a):
        return len(self._self[a])

    def lindex(self, a, i):
        return len(self._self[a][i])

    def rpush(self, a, v):
        self._self[a] = self._self.get(a, [])
        self._self[a].append(v)
        return len(self._self[a]) - 1

    def delete(self, a):
        if a in self._self:
            del self._self[a]


redox = Redox()


class Brain:
    global redox

    @property
    def città(self):
        return redox.lrand("CITTA")

    @property
    def nomecen(self):
        return redox.lrand("NOMICEN")

    @property
    def attardi(self):
        return (lambda x: x[0].upper() + x[1:])(redox.lrand("ATTARDI"))

    @property
    def proverbiUno(self):
        return redox.lrand("PROV1")

    @property
    def proverbiDue(self):
        return redox.lrand("PROV2")

    @property
    def proverbioandid(self):
        # prov1 e prov2 sono lunghi uguali
        i = list(range(0, redox.llen("PROV1")))
        shuffle(i)
        # TODO: capire perché c'è in mezzo '\r'
        p = ' '.join([
            redox.lindex("PROV1", i[0]).replace(b'\r', b'').decode('utf8'),
            redox.lindex("PROV2", i[1]).replace(b'\r', b'').decode('utf8')
        ])

        return p, "%dP%d" % (i[0], i[1])

    @property
    def proverbiobyid(self, idp):
        try:
            p = idp.split('P')
            return u' '.join([
                redox.lindex("PROV1", int(p[0])).decode('utf8'),
                redox.lindex("PROV2", int(p[1])).decode('utf8')
            ])
        except:
            return


brain = Brain()