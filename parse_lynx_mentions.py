#!/usr/bin/env/python
import glob
import subprocess
import traceback

import PyPDF2 
import textract

from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

from natsort import natsorted

import warnings
warnings.simplefilter("ignore")


import io
 
from pdfminer.converter import TextConverter
from pdfminer.pdfinterp import PDFPageInterpreter
from pdfminer.pdfinterp import PDFResourceManager
from pdfminer.pdfpage import PDFPage
 
def pdfmine(pdf_path):
    resource_manager = PDFResourceManager()
    fake_file_handle = io.StringIO()
    converter = TextConverter(resource_manager, fake_file_handle)
    page_interpreter = PDFPageInterpreter(resource_manager, converter)
 
    with open(pdf_path, 'rb') as fh:
        for page in PDFPage.get_pages(fh, caching=True, check_extractable=True):
            page_interpreter.process_page(page)
        
        text = fake_file_handle.getvalue()
 
    # close open handles
    converter.close()
    fake_file_handle.close()
 
    if text:
        return text


def get_keywords(pdf_file):
    

    with open(pdf_file, 'rb') as input_file:
        input_buffer = BytesIO(input_file.read())

    try:
        pdfReader = PdfFileReader(input_buffer)
    except utils.PdfReadError:
        pdfReader = PdfFileReader(decompress_pdf(input_file))

    with open(pdf_file, 'rb') as pdfFileObj:



        # Read the PDF file
        pdfReader = PyPDF2.PdfFileReader(pdfFileObj, strict = False)

        # Get the number of pages
        num_pages = pdfReader.numPages
        count = 0
        text = ""

        #The while loop will read each page
        while count < num_pages:
            pageObj = pdfReader.getPage(count)
            count +=1
            text += pageObj.extractText()

    # Check if PyPDF succeeded
    if text != "":
        text = text
        # If the above returns as False, we run the OCR library textract to 
    else:
        text = textract.process(pdf_file, method='tesseract', language='eng')
        print('Read {} with textract instead of PyPDF2'.format(pdf_file))
    # Now we have a text variable which contains all the text derived 
    # from our PDF file. Type print(text) to see what it contains. It 
    # likely contains a lot of spaces, possibly junk such as '\n' etc.


    # Now, we will clean our text variable, and return it as a list of keywords.

    # Break text into individual words
    tokens = word_tokenize(text)

    # Punctiation we don't care about
    punctuation = ['(',')',';',':','[',']',',']

    # Clean standard garbage words like "the", "I", "and", etc. 
    stop_words = stopwords.words('english')
   
    #We create a list comprehension which only returns a list of words #that are NOT IN stop_words and NOT IN punctuations.
    keywords = [word for word in tokens if not word in stop_words and not word in punctuation]

    return keywords



def main():
    pdf_files = glob.glob('*.pdf')

    # Sort the PDF files by submission ID, ignoring the fact that we don't use leading zero pads
    sorted_pdf_files = natsorted(pdf_files, key=lambda y: y.lower())

    for pdf in sorted_pdf_files:
        try:
            keywords = pdfmine(pdf)
        except:
            print('Error reading {}'.format(pdf))
            traceback.print_exc()
    
        
        print(keywords)

    # checklist = ['Lynx','LYNX']
    # matches = [c for c in checklist if c in keywords]

    # if keywords.count('Lynx') > 1:
    #     print(keywords.count('Lynx'), "mentions of Lynx in {}".format(pdf_file))
    # if keywords.count('LUVOIR') > 1:
    #     print(keywords.count('LUVOIR'), "mentions of LUVOIR in {}".format(pdf_file))
    # if keywords.count('Origins Space Telescope') > 1:
    #     print(keywords.count('Origins Space Telescope'), "mentions of Origins in {}".format(pdf_file))
    # if keywords.count('HabEX') > 1:
    #     print(keywords.count('HabEx'), "mentions of HabEx in {}".format(pdf_file))  


if __name__ == "__main__":
    main()
