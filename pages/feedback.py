"""
Feedback collection page for the chatbot
"""

import streamlit as st
import pandas as pd
import sqlite3
from datetime import datetime
from src.utils.config import get_config

st.set_page_config(page_title="Chatbot Feedback", page_icon="💬")

st.title("Provide Feedback on Industrial Chatbot")

# Connect to database
config = get_config()
db_path = config['database']['path']
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Create feedback table if it doesn't exist
cursor.execute('''
CREATE TABLE IF NOT EXISTS user_feedback (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    user_name TEXT,
    rating INTEGER,
    comment TEXT,
    suggested_improvements TEXT
)
''')
conn.commit()

# Feedback form
with st.form("feedback_form"):
    st.write("Please share your experience with our chatbot")

    user_name = st.text_input("Your Name (Optional)")

    rating = st.slider(
        "How would you rate your experience?",
        min_value=1,
        max_value=5,
        value=3,
        step=1,
        help="1 = Poor, 5 = Excellent"
    )

    comment = st.text_area(
        "What did you like or dislike about the chatbot?",
        height=100
    )

    suggested_improvements = st.text_area(
        "How can we improve the chatbot?",
        height=100
    )

    submit_button = st.form_submit_button("Submit Feedback")

    if submit_button:
        # Save feedback to database
        cursor.execute(
            'INSERT INTO user_feedback (user_name, rating, comment, suggested_improvements) VALUES (?, ?, ?, ?)',
            (user_name, rating, comment, suggested_improvements)
        )
        conn.commit()

        st.success("Thank you for your feedback! We appreciate your input.")

# Show recent feedback (for admins)
st.header("Recent Feedback")
admin_view = st.checkbox("Show admin view")

if admin_view:
    password = st.text_input("Admin Password", type="password")

    if password == "admin123":  # Simple password for demo purposes
        # Fetch recent feedback
        cursor.execute('''
        SELECT timestamp, user_name, rating, comment, suggested_improvements 
        FROM user_feedback
        ORDER BY timestamp DESC
        LIMIT 10
        ''')

        feedback_data = cursor.fetchall()

        if feedback_data:
            # Convert to DataFrame
            df = pd.DataFrame(feedback_data, columns=[
                              'Timestamp', 'User', 'Rating', 'Comment', 'Suggestions'])
            st.dataframe(df)

            # Average rating
            avg_rating = df['Rating'].mean()
            st.metric("Average Rating", f"{avg_rating:.2f} / 5")
        else:
            st.info("No feedback available yet.")
    elif password:
        st.error("Incorrect password")

# Close connection
conn.close()
