#! /usr/bin/env python
# vim: set fileencoding=utf-8:

from random import randint
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


class Redos:

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
        except ImportError:
            return object.__getattribute__(self, item)

        if isinstance(self._self, redis.Redis):
            return getattr(self._self, item)
        else:
            return object.__getattribute__(self, item)

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


class Brain:

    def __init__(self):
        self._brain = Redos()

    def choicefromlist(self, name):
        try:
            i = randint(0, self._brain.llen(name) - 1)
            return self._brain.lindex(name, i)
        except:
            return 'NISBA'

    @property
    def città(self):
        return self.choicefromlist("CITTA")

    def getNomecen(self):
        return self.choicefromlist("NOMICEN")

    def getAttardi(self):
        return self.choicefromlist("ATTARDI")

    def getProverbiUno(self):
        return self.choicefromlist("PROV1")

    def getProverbiDue(self):
        return self.choicefromlist("PROV2")

    def getProverbioandid(self):
        i1 = randint(0, self._brain.llen("PROV1") - 1)
        i2 = randint(0, self._brain.llen("PROV2") - 2)
        if i2 >= i1:
            i2 += 1
        p = u"%s %s" % (self._brain.lindex("PROV1", i1).decode(
            'utf8'), self._brain.lindex("PROV2", i2).decode('utf8'))
        return p, "%dP%d" % (i1, i2)

    def getProverbiobyid(self, idp):
        try:
            p = idp.split('P')
            return u"%s %s" % (self._brain.lindex("PROV1", int(p[0])).decode('utf8'),
                               self._brain.lindex("PROV2", int(p[1])).decode('utf8'))
        except:
            return

brain = Brain()
