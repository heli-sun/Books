import streamlit as st
import pandas as pd
from recommender import find_books_by_author, find_books_by_genre, get_content_based_recommendations, create_model_and_get_matrix
import ast
import base64
import os 
import hashlib

def file_hash(filepath):
    with open(filepath, "rb") as f:
        return hashlib.md5(f.read()).hexdigest()

books_hash = file_hash('books_data.csv')

@st.cache_data
def load_data(file_hash):
    return pd.read_csv('books_data.csv')

df = load_data(books_hash)

@st.cache_data
def load_model(file_hash):
    df = pd.read_csv('books_data.csv')
    return create_model_and_get_matrix(df)

cosine_sim_matrix = load_model(books_hash)


st.set_page_config(
    page_title="Book Discovery Tool",
    page_icon="favicon.png"
)

st.set_page_config(page_title="Book Discovery Tool", layout="wide")

# Function to get the Base64 representation of an image
def get_base64_image(image_path):
    try:
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode()
    except FileNotFoundError:
        st.error(f"Error: The file '{image_path}' was not found in the same folder as app.py.")
        return None

# Embed the Base64 image directly into the CSS
image_b64 = get_base64_image("bookshop.jpg")
if image_b64:
    page_bg_img = f'''
    <style>
    .stApp {{
        background-image: url("data:image/jpeg;base64,{image_b64}");
        background-size: cover;
        background-repeat: no-repeat;
        background-attachment: fixed;
    }}
    </style>
    '''
    st.markdown(page_bg_img, unsafe_allow_html=True)

# CSS for custom font, text color, and layout
st.markdown("""
<style>
    /* Import a beautiful, readable font: Garamond */
    @import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@400;700&display=swap');

    /* Set all text to Garamond, warm white, and bolder */
    body, .stApp, .st-emotion-cache-1c7y3km {
        color: #ffe8c2;
        font-family: 'Cormorant Garamond', serif;
        font-weight: 700;
        text-shadow: 1px 1px 3px rgba(0, 0, 0, 0.7);
    }

    /* Error and warning messages with warm glow */
    .stAlert {
        border: 4px solid;
        border-image: linear-gradient(to right, #f4c542, #e89c3f, #d86f3c, #a94438, #6b2e1f);
        border-image-slice: 1;
        background-color: rgba(255, 255, 255, 0.2);
        box-shadow: 0 0 15px rgba(255, 200, 100, 0.3);
    }
    .stAlert div[data-testid="stMarkdownContainer"] p {
        color: #ffe8c2 !important;
        text-shadow: 1px 1px 3px rgba(0, 0, 0, 0.7);
    }


    .rainbow-title-wrapper {
        background: linear-gradient(
            135deg,
            #291700,
            #6E3100,
            #361B00,
            #4F2500,
            #753400
        );
        padding: 10px 35px;
        clip-path: polygon(
            10% 0%, 90% 0%, 100% 30%, 95% 60%, 100% 100%, 70% 90%, 50% 100%, 30% 90%, 0% 100%, 5% 60%, 0% 30%
        );
        box-shadow: 0 0 20px rgba(0, 0, 0, 0.6);
        display: flex;
        justify-content: center;
        align-items: center;
        width: fit-content;
        margin: 0 auto 90px auto;
    }


    /* Main headings with warm rainbow gradient */
    .rainbow-title {
        background: linear-gradient(to right, #f4c542, #e89c3f, #F74A2A, #e89c3f, #f4c542);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 700;
        font-family: 'Cormorant Garamond', serif;
        text-align: center;

        text-shadow: 0.1px 0.4px 0.8px rgba(0, 0, 0, 0.3);
            
    }


            
    /* Container border with warm gradient and glow */
    .rainbow-border-container {
        border-width: 4px;
        border-style: solid;
        border-image: linear-gradient(to right, #f4c542, #e89c3f, #d86f3c, #a94438, #6b2e1f);
        border-image-slice: 1;
        padding: 15px;
        margin-bottom: 20px;
        background-color: rgba(0, 0, 0, 0.4);
        border-radius: 10px;
        box-shadow: 0 0 15px rgba(255, 200, 100, 0.3);
    }

    /* Wavy box with warm glow */
    .wavy-rainbow-box {
        border-width: 4px;
        border-style: solid;
        border-image: linear-gradient(to right, #f4c542, #e89c3f, #d86f3c, #a94438, #6b2e1f);
        border-image-slice: 1;
        padding: 15px;
        margin-bottom: 20px;
        background-color: rgba(0, 0, 0, 0.4);
        border-radius: 40% 60% 70% 30% / 50% 50% 50% 50%;
        box-shadow: 0 0 15px rgba(255, 200, 100, 0.3);
    }

    /* Headings and text inside containers */
    h2, h3 {
        color: #ffe8c2 !important;
        font-weight: 700;
        text-shadow: 1px 1px 3px rgba(0, 0, 0, 0.7);
    }

    /* Flexbox for header layout */
    .header-container {
        display: flex;
        align-items: center;
    }

    /* Icon positioning */
    .icon-adjusted {
        margin-top: 15px;
        margin-right: 15px;
    }
</style>
""", unsafe_allow_html=True)


