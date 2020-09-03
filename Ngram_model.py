import json
import os
from nltk import trigrams
from collections import defaultdict
import random
import settings
import pandas as pd

def create_trigram_model():
    path = settings.ngram_dir
    if not os.path.isdir(path):
        os.mkdir(path)
    if os.path.exists(settings.ngram_model):
        return

    print('----- Analyzing Trigram Model ------')
    songs_list_as_tuples = []
    df = pd.read_csv(settings.csv_file_name, encoding="utf-8-sig")
    df = df[df['lyrics'].notna()]
    # df = df[(df['year'] >= 80) & (df['year'] <= 80)]

    # Convert lyrics to a list of words, while '\n' is a word too
    for index, row in df.iterrows():
        song_lines_list = row['lyrics'].split('\n')
        for i, line in enumerate(song_lines_list):
            song_lines_list[i] = line + ' \n'
        song_lines_list = ' '.join(song_lines_list)
        song_lines_list = song_lines_list.split(' ')
        song_as_words = list(filter(''.__ne__, song_lines_list))
        song_as_words = (song_as_words,row['weeks'])
        songs_list_as_tuples.append(song_as_words)

    # Create a placeholder for model
    model = defaultdict(lambda: defaultdict(lambda: 0))

    # Count frequency of co-occurance
    for song in songs_list_as_tuples:
        for w1, w2, w3 in trigrams(['~~~','~~~']+song[0]+['^^^','^^^']):
            model[w1+'@'+w2][w3] += song[1]

    # Let's transform the counts to probabilities
    for key in model:
        total_count = float(sum(model[key].values()))
        for w3 in model[key]:
            model[key][w3] /= total_count

    print('-----  Storing Data ------')

    with open(settings.ngram_model, 'w') as json_file:
        json.dump(model, json_file, indent=4)
        json_file.seek(0)

    print('-----  DONE ------')



def generate_song(model):

    text_temp = ['~~~','~~~']
    text = ['~~~','~~~']


    sentence_finished = False
    num_of_words = 700

    while not sentence_finished:
        # select a random probability threshold
        if len(text_temp) > num_of_words:
            break

        r = random.random()
        accumulator = .0

        for word in model['@'.join(text_temp[-2:])].keys():
            accumulator += model['@'.join(text_temp[-2:])][word]
            # select words that are above the probability threshold
            if accumulator >= r:
                counter = word.count('%')
                if counter > 0:
                    pres = '%'*counter
                    start = int('1'+('0'*(counter-1)))
                    end = int('9'+('0'*(counter-1)))
                    new_word = word.replace(pres, str(random.randint(start, end)))
                    text.append(new_word)
                    text_temp.append(word)
                else:
                    text.append(word)
                    text_temp.append(word)
                break

        if text_temp[-2:] == ['^^^', '^^^']:
            sentence_finished = True

    # Generate a song as list of words & handle '/n'
    song_as_words = [t for t in text if t]
    for i in range (0, len(song_as_words)-1):
        if song_as_words[i]=='\n':
            song_as_words[i+1]='\n'+song_as_words[i+1]
    song_as_words = list(filter('\n'.__ne__, song_as_words))
    for i in range(0, len(song_as_words) - 1):
        if song_as_words[i] == '\n\n':
            song_as_words[i + 1] = '\n\n' + song_as_words[i + 1]
    song_as_words = list(filter('\n\n'.__ne__, song_as_words))
    song = ' '.join(song_as_words)
    song = song[8:-8]
    return song


    # Generate song with fix statistics

    # # Calculate Statistics
    # with open(settings.statistics_json, 'r') as json_file:
    #     statistics = json.load(json_file)
    #     json_file.seek(0)
    #
    # words_per_line = statistics['average_words_per_line']
    # lines_per_stanza = statistics['average_lines_per_stanza']
    #
    # # split lines every 'words_per_line' number
    # song = song.split()
    # song = '\n'.join([' '.join(song[i:i + words_per_line]) for i in range(0, len(song), words_per_line)])
    # # split lines to stanzas
    # song = song.split('\n')
    # song = '\n\n'.join(['\n'.join(song[i:i + lines_per_stanza]) for i in range(0, len(song), lines_per_stanza)])
    # # return song
    # return song
