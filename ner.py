import spacy
from spacy.tokens import DocBin
from tqdm import tqdm
import json
import jsonlines
import pickle

# Generate the config file
# python -m spacy init config config.cfg --lang en --pipeline ner --optimize efficiency

nlp = spacy.load("en_core_web_sm")
db = DocBin()

with jsonlines.open('C:/College/BE_Project/Project/spacy3/training_data.jsonl') as reader:
    for TRAIN_DATA in reader:
        for text, annot in tqdm(TRAIN_DATA['annotations']):
            doc = nlp.make_doc(text)
            ents = []
            for start, end, label in annot['entities']:
                span = doc.char_span(start, end, label=label, alignment_mode="contract")
                if span is None:
                    print('Skipping entity')
                else:
                    ents.append(span)
            doc.ents = ents
            db.add(doc)

db.to_disk('C:/College/BE_Project/Project/spacy3/training_data.spacy')

# Train model
# python -m spacy train config.cfg --output ./ --paths.train ./training_data.spacy --paths.dev ./training_data.spacy