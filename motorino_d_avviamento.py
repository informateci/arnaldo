#!/usr/bin/env python
# -*- coding: utf-8 -*-

import subprocess
import signal
import urllib.parse
import json
import hashlib
import tornado.httpserver
import tornado.ioloop
import tornado.web

from arnaldo.brain import redox
from arnaldo.arnaldo import ArnaldoProcess
from arnaldo.conf import PORT, NICK, SLISTEN
import os
PROCESS = None


def rinasci_arnaldo():
    global PROCESS

    if PROCESS is not None:
        os.kill(PROCESS.pid, signal.SIGUSR1)
        os.kill(PROCESS.pid, signal.SIGTERM)

    subprocess.check_call(['git', 'pull'])
    subprocess.check_call(['rm', '-rf', '*.pyc'])
    """PROCESS = subprocess.Popen(
        ('python arnaldo.py irc.freenode.net %s %s' % (CHAN, NICK)).split())"""
    accendi_il_cervello()
    PROCESS = ArnaldoProcess()
    PROCESS.start()

    subprocess.Popen('rm -f arnaldo.commit'.split())


def accendi_il_cervello():

    fosforo = [
        ('dati/citta.txt', 'CITTA'),
        ('dati/nounlist.txt', 'NOMICEN'),
        ('dati/attardi.txt', 'ATTARDI'),
        ('dati/prov1.txt', 'PROV1'),
        ('dati/prov2.txt', 'PROV2')
    ]

    for (data_file, redis_name) in fosforo:
        h = hashlib.md5(open(data_file).read().encode('utf8')).hexdigest()
        if redox.get('__hash_' + redis_name) != h:
            redox.set('__hash_' + redis_name, h)
            with open(data_file, 'r') as f:
                lines = f.readlines()
            print("Rigenero", redis_name)
            for line in lines:
                redox.rpush(redis_name, bytes(line.encode('utf8')).decode('utf8').strip())

    hs = hashlib.md5(open('dati/passvord.txt').read().encode('utf-8')).hexdigest()
    if redox.get("passvordfhash") != hs:
        redox.set("prov2fhash", hs)
        passf = open('dati/passvord.txt', 'r')
        redox.set("httppasswd", passf.readline()[:-1])
        passf.close()


class do_the_404(tornado.web.RequestHandler):

    def get(self):
        self.clear()
        self.set_status(404)
        self.set_header('Content-Type', 'text/html')
        self.finish('<html><h1>ONORE AL COMMENDATORE</h1><audio autoplay loop>'
                    '<source src="http://k002.kiwi6.com/hotlink/7dfwc95g6j/ztuovbziexvt.128.mp3" type="audio/mp3">'
                    '</audio><p><img alt="" src="http://25.media.tumblr.com/tumblr_lxom7sxjDv1qcy8xgo1_500.gif" '
                    'class="alignnone" width="500" height="333"></p></html>')


class le_poste(tornado.web.RequestHandler):

    def get(self):
        self.redirect("/")

    def post(self):
        post_data = urllib.parse.parse_qs(self.request.body)
        author = None
        message = None
        for key, value in post_data.iteritems():
            if key == "payload" and len(value) > 0:
                payload = json.loads(value[0])
                commits = payload.get('commits', None)
                if commits is not None and len(commits) > 0:
                    author = commits[0].get('author', None)
                    message = commits[0].get('message', None)
                    author = author.get('name', None)
                    print("Commit di %s, comment: \"%s\"" % (author, message))

        if author is not None and message is not None:
            f = open("arnaldo.commit", 'w')
            f.write("%s:%s" % (author, message))
            f.close()
            rinasci_arnaldo()
            self.clear()
            self.set_status(200)
            self.finish('OK')


if __name__ == '__main__':
    print('Starting %s' % (NICK, ))
    rinasci_arnaldo()

    print("Starting webserver (%s)" % (PORT, ))
    accatitipi = tornado.web.Application([
        (r"/", do_the_404),
        (r"/github", le_poste)
    ])
    http_server = tornado.httpserver.HTTPServer(accatitipi)
    http_server.listen(PORT, SLISTEN)
    try:
        tornado.ioloop.IOLoop.instance().start()
    except KeyboardInterrupt:
        # faster pussycat
        os.kill(PROCESS.pid, signal.SIGTERM)
