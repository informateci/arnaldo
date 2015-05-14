# vim: set fileencoding=utf-8:

from arnaldo.modules import Arnaldigno, comanda
from arnaldo import brain
from imgurpython import ImgurClient
from arnaldo.conf import imgur_client_id, imgur_client_secret
from BeautifulSoup import BeautifulSoup
import urllib2
import random

imgurclient = ImgurClient(imgur_client_id, imgur_client_secret)

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
        data = urllib2.urlopen(
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
        i = random.choice(imgurclient.subreddit_gallery('boobs'))
        self.r(e, "%s" % i.link)

    @comanda('^peppa (.+)')
    def peppa(self, e, match):
        try:
            uguale = match.groups()[0]
            self.r(e, '<peppe> %s=merda' % uguale)
        except:
            pass

