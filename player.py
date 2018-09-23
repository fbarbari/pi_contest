from kivy.uix.popup import Popup
from kivy.properties import BooleanProperty

import os
import pickle

from collections import namedtuple

Player = namedtuple('Player', ['name', 'score', 'score_str'])


class PlayerPopup(Popup):

    MAX_PLAYER_LENGTH = 10
    MAX_PLAYER_TOPLIST = 10

    saved = BooleanProperty(False)

    def __init__(self, score=0, score_str="",
                 file_score='the_scores.txt', *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.score = score
        if score_str:
            self.score_str = score_str
        else:
            self.score_str = self.score
        self.file_score = file_score

        self.series = []
        self.series = self._read()

        self.title = "Inserisci nome per punteggio\n{}".format(self.score_str)

    def _read(self):
        try:
            return pickle.load(open(self.file_score, 'rb'))
        except BaseException:
            return []

    def _write(self):
        pickle.dump(self.series, open(self.file_score, 'wb'))

    def _sort(self):
        self.series = sorted(self.series, key=lambda tup: tup[1], reverse=True)

    def reset(self):
        try:
            os.remove(self.file_score)
        except BaseException:
            print("except removing {}".format(self.file_score))

    def save(self):
        self._sort()
        self._write()
        self.saved = True
        score = self.player.score_str.split(", ")
        HerPopup(
            "'{}' ha calcolato\n{}\n{}".format(
                self.player.name,
                score[0],
                score[1]),
            "Nome salvato").open()
        self.dismiss()

    def add(self, *args, **kwargs):
        self.series.append(self.player)
        self.save()

    def replace(self, *args, **kwargs):
        ranks = self.player_rank_all()
        print(ranks)
        if ranks:
            self.series[ranks[-1]] = self.player
            self.save()
        else:
            self.add()

    def is_unique(self):
        return not self.player.name in [i.name for i in self.series]

    def list(self, format=True, all_players=False):
        if not self.series:
            return ""
        if all_players:
            s = slice(None, None, None)
        else:
            s = slice(self.MAX_PLAYER_TOPLIST)
        if format:
            return "\n".join(["{:2d}. {:10s} : {}".format(
                i + 1, item.name, item.score_str) for i, item in enumerate(self.series[s])])
        else:
            return self.series[s]

    def player_rank(self):
        return [i[0] for i in self.series].index(self.player[0]) + 1

    def player_rank_all(self):
        return [i for i, v in enumerate(
            self.series) if v.name == self.player.name]

    def player_score(self):
        for i in self.series:
            if self.player[0] == i[0]:
                return i[1]

    def save_player(self, player_name):

        self.player = Player(player_name, self.score, self.score_str)

        if not player_name:
            HerPopup("Inserisci un nome", "Errore nel nome").open()
        else:

            if self.is_unique():
                self.add()
            else:
                pop = ExistingPopup("Nome '{}' già registrato\ncon punteggio\n{}\nalla posizione {}".format(
                    player_name,
                    self.player_score(),
                    self.player_rank()),
                    "attenzione"
                )
                pop.ids.save_button.bind(on_press=self.add)
                # pop.ids.save_button.bind(on_press=pop.dismiss)
                pop.ids.replace_button.bind(on_press=self.replace)
                pop.open()


class TemplatePopup(Popup):
    pass


class HerPopup(TemplatePopup):

    def __init__(self, msg, title=""):
        super().__init__()
        self.title = title
        self.ids.msg.text = msg


class ExistingPopup(TemplatePopup):

    def __init__(self, msg, title=""):
        super().__init__()
        self.title = title
        self.ids.msg.text = msg
