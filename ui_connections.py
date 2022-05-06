# -*- coding: utf-8 -*-
"""
Created on Wed Apr 20 12:12:05 2022

@author: Mayur
"""
#StreamLit
import streamlit as st

#Definition Python File
import functions

# Plot
import seaborn as sns
import matplotlib.pyplot as plt


def analysis(raw_text):
    common_tokens = st.sidebar.number_input("Most Common Tokens", 5, 20)

    if st.button("Analyse"):
        with st.expander("Original Text"):
            st.write(raw_text)

        #
        with st.expander("Text Analysis"):
            text_df = functions.text_analyze(raw_text)
            st.dataframe(text_df)

        with st.expander("Entities"):
            entities_df = functions.get_entities(raw_text)
            st.dataframe(entities_df)

        # Layouts
        col1, col2 = st.columns(2)

        with col1:
            with st.expander("Word Stats"):
                st.info("Word Statistics")
                stats = functions.get_word_stats(raw_text)
                st.dataframe(stats)

            with st.expander("Top Keywords"):
                st.info("Top Keywords")
                common_words = functions.get_common_words(raw_text, common_tokens)
                st.write(common_words)

            with st.expander("Sentiment"):
                st.info("Sentiment Analysis")
                sentiment = functions.get_sentiments(raw_text)
                st.dataframe(sentiment)

        with col2:
            with st.expander("Plot Word Freq"):
                st.info("Word Frequencies")
                fig1 = plt.figure()
                sns.barplot(x=common_words['Words'], y=common_words['Count'])
                plt.xticks(rotation=45)
                st.pyplot(fig1)

            with st.expander("Plot PoS"):
                st.info("Part-Of-Speech")
                fig = plt.figure()
                sns.countplot(text_df['PoS'])
                plt.xticks(rotation=45)
                st.pyplot(fig)

            with st.expander("WordCloud"):
                st.info("WordCloud")
                fig2 = functions.plot_wordcloud(raw_text)
                st.pyplot(fig2)

        with st.expander("Download Results"):
            functions.download_results(text_df)
