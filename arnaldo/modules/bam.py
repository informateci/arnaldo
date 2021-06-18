# vim: set fileencoding=utf-8:
from arnaldo.brain import redox
from arnaldo.modules import Arnaldigno, comanda
import time
import re
import datetime
runicode = r"u'\\N{(.*?)}'"

class BAM(Arnaldigno):

    def __init__(self, *args):
        super(BAM, self).__init__(*args)
        self.BAM = None

    @comanda('.')
    def BAMBAM(self, e, match):
        redox.set(e.source.nick, time.time())
        t = e.arguments[0]
        runi = re.search(runicode, t)
        if (runi is not None):
            try:
                self.r(e, "%s" % eval(runi.group()) )
            except:
                pass
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
            ts = redox.get(ggallin)
            if ts:
                response = "chiaro il %s" % datetime.datetime.fromtimestamp(
                    float(ts)).strftime('%d/%m/%y %H:%M:%S')
            else:
                response = "macche'"
            self.r(e, response)
        except:
            pass
