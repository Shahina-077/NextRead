# Next Read 📚  
*A Content-Based Book Recommendation App*

## Overview
Next Read is a web-based book recommendation application that suggests similar books based on a user’s search by **book title, author, or genre**.  
The system uses textual similarity between books rather than user ratings or reviews.

This project demonstrates how classical machine learning techniques can be applied to build a simple and effective recommendation system.

---

## Features
- Search books by **title**, **author**, or **genre**
- Recommend top 5 similar books
- Content-based recommendations using book metadata
- Interactive web interface built with Streamlit
- Detailed view for each recommended book

---

## How It Works (High-Level)
1. Book information (author, genre, description) is combined into a single text representation.
2. Text data is converted into numerical vectors using **TF-IDF**.
3. **Cosine similarity** is used to measure similarity between books.
4. Based on the user’s input, the most similar books are identified and displayed.

---

## Technologies Used
- Python  
- Streamlit  
- Pandas  
- Scikit-learn (TF-IDF, Cosine Similarity)

---
## Deployment

The application is deployed using Streamlit Community Cloud and can be accessed via a public URL.

https://nextreads.streamlit.app/

