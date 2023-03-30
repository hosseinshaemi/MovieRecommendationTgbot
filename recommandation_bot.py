import telebot
import numpy as np
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer

BOT_TOKEN = 'YOUR BOT TOKEN'

def multiple_features(row):
  try:
    return f"{row['keywords']} {row['cast']} {row['genres']} {row['director']}"
  except:
    print(row)

def extract_movie_names(recomm_array: list) -> str:
  names = []
  for item in recomm_array[0:11]:
    names.append(' by '.join(df.iloc[[item[0]]][['title', 'director']].values[0]))
  return '\n'.join(names)

def create_recommandations(movname: str) -> str:
  movinx = df.index[df['title'] == movname].tolist()[0]
  sort_recommandations = sorted(list(enumerate(cosine_similarity[movinx])) , key=lambda x : x[1], reverse=True)
  result = extract_movie_names(sort_recommandations)
  return result

df = pd.read_csv('dataset.csv').set_index('index')

for ftr in ['keywords', 'cast', 'genres', 'director']: df[ftr] = df[ftr].fillna('')
df['multiple_features'] = df.apply(multiple_features, axis=1)
cv = CountVectorizer(lowercase=True)
count_matrix = cv.fit_transform(df['multiple_features'])
cosine_similarity = cosine_similarity(count_matrix)
bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=['start'])
def welcome_handler(message):
  bot.reply_to(message, "Welcome to movie recommander bot :)\nSend a movie name!")
  return

@bot.message_handler(func=lambda msg: True, content_types=['text', 'audio', 'document', 'photo', 'sticker', 'video', 'video_note', 'voice', 'location', 'contact'])
def movie_handler(message):
  if (message.content_type != 'text'):
    bot.reply_to(message, 'Oops!!!, Please send me a movie name.')
    return
  if (not (message.text in df['title'].unique())):
    bot.reply_to(message, 'Oops!!!, This movie is not in my dataset!')
    return
  result = create_recommandations(message.text)
  bot.reply_to(message, result)

if __name__ == '__main__':
  bot.infinity_polling()