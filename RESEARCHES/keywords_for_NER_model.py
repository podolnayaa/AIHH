import pymorphy2
import razdel
import pandas as pd


#НЕ 

# очищение текста обязанностей и втоматическое создание тестовой выборки для NER-модели 
# нужные слова ищутся из списка зарезервированных слов ниже
# итог приводится в нужной форме для дальнейшего обучения spacy NER

def preprocess_text(text):
    words = list(razdel.tokenize(text.lower()))  # токенизация и приведение к нижнему регистру
    return words

def lemmatize_words(words):
    morph = pymorphy2.MorphAnalyzer()
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

text = "Обязанности:  Создание технической документации: Технического задания, Программа и методика испытаний, Протоколы совещаний, Руководства пользователя различного уровня сложности (для пользователя, для администраторов, для разработчиков). Анализ бизнес-процессов предметной области Понимание нотаций IDEF0, BPMN, UML Сбор, формализация, обсуждение и согласование возможных решений с заказчиками и разработчиками Составление и поддержание в актуальном состоянии технической и эксплуатационной документации на ПО  Требования:  Понимание принципов разработки программного обеспечения. Опыт работы с системами управления проектами. Владение Microsoft Word, Excel, Visio, Draw.io, Confluence; Умение создавать, редактировать, иллюстрировать и адаптировать технический материал под Заказчика и Разработчика; Орфографическая и стилистическая грамотность, грамотная устная речь, аккуратность.  Условия:   График работы 5\\2, гибкое начало рабочего времени;   Крутой офис в собственном коттедже;   Офис оборудован всем необходимым для комфортной работы и отдыха: чай, кофе и пр. в обеденной зоне. Спортивный уголок, места для отдыха;   Помогаем сотрудникам профессионально расти вместе с компанией: покупаем необходимую литературу, покупаем доступ к онлайн-ресурсам (вебинары, конференции, тренинги), приглашаем высококвалифицированных специалистов для обсуждения опыта и проектирования сложных проектов;   Корпоративные мероприятия, обучение английскому языку;  Официальное трудоустройство, своевременная оплата труда. "
keyword_dict = {
    ("написание", "редактирование", "формулирование", "сочинение", "корректировка", "отвечать",
     "анализировать", "реферировать", "преобразование", "сверка", "копирование", "вставка",
     "удаление", "поиск", "замена", "подчеркивать", "отмечать", "выравнивание",
      "компоновать","компоновка", "сборка", "раздел", "объединение", "публиковать","публикация", "сортировка",
     "индексация", "группировка", "экспорт", "архивировать","встреча",
     "распаковывать", "подписывать", "подписание",  "рисовать", "изображать", "отображение", "создавать", "формировать", "сжимать",
     "вращать", "отражать", "выравнивать", "выделять","участие", "прием", "отправка","контроль", "погрузка", "приемка",
     "заключение","раскредитование","передача","осуществлять","урегулирование",
     "контроль","выполнение","перевозка","вести","работа","пополнение","обеспечение","перемещение","доставка","встреча",
     "помощь","поддержание","соблюдение","организация","осуществление","участие","выполнение","выдавать","работать",
     "разработка","разрабатывать","протоколирование","сверка","проведение","оформление","продажа","настройка","отвозить","развозка",
     "уборка","убирать","запись","записывать","обслуживание","обслуживать",
     "создание","создавать","инвентаризация","знание","знать"

     ): "НЕЛЬЗЯ",

    ("прием","знание","оформление","печать","предоставлять","информация","осуществление","сверка","формирование","производство","подготовка",
     "распределение","регистрация","отчетность","учет","управление",
     "консультирование","закупка","сверка","списание","анализировать","анализ",
        "контроль","проверка","подписание","учет","выражать", "преобразовывать", "моделировать", "заполнение", "подготовка", "симулировать", "оптимизировать", "вычислять", "рассчитывать",
     "подсчитывать", "считать", "определять", "измерять", "пересчитывать", "суммировать", "умножать", "делить",
     "вычитать", "интегрировать", "дифференцировать", "округлять", "аппроксимировать", "анализировать", "оптимизировать",
     "моделировать", "сравнивать", "уточнять", "апроксимировать", "проверять", "редактировать","распознавать", "классифицировать", "сегментировать", "аннотировать", "улучшать", "искажать", "фильтровать",
     "обрезать", "масштабировать", "изменять размер", ): "МОЖНО"

}
#results = find_keywords(text, keyword_dict)
#print(results)



#считываем обязанности, в каждой находим слова для категорий МОЖНО И НЕЛЬЗЯ и начало конец этих слов
#создаем обучающую выборку для NER модели

data = pd.read_csv(r'data.csv', header=0, encoding='cp1251', sep=';')
data = list(data["text"][1:5])
TRAIN_DATA = []
for d in data:
    TRAIN_DATA.append(find_keywords(d, keyword_dict))
print(TRAIN_DATA)
