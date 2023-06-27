


#Train NER from a blank spacy model
import spacy
from spacy.training import Example
import pandas as pd
from pymorphy2 import MorphAnalyzer
morph = MorphAnalyzer()
import razdel
from spacy.scorer import Scorer




def preprocess_text(text):
    words = list(razdel.tokenize(text.lower()))  # токенизация и приведение к нижнему регистру
    return words

def lemmatize_words(words):
    lemmatized_words = [ morph.parse(word.text)[0].normal_form for word in words]
    return lemmatized_words

def find_keywords(text, keyword_dict):
    positions = {}
    positions["text"]=text
    words = preprocess_text(text)
    lemmatized_words = lemmatize_words(words)
    start_idx = 0
    for i, word in enumerate(lemmatized_words):
        word_length = len(words[i].text)
        end_idx = start_idx + word_length - 1
        for keyword, category in keyword_dict.items():
            if word in keyword:
                if category in positions:
                    positions[category].append((start_idx, end_idx))
                else:
                    positions[category] = [(start_idx, end_idx)]
                break
        start_idx += word_length + 1
    return positions


nlp=spacy.blank("ru")
nlp.add_pipe('ner')
nlp.begin_training()
ner=nlp.get_pipe('ner')
ruler = nlp.add_pipe("entity_ruler")


