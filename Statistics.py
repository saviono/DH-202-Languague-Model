import json
import os
import numpy as np
import matplotlib.pyplot as plt
import settings
import pandas as pd
import plotly.express as px


def statistics_per_song(song):
    chars_num = len(song)
    song = song.split('\n')
    stanza_num = song.count('') + 1
    words_num = 0
    song = list(filter(''.__ne__, song))
    lines_num = len(song)
    for line in song:
        words_num += len(line.split())
    return {
        "lines": lines_num,
        "words_per_line": int(round(words_num / lines_num)),
        "stanza": stanza_num,
        "lines_per_stanza": int(round(lines_num / stanza_num)),
        "chars": chars_num,
        "words": words_num
    }


def create_average_statistics_database(input_file, output_file):
    path = settings.statistics_dir
    if not os.path.isdir(path):
        os.mkdir(path)
    df = pd.read_csv(input_file, encoding="utf-8-sig", usecols=['lyrics'])
    total_stanza_num = 0
    total_lines_num = 0
    total_words_num = 0
    total_chars_num = 0
    songs_num = 0
    for index, row in df.iterrows():
        song_statistics = statistics_per_song(row['lyrics'])
        total_stanza_num += song_statistics['stanza']
        total_lines_num += song_statistics['lines']
        total_words_num += song_statistics['words']
        total_chars_num += song_statistics['chars']
        songs_num += 1
    average_stanzas = int(round(total_stanza_num / songs_num))
    average_lines = int(round(total_lines_num / songs_num))
    average_words = int(round(total_words_num / songs_num))
    average_chars = int(round(total_chars_num / songs_num))

    statistics = {
        "average_lines": average_lines,
        "average_words_per_line": int(round(average_words / average_lines)),
        "average_stanzas": average_stanzas,
        "average_lines_per_stanza": int(round(average_lines / average_stanzas)),
        "average_chars": average_chars,
        "average_words": average_words
    }

    with open(output_file, 'w') as json_file:
        json.dump(statistics, json_file, indent=4)
        json_file.seek(0)

    print('------------ Statistics file generated ---------------')
    return statistics


def calc_common_words_number_for_generated_song(song):
    with open(settings.word_cloud_billboard_list_json) as file:
        data = json.load(file)
        cloud_set = set(data)
        song_set = set(song.split())
        inter = set.intersection(cloud_set, song_set)
    return (len(inter))


def find_best_song(input_file):
    df = pd.read_csv(input_file, encoding="utf-8-sig", usecols=['lyrics'])
    result = None

    with open(settings.statistics_json, 'r') as json_file:
        billboard_statistics = json.load(json_file)
        json_file.seek(0)

    songs_stanza = []
    while (not songs_stanza):
        for index, row in df.iterrows():
            song_statistics = statistics_per_song(row['lyrics'])
            if abs(song_statistics['stanza'] - billboard_statistics['average_stanzas']) <=1:
                songs_stanza.append(row['lyrics'])

    songs_lines_per_stanza = []
    while (not songs_lines_per_stanza):
        for song in songs_stanza:
            song_statistics = statistics_per_song(song)
            if abs((song_statistics['lines']/song_statistics['stanza']) - billboard_statistics['average_lines_per_stanza']) == 0:
                songs_lines_per_stanza.append(song)

    songs_words_per_lines = []
    while (not songs_words_per_lines):
        for song in songs_lines_per_stanza:
            song_statistics = statistics_per_song(song)
            if abs((song_statistics['words']/song_statistics['lines']) - billboard_statistics['average_words_per_line']) <=1:
                songs_words_per_lines.append(song)

    songs_lines = []
    while (not songs_lines):
        for song in songs_words_per_lines:
            song_statistics = statistics_per_song(song)
            if abs(song_statistics['lines'] - billboard_statistics['average_lines']) <= 5:
                songs_lines.append(song)

    songs_words = []
    while (not songs_words):
        for song in songs_lines:
            song_statistics = statistics_per_song(song)
            if abs(song_statistics['words'] - billboard_statistics['average_words']) <= 30:
                songs_words.append(song)

    songs_chars = []
    while (not songs_chars):
        for song in songs_words:
            song_statistics = statistics_per_song(song)
            if abs(song_statistics['chars'] - billboard_statistics['average_chars']) <= 100:
                songs_chars.append(song)



    # print('result:' + str(len(songs_chars)))
    # print('####################################################')
    # for i, song in enumerate(songs_chars):
    #     print(str(i) + '****************************')
    #     print(song)
    #     print('****************************')

    s = ''
    min = 0
    for song in songs_chars:
        res = calc_common_words_number_for_generated_song(song)
        if (res > min):
            s = song
            min = res

    return s


def calc_common_words_intersatction():
    with open(settings.word_cloud_billboard_list_json) as file:
        billboard = json.load(file)
        billboard_set = set(billboard)
    with open("chars songs worldcloud.json") as file:
        chars = json.load(file)
        chars_set = set(chars)
    with open("ngram songs worldcloud.json") as file:
        ngram = json.load(file)
        ngram_set = set(ngram)

    chars_res = set.intersection(billboard_set, chars_set)
    ngrams_res = set.intersection(billboard_set, ngram_set)
    # chars_res = billboard_set.difference(chars_set)
    # ngrams_res = billboard_set.difference(ngram_set)

    return (ngrams_res ,chars_res)


def create_words_per_songs_graph_database():
    x = list(range(0, 901))
    songs = [0] * 901
    songs_2 = [0] * 901
    songs_3 = [0] * 901

    df = pd.read_csv(settings.ngram_model_input_experiment_database, encoding="utf-8-sig")
    df2 = pd.read_csv(settings.chars_model_input_experiment_database, encoding="utf-8-sig")
    df3 = pd.read_csv(settings.csv_file_name, encoding="utf-8-sig")
    for i, row in df.iterrows():
        words = len(row['lyrics'].split())
        songs[words] += 1

    for i, row in df2.iterrows():
        words = len(row['lyrics'].split())
        songs_2[words] += 1
    max=0
    for i, row in df3.iterrows():
        words = len(row['lyrics'].split())
        if words <=900:
            songs_3[words] += 1

    data = {'words': x,
            'ngram songs': songs,
            'char songs' : songs_2,
            'billboard songs' : songs_3
            }

    df4 = pd.DataFrame(data, columns=['words', 'ngram songs','char songs','billboard songs'])
    df4.to_csv('words per songs graph.csv', index=False, encoding='utf-8-sig')



