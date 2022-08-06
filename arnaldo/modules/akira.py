import re
import random

from arnaldo.modules import Arnaldigno, comanda


class Akira(Arnaldigno):

    @comanda(r'TETSU(O+)([!?]*)')
    def tetsuo(self, e, match):

        ooo, esclama = match.groups()
        aaa = "A" * len(ooo)

        self.r(e, f'KANED{aaa}{esclama}')

        return True

    @comanda(r'KANED(A+)([!?]*)')
    def tetsuo(self, e, match):

        aaa, esclama = match.groups()
        ooo = "O" * len(aaa)

        self.r(e, f'TETSU{ooo}{esclama}')

        return True
