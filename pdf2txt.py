from PyPDF2 import PdfFileReader, PdfFileWriter

file_path = 'pdf_resumes/sample.pdf'
pdf = PdfFileReader(file_path)

res_text = ''
for page in range(1, pdf.getNumPages()):
    res_text += pdf.getPage(page).extractText()

print(res_text)
f = open('sample_resume.txt', 'w')
f.write(res_text)
f.close()
