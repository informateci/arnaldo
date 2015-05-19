# vim: set fileencoding=utf-8:
# -*- coding: utf8 -*-
from arnaldo.brain import brain

from arnaldo.modules import Arnaldigno, comanda
from imgurpython import ImgurClient
from arnaldo.conf import imgur_client_id, imgur_client_secret
from bs4 import BeautifulSoup
from urllib import request, parse
import random
import json

imgurclient = ImgurClient(imgur_client_id, imgur_client_secret)


class Sproloquio(Arnaldigno):

    @comanda('attardati')
    def attardati(self, e, match):
        self.r(e, u"Stefano %s Attardi" % brain.attardi)

    @comanda('ANAL')
    def anal(self, e, match):
        self.r(e, "%s ANAL %s" % (brain.citta, brain.nomecen.upper()))

    @comanda('proverbia')
    def proverbia(self, e, match):
        self.r(e, self.proverbiaandid()[0])

    def proverbiaandid(self):
        return brain.proverbioandid

    def proverbiabyid(self, idp):
        return brain.proverbiobyid(idp)

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
        i = random.choice(imgurclient.subreddit_gallery('boobies'))
        self.r(e, "%s" % i.link)

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
            response = request.urlopen(
                "http://ajax.googleapis.com/ajax/services/search/images?safe=off&tbs=isz:lt,istl:vga&rsz=8&v=1.0&q=" +
                parse.quote(uguale)
            )
            self.r(e, random.choice(json.loads(response.read().decode('utf8'))['responseData']['results'])['url'])
        except Exception as e:
            print('gugola:', e)
