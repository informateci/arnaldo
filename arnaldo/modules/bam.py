# vim: set fileencoding=utf-8:

from arnaldo.modules import Arnaldigno, comanda
from arnaldo.brain import brain
import time
import re
import datetime


class BAM(Arnaldigno):

    def __init__(self, *args):
        super(BAM, self).__init__(*args)
        self.BAM = None

    @comanda('.')
    def BAMBAM(self, e, match):
        brain.set(e.source.nick, time.time())
        t = e.arguments[0]
        if self.BAM == t:
            self.r(e, self.BAM)
            self.BAM = None
        else:
            try:
                if self.BAM.lower() == self.BAM and \
                        self.BAM.upper() == t:
                    marks = re.compile("([!?.;:]+)$")
                    m = marks.search(t)
                    if m:
                        m = m.groups()[0]
                        t = marks.sub('', t)
                    else:
                        m = ''
                    t = re.sub('i?[aeiou]$', '', t, flags=re.IGNORECASE)
                    self.r(e, "%sISSIMO%s" % (t, m))
                    self.BAM = None
                else:
                    self.BAM = t
            except:
                self.BAM = t

        return True

    @comanda('^arnaldo hai visto (.+)\\?')
    def chilhavisto(self, e, match):
        try:
            ggallin = match.groups()[0]
        except:
            ggallin = None

        if not ggallin:
            return

        try:
            ts = brain.get(ggallin)
            if ts:
                response = "chiaro il %s" % datetime.datetime.fromtimestamp(
                    float(ts)).strftime('%d/%m/%y %H:%M:%S')
            else:
                response = "macche'"
            self.r(e, response)
        except:
            pass
