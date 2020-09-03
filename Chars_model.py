import random
from collections import *
from Statistics import *
import pandas as pd
import enchant

def split(word):
    return [char for char in word]

class char_lm(object):
    def __init__(self, order=11):
        self.order = order
        self.chars = set()
        self.songs_list = []
        self.lm = defaultdict(Counter)
        self.conds = {}

        path = settings.chars_dir
        if not os.path.isdir(path):
            os.mkdir(path)

        path = settings.chars_model
        if os.path.exists(path):
            print('----- Reading Chars Model Database ------')
            with open(settings.chars_model, 'r') as json_file:
                self.conds = json.load(json_file)
                json_file.seek(0)
            print('-----  DONE ------')
        else:
            df = pd.read_csv(settings.csv_file_name, encoding="utf-8-sig", usecols=['lyrics', 'weeks', 'year'])
            for index, row in df.iterrows():
                self.chars.update(split(row['lyrics']))
                pad = "~" * self.order
                self.songs_list.append((pad + row['lyrics'], row['weeks']))
            self.chars = sorted(list(self.chars))
            self.train_char_lm()

    def train_char_lm(self):
        def normalize(counter):
            s = float(sum(counter.values()))
            return [(c, cnt / s) for c, cnt in counter.items()]

        print('----- Analyzing Chars Model ------')
        self.c_count = len(self.chars)
        order = self.order
        for song in self.songs_list:
            for i in range(len(song[0]) - self.order):
                history, char = song[0][i:i + order], song[0][i + order]
                self.lm[history][char] += int(song[1])

        outlm = {hist: normalize(chars) for hist, chars in self.lm.items()}

        print('-----  Storing Data ------')

        with open(settings.chars_model, 'w') as json_file:
            json.dump(outlm, json_file, indent=4)
            json_file.seek(0)

        print('-----  DONE ------')

        self.conds = outlm
        return self

    def generate_letter(self, history):
        order = self.order
        history = history[-order:]
        dist = self.conds.get(history)
        if dist is None:
            return None
        x = random.random()
        for c, v in dist:
            x = x - v
            if x <= 0: return c

    def generate_song(self, nletters=3500):
        history = "~" * self.order
        d = enchant.Dict("en_US")
        out = []
        for i in range(nletters):
            c = self.generate_letter(history)
            if c is None:
                break
            history = history[-self.order:] + c
            if c == '%':
                c = str(random.randint(0, 9))
            out.append(c)

        song = "".join(out)
        song_words_list = song.split()
        last_word = song_words_list[-1]
        if d.check(last_word) and len(last_word) > 2:
            return song
        else:
            return ' '.join(song_words_list[:-1])
