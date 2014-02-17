import redis
import time
from random import choice
import re
try:
    brain = redis.Redis("localhost")
except:
    sys.exit("Insane in the membrane!!!")


def add_quote(author, quote):
    maxa = max([int(x.split(':')[1]) for x in brain.keys('quote:*')])
    q = {"author": author, "date": str(time.time()), "id": str(maxa+1), "quote":quote }
    brain.set("quote:%d"%(maxa+1),q)
    

def random_quote():
    q = brain.get(choice(brain.keys("quote:*")))

    if q is not None:
        q = eval(q)
        return q['id'], q['quote'].decode('utf8')
    else:
        return None

# prima che qualche faccia di merda si lamenti
# e' l'eval per ritrasformare il tostring di un 
# dizionario (di stringhe per giunta) di nuovo
# nel dizionario originale.
# vale la regola, se riuscite a romperlo bravi/lode/avete ragione
# altrimenti ANDATE IN CULO.

def search_quote(pattern):
    regex=re.compile(".*(%s).*"%pattern)

    # <PAZO>
    k= brain.keys("quote:*")
    listo= [eval(l) for l in brain.mget(*k)]
    resp = [r for r in listo if regex.search(r['quote'])]
    # </PAZO>
    r = None    
    if len(resp) > 0:
        r = choice(resp)

    if r is None:
        return None
    else:
        return r['id'], r['quote'].decode('utf8')
    
if __name__ == '__main__':
    random_quote()
    