patterns = [{"label": "МОЖНО", "pattern": "прием"}, {"label": "МОЖНО", "pattern": "знание"},{"label": "МОЖНО", "pattern": "оформление"},
    {"label": "МОЖНО", "pattern": "печать"},{"label": "МОЖНО", "pattern": "предоставлять"},{"label": "МОЖНО", "pattern": "информация"},{"label": "МОЖНО", "pattern": "осуществление"},
    {"label": "МОЖНО", "pattern": "сверка"},{"label": "МОЖНО", "pattern": "формирование"},{"label": "МОЖНО", "pattern": "производство"},{"label": "МОЖНО", "pattern": "подготовка"},
    {"label": "МОЖНО", "pattern": "распределение"}, {"label": "МОЖНО", "pattern": "регистрация"},{"label": "МОЖНО", "pattern": "отчетность"}, {"label": "МОЖНО", "pattern": "учет"},{"label": "МОЖНО", "pattern": "управление"},
    {"label": "МОЖНО", "pattern": "закупка"},{"label": "МОЖНО", "pattern": "сверка"},
    {"label": "МОЖНО", "pattern": "списание"},{"label": "МОЖНО", "pattern": "анализировать"},{"label": "МОЖНО", "pattern": "анализ"},{"label": "МОЖНО", "pattern": "проверка"},
    {"label": "МОЖНО", "pattern": "подписание"},{"label": "МОЖНО", "pattern": "выражать"}, {"label": "МОЖНО", "pattern": "преобразовывать"},{"label": "МОЖНО", "pattern": "моделировать"},
    {"label": "МОЖНО", "pattern": "заполнение"},{"label": "МОЖНО", "pattern": "подготовка"},{"label": "МОЖНО", "pattern": "оптимизировать"},{"label": "МОЖНО", "pattern": "вычислять"},
    {"label": "МОЖНО", "pattern": "рассчитывать"},{"label": "МОЖНО", "pattern": "считать"}, {"label": "МОЖНО", "pattern": "контроль"}, {"label": "МОЖНО", "pattern": "определять"},{"label": "МОЖНО", "pattern": "измерять"},
    {"label": "МОЖНО", "pattern": "пересчитывать"},{"label": "МОЖНО", "pattern": "суммировать"}, {"label": "МОЖНО", "pattern": "оптимизировать"},{"label": "МОЖНО", "pattern": "моделировать"},
    {"label": "МОЖНО", "pattern": "сравнивать"},{"label": "МОЖНО", "pattern": "уточнять"}, {"label": "МОЖНО", "pattern": "проверять"},{"label": "МОЖНО", "pattern": "редактировать"},
    {"label": "МОЖНО", "pattern": "распознавать"},{"label": "МОЖНО", "pattern": "аннотировать"}, {"label": "МОЖНО", "pattern": "классифицировать"},{"label": "МОЖНО", "pattern": "улучшать"},
    {"label": "МОЖНО", "pattern": "оформлять"},{"label": "МОЖНО", "pattern": "оформление"}, {"label": "МОЖНО", "pattern": "продажа"},{"label": "МОЖНО", "pattern": "отчетность"},  {"label": "МОЖНО", "pattern": "ответы"},
    {"label": "МОЖНО", "pattern": "отвечать"},{"label": "НЕЛЬЗЯ", "pattern": "написание"}, {"label": "НЕЛЬЗЯ", "pattern": "консультирование"},{"label": "НЕЛЬЗЯ", "pattern": "формулирование"},{"label": "НЕЛЬЗЯ", "pattern": "сочинение"},
    {"label": "НЕЛЬЗЯ", "pattern": "корректировка"},{"label": "НЕЛЬЗЯ", "pattern": "отвечать"},{"label": "НЕЛЬЗЯ", "pattern": "преобразование"},{"label": "НЕЛЬЗЯ", "pattern": "сверка"},
    {"label": "НЕЛЬЗЯ", "pattern": "вставка"},{"label": "НЕЛЬЗЯ", "pattern": "замена"},{"label": "НЕЛЬЗЯ", "pattern": "компоновать"},{"label": "НЕЛЬЗЯ", "pattern": "компоновка"},
    {"label": "НЕЛЬЗЯ", "pattern": "сборка"},{"label": "НЕЛЬЗЯ", "pattern": "публиковать"},{"label": "НЕЛЬЗЯ", "pattern": "индексация"},{"label": "НЕЛЬЗЯ", "pattern": "группировка"},
    {"label": "НЕЛЬЗЯ", "pattern": "экспорт"}, {"label": "НЕЛЬЗЯ", "pattern": "встреча"}, {"label": "НЕЛЬЗЯ", "pattern": "распаковывать"}, {"label": "НЕЛЬЗЯ", "pattern": "подписание"},
    {"label": "НЕЛЬЗЯ", "pattern": "подписывать"}, {"label": "НЕЛЬЗЯ", "pattern": "лечить"},{"label": "НЕЛЬЗЯ", "pattern": "знать"}, {"label": "НЕЛЬЗЯ", "pattern": "изображать"},{"label": "НЕЛЬЗЯ", "pattern": "создавать"}, {"label": "НЕЛЬЗЯ", "pattern": "формирование"},{"label": "НЕЛЬЗЯ", "pattern": "участие"}, {"label": "НЕЛЬЗЯ", "pattern": "выделение"},
    {"label": "НЕЛЬЗЯ", "pattern": "прием"}, {"label": "НЕЛЬЗЯ", "pattern": "отправка"},{"label": "НЕЛЬЗЯ", "pattern": "контроль"}, {"label": "НЕЛЬЗЯ", "pattern": "разгрузка"},{"label": "НЕЛЬЗЯ", "pattern": "раскредитование"}, {"label": "НЕЛЬЗЯ", "pattern": "осуществлять"},
    {"label": "НЕЛЬЗЯ", "pattern": "перевозка"}, {"label": "НЕЛЬЗЯ", "pattern": "выполнение"},{"label": "НЕЛЬЗЯ", "pattern": "обеспечение"}, {"label": "НЕЛЬЗЯ", "pattern": "пермещение"},{"label": "НЕЛЬЗЯ", "pattern": "досавка"}, {"label": "НЕЛЬЗЯ", "pattern": "встреча"},
    {"label": "НЕЛЬЗЯ", "pattern": "помощь"}, {"label": "НЕЛЬЗЯ", "pattern": "поддержание"},{"label": "НЕЛЬЗЯ", "pattern": "соблюдение"}, {"label": "НЕЛЬЗЯ", "pattern": "организация"},{"label": "НЕЛЬЗЯ", "pattern": "выполнение"}, {"label": "НЕЛЬЗЯ", "pattern": "выдавать"},
    {"label": "НЕЛЬЗЯ", "pattern": "работать"}, {"label": "НЕЛЬЗЯ", "pattern": "разработка"},{"label": "НЕЛЬЗЯ", "pattern": "протоколирование"}, {"label": "НЕЛЬЗЯ", "pattern": "сверка"},{"label": "НЕЛЬЗЯ", "pattern": "разрабатывать"}, {"label": "НЕЛЬЗЯ", "pattern": "проведение"},
    {"label": "НЕЛЬЗЯ", "pattern": "оформление"}, {"label": "НЕЛЬЗЯ", "pattern": "настройка"},{"label": "НЕЛЬЗЯ", "pattern": "уборка"}, {"label": "НЕЛЬЗЯ", "pattern": "общаться"},{"label": "НЕЛЬЗЯ", "pattern": "общение"}, {"label": "НЕЛЬЗЯ", "pattern": "записывание"},
    {"label": "НЕЛЬЗЯ", "pattern": "обслуживание"}, {"label": "НЕЛЬЗЯ", "pattern": "обслуживать"},{"label": "НЕЛЬЗЯ", "pattern": "инвентаризация"}, {"label": "НЕЛЬЗЯ", "pattern": "управление"},
    {"label": "НЕЛЬЗЯ", "pattern": "доставка"}, {"label": "НЕЛЬЗЯ", "pattern": "встреча"},{"label": "НЕЛЬЗЯ", "pattern": "встречать"}, {"label": "НЕЛЬЗЯ", "pattern": "планирование"},{"label": "НЕЛЬЗЯ", "pattern": "планировать"}, {"label": "НЕЛЬЗЯ", "pattern": "установка"},{"label": "НЕЛЬЗЯ", "pattern": "приготовление"}, {"label": "НЕЛЬЗЯ", "pattern": "прогулка"},{"label": "НЕЛЬЗЯ", "pattern": "сидеть"}, {"label": "НЕЛЬЗЯ", "pattern": "выполнение"},
    {"label": "НЕЛЬЗЯ", "pattern": "замена"}, {"label": "НЕЛЬЗЯ", "pattern": "ремонт"}, {"label": "НЕЛЬЗЯ", "pattern": "обкатка"}, {"label": "НЕЛЬЗЯ", "pattern": "разборка"},
    {"label": "НЕЛЬЗЯ", "pattern": "запуск"}, {"label": "НЕЛЬЗЯ", "pattern": "улучшение"},{"label": "НЕЛЬЗЯ", "pattern": "замена"}, {"label": "НЕЛЬЗЯ", "pattern": "управление"},
            {"label": "НЕЛЬЗЯ", "pattern": "работа"}, {"label": "НЕЛЬЗЯ", "pattern": "разработка"},  {"label": "НЕЛЬЗЯ", "pattern": "интеграция"},  {"label": "НЕЛЬЗЯ", "pattern": "поддержка"},

            ]



