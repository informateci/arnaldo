# vim: set fileencoding=utf-8:

from arnaldo.modules import Arnaldigno, comanda
#

from collections import defaultdict
import urllib2
import datetime
import urllib


class Accolli(Arnaldigno):

    def __init__(self, *args):
        super(Accolli, self).__init__(*args)
        self.contabrazze = defaultdict(list)

    @comanda('^brazzami (.+)')
    def brazzafazza(self, e, match):
        h = e.source.host
        d = datetime.datetime.now()
        self.contabrazze[h] = filter(
            lambda x: (d - x).total_seconds() < 60 * 30, self.contabrazze[h])
        l = self.contabrazze[h]
        if not len(l) or ((d - l[0]).total_seconds() < 60 * 30 and len(l) < 3):
            self.contabrazze[h].append(d)
            urlo = match.groups()[0]
            response = urllib2.urlopen(
                "http://brazzifier.ueuo.com/index.php?urlz=" + urlo
            ).read()
            self.r(e, response)
        else:
            self.r(e, "hai rotto il cazzo.")

    @comanda('^markoviami(.*)')
    def markoviami(self, e, match):
        request = "?"
        ids = match.groups()[0].strip().split()

        if len(ids) > 0:
            for id in ids:
                request = request + "tweetid=" + id.strip() + "&"
        else:
            request += "tweetid=Pontifex_it"

        response = urllib2.urlopen(
            "http://markoviami.appspot.com/" + request
        ).read().decode('utf8')
        self.r(e, response)

    # @comanda('^facci (.+)') # MA TI CHETI?
    def accollo(self, e, match):
        try:
            ggallin = match.groups()[0]
        except:
            return

        ggallin = ggallin.replace("@t", "\t")
        ggallin = ggallin.replace("@n", "\n")
        urlo = "http://shell.appspot.com/shell.do"
        session = "agVzaGVsbHITCxIHU2Vzc2lvbhjdlpXJnooGDA"
        para = (("statement", ggallin), ("session", session))
        para = urllib.urlencode(para)
        response = urllib.urlopen(urlo + "?&" + para).read()
        self.r(e, response)
