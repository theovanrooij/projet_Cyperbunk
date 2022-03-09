import pdfplumber
content = []
with pdfplumber.open(r'2000 -/Thin-Air-Richard-Morgan.pdf') as pdf:
    for i in range(0,len(pdf.pages)):

        page = pdf.pages[i]
        content += page.extract_text()

content = "".join(content)
with open('2000 -Thin-Air-Richard-Morgan.txt', 'w') as f:
    f.write(content)

