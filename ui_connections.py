# -*- coding: utf-8 -*-
"""
Created on Wed Apr 20 12:12:05 2022

@author: Mayur
"""
#StreamLit
import streamlit as st

#Definition Python File
import functions


def analysis(raw_text):
    common_tokens = st.sidebar.number_input("Most Common Tokens", 5, 20)

    #Dataframes for extracted data
    text_df = functions.text_analyze(raw_text)  #Text Information
    entities_df = functions.get_entities(raw_text) #Text Tags Information (GPE, ORG)
    stats = functions.get_word_stats(raw_text)  #Word Statistics
    common_words = functions.get_common_words(raw_text, common_tokens) #Most common words
    sentiment = functions.get_sentiments(raw_text) #Polarity and Subjectivity of Text

    if st.button("Analyse"):
        with st.expander("Original Text"):
            st.write(raw_text) #Display Raw Text

        with st.expander("Text Analysis"):
            st.dataframe(text_df)  #Display Text Information

        with st.expander("Entities"):
            st.dataframe(entities_df)  #Display Tag Information

        # Layouts
        col1, col2 = st.columns(2)

        with col1:
            with st.expander("Word Stats"):
                st.info("Word Statistics")
                st.dataframe(stats)  #Display Word Statistics

            with st.expander("Top Keywords"):
                st.info("Top Keywords")
                st.write(common_words)  #Display Common Keywords

            with st.expander("Sentiment"):
                st.info("Sentiment Analysis")
                st.dataframe(sentiment)  #Display Sentiment Values

        with col2:
            with st.expander("Plot Word Freq"):
                st.info("Word Frequencies")
                word_freq = functions.plot_wordfreq(common_words)
                st.pyplot(word_freq)  #Display Word Freq. Graph

            with st.expander("Plot PoS"):
                st.info("Part-Of-Speech")
                pos = functions.plot_pos(text_df)
                st.pyplot(pos) #Display PoS Count Graph

            with st.expander("WordCloud"):
                st.info("WordCloud")
                wc = functions.plot_wordcloud(raw_text)
                st.pyplot(wc) #Display WordCloud

        with st.expander("Download Results"):
            functions.download_results(text_df) #Download Text Information
