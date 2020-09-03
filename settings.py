import os

# csv_file_name = 'database_with_lyrics.csv'
csv_file_name = 'database_with_lyrics.csv'

statistics_dir = os.getcwd()+'\statistics'
statistics_json = statistics_dir+'\\billboard songs structure statistics.json'

word_cloud_dir = os.getcwd()+'\word cloud images'
word_cloud_billboard_image = word_cloud_dir+"\\billboard songs worldcloud"+".png"
word_cloud_billboard_list_json = word_cloud_dir+"\\billboard songs worldcloud list.json"
word_cloud_ngram_image = word_cloud_dir+"\\ngram model songs worldcloud"+".png"
word_cloud_ngram_list_json = word_cloud_dir+"\\ngram model songs worldcloud list.json"
word_cloud_char_image = word_cloud_dir+"\\char model songs worldcloud"+".png"
word_cloud_char_list_json = word_cloud_dir+"\\char model songs worldcloud list.json"
word_cloud_pattern = '\\billboard'

sentiment_dir = os.getcwd()+'\sentiment analysis'
sentiment_csv = sentiment_dir+'\sentiment_analysis_stat.csv'
sentiment_decade_image = sentiment_dir+'\sentiment decade songs.png'
sentiment_billboard_image = sentiment_dir+'\\sentiment billboard songs.png'
sentiment_song_image = sentiment_dir+'\generated song statistics.png'

ngram_dir = os.getcwd()+'\\ngram model'
ngram_model = ngram_dir+'\\trigram model database.json'
ngram_model_input_experiment_database = ngram_dir +'\\ngram model experiment database.csv'
ngram_model_output_experiment_statistics = statistics_dir +'\\ngram model experiment statistics.json'

chars_dir = os.getcwd()+'\\chars model'
chars_model = chars_dir+'\\chars model database.json'
chars_model_input_experiment_database = chars_dir +'\\chars model experiment database.csv'
chars_model_output_experiment_statistics = statistics_dir +'\\chars model experiment statistics.json'

