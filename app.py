import streamlit as st
import pandas as pd

from recommender import (
    df,
    recommend_by_title,
    recommend_by_author,
    recommend_by_genre
)

# --------------------------------------------------
# Streamlit config (MUST be first Streamlit command)
# --------------------------------------------------
st.set_page_config(page_title="Discover books that match your favourite reads 📚")

# --------------------------------------------------
# Session state initialization
# --------------------------------------------------
if "selected_book" not in st.session_state:
    st.session_state.selected_book = None

if "results" not in st.session_state:
    st.session_state.results = None

# --------------------------------------------------
# DETAIL PAGE (runs first if a book is selected)
# --------------------------------------------------
if st.session_state.selected_book is not None:
    book = df[df['Book'] == st.session_state.selected_book].iloc[0]

    st.markdown(
        """
        <style>
        .detail-box {
            max-width: 600px;
            margin: auto;
            padding: 25px;
            border-radius: 10px;
            background-color: #f9f9f9;
            box-shadow: 0 4px 10px rgba(0,0,0,0.1);
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
    f"""
    <style>
    .detail-box {{
        max-width: 600px;
        margin: auto;
        padding: 25px;
        border-radius: 10px;
        background-color: #f9f9f9;
        box-shadow: 0 4px 10px rgba(0,0,0,0.1);
    }}
    </style>

    <div class="detail-box">
        <h2>{book['Book']}</h2>
        <p><strong>Author:</strong> {book['Author']}</p>
        <p><strong>Genre:</strong> {book['Genres']}</p>
        <h3>Description</h3>
        <p>{book['Description']}</p>
    </div>
    """,
    unsafe_allow_html=True
)

    st.write("")
    if st.button("⬅ Back to recommendations"):
        st.session_state.selected_book = None
        st.rerun()

    st.stop()

# --------------------------------------------------
# MAIN SEARCH PAGE
# --------------------------------------------------
st.title("Discover books that match your favourite reads 📚")

search_type = st.selectbox(
    "Search by",
    ["Book Title", "Author", "Genre"]
)

query = st.text_input("Enter book title, author, or genre")

# --------------------------------------------------
# SEARCH ACTION (store results in session_state)
# --------------------------------------------------
if st.button("Get Recommendations"):

    if query.strip() == "":
        st.warning("Please enter a valid input.")

    else:
        if search_type == "Book Title":
            st.session_state.results = recommend_by_title(query)

        elif search_type == "Author":
            st.session_state.results = recommend_by_author(query)

        else:
            st.session_state.results = recommend_by_genre(query)

# --------------------------------------------------
# DISPLAY RESULTS (independent of button click)
# --------------------------------------------------
if st.session_state.results is not None:

    if st.session_state.results.empty:
        st.error("No recommendations found.")

    else:
        st.subheader("Recommended Books")

        cols = st.columns(2)

        for i, (_, row) in enumerate(st.session_state.results.iterrows()):
            with cols[i % 2]:

                if st.button(row['Book'], key=f"book_{i}_{row['Book']}"):
                    st.session_state.selected_book = row['Book']
                    st.rerun()

                st.write(f"Author: {row['Author']}")
                st.write(f"Genre: {row['Genres']}")
                st.markdown("---")
