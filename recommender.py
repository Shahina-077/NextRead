import pandas as pd
import re

df = pd.read_csv("goodreads_data.csv")

# To Keep only required columns
df = df[['Book', 'Author', 'Description', 'Genres']]

# To Handle missing values
df['Description'] = df['Description'].fillna('')
df['Genres'] = df['Genres'].fillna('')
df['Author'] = df['Author'].fillna('')

# Clean Genres column
df['Genres'] = df['Genres'].str.replace('[', '', regex=False)
df['Genres'] = df['Genres'].str.replace(']', '', regex=False)
df['Genres'] = df['Genres'].str.replace("'", '', regex=False)

# Combine content features
df['content'] = (
    df['Author'] + ' ' +
    df['Genres'] + ' ' +
    df['Description']
)

# Verify
#print(df.head())
#print(df.isnull().sum())
#COSINE SIMILARITY
def normalize_text(text):
    text = str(text).lower()
    text = re.sub(r'[^a-z0-9\s]', ' ', text)
    text = re.sub(r'\s+', ' ', text)
    return text.strip()
df['Book_search'] = df['Book'].apply(normalize_text)

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# TF-IDF Vectorization
tfidf = TfidfVectorizer(stop_words='english')
tfidf_matrix = tfidf.fit_transform(df['content'])

# Compute cosine similarity
cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)

#print("TF-IDF matrix shape:", tfidf_matrix.shape)
#print("Cosine similarity matrix shape:", cosine_sim.shape)

def recommend_by_title(book_title, top_n=5):
    query = normalize_text(book_title)

    matches = df[df['Book_search'].str.contains(query, na=False)]

    if matches.empty:
        return pd.DataFrame(columns=['Book', 'Author', 'Genres'])

    idx = matches.index[0]

    similarity_scores = list(enumerate(cosine_sim[idx]))
    similarity_scores = sorted(similarity_scores, key=lambda x: x[1], reverse=True)

    similarity_scores = similarity_scores[1:top_n + 1]
    book_indices = [i[0] for i in similarity_scores]

    return df[['Book', 'Author', 'Genres']].iloc[book_indices]

def recommend_by_author(author_name, top_n=5):
    # Step 1: Get books by the same author
    author_books = df[df['Author'].str.contains(author_name, case=False)]

    # If enough books, return them
    if len(author_books) >= top_n:
        return author_books[['Book', 'Author', 'Genres']].head(top_n)

    # Step 2: Use similarity to fill remaining slots
    recommendations = author_books.copy()

    for _, row in author_books.iterrows():
        idx = row.name
        similarity_scores = list(enumerate(cosine_sim[idx]))
        similarity_scores = sorted(similarity_scores, key=lambda x: x[1], reverse=True)

        for i, _ in similarity_scores:
            book = df.iloc[i]
            if book['Book'] not in recommendations['Book'].values:
                recommendations = pd.concat(
                    [recommendations, book.to_frame().T],
                    ignore_index=True
                )
            if len(recommendations) >= top_n:
                break

        if len(recommendations) >= top_n:
            break

    return recommendations[['Book', 'Author', 'Genres']]
def recommend_by_genre(genre_name, top_n=5):
    query = normalize_text(genre_name)

    # Create a normalized genre column on the fly
    genre_series = df['Genres'].apply(normalize_text)

    matches = df[genre_series.str.contains(query, na=False)]

    if matches.empty:
        return pd.DataFrame(columns=['Book', 'Author', 'Genres'])

    return matches[['Book', 'Author', 'Genres']].head(top_n)

