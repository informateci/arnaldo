# vim: set fileencoding=utf-8:
# -*- coding: utf8 -*-
from urllib import request, parse
import random

from arnaldo.modules import Arnaldigno, comanda
from imgurpython import ImgurClient
from arnaldo.conf import imgur_client_id, imgur_client_secret
from bs4 import BeautifulSoup
import arnaldo.brain as b
import requests

imgurclient = ImgurClient(imgur_client_id, imgur_client_secret)


class Sproloquio(Arnaldigno):

    @comanda('attardati')
    def attardati(self, e, match):
        self.r(e, u"Stefano %s Attardi" % b.brain.attardi)

    @comanda('ANAL')
    def anal(self, e, match):
        self.r(e, "%s ANAL %s" % (b.brain.citta, b.brain.nomecen.upper()))

    @comanda('proverbia')
    def proverbia(self, e, match):
        self.r(e, self.proverbiaandid()[0])

    def proverbiaandid(self):
        return b.brain.proverbioandid

    def proverbiabyid(self, idp):
        return b.brain.proverbiobyid(idp)

    @comanda('beuta')
    def beuta(self, e, match):
        cocktail_id = random.randint(1, 4750)
        data = request.urlopen(
            "http://www.cocktaildb.com/recipe_detail?id=%d" % cocktail_id)
        soup = BeautifulSoup(data.read())
        directions = soup.findAll("div", {"class": "recipeDirection"})
        measures = soup.findAll("div", {"class": "recipeMeasure"})

        ret = []
        ret += [u"== %s ==\n" % soup.find("h2").text]

        for m in measures:
            ret += [u' '.join([x.strip() for x in m.findAll(text=True)])]

        ret += [u'']

        for d in directions:
            ret += [u' '.join([x.strip() for x in d.findAll(text=True)])]

        ret += [u'enjoy']
        self.r(e, '\n'.join(ret))

    @comanda('boobs please')
    def boobs(self, e, match):
        i = random.choice(requests.get('http://www.reddit.com/r/boobies/new.json', headers = {'User-agent': 'Boobs bot'} ).json()['data']['children'])['data']['url']
        self.r(e, "%s" % i)

    @comanda('^peppa (.+)')
    def peppa(self, e, match):
        try:
            uguale = match.groups()[0]
            self.r(e, '<peppe> %s=merda' % uguale)
        except Exception as e:
            print(e)

    @comanda('^gugola (.+)')
    def gugola(self, e, match):
        try:
            uguale = match.groups()[0].encode('utf-8')
            self.r(e, random.choice(requests.get("https://duckduckgo.com/i.js?q=%s&o=json" % parse.quote(uguale)).json()['results'])['image'])
        except Exception as e:
            print('gugola:', e)
