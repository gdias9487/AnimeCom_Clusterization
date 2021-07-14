import os

os.system('python -m pip install scikit-learn==0.22.2.post1')
os.system('python.exe -m pip install --upgrade pip')
os.system('python -m pip install mysql-connector-python')
os.system('python -m pip install flask-ngrok')
os.system('python -m pip install num2words')
os.system('python -m pip install unidecode')
os.system('python -m pip install nltk')
os.system('python -m pip install sklearn')
os.system('python -m pip install pandas')

from flask_ngrok import run_with_ngrok
from flask import Flask, request
from unidecode import unidecode
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from decimal import DecimalException
from nltk.stem import SnowballStemmer, WordNetLemmatizer
from sklearn.feature_extraction.text import TfidfVectorizer
import joblib

import pandas as pd
import json, re, nltk, string, num2words
import mysql.connector

nltk.download('stopwords')

Flask.name= "AnimeCom"
app = Flask(__name__)
run_with_ngrok(app)   #starts ngrok when the app is run

@app.route("/")
def inicio(): 
    return 'AnimeCom - IAAD'

@app.route("/read")
def read(): 
    my_json = json.loads(request.args.get('params'))
    conn = mysql.connector.connect(host="localhost", user="animecom", passwd="12345678", db="animecom")
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM {my_json['table']} WHERE {my_json['condition']}")
    result = cursor.fetchall()
    conn.close()
    return json.dumps({'result': result})

@app.route("/readAll")
def readAll():
    my_json = json.loads(request.args.get('params'))
    conn = mysql.connector.connect(host="localhost", user="animecom", passwd="12345678", db="animecom")
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM {my_json['table']} as A INNER JOIN Evaluation as E ON A.uid = E.anime_uid WHERE {my_json['condition']} AND A.genre NOT LIKE '%Hentai%'AND A.genre NOT LIKE '%Yaoi%'AND A.genre NOT LIKE '%Yuri%' ORDER BY RAND() LIMIT 15")
    result = cursor.fetchall()
    conn.close()
    return json.dumps({'result': result})

@app.route("/readCluster")
def readCluster():
    my_json = json.loads(request.args.get('params'))
    conn = mysql.connector.connect(host="localhost", user="animecom", passwd="12345678", db="animecom")
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM {my_json['table']} as A INNER JOIN Evaluation as E ON A.uid = E.anime_uid WHERE {my_json['condition']} AND A.genre NOT LIKE '%Hentai%'AND A.genre NOT LIKE '%Yaoi%'AND A.genre NOT LIKE '%Yuri%' ORDER BY RAND() LIMIT 15")
    result = cursor.fetchall()
    conn.close()
    return json.dumps({'result': result})

@app.route("/insert")
def insert(): 
    my_json = json.loads(request.args.get('params'))
    conn = mysql.connector.connect(host="localhost", user="animecom", passwd="12345678", db="animecom")
    cursor = conn.cursor()
    cursor.execute(f"INSERT INTO {my_json['table']} ({my_json['fields']}) VALUES ({my_json['values']});")
    conn.commit()
    conn.close()
    return json.dumps({'result': True})

@app.route("/update")
def update(): 
    my_json = json.loads(request.args.get('params'))
    
    conn = mysql.connector.connect(host="localhost", user="animecom", passwd="12345678", db="animecom")
    cursor = conn.cursor()
    cursor.execute(f"UPDATE {my_json['table']} SET {my_json['values']} WHERE {my_json['condition']};")
    conn.commit()
    conn.close()
    return json.dumps({'result': True})

@app.route("/delete")
def delete(): 
    my_json = json.loads(request.args.get('params'))
    conn = mysql.connector.connect(host="localhost", user="animecom", passwd="12345678", db="animecom")
    cursor = conn.cursor()
    cursor.execute(f"DELETE FROM {my_json['table']} WHERE {my_json['condition']};")
    conn.commit()
    conn.close()
    return json.dumps({'result': True})

def processamento(text, n=30):
  #processamento básico
  text = text.lower()
  text = unidecode(text)
  text = re.sub(',|\.|/|$|\(|\)|-|\+|:|•', '', text)

  #Remove espaços
  text = re.sub('\s+', ' ', text)

  #Remove stopword
  stop_words = stopwords.words('english') 
  text = ' '.join([word for word in word_tokenize(text) if word not in stop_words])

  #remove remanescentes
  text = ' '.join([word for word in word_tokenize(text) if not ( len(word)<2 and not word.isdigit() or "'" in word and len(word)<4)])

  #remove simbolos
  symbols = string.punctuation
  for s in symbols:
    text = text.replace(s,'')

  #substituindo números por dígitos
  text_temp = word_tokenize(text)
  for index, word in enumerate(text_temp):
    try:
      if word.isnumeric():
        text_temp[index] = num2words.num2words(word)
    except (ValueError, DecimalException):
      text_temp[index] = ''
      continue
  text = ' '.join(text_temp)

  #Aplicando o lemmatizer
  lemmatizer = WordNetLemmatizer()
  text = ' '.join([lemmatizer.lemmatize(word) for word in word_tokenize(text)])

  #Aplicando o Stemmer
  stemmer = SnowballStemmer('english')
  text = ' '.join([stemmer.stem(word) for word in word_tokenize(text)])
  
  return text
  
def TFIDF(text_reviews, n=30):
  #Aplicando o TFI-DF
  tfIdfVectorizer=TfidfVectorizer(use_idf=True)
  tfIdf = tfIdfVectorizer.fit_transform([text_reviews])

  df = pd.DataFrame(tfIdf[0].T.todense(), index=tfIdfVectorizer.get_feature_names(), columns=["TF-IDF"])
  df = df.sort_values('TF-IDF', ascending=False)
  df = df.head(n)
  return ' '.join(df.index)

@app.route("/clusterization")
def clusterization():
    # Recupera o texto do usuário
    my_json = json.loads(request.args.get('params'))
    text_user = my_json['text']

    # processamento
    text_user = processamento(text_user)
    text_user = TFIDF(text_user)

    # vetoriza
    bag_of_words_model_loaded = joblib.load(r'banco\bag_of_words.pkl')
    bag_of_words = bag_of_words_model_loaded.transform([text_user] * 3)

    # redimensiona
    pca_loaded = joblib.load(r'banco\pca.pkl')
    text_user = pca_loaded.transform(bag_of_words.toarray())

    # Carrega o clusterizador treinado
    model_loaded = joblib.load(r'banco\kmeans.pkl')

    # Clusteriza o texto do usuário
    rotulo_user = model_loaded.predict(text_user)

    # recupera os rotulos de treinamento e os uid dos animes em que a review usada para treino se refere
    rotulos_loaded = open(r'banco\rotulos.txt')
    animes_loaded = open(r'banco\animes_uid.txt')

    animes = []  # Uid dos animes que com base na review pertecem ao mesmo grupo que o texto do usuário
    animes_uid = eval(animes_loaded.readline())
    for i, rotulo in enumerate(eval(rotulos_loaded.readline())):
        if rotulo in rotulo_user:
            animes.append(animes_uid[i])

    return json.dumps({'animes_uid': tuple(animes)})

app.run()
