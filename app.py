import streamlit as st
import pandas as pd
import random
import requests

st.set_page_config(layout="wide")

# Fetch description from Google Books API (cached)
@st.cache_data(show_spinner=False)
def fetch_description(isbn):
    url = f"https://www.googleapis.com/books/v1/volumes?q=isbn:{isbn}"
    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            data = response.json()
            items = data.get('items')
            if items:
                volume_info = items[0].get('volumeInfo', {})
                description = volume_info.get('description', 'No description found.')
                return description
    except Exception:
        pass
    return "No description available."

# Load data
@st.cache_data(show_spinner=False)
def load_data():
    df_books = pd.read_csv('data/BX-Books.csv', sep=';', encoding='latin-1')
    df_books_ratings = pd.read_csv('data/BX-Book-Ratings-Subset.csv', sep=';', encoding='latin-1')
    df_users = pd.read_csv('data/BX-Users.csv', sep=';', encoding='latin-1')
    return df_books, df_books_ratings, df_users

df_books, df_books_ratings, df_users = load_data()

# Compute average ratings
avg_ratings = df_books_ratings.groupby('ISBN')['Book-Rating'].mean().reset_index()
avg_ratings.rename(columns={'Book-Rating': 'Average-Rating'}, inplace=True)

df_books = df_books.merge(avg_ratings, on='ISBN', how='left')
df_books['Average-Rating'] = df_books['Average-Rating'].fillna(0)

# Initialize session state
if 'ISBN' not in st.session_state:
    st.session_state['ISBN'] = random.choice(df_books['ISBN'].unique())
if 'User-ID' not in st.session_state:
    st.session_state['User-ID'] = 98783
if 'Friends' not in st.session_state:
    st.session_state['Friends'] = [277427, 278026, 277523, 276680]
if 'ratings' not in st.session_state:
    st.session_state['ratings'] = {}

# Book select callback
def select_book(isbn):
    st.session_state['ISBN'] = isbn
import streamlit as st

st.sidebar.image("images/logo.jpg", width=200)
st.sidebar.write("Welcome to the Book Recommender!")

# Sidebar: Rate current book
st.sidebar.header("Rate the current book📚")
current_isbn = st.session_state['ISBN']
current_book = df_books[df_books['ISBN'] == current_isbn]
if not current_book.empty:
    title = current_book['Book-Title'].values[0]
    author = current_book['Book-Author'].values[0]
    st.sidebar.write(f"**{title}** by {author}")
    rating = st.sidebar.slider('Your Rating', 1, 10, 5, key='rating_slider')
    if st.sidebar.button('Submit Rating'):
        st.session_state['ratings'][current_isbn] = rating
        st.sidebar.success(f'You rated "{title}" with {rating} stars!')

# Sidebar: Show rated books
st.sidebar.markdown("---")
st.sidebar.subheader("Your Rated Books")
if st.session_state['ratings']:
    for isbn, rate in st.session_state['ratings'].items():
        book = df_books[df_books['ISBN'] == isbn]
        if not book.empty:
            title = book['Book-Title'].values[0]
            author = book['Book-Author'].values[0]
            st.sidebar.write(f"**{title}** by {author} — ⭐ {rate}")
else:
    st.sidebar.write("No books rated yet.")

# Main view: Selected book info
df_book = df_books[df_books['ISBN'] == current_isbn].iloc[0]
cover, info = st.columns([2, 3])
with cover:
    st.image(df_book['Image-URL-L'])
with info:
    st.title(df_book['Book-Title'])
    st.markdown(df_book['Book-Author'])
    st.caption(f"{df_book['Year-Of-Publication']} | {df_book['Publisher']}")
    st.markdown(f"**Average Rating:** {df_book['Average-Rating']:.1f} / 10")
    # Show description for selected book
    description = fetch_description(current_isbn)
    st.markdown("**Description:**")
    st.write(description)

# Recommendation helper function
def recommendations(df, title="Top Recommended Books"):
    if df.empty:
        st.info("No recommendations available.")
        return

    st.markdown(f"### {title}")
    for i, row in df.iterrows():
        with st.container():
            col1, col2 = st.columns([1, 4])
            with col1:
                st.image(row['Image-URL-M'], width=100)
            with col2:
                st.markdown(f"**{row['Book-Title']}**")
                st.markdown(f"*by {row['Book-Author']}*")
                st.caption(f"📅 {row['Year-Of-Publication']} | 🏢 {row['Publisher']}")
                st.markdown(f"**Average Rating:** {row['Average-Rating']:.1f} / 10")
                # Fetch and show description dynamically for recommended books
                desc = fetch_description(row['ISBN'])
                st.markdown(desc)
                st.button("📖 View Details", key=row['ISBN'], on_click=select_book, args=(row['ISBN'],))
            st.markdown("---")

# Sidebar cache for ISBN groups (for recommendations by similarity)
@st.cache_data(show_spinner=False)
def get_isbn_groups(df_ratings):
    return df_ratings.groupby('ISBN')['User-ID'].apply(list).to_dict()

dict_isbn_groups = get_isbn_groups(df_books_ratings)

# Simple Jaccard similarity
def jaccard_distance(list_a, list_b):
    set_a, set_b = set(list_a), set(list_b)
    intersection = set_a.intersection(set_b)
    union = set_a.union(set_b)
    if not union:
        return 0
    return len(intersection) / len(union)

# Recommendations by favorite authors
st.subheader('Keep digging your favorite authors')
userid = st.session_state['User-ID']
user_books = df_books_ratings[df_books_ratings['User-ID'] == userid]
if not user_books.empty:
    user_books = user_books.merge(df_books, on='ISBN')
    authors = user_books['Book-Author'].unique()
    read_titles = user_books['Book-Title']
    recs = df_books[df_books['Book-Author'].isin(authors) & ~df_books['Book-Title'].isin(read_titles)]
    if not recs.empty:
        recommendations(recs.sample(min(10, len(recs))))

# Recommendations trending among friends
st.subheader('Trending among your friends')
friends = st.session_state['Friends']
friends_ratings = df_books_ratings[df_books_ratings['User-ID'].isin(friends)]
friends_books = friends_ratings.merge(df_books, on='ISBN').drop_duplicates(subset=['Book-Title'])
if not friends_books.empty:
    recommendations(friends_books.sample(min(10, len(friends_books))))

# Recommendations from people with similar interests
st.subheader(f'People with common interests read similar to "{df_book["Book-Title"]}"')
if current_isbn not in dict_isbn_groups:
    st.write("No rating data for this book to find common interest.")
else:
    base_users = dict_isbn_groups[current_isbn]
    similarity_scores = []
    for other_isbn, users in dict_isbn_groups.items():
        if other_isbn == current_isbn:
            continue
        score = jaccard_distance(base_users, users)
        if 0 < score < 0.8:
            similarity_scores.append((other_isbn, score))
    similarity_scores.sort(key=lambda x: x[1], reverse=True)
    top_similar_isbns = [x[0] for x in similarity_scores[:10]]
    similar_books = df_books[df_books['ISBN'].isin(top_similar_isbns)]
    if not similar_books.empty:
        recommendations(similar_books)

# About us
st.subheader('About us')
st.write(
    'BookCrossing is an online platform that allows users to share and read books by connecting with others.\n'
    'Recommendations are personalized based on your favorite authors, your BookCrossing friends, and others with shared interests.\n'
    'Rate books to improve your suggestions and explore more titles you might enjoy!'
)
