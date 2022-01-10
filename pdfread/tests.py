from django.test import TestCase
import pdfplumber
# Create your tests here.

pdf = pdfplumber.open("대공황_이후_주요_금융위기_비교.pdf")
first_page = pdf.pages[0]
print(first_page.extract_text())
pdf.close()