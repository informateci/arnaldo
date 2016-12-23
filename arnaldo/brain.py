#! /usr/bin/env python
# vim: set fileencoding=utf-8:

from random import randint
# ci fisto anche tutta la roba condivisibile,
# non condivisibile eticamente, condivisibile che si condivide
import urllib
import json
from blinker import signal as lasigna

dimme = lasigna('dimmelo')


def request_oembed(url):
    query = urllib.urlencode((('url', url),))
    data = urllib.urlopen('http://noembed.com/embed?' + query)
    respa = json.loads(data.read())  # meglio una raspa d'una ruspa
    return respa


try:
    import redis

    brain = redis.Redis("localhost", decode_responses=True)
    try:
        brain.set('vaffanculo', 'uno')
    except:
        raise
except:
    # L'HAI VOLUTO IL DUCK TYPING?

    class suca:

        def __init__(self):
            self.suca = {}

        def set(self, a, b):
            self.suca[a] = b

        def get(self, a):
            return self.suca.get(a, None)

        def llen(self, a):
            return len(self.suca[a])

        def lindex(self, a, i):
            return len(self.suca[a][i])

        def rpush(self, a, v):
            self.suca[a] = self.suca.get(a, [])
            self.suca[a].append(v)
            return len(self.suca[a]) - 1

        def delete(self, a):
            if a in self.suca:
                del self.suca[a]

    brain = suca()


def choicefromlist(name):
    try:
        i = randint(0, brain.llen(name) - 1)
        return brain.lindex(name, i)
    except:
        return 'NISBA'


def getCitta():
    return choicefromlist("CITTA")


def getNomecen():
    return choicefromlist("NOMICEN")


def getAttardi():
    return choicefromlist("ATTARDI")


def getProverbiUno():
    return choicefromlist("PROV1")


def getProverbiDue():
    return choicefromlist("PROV2")


def getProverbioandid():
    i1 = randint(0, brain.llen("PROV1") - 1)
    i2 = randint(0, brain.llen("PROV2") - 2)
    if i2 >= i1:
        i2 += 1
    p = u"%s %s" % (brain.lindex("PROV1", i1), brain.lindex("PROV2", i2))
    return p, "%dP%d" % (i1, i2)


def getProverbiobyid(idp):
    try:
        p = idp.split('P')
        return u"%s %s" % (brain.lindex("PROV1", int(p[0])),
                           brain.lindex("PROV2", int(p[1])))
    except:
        return u"macche'"
