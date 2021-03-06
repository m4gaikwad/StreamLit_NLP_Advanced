# -*- coding: utf-8 -*-
"""
Created on Wed Apr 20 11:40:42 2022

@author: Mayur
"""

import streamlit as st
import docx2txt
#import PyPDF2 as pypdf

# Definitions
import functions

#UI Implementation
import ui_connections

#Page Configuration
PAGE_CONFIG = {'page_title': 'NLP Analysis',
               'page_icon': '🔍',
               'initial_sidebar_state': 'collapsed'}

st.set_page_config(**PAGE_CONFIG)


#Pages
def nlp():
    st.subheader("NLP Files Process")
    text_file = st.file_uploader('Upload Files',
                                 type=['pdf', 'txt', 'docx'])
    if text_file is not None:
        #st.write(dir(text_file))
        if text_file.type == 'application/pdf':
            raw_text = functions.read_pdf(text_file)
            ui_connections.analysis(raw_text)

        elif text_file.type == 'text/plain':
            raw_text = str(text_file.read(), 'utf-8')
            ui_connections.analysis(raw_text)

        elif text_file.type == 'application/vnd.openxmlformats-officedocument.wordprocessingml.document':
            raw_text = docx2txt.process(text_file)
            ui_connections.analysis(raw_text)

        else:
            st.error('Please Upload File with PDF or Text or DOCX format.')


def about():
    st.subheader("About")
    st.info('By : Mayur Gaikwad')


def main():
    st.title("NLP with Streamlit")
    menu = ["Home", "NLP", "About"]

    choice = st.sidebar.selectbox("Menu", menu)

    if choice == "Home":
        st.subheader("Analyse Text")
        raw_text = st.text_area("Enter Text Here")
        ui_connections.analysis(raw_text)

    elif choice == "NLP":
        nlp()

    else:
        about()


if __name__ == "__main__":
    main()
