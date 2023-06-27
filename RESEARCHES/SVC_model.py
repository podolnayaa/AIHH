from natasha import (
    Segmenter,
    MorphVocab,
    Doc,
    NewsEmbedding,
    NewsMorphTagger
)
from pymorphy2 import MorphAnalyzer
#для преобразования к нормальной форме слова
morph = MorphAnalyzer()
import razdel
import numpy as np
import pandas as pd
import nltk
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix
from sklearn import svm
import time

nltk.download('stopwords')
stop_words = nltk.corpus.stopwords.words('russian')
segmenter = Segmenter()
morph_vocab = MorphVocab()
emb = NewsEmbedding()
morph_tagger = NewsMorphTagger(emb)
stemmer = nltk.stem.snowball.RussianStemmer(ignore_stopwords=True)


def preprocess_text_lem(text):
    doc = Doc(text)
    doc.segment(segmenter) # токенизация
    doc.tag_morph(morph_tagger) # морфологические метки
    print(doc)
    for token in doc.tokens:
        if token.text not in stop_words and token.text.isalpha():
            token.lemmatize(morph_vocab) # лемматизация
            print(token.lemma)
    return ' '.join([token.lemma for token in doc.tokens if token.lemma is not None])


def preprocess_text(text):
    tokens = list(razdel.tokenize(text.lower()))  # токенизация и приведение к нижнему регистру
    tokens = [token.text for token in tokens]  # удаление стоп-слов и символов
    tokens = [morph.normal_forms(token)[0] for token in tokens] #приведение к нормальной форме слова
    tokens = [stemmer.stem(token) for token in tokens]  # стемминг
    return ' '.join(tokens)


def vectorization(texts, labels):
    result_vectors = []
    for text in texts:
        word_vectors = []
        for word in segmenter.tokenize(text):
            if word.text in emb:
                word_vectors.append(emb[word.text])
        if len(word_vectors) == 0:
            labels = labels.drop(texts[texts == text].index.values[0])
            texts = texts.drop(texts[texts == text].index.values[0])
            continue
        result_vectors.append(np.mean(word_vectors, axis=0))

    return result_vectors, labels


    # считываем csv файл с данными
data = pd.read_csv(r'data.csv', header=0, encoding='cp1251', sep=';')


    # предобработка и удаление дупликатов
#data['text'] = data['text'].apply(preprocess_text_lem) # Лемматизация обязательна для семантической векторизации
data['text'] = data['text'].apply(preprocess_text) # стемминг
data = data.drop_duplicates()

    # векторизация
# семантическая векторизация дала результат 0,76 и заняла 0,080 по времени
#X, y = vectorization(data['text'], data['label'])

#векторизация с помощью tf-idf дала результат 0,86 и заняла 0,063 по времени
vectorizer = TfidfVectorizer() # tf-idf
vectorizer.fit(data['text']) # составление словаря уникальных слов для векторизатора
X, y = vectorizer.transform(data['text']), data['label']

acc = [0]
fit_time = [0]
clfs = [None]
iter = 100
matrix = 0
for i in range(iter):
        # разбиваем на обучающую и контрольную выборки
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

        # объекты модели и их обучение с замерением
    clfs = [svm.SVC(C=3, gamma=0.8)]
    for i in range(len(clfs)):
        start_time = time.time()
        clfs[i].fit(X_train, y_train)
        fit_time[i] += time.time() - start_time
        acc[i] += clfs[i].score(X_test, y_test)
    y_pred = clfs[i].predict(X_test)
    matrix = confusion_matrix(y_test, y_pred)



#Метрика acc, recall, precision, fscore
print("acc= ")

for i in range(len(clfs)):
    print(f"{acc[i] / iter} {fit_time[i] / iter}")

print("matrix= ", matrix)

recall = matrix[0][0]/ (matrix[0][0]+matrix[1][0])
precision = matrix[0][0]/ (matrix[0][0]+matrix[0][1])
f_score = 2 * ((precision * recall) / (precision + recall + 1e-100))
print("recall= ",recall)
print("precision = ", precision)
print("f_score = ", f_score)