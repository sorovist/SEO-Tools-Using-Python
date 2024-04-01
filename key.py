import pandas as pd
from pytrends.request import TrendReq
import matplotlib.pyplot as plt
import streamlit as st

def app():

    st.title("Keyword Analysis")

    # Initialize TrendReq object
    trends = TrendReq()

    # Get user input for keyword
    keyword = st.text_input("Enter the Keyword you want to analyze")

    if keyword:  # Check if keyword is not empty
        # Fetch interest by region data
        st.header("Interest by Region")
        trends.build_payload(kw_list=[keyword])
        data_region = trends.interest_by_region()

        # Sample the data
        sampled_data = data_region.sample(5)
        
        # Display sampled data in a table
        st.write(sampled_data)

        # Plot interest by region
        st.subheader("Interest by Region Plot")
        fig, ax = plt.subplots(figsize=(10, 6))
        sampled_data.reset_index().plot(x="geoName", y=keyword, kind="bar", ax=ax)
        st.pyplot(fig)

    
        # Fetch suggestions for the entered keyword
        st.header("Keyword Suggestions")
        keyword_suggestions = trends.suggestions(keyword=keyword)
        data_suggestions = pd.DataFrame(keyword_suggestions)
        st.write(data_suggestions.drop(columns=["mid"]).rename(columns={"title": "Title", "type": "Type"}))

        # Fetch trending searches data
        st.header("Trending Searches Of India")
        data_trending = trends.trending_searches(pn="india")
        st.write(data_trending.rename(columns={0: "Search Term"}))

    

    