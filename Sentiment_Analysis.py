import os
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import settings
from datetime import date

def calc_sentiment_analysis_statistics(input_file_csv_database):
    path = settings.sentiment_dir
    if not os.path.isdir(path):
        os.mkdir(path)
    df = pd.read_csv(input_file_csv_database, encoding="utf-8-sig")
    sid = SentimentIntensityAnalyzer()

    print('----- Sentiment Analysis To Songs ------')
    num_positive = 0
    num_negative = 0
    num_neutral = 0

    songs_num = len(df.index)
    for index, row in df.iterrows():
        comp = sid.polarity_scores(row['lyrics'])
        if comp['compound'] >= 0.5:
            num_positive += 1
        elif -0.5 < comp['compound'] < 0.5:
            num_neutral += 1
        else:
            num_negative += 1

    today = date.today()
    today = today.strftime("%B %d, %Y")
    sid = SentimentIntensityAnalyzer()

    # Data to plot
    labels = 'Negative', 'Neutral', 'Positive'
    sizes = [num_negative, num_neutral, num_positive]
    colors = ['yellowgreen', 'lightcoral', 'lightskyblue']
    explode = (0, 0.1, 0)  # explode 1st slice

    # Plot
    plt.pie(sizes, explode=explode, labels=labels, colors=colors,
            autopct='%1.1f%%', shadow=True, startangle=140)
    plt.axis('equal')

    plt.title('1970-2018 Billboard Songs Distribution By Number ', fontweight='bold')
    plt.xticks([0], [today], fontweight='bold')

    # plt.savefig('say waht', bbox_inches='tight')
    # SHOULD PUT IN COMMENT
    # plt.show()
    print('------------ DONE ---------------')
    return "Number of Positive songs:"+ str(num_positive)+'\n'+ \
           "Number of Negative songs:" + str(num_negative) +'\n'+ \
           "Number of Neutral songs:" + str(num_neutral)

def calc_generated_song_sentiment_analysis_statistics(song):
    today = date.today()
    today = today.strftime("%B %d, %Y")
    sid = SentimentIntensityAnalyzer()
    comp = sid.polarity_scores(song)

    if comp['compound'] >= 0.5:
        return 'Generated Song is POSITIVE'
    elif -0.5 < comp['compound'] < 0.5:
        return 'Generated Song is NEUTRAL'
    else:
        return 'Generated Song is NEGATIVE'



