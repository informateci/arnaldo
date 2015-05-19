#! /usr/bin/env python
# vim: set fileencoding=utf-8:

from random import randrange, shuffle
# ci fisto anche tutta la roba condivisibile,
# non condivisibile eticamente, condivisibile che si condivide
from urllib import request, parse
import json
import redis
from blinker import signal as lasigna

dimme = lasigna('dimmelo')


def request_oembed(url):
    query = parse.urlencode((('url', url),))
    data = request.urlopen('http://noembed.com/embed?' + query)
    respa = json.loads(data.read().decode('utf-8'))  # meglio una raspa d'una ruspa
    return respa


class Redisnt:

    robba = {}

    def __init__(self, x):
        print("Ignoring", x)

    def lrand(self, a):
        try:
            return self.lindex(a, randrange(self.llen(a)))
        except Exception:
            return 'NISBA'

    def lrand(self, a):
        try:
            return self.lindex(a, randrange(self.llen(a)))
        except Exception:
            return 'NISBA'

    def set(self, a, b):
        Redisnt.robba[a] = b

    def get(self, a):
        return Redisnt.robba.get(a, None)

    def llen(self, a):
        return len(Redisnt.robba[a])

    def lindex(self, a, i):
        return Redisnt.robba[a][i]

    def rpush(self, a, v):
        Redisnt.robba[a] = Redisnt.robba.get(a, [])
        Redisnt.robba[a].append(v)
        return len(Redisnt.robba[a]) - 1

    def delete(self, a):
        if a in Redisnt.robba:
            del Redisnt.robba[a]


class RedisExtended(redis.Redis):

    def lrand(self, a):
        try:
            return self.lindex(a, randrange(self.llen(a)))
        except Exception:
            return 'NISBA'


try:
    import redis.exceptions
    q = redis.Redis("localhost")
    q.get("stocazzo")
    Redox = RedisExtended
except redis.exceptions.ConnectionError:
    print("No redis server")
finally:
    Redox = Redisnt


class Brain:

    def __init__(self):
        self.data = Redox("localhost")

    @property
    def citta(self):
        return self.data.lrand("CITTA")

    @property
    def nomecen(self):
        return self.data.lrand("NOMICEN")

    @property
    def attardi(self):
        return (lambda x: x[0].upper() + x[1:])(self.data.lrand("ATTARDI"))

    @property
    def proverbiUno(self):
        return self.data.lrand("PROV1")

    @property
    def proverbiDue(self):
        return self.data.lrand("PROV2")

    @property
    def proverbioandid(self):
        # prov1 e prov2 sono lunghi uguali
        i = list(range(0, self.data.llen("PROV1")))
        shuffle(i)
        p = ' '.join([
            self.data.lindex("PROV1", i[0]),
            self.data.lindex("PROV2", i[1])
        ])

        return p, "%dP%d" % (i[0], i[1])

    @property
    def proverbiobyid(self, idp):
        try:
            p = idp.split('P')
            return u' '.join([
                self.data.lindex("PROV1", int(p[0])),
                self.data.lindex("PROV2", int(p[1]))
            ])
        except Exception as e:
            print('proverbiobyid', e)


brain = Brain()
