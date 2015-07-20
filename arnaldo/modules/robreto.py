from arnaldo.modules import Arnaldigno, comanda
import re
import random


class Robreto(Arnaldigno):

    @comanda('(.*robreto.*)')
    def robreto(self, e, match):
        vow = "aeiouy"
        vow += vow.upper()
        con = "bcdfghjklmnpqrstvwxz"
        con += con.upper()
        # cv_pattern = "([%s][%s])" % (con, vow)
        ll_pattern = "([a-zA-Z][a-zA-Z])"
        cvc_pattern = "([%s][%s][%s])" % (con, vow, con)

        tokenamelo = ["(robreto)", "([0-9A-Za-z]+)", "(\s+)", "(.)"]
        la_stringa = match.groups()[0]
        al_stingra = ""

        while la_stringa:
            m = [x for x in [re.match("^" + token, la_stringa) for token in tokenamelo] if x]
            wut = m[0].groups()[0]
            la_stringa = la_stringa[len(wut):]
            if wut == 'robreto':
                la_stringa = la_stringa.lstrip()
            else:
                moneta = random.random()
                cvs = re.findall(ll_pattern if (moneta > 0.5) else cvc_pattern, wut)
                if cvs:
                    torev = random.choice(cvs)
                    al_stingra += re.sub(torev, torev[::-1], wut, 1)
                else:
                    al_stingra += wut

        self.r(e, al_stingra)

        return True


if __name__ == '__main__':
    def printamela(x):
        print x

    class Coso(object):
        def groups(self):
            return ["messaggio per fare robreto"]

        def register_command(self, x, y):
            pass

        def reply(self, x, y):
            print y

    c = Robreto(Coso())
    c.robreto(printamela, Coso())
