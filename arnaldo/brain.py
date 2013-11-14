#! /usr/bin/env python
# vim: set fileencoding=utf-8:

from random import choice, randint

try:
    import redis

    brain = redis.Redis("localhost")
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
            return self.suca.get(a,None)
        def llen(self, a):
            return len(self.suca[a])
        def lindex(self, a, i):
            return len(self.suca[a][i])
        def rpush(self, a, v):
            self.suca[a] = self.suca.get(a,[])
            self.suca[a].append(v)
            return len(self.suca[a]) -1
        def delete(self, a):
            if self.suca.has_key(a):
                del self.suca[a]

    brain = suca()

def choicefromlist(name):
    try:
        i=random.randint(0,b.llen(name)-1)
        return b.lindex(name, i)
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
    i1=random.randint(0,b.llen("PROV1")-1)
    i2=random.randint(0,b.llen("PROV2")-2)
    if i2 >= i1:
        i2 += 1
    p=u"%s %s"%(b.lindex("PROV1", i1).decode('utf8'),self.b.lindex("PROV2", i2).decode('utf8'))
    return (p, "%dP%d"%(i1,i2))

def getProverbiobyid(idp):
    try:
        p=idp.split('P')
        return u"%s %s"%(b.lindex("PROV1", int(p[0])).decode('utf8'),self.b.lindex("PROV2", int(p[1])).decode('utf8'))
    except:
        return "macche'"

