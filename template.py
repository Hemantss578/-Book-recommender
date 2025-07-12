import streamlit as st

# Set selected book in session
def select_book(isbn):
    st.session_state['ISBN'] = isbn

def select_user(userid):
    st.session_state['User-ID'] = userid

def add_friend(friends_list):
    st.session_state['Friends'] = friends_list

# Tile view for recommendations (grid layout)
def tile_item(column, item):
    with column:
        # Book cover image
        st.image(item['Image-URL-M'], use_container_width=True)

        # Book title and rating
        st.caption(item['Book-Title'])

        # Show average rating (scale of 1-10)
        avg_rating = item.get('Average-Rating', 0)
        if avg_rating > 0:
            st.write(f"⭐ Average Rating: {avg_rating:.1f} / 10")
        else:
            st.write("⚠️ No ratings yet")

        # Select button
        if st.button(label="Select", key=f"{item['ISBN']}"):
            st.session_state['ISBN'] = item['ISBN']

# List-style recommendations with details
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
                avg_rating = row.get('Average-Rating', 0)
                if avg_rating > 0:
                    st.caption(f"⭐ Average Rating: {avg_rating:.1f} / 10")
                else:
                    st.caption("No ratings yet")
            st.markdown("---")


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

                # Show average rating if available
                avg_rating = row.get('Average-Rating', 0)
                if avg_rating > 0:
                    st.markdown(f"⭐ **Average Rating:** {avg_rating:.1f} / 10")
                else:
                    st.markdown("⚠️ No rating available.")

                st.button("📖 View Details", key=row['ISBN'], on_click=select_book, args=(row['ISBN'],))
            st.markdown("---")

# Sidebar feedback
def wrong_credentials():
    st.sidebar.error('❌ Wrong User-ID. Please try again.')

def welcome_user():
    st.sidebar.success('🎉 Welcome to BookCrossing!')
    st.sidebar.info('📚 Start reading books to get personalized recommendations.')

def already_added():
    st.sidebar.warning('👥 User is already on your friend list.')

def friend_not_found():
    st.sidebar.error("🚫 We couldn't find your friend.")
    st.sidebar.info('Please insert a valid **User-ID**.')
