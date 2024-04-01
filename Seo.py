import requests
from bs4 import BeautifulSoup
import nltk
from nltk.tokenize import word_tokenize
from nltk.util import ngrams
import streamlit as st

def app():
    
    nltk.download('stopwords')
    nltk.download('punkt') 

    st.title("SEO Analysis")
    url = st.text_input('Enter the URL you want to analyze')


    def seo_analysis(url):
    # Save the good and the warnings in lists
        good = []
        bad = []
    # Send a GET request to the website
        response = requests.get(url)
    # Check the response status code
        if response.status_code != 200:
            st.error("Error: Unable to access the website.")
            return

    # Parse the HTML content
        soup = BeautifulSoup(response.content, 'html.parser')

    # Extract the title and description
        title = soup.find('title').get_text()
        description = soup.find('meta', attrs={'name': 'description'})['content']

    # Check if the title and description exist
        if title:
            good.append("Title Exists! Great!")
        else:
            bad.append("Title does not exist! Add a Title")

        if description:
            good.append("Description Exists! Great!")
        else:
            bad.append("Description does not exist! Add a Meta Description")

    # Grab the Headings
        hs = ['h1', 'h2', 'h3', 'h4', 'h5', 'h6']
        h_tags = []
        for h in soup.find_all(hs):
            good.append(f"{h.name}-->{h.text.strip()}")
            h_tags.append(h.name)

        if 'h1' not in h_tags:
            bad.append("No H1 found!")

    # Extract the images without Alt
        for i in soup.find_all('img', alt=''):
            bad.append(f"No Alt: {i}") 

    # Extract keywords
    # Grab the text from the body of html
        bod = soup.find('body').text

    # Extract all the words in the body and lowercase them in a list
        words = [i.lower() for i in word_tokenize(bod)]

    #extract bigrams
        bi_grams= ngrams(words, 2)
        freq_bigrams = nltk.FreqDist(bi_grams)
        bi_grams_freq= freq_bigrams.most_common(10)

    # Grab a list of English stopwords
        sw = nltk.corpus.stopwords.words('english')
        new_words = []

    # Put the tokens which are not stopwords and are actual words (no punctuation) in a new list
        for i in words:
            if i not in sw and i.isalpha():
                new_words.append(i)

    # Extract the fequency of the words and get the 10 most common ones
        freq = nltk.FreqDist(new_words)
        keywords= freq.most_common(10)

    # Print the results
    
        tab1, tab2, tab3, tab4 = st.tabs(['Keywords','Bigrams','Good', 'Bad'])
        with tab1:
            for i in keywords:
                st.text(i)
        with tab2:
            for i in bi_grams_freq:
                st.text(i)
        with tab3:
            for i in good:
                st.success(i)
        with tab4:
            for i in bad:
                st.text(i)   

    # Call the function to see the results
    if url:
        seo_analysis(url)