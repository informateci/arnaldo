from functools import partial


def comanda(regex):
    def d(f):
        f.regex = regex
        return f
    return d


class Arnaldigno(object):
    def __init__(self, arnaldo):
        self.arnaldo = arnaldo

        for name, thing in self.__class__.__dict__.iteritems():
            regexp = getattr(thing, 'regex', None)

            if regexp:
                if '%s' in regexp:
                    regexp = regexp % (self.arnaldo.nickname,)

                self.arnaldo.register_command(regexp, partial(thing, self))

    def r(self, e, m):
        self.arnaldo.reply(e, m)
