# vim: set fileencoding=utf-8:

from arnaldo.modules import Arnaldigno, comanda
from arnaldo.brain import brain, request_oembed

#
import hashlib
import time
import re
import datetime
import requests

#

URL_RE = re.compile(
    r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)"
    r"(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|"
    r'[^\s`!()\[\]{};:\'".,<>?\xab\xbb\u201c\u201d\u2018\u2019]))'
)


def check_SI(p):
    mapping = [
        (-24, ("y", "yocto")),
        (-21, ("z", "zepto")),
        (-18, ("a", "atto")),
        (-15, ("f", "femto")),
        (-12, ("p", "pico")),
        (-9, ("n", "nano")),
        (-6, ("u", "micro")),
        (-3, ("m", "mili")),
        (-2, ("c", "centi")),
        (-1, ("d", "deci")),
        (3, ("k", "kilo")),
        (6, ("M", "mega")),
        (9, ("G", "giga")),
        (12, ("T", "tera")),
        (15, ("P", "peta")),
        (18, ("E", "exa")),
        (21, ("Z", "zetta")),
        (24, ("Y", "yotta")),
    ]

    for check, value in mapping:
        if p <= check:
            return value


class Linkini(Arnaldigno):
    @comanda("spotify")
    def despotifizzalo(self, e, match):
        matcharella = re.match(".*spotify:track:([a-zA-Z0-9]+)", e.arguments[0])
        allurls = URL_RE.findall(e.arguments[0])

        if matcharella is not None:
            spotisource = "https://open.spotify.com/track/" + matcharella.groups()[0]
        elif len(allurls) == 1:
            spotisource = allurls[0][0]
        else:
            return True

        traducella = requests.get("https://songwhip.com/" + spotisource)

        if not traducella.ok:
            return True

        tutubers = re.findall(r'https://youtube.com/watch\?v=[^"]+', traducella.text)

        if len(tutubers) > 0:
            self.r(e, "^---- " + tutubers[0])

        return True


    @comanda("twitter.com\\/")
    def nitterizzamelo(self, e, match):
        matcharella = re.search("https?:..(www.)?twitter.com\\/[^ ]*status[^ ]*", e.arguments[0])
        if matcharella is None:
            return True

        urla = matcharella[0]
        nittera = urla.replace("twitter.com", "nitter.net")

        self.r(e, nittera)
        return True


    @comanda(".")
    def oembeddalo(self, e, match):
        allurls = URL_RE.findall(e.arguments[0])
        if len(allurls) != 1:
            return True

        # tipo goto ma peggio
        try:
            respa = request_oembed(allurls[0][0])
        except:
            pass
        thaurlhash = hashlib.md5(allurls[0][0].encode()).hexdigest()
        hashish = brain.get("urlo:%s" % thaurlhash)

        try:
            if hashish is None:  # NO FUMO NO FUTURE
                ts = time.time()
                nic = e.source.nick
                brain.set("urlo:%s" % thaurlhash, "%f:%s:%d" % (ts, nic, 1))
                self.r(e, respa["title"])
            elif "[pnd]" not in e.arguments[0].lower():
                secondianno = 31556926  # num secondi in un anno youdontsay.png
                ts, nic, v = hashish.split(":")
                ts = float(ts)
                delta = time.time() - ts
                v = int(v) + 1
                brain.set("urlo:%s" % thaurlhash, "%f:%s:%d" % (ts, nic, v))
                manti, expo = map(float, ("%e" % (delta / secondianno)).split("e"))
                symb, todo = check_SI(expo * v)
                dignene = "%.2f %sGaggo [postato da %s il %s]" % (
                    manti + v,
                    symb,
                    nic,
                    datetime.datetime.fromtimestamp(ts).strftime("%d/%m/%y %H:%M:%S"),
                )
                self.r(e, dignene)
        except:
            pass

        return True
