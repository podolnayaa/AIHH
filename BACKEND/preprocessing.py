import re
from pymorphy2 import MorphAnalyzer
#для преобразования к нормальной форме слова
morph = MorphAnalyzer()
import razdel

def preprocess_text(text):
    tokens = list(razdel.tokenize(text.lower()))  # токенизация и приведение к нижнему регистру
    tokens = [token.text for token in tokens]  # удаление стоп-слов и символов

    return ' '.join(tokens)

def preprocessing(description: str) -> list:
    patterns = "[A-Za-z0-9!#$%&'()*+,./:;<=>?@[\]^_`{|}~—\"\-]+"
    description = re.sub(patterns, '', description)
    description =  re.split(r'\s+(?=[А-Я])', description)

    new_desc = []
    for d in description:
        new_desc.append(preprocess_text(d))


    start,end = False, False
    index_start= 0
    index_end = 0
    for i, n in enumerate(new_desc):
        if 'обязанности' in new_desc[i] and start==False:
            index_start = i
            start = True
        if 'требования' in new_desc[i] and end==False:
            index_end = i
            end = True


    responsibilities = new_desc[index_start+1:index_end]
    responsibilities_end = []
    for r in responsibilities:
        print(len(r))
        if len(r) >= 6:
            responsibilities_end.append(r)
    return responsibilities_end


if __name__ == "__main__":

    data = " Обязанности:  Разработка web-интерфейсов для внутренних сервисов Интеграция сервисов по АPI (только в части фронтенд) Доработка и поддержка сайта  Требования:  Навыки работы со стеком: Vue 3 (Composition API), Nuxt 3, TailwindCSS Знания языка программирования Javascript\TypeScript Навыки работы с Git  Необязательные требования:  Наличие пет проектов на требуемом стеке, если нет опыта коммерческой разработки.  Условия:  Официальное трудоустройство по ТК РФ; Работу в комфортном офисе в центре города, в минуте от набережной (график 5/2, с 9:00 до 18:00); "
    print(preprocessing(data))