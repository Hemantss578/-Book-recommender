# Book-Recommendation-System
A book recommendation system based on a hybrid approach of both content-based and collaborative filtering.
# Book Recommender System

A personalized book recommendation web app built with **Streamlit** that suggests books based on your reading preferences, favorite authors, friends' trends, and users with similar interests. It leverages the Book-Crossing dataset to provide recommendations along with average ratings and book details.

---

## Features

- **Personalized recommendations** based on your favorite authors.
- Discover books **trending among your friends**.
- Get suggestions from users with **similar reading interests**.
- Rate books on a scale of 1 to 10 to improve recommendations.
- View detailed information and average ratings for books.
- Sidebar with user ratings and a custom logo for better UX.
- Jaccard similarity used for identifying users with common interests.

---

## Dataset

This project uses the [Book-Crossing dataset](http://www2.informatik.uni-freiburg.de/~cziegler/BX/):

- `BX-Books.csv`: Book metadata including title, author, year, publisher, and image URLs.
- `BX-Book-Ratings-Subset.csv`: Ratings of books by users on a scale from 1 to 10.
- `BX-Users.csv`: User information.

