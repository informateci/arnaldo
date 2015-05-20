# vim: set fileencoding=utf-8:

import irc.bot
import irc.strings
import os
import os.path
import sys
import time
import traceback
import signal

#
from arnaldo.conf import CHAN, SLISTEN, PORT, arnaldo_port, arnaldo_server
from arnaldo.conf import NICK
from .utieffa import *
from .vedetta import Vedetta, dimme
#

from .modules.sproloquio import Sproloquio
from .modules.parliamo import Parliamo
from .modules.quotatore import Quotatore
from .modules.accolli import Accolli
from .modules.icsah import Icsah
from .modules.bam import BAM
from .modules.fitura import Fitura
from .modules.linkini import Linkini
from .modules.robreto import Robreto
from .modules.karma import Karmelo

import multiprocessing


class Arnaldo(irc.bot.SingleServerIRCBot):

    def __init__(self, channel, nickname, server, port=6667):
        irc.client.ServerConnection.buffer_class = BambaRosaNasaBuffer
        irc.bot.SingleServerIRCBot.__init__(
            self, [(server, port)], nickname, nickname)
        self.nickname = nickname
        self.channel = channel
        self.commands = []

        dimme.connect(self.dimmeame)

        self.modules = [x(self) for x in [
            Accolli, BAM, Fitura, Icsah, Karmelo, Linkini, Parliamo, Quotatore, Robreto, Sproloquio
        ]]

    def dimmeame(self, msg):
        conn = self.connection
        if isinstance(msg, tuple):
            conn.privmsg(self.channel, '<%s>: %s' % msg)
        else:
            conn.privmsg(self.channel, '* %s' % msg)

    def on_muori(self):
        author = None
        message = None
        if os.path.isfile('arnaldo.commit'):
            try:
                f = open('arnaldo.commit', "r")
                allo = f.readline()
                allo = allo.decode('utf8')
                f.close()
                allo = allo.split(':')
                author = allo[0]
                message = ":".join(allo[1:])
            except:
                pass
        if author is not None and message is not None:
            message = '[%s ha committato "%s"]' % (author, message)
        self.connection.privmsg(
            self.channel,
            message if message is not None else "speriamo venga la guerra!")
        self.connection.disconnect("mi levo di 'ulo.")
        sys.exit(0)

    def on_nicknameinuse(self, c, e):
        c.nick(c.get_nickname() + "_")

    def on_welcome(self, c, e):
        c.join(self.channel)

    def on_privmsg(self, c, e):
        self.do_command(e)

    def on_pubmsg(self, c, e):
        self.do_command(e)

    def register_command(self, regexp, handler, admin=False):
        self.commands.append((re.compile(regexp), handler))

    def do_command(self, e):
        for r, callback in self.commands:
            match = r.search(e.arguments[0])
            if match:
                try:
                    if not callback(e, match):
                        return True
                except Exception as ex:
                    excfazza = "Error in"
                    for frame in traceback.extract_tb(sys.exc_info()[2]):
                        fname, lineno, fn, text = frame
                        excfazza = "%s %s on line %d; " % (
                            excfazza, fname, lineno)
                    self.reply(
                        e,
                        excfazza + '      Exception: ' + str(
                            ex).replace('\n', ' - '))
                    continue

    def reply(self, e, m):
        multiline_tout = 0.5
        target = e.source.nick \
            if e.target == self.connection.get_nickname() \
            else e.target
        if '\n' in m:
            ll = m.split('\n')
            if len(ll) > 12:
                self.connection.privmsg(target, "flodda tu ma'")
            else:
                for l in ll:
                    self.connection.privmsg(target, l)
                    time.sleep(multiline_tout)
        else:
            self.connection.privmsg(target, m)


class ArnaldoProcess(multiprocessing.Process):

    def __init__(self):
        super(multiprocessing.Process, self).__init__()
        self.T800 = None
        self.bot = None

    def run(self):
        self.T800 = Vedetta()
        self.T800.start()
        self.bot = Arnaldo(CHAN, NICK, arnaldo_server, arnaldo_port)

        try:  # Windows workaround
            signal.signal(signal.SIGUSR1, self.fista_duro_e_vai_sicuro)
        except:
            pass

        try:
            self.bot.start()
        except KeyboardInterrupt:
            self.T800.stop()

    def fista_duro_e_vai_sicuro(self, ma, cche):
        print("fisto duro e vado sicuro")
        if self.bot:
            self.bot.on_muori()
        if self.T800:
            self.T800.stop()
        print("per davvero")