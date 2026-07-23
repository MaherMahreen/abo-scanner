"""
==========================================
ABO SCANNER
SCORE ENGINE v1.0
==========================================
"""

class ScoreEngine:

    def __init__(self):
        self.score = 0
        self.alasan = []

    def tambah(self, poin, alasan):
        self.score += poin
        self.alasan.append(alasan)

    def hasil(self):
        return {
            "score": self.score,
            "alasan": self.alasan
        }

    def reset(self):
        self.score = 0
        self.alasan = []
