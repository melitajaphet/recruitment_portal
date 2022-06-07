import fitz
doc = fitz.open('app/static/uploads/paarsh_letter.pdf') 

for page in doc:
    text = page.get_text()
    print(text)