ruler.add_patterns(patterns)



#New label to add
LABEL = "МОЖНО"
LABEL2 = "НЕЛЬЗЯ"



#Training examples in the required format
def preprocess_text(text):
    tokens = list(razdel.tokenize(text.lower()))  # токенизация и приведение к нижнему регистру
    tokens = [token.text for token in tokens]  # удаление стоп-слов и символов
    tokens = [morph.normal_forms(token)[0] for token in tokens] #приведение к нормальной форме слова
    return ' '.join(tokens)



data = pd.read_csv(r'data.csv', header=0, encoding='cp1251', sep=';', on_bad_lines='skip')
data = list(data["text"][:400])
TRAIN_DATA = []
for sentence in data:
    prep_t = preprocess_text(sentence)
    doc = nlp(prep_t)
    entities = []
    for ent in doc.ents:
        entities.append([ent.start_char, ent.end_char, ent.label_])
    TRAIN_DATA.append([prep_t, {"entities": entities}])


#Add the new label to ner
ner.add_label(LABEL)
ner.add_label(LABEL2)


#Resume training
optimizer = nlp.resume_training()
move_names = list(ner.move_names)


#List of pipes you want to train
pipe_exceptions = ["ner", "trf_wordpiecer", "trf_tok2vec"]


#List of pipes which should remain unaffected in training
other_pipes = [pipe for pipe in nlp.pipe_names if pipe not in pipe_exceptions]


#Importing requirements
from spacy.util import minibatch, compounding
import random


#Begin training by disabling other pipeline components
with nlp.disable_pipes(*other_pipes):
    sizes = compounding(1.0, 4.0, 1.001)
    #Training for 30 iterations
    for itn in range(20):
        #shuffle examples before training
        random.shuffle(TRAIN_DATA)
        #batch up the examples using spaCy's minibatch
        batches = minibatch(TRAIN_DATA, size=sizes)
        #ictionary to store losses
        losses = {}
        for batch in batches:
            for text, annotations in batch:
                doc = nlp.make_doc(text)
                example = Example.from_dict(doc, annotations)
                nlp.update([example], drop=0.35, sgd=optimizer, losses=losses)

        print("Losses", losses)


#Output directory
from pathlib import Path
output_dir=Path('C://Users/ddqqp/IdeaProjects/AIHH/')


#Saving the model to the output directory

if not output_dir.exists():
    output_dir.mkdir()
nlp.meta['name'] = 'my_ner'  #rename model
nlp.to_disk(output_dir)
print("Saved model to", output_dir)



#Testing the NER
test_texts = ["осуществление переноса денежных средств","осуществлять расчет персонала и гостей",
              "умение работать в режиме многозадачности", "доставка сотрудников, оборудования фирмы по производственным объектам"]


for i in range(len(test_texts)):
    doc = nlp(test_texts[i])
    print("Entities in '%s'" % test_texts[i])
    for ent in doc.ents:
        print(ent, ent.label_)

#Метрика acc, recall, precision, fscore
data = pd.read_csv(r'data.csv', header=0, encoding='cp1251', sep=';')
data = list(data["text"][500:750])
TEST_DATA = []
for sentence in data:
    prep_t = preprocess_text(sentence)
    doc = nlp(prep_t)
    entities = []
    for ent in doc.ents:
        entities.append([ent.start_char, ent.end_char, ent.label_])
    TEST_DATA.append([prep_t, {"entities": entities}])

def evaluate(ner_model, examples):
    scorer = Scorer()
    example = []
    for input_, annot in examples:
        pred = ner_model(input_)
        #print(pred,annot)
        temp = Example.from_dict(pred, dict.fromkeys(annot))
        example.append(temp)
    scores = scorer.score_tokenization(example)
    #scores = scorer.score(example)
    return scores

results = evaluate(nlp, TEST_DATA)
print(results)