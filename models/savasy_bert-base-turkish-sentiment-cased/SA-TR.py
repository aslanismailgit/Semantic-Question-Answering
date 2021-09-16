
from transformers import pipeline, AutoModelForTokenClassification, AutoTokenizer

model= transformers.AutoModelForSequenceClassification.from_pretrained(".")
tokenizer=transformers.AutoTokenizer.from_pretrained(".")




dosya=["dvd.tsv","Books.tsv","Kitchen.tsv","electronics.tsv"][3]



data = [line.strip().split("\t") for line in open(dosya)]

sa= pipeline("sentiment-analysis", model=model, tokenizer=tokenizer)


real=[d[1] for d in data]

pred=[sa(d[0]) for d in data]
pred2=[p[0]['label'].split("_")[1] for p in pred]


res=[a==b for (a,b) in zip(pred2, real)]
sum(res)/len(res)

