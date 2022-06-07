import spacy
import os
import pathlib
import ocr
import score
import shutil

def resume_score():

    for filename in os.listdir("C:/College/BE_Project/Project/spacy3/uploads/pdf"):
        with open(os.path.join("C:/College/BE_Project/Project/spacy3/uploads/pdf/", filename), 'r') as f:
            path = os.path.join("C:/College/BE_Project/Project/spacy3/uploads/pdf/", filename)
            ocr.pdf_to_text(path)

    nlp_ner = spacy.load("C:/College/BE_Project/Project/spacy3/model-best/")

    text_list = os.listdir("C:/College/BE_Project/Project/spacy3/uploads/text/")
    text_path = "C:/College/BE_Project/Project/spacy3/uploads/text/"
    text = ''
    if len(text_list) != 0:
        for filename in text_list :
            with open(text_path + filename, 'r') as f:
                resume_text = f.readlines()
                text = text.join(resume_text)
                doc = nlp_ner(text)
                            
                output = doc.to_json()
                entities = {'NAME': [], 'SKILL': [], 'EMAIL': [], 'CONTACT': [], 'POSITION': [], 'LOCATION': [], 'EDUCATION': [], 'ORG': [], 'COLLEGE': []}
                for ent in doc.ents:
                    entities[ent.label_].append(ent.text)
                            
                final = score.score(entities)
                print('Score for ' + filename + ' is ' + str(final))