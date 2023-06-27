
import clfs from SVC_model


#сравнение двух моделей, выбор одной для внедрения в модуль классификации


########################################## SVC_MODEL
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



##############################NER_MODEL
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

