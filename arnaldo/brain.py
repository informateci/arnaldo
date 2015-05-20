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


class RedisExtended(redis.Redis):

    def lrand(self, a):
        try:
            return self.lindex(a, randrange(self.llen(a)))
        except Exception:
            return 'NISBA'


class Brain:

    def __init__(self):
        self.data = RedisExtended("localhost")

    @property
    def citta(self):
        return self.data.lrand("CITTA").decode('utf8')

    @property
    def nomecen(self):
        return self.data.lrand("NOMICEN").decode('utf8')

    @property
    def attardi(self):
        return (lambda x: x[0].upper() + x[1:].lower())(self.data.lrand("ATTARDI").decode('utf8'))

    @property
    def proverbiUno(self):
        return self.data.lrand("PROV1").decode('utf8')

    @property
    def proverbiDue(self):
        return self.data.lrand("PROV2").decode('utf8')

    @property
    def proverbioandid(self):
        # prov1 e prov2 sono lunghi uguali
        i = list(range(0, self.data.llen("PROV1")))
        shuffle(i)
        p = ' '.join([
            self.data.lindex("PROV1", i[0]).decode('utf8'),
            self.data.lindex("PROV2", i[1]).decode('utf8')
        ])

        return p, "%dP%d" % (i[0], i[1])

    @property
    def proverbiobyid(self, idp):
        try:
            p = idp.split('P')
            return u' '.join([
                self.data.lindex("PROV1", int(p[0]).decode('utf8')),
                self.data.lindex("PROV2", int(p[1]).decode('utf8'))
            ])
        except Exception as e:
            print('proverbiobyid', e)

brain = Brain()
