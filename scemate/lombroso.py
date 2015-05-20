from arnaldo.brain import redox
import datetime
import pickle

# utility sceme per affettare il cervello di arnaldo e dumpare la roba
# senza poesia fa qualche file pickle della roba only in memory


def dump_quote():
    keys = redox.keys("quote:*")
    quotazze = redox.mget(*keys)
    # quotazze = [ eval(q) for q in quotazze ]
    # il formato e' list di {'date':string, 'quote': string, 'id':string,
    # 'author': string}
    pickle.dump(quotazze,
                open("quotes_%s.p" %
                (datetime.datetime.now().strftime("%Y-%m-%d-%H:%M")), "wb"))


def dump_gaggold():
    keys = redox.keys("urlo:*")
    urli = redox.mget(*keys)
    urlazzi = [dict(date=q[0], nick=q[1], num=q[2])
               for q in [q.split(':') for q in urli]]
    # il formato e' list di {'date': string, 'nick': string, 'num': string}
    pickle.dump(urlazzi,
                open("urls_%s.p" %
                (datetime.datetime.now().strftime("%Y-%m-%d-%H:%M")), "wb"))
