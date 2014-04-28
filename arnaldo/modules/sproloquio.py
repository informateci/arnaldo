# vim: set fileencoding=utf-8:

from arnaldo.modules import Arnaldigno, comanda
from arnaldo import brain

from BeautifulSoup import BeautifulSoup
import urllib2
import random


class Sproloquio(Arnaldigno):
    @comanda('attardati')
    def attardati(self, e, match):
        self.r(e, u"Stefano %s Attardi" % brain.getAttardi().decode('utf8'))

    @comanda('ANAL')
    def anal(self, e, match):
        self.r(e, "%s ANAL %s" % (brain.getCitta(), brain.getNomecen()))

    @comanda('proverbia')
    def proverbia(self, e, match):
        self.r(e, self.proverbiaandid()[0])

    def proverbiaandid(self):
        return brain.getProverbioandid()

    def proverbiabyid(self, idp):
        return brain.getProverbiobyid(idp)

    @comanda('beuta')
    def beuta(self, e, match):
        cocktail_id = random.randint(1, 4750)
        data = urllib2.urlopen("http://www.cocktaildb.com/recipe_detail?id=%d" % cocktail_id)
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
        urlo = "http://imgur.com/r/boobies/new/day/page/%d/hit?scrolled"
        response = urllib2.urlopen(urlo % random.randint(1, 50)).read()
        soup = BeautifulSoup(response)
        l = soup.findAll("div", {"class": "post"})
        i = random.choice(l)
        self.r(e, "http://i.imgur.com/%s.jpg" % i.get("id"))

