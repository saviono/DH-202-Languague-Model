import json
import settings
from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import os
from PIL import Image

# plot the WordCloud image
def plot_wordcloud(wordcloud):
    plt.figure(figsize=(8, 8), facecolor=None)
    plt.imshow(wordcloud)
    plt.axis("off")
    plt.tight_layout(pad=0)
    plt.show()

def create_wordcloud_database(input_file_csv_database, output_file_png_image, output_file_json_list):
    path = settings.word_cloud_dir
    if not os.path.isdir(path):
        os.mkdir(path)
    df = pd.read_csv(input_file_csv_database, encoding="UTF-8-sig")
    stopwords = set(STOPWORDS)
    print('------ Generates WordCloud ------')
    text=''
    for index, row in df.iterrows():
        text = text + ' ' + row['lyrics']

    mask = np.array(Image.open('billboard.jpeg'))
    wordcloud = WordCloud(width=3000, height=2000,
                          random_state=1, background_color='white',
                          colormap='rainbow', collocations=False,
                          stopwords=stopwords,max_words=200, mask=mask).generate(text)

    plot_wordcloud(wordcloud)
    # Save wordcloud to dir
    wordcloud.to_file(output_file_png_image)

    with open(output_file_json_list, 'w') as json_file:
        json.dump(wordcloud.words_, json_file, indent=4)
        json_file.seek(0)
    print('------------ DONE ---------------')
