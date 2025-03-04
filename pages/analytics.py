"""
Analytics dashboard for chatbot performance
"""

import streamlit as st
import pandas as pd
import sqlite3
import altair as alt
from datetime import datetime, timedelta
from src.utils.config import get_config

st.set_page_config(page_title="Chatbot Analytics",
                   page_icon="📊", layout="wide")

st.title("Industrial Chatbot Analytics")

# Connect to database
config = get_config()
db_path = config['database']['path']
conn = sqlite3.connect(db_path)

# Date range selector
st.sidebar.header("Filter Options")
date_range = st.sidebar.selectbox(
    "Select Date Range",
    ["Today", "Last 7 days", "Last 30 days", "All time"]
)

# Get current date
today = datetime.now().date()

# Set start date based on selection
if date_range == "Today":
    start_date = today
elif date_range == "Last 7 days":
    start_date = today - timedelta(days=7)
elif date_range == "Last 30 days":
    start_date = today - timedelta(days=30)
else:  # All time
    start_date = datetime(2000, 1, 1).date()

# Query interactions table
query = f"""
SELECT 
    DATE(timestamp) as date,
    COUNT(*) as interaction_count,
    AVG(LENGTH(query)) as avg_query_length,
    COUNT(CASE WHEN feedback = 'positive' THEN 1 END) as positive_feedback,
    COUNT(CASE WHEN feedback = 'negative' THEN 1 END) as negative_feedback
FROM 
    interactions
WHERE 
    DATE(timestamp) >= '{start_date}'
GROUP BY 
    DATE(timestamp)
ORDER BY 
    date
"""

df = pd.read_sql_query(query, conn)

# Check if we have data
if df.empty:
    st.info("No data available for the selected time period.")
else:
    # Create three columns
    col1, col2 = st.columns(2)

    # Create first chart - Interactions over time
    interactions_chart = alt.Chart(df).mark_line(point=True).encode(
        x='date:T',
        y='interaction_count:Q',
        tooltip=['date', 'interaction_count']
    ).properties(
        title="Interactions Over Time",
        width=400
    )

    col1.altair_chart(interactions_chart, use_container_width=True)

    # Create second chart - Feedback distribution
    if 'positive_feedback' in df.columns and 'negative_feedback' in df.columns:
        # Prepare data for feedback chart
        feedback_data = pd.DataFrame({
            'type': ['Positive', 'Negative'],
            'count': [df['positive_feedback'].sum(), df['negative_feedback'].sum()]
        })

        feedback_chart = alt.Chart(feedback_data).mark_bar().encode(
            x='type:N',
            y='count:Q',
            color='type:N',
            tooltip=['type', 'count']
        ).properties(
            title="Feedback Distribution",
            width=400
        )

        col2.altair_chart(feedback_chart, use_container_width=True)

    # Top queries section
    st.header("Top Queries")

    top_queries_query = f"""
    SELECT 
        query, 
        COUNT(*) as count
    FROM 
        interactions
    WHERE 
        DATE(timestamp) >= '{start_date}'
    GROUP BY 
        query
    ORDER BY 
        count DESC
    LIMIT 10
    """

    top_queries_df = pd.read_sql_query(top_queries_query, conn)

    if not top_queries_df.empty:
        st.table(top_queries_df)
    else:
        st.info("No queries available for the selected time period.")

# Close connection
conn.close()
