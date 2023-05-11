# vim: set fileencoding=utf-8:
# -*- coding: utf8 -*-
from urllib import parse
import random

from arnaldo.modules import Arnaldigno, comanda
from arnaldo import brain
from imgurpython import ImgurClient
from arnaldo.conf import imgur_client_id, imgur_client_secret
from bs4 import BeautifulSoup
import requests

#imgurclient = ImgurClient(imgur_client_id, imgur_client_secret)


class Sproloquio(Arnaldigno):
    @comanda("attardati")
    def attardati(self, e, match):
        self.r(e, "Stefano %s Attardi" % brain.getAttardi())

    @comanda("ANAL")
    def anal(self, e, match):
        self.r(e, "%s ANAL %s" % (brain.getCitta(), brain.getNomecen()))

    @comanda("proverbia")
    def proverbia(self, e, match):
        self.r(e, self.proverbiaandid()[0])

    def proverbiaandid(self):
        return brain.getProverbioandid()

    def proverbiabyid(self, idp):
        return brain.getProverbiobyid(idp)

    @comanda("beuta")
    def beuta(self, e, match):
        cocktail_id = random.randint(1, 4750)
        data = requests.get(
            "http://web.archive.org/web/20160820200809/http://www.cocktaildb.com/recipe_detail",
            params={"id": cocktail_id},
        )
        if not data.ok:
            self.r(e, "oggi bimbi si va a secco")
            return

        soup = BeautifulSoup(data.text)
        directions = soup.findAll("div", {"class": "recipeDirection"})
        measures = soup.findAll("div", {"class": "recipeMeasure"})

        ret = []
        ret += [u"== %s ==\n" % soup.find("h2").text]

        for m in measures:
            ret += [" ".join([x.strip() for x in m.findAll(text=True)])]

        ret += [""]

        for d in directions:
            ret += [" ".join([x.strip() for x in d.findAll(text=True)])]

        ret += ["enjoy"]
        self.r(e, "\n".join(ret))

    @comanda("boobs please")
    def boobs(self, e, match):
        i = random.choice(
            requests.get(
                "http://www.reddit.com/r/boobies/new.json",
                headers={"User-agent": "Boobs bot"},
            ).json()["data"]["children"]
        )["data"]["url"]
        self.r(e, "%s" % i)

    @comanda("^peppa (.+)")
    def peppa(self, e, match):
        try:
            uguale = match.groups()[0]
            self.r(e, "<peppe> %s=merda" % uguale)
        except Exception as e:
            print(e)

    @comanda("^gagga (.+)")
    def gagga(self, e, match):
        try:
            x = match.groups()[0].upper()

            self.r(e, ' '.join([z for z in x]))
            for i in range(1, len(x)-1):
                self.r(e, f"{x[i]}{' ' * (2*(len(x) - 2)+1) }{x[len(x) - i - 1]}")
            self.r(e, ' '.join([z for z in x[::-1]]))

        except Exception as e:
            print(e)

    @comanda("^gugola (.+)")
    def gugola(self, e, match):
        try:
            uguale = match.groups()[0].encode("utf-8")
            self.r(
                e,
                random.choice(
                    requests.get(
                        "https://duckduckgo.com/i.js?q=%s&o=json" % parse.quote(uguale)
                    ).json()["results"]
                )["image"],
            )
        except Exception as e:
            print("gugola:", e)

    @comanda('^che bell(. .+)')
    def belo(self, e, match):
        try:
            virgilio = match.groups()[0]
            if len(virgilio) > 5 and len(virgilio) <= 30:
                self.r(e, 'bell%s... e` come il treno!' % virgilio)
        except:
            pass


