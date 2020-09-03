import Ngram_model
import Chars_model
from CSV_Builder import *
from Statistics import *
from Word_Cloud import *
from Sentiment_Analysis import *

def pre_process_data():
    # create_csv_with_lyrics_database()
    print('----- Billboard ------')
    create_average_statistics_database(settings.csv_file_name,settings.statistics_json)
    print(calc_sentiment_analysis_statistics(settings.csv_file_name))
    create_wordcloud_database(settings.csv_file_name, settings.word_cloud_billboard_image, settings.word_cloud_billboard_list_json)

def run_experiment():
    ngram_songs = []
    chars_songs = []
    neural_model = Chars_model.char_lm(11)
    Ngram_model.create_trigram_model()
    with open(settings.ngram_model, 'r') as json_file:
        print('----- Reading Trigram Model Database ------')
        model = json.load(json_file)
        print('----- DONE ------')
    for i in range(20000):
        ngram_songs.append(Ngram_model.generate_song(model))
        chars_songs.append(neural_model.generate_song(2000))
        if (i!=0) and (i%1000==0):
            print('Generated '+str(i)+'Songs')
    data1 = {'lyrics': ngram_songs}
    data2 = {'lyrics': chars_songs}
    df1 = pd.DataFrame(data1, columns=['lyrics'])
    df2 = pd.DataFrame(data2, columns=['lyrics'])
    df1 = df1[df1['lyrics'].map(lambda song: isinstance(song, str) and len(song) > 30)]
    df2 = df2[df2['lyrics'].map(lambda song: isinstance(song, str) and len(song) > 30)]
    df1.to_csv(settings.ngram_model_input_experiment_database, index=False, encoding='utf-8-sig')
    df2.to_csv(settings.chars_model_input_experiment_database, index=False, encoding='utf-8-sig')
    print('----- Experiment Done -----')

if __name__ == "__main__":
    # pre_process_data()
    run_experiment()
    print('----- Ngram Model ------')
    create_average_statistics_database(settings.ngram_model_input_experiment_database, settings.ngram_model_output_experiment_statistics)
    print(calc_sentiment_analysis_statistics(settings.ngram_model_input_experiment_database))
    create_wordcloud_database(settings.ngram_model_input_experiment_database, settings.word_cloud_ngram_image, settings.word_cloud_ngram_list_json)
    print('----- Chars Model ------')
    create_average_statistics_database(settings.chars_model_input_experiment_database, settings.chars_model_output_experiment_statistics)
    print(calc_sentiment_analysis_statistics(settings.chars_model_input_experiment_database))
    create_wordcloud_database(settings.chars_model_input_experiment_database, settings.word_cloud_char_image, settings.word_cloud_char_list_json)
    print('----- Creates Graphs Database ------')
    create_words_per_songs_graph_database()
    print("--------------------------------------------------------------")
    print('Ngram best song statistics')
    print("--------------------------------------------------------------")
    best_ngram_model_song = find_best_song(settings.ngram_model_input_experiment_database)
    print(statistics_per_song(best_ngram_model_song))
    print('Number of common words is: '+ str(calc_common_words_number_for_generated_song(best_ngram_model_song)))
    print(calc_generated_song_sentiment_analysis_statistics(best_ngram_model_song))
    print("---------------------LYRICS-----------------------------")
    print(best_ngram_model_song)
    print("**************************************************************")
    print("**************************************************************")
    print("**************************************************************")
    print("--------------------------------------------------------------")
    print('Chars best song statistics')
    print("--------------------------------------------------------------")
    best_chars_model_song = find_best_song(settings.chars_model_input_experiment_database)
    print(statistics_per_song(best_chars_model_song))
    print('Number of common words is: '+ str(calc_common_words_number_for_generated_song(best_chars_model_song)))
    print(calc_generated_song_sentiment_analysis_statistics(best_chars_model_song))
    print("---------------------LYRICS-----------------------------")
    print(best_chars_model_song)
    print("**************************************************************")
    print("**************************************************************")
    print("**************************************************************")
    print('Billboard statistics')
    with open(settings.statistics_json, 'r') as json_file:
        statistics = json.load(json_file)
        json_file.seek(0)
    print(statistics)
    print("--------------------------------------------------------------")
    print('Ngram statistics')
    with open(settings.ngram_model_output_experiment_statistics, 'r') as json_file:
        statistics = json.load(json_file)
        json_file.seek(0)
    print(statistics)
    print("--------------------------------------------------------------")
    print('Chars statistics')
    with open(settings.chars_model_output_experiment_statistics, 'r') as json_file:
        statistics = json.load(json_file)
        json_file.seek(0)
    print(statistics)



















# def little_exp():
#
#     for i in range (2,30):
#         chars_songs = []
#         neural_model = Chars_model2.char_lm(11, i)
#         for j in range(5000):
#             chars_songs.append(neural_model.generate_song(2000))
#             if (j != 0) and (j % 100 == 0):
#                 print('Generated ' + str(j) + 'Songs')
#         data2 = {'lyrics': chars_songs}
#         df2 = pd.DataFrame(data2, columns=['lyrics'])
#         df2 = df2[df2['lyrics'].map(lambda song: isinstance(song, str) and len(song) > 30)]
#         df2.to_csv(settings.chars_dir+"\\char_model_generated_"+str(i)+".csv", index=False, encoding='utf-8-sig')
#         create_average_statistics_database(settings.chars_dir+"\\char_model_generated_"+str(i)+".csv",settings.chars_dir+"\\output_statistics"+str(i)+".json")
#         print('----- Experiment Done -----')