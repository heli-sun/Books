import pandas as pd
import ast
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import re

def clean_text(text):
    text = str(text).lower()
    text = re.sub(r'[^a-z0-9\s]', '', text)
    return text

def create_model_and_get_matrix(df):
    """
    Creates a TF-IDF model based on book descriptions.
    """
    df['description'] = df['description'].fillna('')
    df['description'] = df['description'].apply(clean_text)
    tfidf = TfidfVectorizer(stop_words='english', max_features=5000)
    tfidf_matrix = tfidf.fit_transform(df['description'])
    cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)
    return cosine_sim

def get_content_based_recommendations(title, cosine_sim_matrix, df, top_n=10):
    """
    Provides recommendations based on similar descriptions.
    """
    if title not in df['title'].values:
        return []
    
    idx = df[df['title'] == title].index[0]
    sim_scores = list(enumerate(cosine_sim_matrix[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[1:top_n + 1]
    book_indices = [i[0] for i in sim_scores]
    return df.iloc[book_indices].to_dict('records')

def find_books_by_author(title, df, top_n=10):
    """
    Finds books by the same author.
    """
    if title not in df['title'].values:
        return []

    selected_authors_str = df[df['title'] == title]['authors'].iloc[0]
    try:
        selected_authors = set(ast.literal_eval(selected_authors_str))
    except (ValueError, SyntaxError):
        selected_authors = set([selected_authors_str.strip()])
    
    if not selected_authors:
        return []

    similar_books = []
    for index, row in df.iterrows():
        try:
            book_authors = set(ast.literal_eval(row['authors']))
            if not selected_authors.isdisjoint(book_authors) and row['title'] != title:
                similar_books.append(row)
        except (ValueError, SyntaxError):
            continue
    # New: Convert list of Series to list of dicts
    if similar_books:
        return pd.DataFrame(similar_books).to_dict('records')
    return []


def calculate_jaccard_similarity(set1, set2):
    """
    Calculates Jaccard Similarity between two sets.
    """
    intersection = len(set1.intersection(set2))
    union = len(set1.union(set2))
    if union == 0:
        return 0
    return intersection / union

def find_books_by_genre(title, df, similarity_threshold=0.3, top_n=10):
    """
    Finds books with a high Jaccard Similarity score on genres.
    """
    if title not in df['title'].values:
        return []

    selected_genres_str = df[df['title'] == title]['categories'].iloc[0]
    try:
        selected_genres = set(ast.literal_eval(selected_genres_str))
    except (ValueError, SyntaxError):
        selected_genres = set([selected_genres_str.strip()])
    
    if not selected_genres:
        return []

    similar_books = []
    for index, row in df.iterrows():
        if row['title'] == title:
            continue
        try:
            book_genres = set(ast.literal_eval(row['categories']))
            similarity_score = calculate_jaccard_similarity(selected_genres, book_genres)
            if similarity_score >= similarity_threshold:
                similar_books.append(row)
        except (ValueError, SyntaxError):
            continue
    # New: Convert list of Series to list of dicts
    if similar_books:
        return pd.DataFrame(similar_books).to_dict('records')
    return []