import streamlit as st
from streamlit_option_menu import option_menu
import Seo, key, home
st.set_page_config(
    page_title="SEO Tools",

)

class MultiApp:

    def __init__(self):
        self.apps=[]
    def add_app(self, title, function):
        self.apps.append({
            "title": title,
            "function": function
        })

    def run():
        with st.sidebar:
            app= option_menu(
                menu_title='SEO Tools',
                options=['Home','SEO Analysis','Keyword Analysis'],
                icons=['house-fill'],
                default_index=1,
                )

        if app=='Home':
            home.app()

        if app=='SEO Analysis':
            Seo.app()

        if app=='Keyword Analysis':
            key.app()

    run()
        