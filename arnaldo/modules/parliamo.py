# vim: set fileencoding=utf-8:

import time

from arnaldo.modules import Arnaldigno, comanda
from arnaldo.brain import request_oembed

from random import choice
from bs4 import BeautifulSoup
import bleach


class Parliamo(Arnaldigno):
    parliamo_summary = ""

    @comanda("e allora\\?$")
    def eallora(self, e, match):
        self.r(e, choice(["e allora le foibe?", "e allora bibbiano?"]))

    @comanda("(^allivello\\?)|(parliamo di)")
    def allivello(self, e, match):
        wikipedia_url = "http://it.wikipedia.org/wiki/Speciale:PaginaCasuale#" + str(
            time.time()
        )
        respa = request_oembed(wikipedia_url)
        corpo = respa.get("html", None)
        text = "macche'"
        if corpo is not None:
            soup = BeautifulSoup(respa["html"])
            if soup.p:
                text = bleach.clean(soup.p, tags=[], strip=True)

        self.parliamo_summary = " ".join(text.split("\n"))
        self.r(e, u"Parliamo di " + respa.get("title", "macche'"))

    @comanda("parliamone")
    def parliamone(self, e, match):
        if self.parliamo_summary:
            self.r(e, self.parliamo_summary[:430])
            self.parliamo_summary = None

    @comanda("anche no")
    def ancheno(self, e, match):
        if self.parliamo_summary:
            self.r(e, "ಥ_ಥ  ockay")
            self.parliamo_summary = "┌∩┐(◕_◕)┌∩┐"
