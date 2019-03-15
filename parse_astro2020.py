#!/usr/bin/env python

import os
import glob
import pickle
import time

import nltk
import PyPDF2

from natsort import natsorted

import re
import fnmatch

from collections import defaultdict

import warnings
# This is a lazy and lousy way to filter warnings, but ¯\_(ツ)_/¯
warnings.simplefilter("ignore")

def search_missions(keywords_dict):

    '''
    Here we use NLTK and regular expressions to search the keword dictionary, 
    consisting of tokenized text. For example, "<Orings> <Space>" finds all 
    instances of "Origins Space" in the text. The angle brackets are used to 
    mark token boundaries, and any whitespace between the angle brackets is ignored.
    '''

    for key in keywords_dict:
        text = nltk.Text(keywords_dict[key])
        lynx = nltk.text.TokenSearcher(text).findall(r"<Lynx>")
        luvoir = nltk.text.TokenSearcher(text).findall(r"<LUVOIR>")
        habex = nltk.text.TokenSearcher(text).findall(r"<HabEx>")
        origins = nltk.text.TokenSearcher(text).findall(r"<Origins> <Space> <Telescope>")

        if len(lynx) > 0:
            print("{} makes {} explicit mentions of Lynx".format(key, len(lynx)))

        if len(luvoir) > 0:
            print("{} makes {} explicit mentions of LUVOIR".format(key, len(luvoir)))

        if len(habex) > 0:
            print("{} makes {} explicit mentions of HabEx".format(key, len(habex)))

        if len(origins) > 0:
            print("{} makes {} explicit mentions of Origins".format(key, len(origins)))



def tokenize_pdf(pdf_file):

    with open(pdf_file, 'rb') as pdfObject:

        pdfReader = PyPDF2.PdfFileReader(pdfObject)

        # Get the number of pages
        num_pages = pdfReader.numPages
        count = 0
        text = ''

        #Read each of those pages
        while count < num_pages:
            pageObj = pdfReader.getPage(count)
            count +=1
            text += pageObj.extractText()

    # Now read the plan text and tokenize it
    tokens = nltk.tokenize.word_tokenize(text)

    # Garbage punctuation & words we don't care about
    punctuation = ['(', ')', ';', ':', '[', ']', ',']
    stop_words = nltk.corpus.stopwords.words('english')

    # Returns a list of words that are not in these garbage lists.
    keywords = [word for word in tokens if not word in stop_words and not word in punctuation]

    bigrams = list(nltk.bigrams(keywords))

    if not os.path.exists('pickles/'):
        print("Creating a pickles/ subdirectory to store the keyword & bigram pickles")
        os.mkdir('pickles/')

    with open('pickles/{}_keywords.pickle'.format(pdf_file[:-4]), 'wb') as keyword_pickle:
        pickle.dump(keywords, keyword_pickle)
    
    with open('pickles/{}_bigrams.pickle'.format(pdf_file[:-4]), 'wb') as bigram_pickle:
        pickle.dump(bigrams, bigram_pickle)

    return keywords, bigrams


def get_keywords(pdf_file):

    pickles_found = (os.path.isfile('pickles/{}_keywords.pickle'.format(pdf_file[:-4]))) & (os.path.isfile('pickles/{}_bigrams.pickle'.format(pdf_file[:-4])))

    if pickles_found:
        with open('pickles/{}_keywords.pickle'.format(pdf_file[:-4]), 'rb') as keyword_pickle:
            keywords = pickle.load(keyword_pickle)

        with open('pickles/{}_bigrams.pickle'.format(pdf_file[:-4]), 'rb') as bigram_pickle:
            bigrams = pickle.load(bigram_pickle)

    else:
        print("Keyword pickles for {} not found, tokenizing PDF from scratch.".format(pdf_file[:-4]))
        keywords, bigrams = tokenize_pdf(pdf_file)

    return keywords, bigrams 

def main():
    pdf_files = glob.glob('*.pdf')
    num_submitted = len(pdf_files)

    # Sort the text files by submission ID, ignoring the fact that we don't use leading zero pads
    sorted_pdf_files = natsorted(pdf_files, key=lambda y: y.lower())

    missions = ['*JWST*', '*WFIRST*', '*AXIS*',
                '*Athena*', '*Lynx*', '*LUVOIR*',
                '*HabEx*', '*ALMA*', '*ngVLA*',
                '*GMT*', '*TMT*']

    mission_dict = defaultdict(list)
    keywords_dict = {}
    bigrams_dict = {}

    for pdf_file in sorted_pdf_files:
        keywords, bigrams = get_keywords(pdf_file)
        keywords_dict["{}".format(pdf_file[:-4])] = keywords
        bigrams_dict["{}".format(pdf_file[:-4])] = bigrams

    print("\nMaster keyword dictionaries created.")

    search_missions(keywords_dict)


        # for mission in missions:
        #     matches = fnmatch.filter(keywords, mission)
        #     if len(matches) > 0:
        #         print('{} mentions of {} in {}'.format(len(matches), mission[1:-1], pdf_file[:-4]))
        #         mission_dict[mission[1:-1]].append(pdf_file)
        # if ('Origins', 'Space') in bigrams:
        #     number_ost_references = bigrams.count(('Origins', 'Space'))
        #     print('{} mentions of OST in {}'.format(number_ost_references, pdf_file[:-4]))
        #     mission_dict["OST"].append(pdf_file)

    print("\nOf {} submitted Astro2020 whitepapers:".format(num_submitted))

    for key in mission_dict.keys():
        print("{} papers explicitly mention {}".format(len(mission_dict[key]), str(key)))


if __name__ == "__main__":
    start_time = time.time()
    main()
    runtime = round((time.time() - start_time), 3)
    print("\nFinished in {} seconds.".format(round(runtime, 3)))
