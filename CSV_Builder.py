import settings
import json
import lyricsgenius
from googletrans import Translator
import pandas as pd
from concurrent.futures import ThreadPoolExecutor as PoolExecutor

csv_file_name = settings.csv_file_name
DATE = 'date'
TITLE = 'title'
ARTIST = 'artist'
top = 'peakPos'
WEEKS = 'weeks'
LYRICS = 'lyrics'

apiErr = []
searchErr = []
lengthErr = []
transErr = []
lang = []

genius = lyricsgenius.Genius("kukkuqI5zxzI1leL4unZQWgCFSsL7905bdNgbO8t8axMZH-DNp-l-3__DqBIzsr1", sleep_time=1)
genius.remove_section_headers = True
translator = Translator()

# read songs cvs
df = pd.read_csv('database_without_lyrics.csv', encoding="utf-8-sig")
df = df[df['lyrics'].notna()]
df = df[df['date'].notna()]
# years = df['date'].apply(func = lambda date: int(date[-2:]))
df['year'] = df['date'].str[-2:].astype(int)

def searchSong(row_num):
        s = genius.search_song(title=df[TITLE][row_num], artist=df[ARTIST][row_num])
        return s

def func_1(item):
    k, r = item
    if k % 200 == 0:
        print("===============================================")
        print(k)
        print("===============================================")
    if not pd.isnull(r[LYRICS]):
        return
    try:
        song = searchSong(k)
    except Exception as e:
        print(f"{e},API ERROR in song: {r[TITLE]} line {k}")
        apiErr.append((k, r[TITLE], r[ARTIST], 'API'))
        return
    if song:
        if len(song.lyrics) > 10000:
            print(f"Length ERROR in song: {r[TITLE]} line {k}")
            lengthErr.append((k, r[TITLE], r[ARTIST], 'LEN'))
            return
        try:
            detected_obj = translator.detect(song.lyrics)
            if not detected_obj.lang == 'en':
                print(f"Song: {r[TITLE]} line {k} is not in English!")
                lang.append((k, r[TITLE], r[ARTIST], 'Not in EN'))
                translated_lyrics = translator.translate(text=song.lyrics, dst='EN')
                df[LYRICS][k] = translated_lyrics.text
                return
        except Exception as e:
            print(f"{e} Translation ERROR in song: {r[TITLE]} line {k}")
            transErr.append((k, r[TITLE], r[ARTIST], 'Trans'))
        df[LYRICS][k] = song.lyrics
    else:
        print(f"Search ERROR in song: {r[TITLE]} line {k}")
        searchErr.append((k, r[TITLE], r[ARTIST], 'SEARCH'))


def create_csv_with_lyrics_database():
    with PoolExecutor(max_workers=15) as executor:
        for _ in executor.map(func_1, df.iterrows()):
        # for _ in executor.map(func_1, itertools.islice(df.iterrows(), 40)):
            pass

    df.to_csv(csv_file_name, index=False, encoding='utf-8-sig')

    with open('apiErr.json', 'w') as json_file:
        json.dump(apiErr, json_file, indent=4)
        json_file.seek(0)
        json_file.close()

    with open('searchErr.json', 'w') as json_file:
        json.dump(searchErr, json_file, indent=4)
        json_file.seek(0)
        json_file.close()

    with open('lengthErr.json', 'w') as json_file:
        json.dump(lengthErr, json_file, indent=4)
        json_file.seek(0)
        json_file.close()

    with open('transErr.json', 'w') as json_file:
        json.dump(transErr, json_file, indent=4)
        json_file.seek(0)
        json_file.close()

    with open('lang.json', 'w') as json_file:
        json.dump(lang, json_file, indent=4)
        json_file.seek(0)
        json_file.close()

    print("=====\nDONE\n=====")

