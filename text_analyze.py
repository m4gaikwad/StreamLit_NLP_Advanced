# -*- coding: utf-8 -*-
"""
Created on Thu Apr 21 14:19:25 2022

@author: Mayur
"""
######### Definitions ###########

# StreamLit and Pandas
import streamlit as st
import pandas as pd

# Time and Encoding
import base64
import time
from io import StringIO
# text pkgs
import spacy
import neattext as nt
from textblob import TextBlob
from collections import Counter

# Read PDF
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfparser import PDFParser

# Plot
import matplotlib.pyplot as plt
from wordcloud import WordCloud

# Global Variables
nlp = spacy.load('en_core_web_sm')


# Text Analysis Using SpaCy
def text_analyze(raw_text):
    txt = nlp(raw_text)
    alldata = [(token.text, token.shape_, token.pos_,
                token.tag_, token.lemma_, token.is_alpha) for token in txt]

    df = pd.DataFrame(alldata, columns=['Token', 'Shape', 'PoS',
                                        'Tag', 'Lemma', 'IsAlpha'])
    return df


def get_entities(raw_text):
    txt = nlp(raw_text)
    entities = [(entity.text, entity.label_) for entity in txt.ents]
    df = pd.DataFrame(entities, columns=['Text', 'Labels'])
    return df


# TextFrame to get length of text, and no. of vowels, consonants and stopwords
def get_word_stats(raw_text):
    docx = nt.TextFrame(raw_text)
    stats = docx.word_stats()
    new_st = dict((k, stats[k])
                  for k in ['Length of Text', 'Num of Vowels',
                            'Num of Consonants', 'Num of Stopwords']
                  if k in stats)
    stats_df = pd.DataFrame(new_st.values(),
                            columns=['Count'],
                            index=new_st.keys())
    return stats_df


# Extracting most common words using SpaCy and Counter
def get_common_words(raw_text, num=5):
    doc = nlp(raw_text)
    words = [token.text
             for token in doc
             if not token.is_stop
             and not token.is_punct
             and not token.is_space]

    word_freq = Counter(words)
    common_words = word_freq.most_common(num)
    common_words = pd.DataFrame(common_words,
                                columns=['Words', 'Count'])
    return common_words


# Extracting sentiment polarity using TextBlob
def get_sentiments(raw_text):
    blob = TextBlob(raw_text)
    sentiment = blob.sentiment
    senti = pd.DataFrame(sentiment, columns=['Values'],
                         index=['Polarity', 'Subjectivity'])
    return senti


# Plotting WordCloud
def plot_wordcloud(raw_text):
    doc = nlp(raw_text)
    words = [token.text
             for token in doc
             if not token.is_stop and not token.is_punct]
    fig = plt.figure()
    wc = WordCloud().generate_from_text(" ".join(words))
    plt.imshow(wc, interpolation='bilinear')
    plt.axis('off')
    return fig


# Downloading Statistics of Text
def download_results(data):
    file = data.to_csv(index=False)
    b64 = base64.b64encode(file.encode()).decode()
    new_file = 'Result_{}.csv'.format(time.strftime("%Y%m%d-%H_%M_%S"))
    st.markdown('###  ⬇ Download CSV File ⬇ ')
    href = f'<a href="data:file/csv;base64,{b64}" download="{new_file}"> Click Here </a>'
    st.markdown(href, unsafe_allow_html=True)


# Read PDF and Extract Text
def read_pdf(text_file):
    output = StringIO()
    parser = PDFParser(text_file)
    doc = PDFDocument(parser)
    rsmgr = PDFResourceManager()
    dev = TextConverter(rsmgr, output, laparams=LAParams())
    interpreter = PDFPageInterpreter(rsmgr, dev)
    for page in PDFPage.create_pages(doc):
        interpreter.process_page(page)
    return (output.getvalue())