st.markdown("""
<div class="rainbow-title-wrapper">
  <h1 class="rainbow-title">✧✧✧✧✧✧Personalized Book Discovery✧✧✧✧✧✧</h1>
</div>
""", unsafe_allow_html=True)
    
st.markdown("### Type in a book you love to get recommendations based on the same author or a similar genre:")

# ALL OF THE CODE BELOW IS OUTSIDE THE BOX
@st.cache_resource
def load_data():
    try:
        df = pd.read_csv('books_data.csv')
        return df
    except FileNotFoundError:
        st.error("books_data.csv not found. Please run the data_fetcher.py script first.")
        return None

df = load_data()

if df is not None:
    @st.cache_resource
    def load_model():
        return create_model_and_get_matrix(df)
    
    cosine_sim_matrix = load_model()

    user_input = st.text_input("Book Title:", "").strip()

    if user_input:
        exact_match_df = df[df['title'].str.lower() == user_input.lower()]
        
        if not exact_match_df.empty:
            selected_book_title = exact_match_df['title'].iloc[0]
            st.success(f"Found a perfect match: '{selected_book_title}'")
        else:
            similar_titles = df[df['title'].str.lower().str.contains(user_input.lower())]['title'].tolist()
            
            if similar_titles:
                st.info("Couldn't find an exact match. Please select from the similar titles below:")
                selected_book_title = st.selectbox("Similar Books:", [''] + similar_titles)
            else:
                st.warning("No similar titles found. Please check your spelling.")
                selected_book_title = None
    else:
        selected_book_title = None

    if st.button("Find similar books") and selected_book_title:
        with st.spinner("Searching for similar books..."):
            
            selected_book_info = df[df['title'] == selected_book_title].iloc[0]
            
            st.markdown('<div class="rainbow-border-container">', unsafe_allow_html=True)
            st.subheader("About the Book You Chose:")
            with st.expander(f"**{selected_book_info['title']}** by {', '.join(ast.literal_eval(selected_book_info['authors']))}"):
                st.write(f"**Author(s):** {', '.join(ast.literal_eval(selected_book_info['authors']))}")
                st.write(f"**Categories:** {', '.join(ast.literal_eval(selected_book_info['categories']))}")
                st.write(f"**Synopsis:** {selected_book_info['description']}")
            st.markdown('</div>', unsafe_allow_html=True)

            author_recommendations = find_books_by_author(selected_book_title, df)
            genre_recommendations = find_books_by_genre(selected_book_title, df, similarity_threshold=0.3)
            content_based_recommendations = get_content_based_recommendations(selected_book_title, cosine_sim_matrix, df)

            genre_titles = {rec['title'] for rec in genre_recommendations}
            content_titles = {rec['title'] for rec in content_based_recommendations}
            
            intersection_titles = genre_titles.intersection(content_titles)
            
            combined_recommendations = [rec for rec in content_based_recommendations if rec['title'] in intersection_titles]

            if author_recommendations or combined_recommendations:
                st.markdown('<div class="rainbow-border-container">', unsafe_allow_html=True)
                st.markdown("### You might also enjoy these books:")
                
                if author_recommendations:
                    st.subheader("✧ Based on the Same Author ✧ :")
                    for i, rec_info in enumerate(author_recommendations, 1):
                        with st.expander(f"**{rec_info['title']}**"):
                            st.write(f"**Author:** {', '.join(ast.literal_eval(rec_info['authors']))}")
                            st.write(f"**Category:** {', '.join(ast.literal_eval(rec_info['categories']))}")
                            st.write(f"**Synopsis:** {rec_info['description']}")
                
                if combined_recommendations:
                    st.subheader("✧ Based on Similar Genre and Concept ✧ :")
                    for i, rec_info in enumerate(combined_recommendations, 1):
                        with st.expander(f"**{rec_info['title']}**"):
                            st.write(f"**Author:** {', '.join(ast.literal_eval(rec_info['authors']))}")
                            st.write(f"**Category:** {', '.join(ast.literal_eval(rec_info['categories']))}")
                            st.write(f"**Synopsis:** {rec_info['description']}")
                st.markdown('</div>', unsafe_allow_html=True)
                
            else:
                st.info("Sorry, we couldn't find any recommendations for this book. Please try a different title!")