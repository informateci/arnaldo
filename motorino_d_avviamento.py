#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pickle
import subprocess
import signal
import urllib.parse
import json
import hashlib
import redis
import tornado.httpserver
import tornado.ioloop
import tornado.web
import sys
from arnaldo.conf import PORT, SERVER, CHAN, NICK, SLISTEN, REDIS, PASSVORD

PROCESS = None


def rinasci_arnaldo():
    global PROCESS

    if PROCESS is not None:
        PROCESS.send_signal(signal.SIGUSR1)
        PROCESS.kill()

    try:
        subprocess.check_call(["git", "pull"])
    except:
        print("io ho provato a pullare ma m'ha fatto brutto, vedi te")
    subprocess.check_call(["rm", "-rf", "*.pyc"])
    PROCESS = subprocess.Popen(
        ("python -m arnaldo %s %s %s" % (SERVER, CHAN, NICK)).split()
    )
    subprocess.Popen("rm -f arnaldo.commit".split())
    accendi_il_cervello()


def accendi_il_cervello():
    try:
        brain = redis.Redis(REDIS)
    except:
        sys.exit("Insane in the membrane!!!")

    hs = hashlib.md5(open("dati/SUB-EST2011-01.csv", "rb").read()).hexdigest()
    if brain.get("cyfhash") != hs:
        brain.set("cyfhash", hs)
        cyf = open("dati/SUB-EST2011-01.csv", "r")
        cy = cyf.read()
        cyf.close()
        print("Rigenero CITTA")
        brain.delete("CITTA")
        for c in [[a.split(",")[1].upper() for a in (cy).split(",,,,")[6:-11]]][0]:
            brain.rpush("CITTA", c)  # in CITTA c'e' la lista delle citta' maiuscole

    hs = hashlib.md5(open("dati/nounlist.txt", "rb").read()).hexdigest()
    if brain.get("nnfhash") != hs:
        brain.set("nnfhash", hs)
        nnf = open("dati/nounlist.txt", "r")
        nn = nnf.read()
        nnf.close()
        print("Rigenero NOMICEN")
        brain.delete("NOMICEN")
        for n in nn.split("\n"):
            brain.rpush(
                "NOMICEN", n.upper()
            )  # in NOMIc'e' la lista dei nomi (comuni) inglesi in maiuscolo

    hs = hashlib.md5(open("dati/attardi.txt", "rb").read()).hexdigest()
    if brain.get("attaffhash") != hs:
        brain.set("attaffhash", hs)
        attaf = open("dati/attardi.txt", "r")
        atta = attaf.readlines()
        attaf.close()
        print("Rigenero ATTARDI")
        brain.delete("ATTARDI")
        for a in [x.capitalize()[:-1] for x in atta]:
            brain.rpush(
                "ATTARDI", a
            )  # in NOMIc'e' la lista dei nomi (comuni) inglesi in maiuscolo

    hs = hashlib.md5(open("dati/prov1.pkl", "rb").read()).hexdigest()
    if brain.get("prov1fhash") != hs:
        brain.set("prov1fhash", hs)
        pkl_file = open("dati/prov1.pkl", "rb")
        PROV1 = pickle.load(pkl_file)
        pkl_file.close()
        print("Rigenero PROV1")
        brain.delete("PROV1")
        for p1 in PROV1:  # lista prima meta' dei proverbi in PROV1
            brain.rpush("PROV1", " ".join(p1))
        del PROV1

    hs = hashlib.md5(open("dati/prov2.pkl", "rb").read()).hexdigest()
    if brain.get("prov2fhash") != hs:
        brain.set("prov2fhash", hs)
        pkl_file = open("dati/prov2.pkl", "rb")
        PROV2 = pickle.load(pkl_file)
        pkl_file.close()
        print("Rigenero PROV2")
        brain.delete("PROV2")
        for p2 in PROV2:  # lista 2a meta' dei proverbi in PROV2
            brain.rpush("PROV2", " ".join(p2))
        del PROV2

    brain.set("httppasswd", PASSVORD)


class do_the_404(tornado.web.RequestHandler):
    def get(self):
        self.clear()
        self.set_status(404)
        self.set_header("Content-Type", "text/html")
        self.finish(
            "<html><h1>ONORE AL COMMENDATORE</h1><audio autoplay loop>"
            '<source src="http://k002.kiwi6.com/hotlink/7dfwc95g6j/ztuovbziexvt.128.mp3" type="audio/mp3">'
            '</audio><p><img alt="" src="http://25.media.tumblr.com/tumblr_lxom7sxjDv1qcy8xgo1_500.gif" '
            'class="alignnone" width="500" height="333"></p></html>'
        )


class le_poste(tornado.web.RequestHandler):
    def get(self):
        self.redirect("/")

    def post(self):
        print(self.request.body)
        post_data = urllib.parse.parse_qs(self.request.body)
        author = None
        message = None
        for key, value in post_data.items():
            if key == "payload" and len(value) > 0:
                payload = json.loads(value[0])
                commits = payload.get("commits", None)
                if commits is not None and len(commits) > 0:
                    author = commits[0].get("author", None)
                    message = commits[0].get("message", None)
                    author = author.get("name", None)
                    print('Commit di %s, comment: "%s"' % (author, message))

        if author is not None and message is not None:
            f = open("arnaldo.commit", "w")
            sw = "%s:%s" % (author, message)
            f.write(sw.encode("utf8"))
            f.close()
            rinasci_arnaldo()
            self.clear()
            self.set_status(200)
            self.finish("OK")


if __name__ == "__main__":
    print("Starting %s" % (NICK,))
    rinasci_arnaldo()

    print("Starting webserver (%s)" % (PORT,))
    accatitipi = tornado.web.Application([(r"/", do_the_404), (r"/github", le_poste)])
    http_server = tornado.httpserver.HTTPServer(accatitipi)
    http_server.listen(PORT, SLISTEN)
    try:
        tornado.ioloop.IOLoop.instance().start()
    except KeyboardInterrupt:
        # faster pussycat
        PROCESS.kill()
        # PROCESS.kill()
