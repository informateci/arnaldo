from arnaldo.modules import Arnaldigno, comanda
from arnaldo import brain


class Disco(Arnaldigno):
    @comanda(
        r"(((luned|marted|gioved|venerd)[iì]'*|sabato)[\s]+sera|mercoled[iì]i'*|domenica)\?*$"
    )
    def aladiscoteca(self, e, match):
        ducazzate = {
            "mercoled": ["che mal di testa", "ma sono andata", "AL"],
            "venerd": [
                "non volevo andare ma Fabio e' venuto a cercarmi e allora sono andata",
                "AL",
            ],
            "domenica": ["...", "AL"],
        }

        dove = "LA DISCOTECA"
        for cazzata in match.groups():
            if cazzata in ducazzate:
                for c in ducazzate[cazzata][:-1]:
                    self.r(e, c)
                dove = ducazzate[-1] + dove
        self.r(e, dove)
