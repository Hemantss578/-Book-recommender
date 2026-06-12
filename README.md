📚 Hybrid Book Recommendation System
An interactive, data-driven Streamlit web application that delivers highly personalized literature suggestions using a hybrid recommendation engine.

📖 Overview
As the volume of published literature grows, finding the right book becomes increasingly challenging. This project aims to solve the "what to read next" problem by deploying a hybrid recommendation system that synthesizes both content-based and collaborative filtering methodologies.

Built entirely in Python and hosted via Streamlit, the application analyzes user profiles, explicit ratings, and reading histories to curate a highly accurate, personalized feed of book recommendations. By calculating user similarities and tracking network trends, the app mimics the organic way readers discover books—through trusted authors, friend networks, and communities with shared tastes.

✨ Core Features
Hybrid Recommendation Engine: Seamlessly integrates collaborative and content-based filtering to overcome the "cold start" problem and provide diverse, accurate suggestions.

Algorithmic User Matching: Utilizes Jaccard Similarity to mathematically identify users with overlapping reading preferences, serving recommendations based on the highest-rated books within those matched clusters.

Author-Centric Content Filtering: Generates tailored reading lists based on a user's explicitly stated favorite authors.

Social & Network Discovery: Aggregates and surfaces trending books within a user's immediate friend network.

Interactive Feedback Loop: Features a built-in 1-to-10 rating mechanism allowing users to evaluate books in real-time. This data is fed back into the algorithm to continuously refine and optimize future suggestions.

Rich UI/UX: A streamlined Streamlit interface featuring an intuitive navigation sidebar, custom branding, and comprehensive book metadata (including cover images, publication details, and global average ratings).

🧠 Methodology
The system's hybrid approach ensures a robust recommendation pipeline:

Collaborative Filtering: Identifies behavioral patterns across the user base. If User A and User B have a high Jaccard similarity score based on their reading history, the system will recommend User A's highly rated books to User B.

Content-Based Filtering: Analyzes item metadata (authors, publishers, publication year) to recommend books similar to those the user has already engaged with.

📊 Dataset Architecture
This model is trained and evaluated on the widely recognized Book-Crossing Dataset, structured into three relational files:

BX-Books.csv: The metadata repository containing Title, Author, Publication Year, Publisher, and Cover Image URLs.

BX-Users.csv: Anonymized demographic data for the user base.

BX-Book-Ratings-Subset.csv: The explicit interaction matrix, containing user-submitted ratings scaled from 1 to 10.

🛠️ Tech Stack
Language: Python 3.x

Frontend/Framework: Streamlit

Data Manipulation: Pandas, NumPy

Algorithms: Custom Jaccard Similarity implementation

🚀 Getting Started
To run this project locally, follow these steps:

1. Clone the repository

Bash
git clone https://github.com/yourusername/Book-Recommendation-System-Streanlit.git
cd Book-Recommendation-System-Streanlit
2. Install dependencies
Ensure you have Python installed, then run:

Bash
pip install -r requirements.txt
3. Run the application
streamlit run app.py
4. Access the web app
Open your browser and navigate to `
