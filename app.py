"""
Industrial NLP Chatbot - Main Application
"""

import streamlit as st
import os
import time
from src.nlp.preprocessor import preprocess_query
from src.nlp.semantic_search import find_best_match
from src.nlp.entity_extractor import extract_entities_from_query
from src.nlp.sentiment import analyze_query_sentiment
from src.database.query import get_knowledge_base, log_interaction
from src.prompts.templates import create_enhanced_prompt
from src.feedback.evaluator import evaluate_response
from src.utils.config import get_config
from src.utils.helpers import get_random_greeting

# Determine which model client to use based on configuration
config = get_config()
model_type = config['models'].get('default', 'groq')

if model_type == 'groq':
    from src.models.groq_client import generate_response
else:
    from src.models.ollama_client import generate_response

# Page configuration
st.set_page_config(
    page_title="Industrial Support Chatbot",
    page_icon="🏭",
    layout="centered"
)

# Custom CSS
st.markdown("""
<style>
    .chat-message {
        padding: 1.5rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
        display: flex;
        flex-direction: row;
        align-items: flex-start;
    }
    .chat-message.user {
        background-color: #F0F2F6;
    }
    .chat-message.assistant {
        background-color: #E1F5FE;
    }
    .chat-message .avatar {
        width: 40px;
        min-width: 40px;
        margin-right: 1rem;
    }
    .chat-message .avatar img {
        max-width: 100%;
        max-height: 40px;
        border-radius: 50%;
    }
    .chat-message .message {
        flex-grow: 1;
    }
</style>
""", unsafe_allow_html=True)

# Sidebar with information
with st.sidebar:
    st.title("Industrial Support Chatbot")
    st.markdown(
        "An NLP-powered chatbot for industrial support using advanced language processing techniques.")

    st.subheader("Current Configuration")
    st.info(f"Model: {model_type.capitalize()}")

    if model_type == 'groq':
        st.info(
            f"Model ID: {config['models']['groq'].get('model_id', 'llama3-8b-8192')}")
    else:
        st.info(
            f"Model ID: {config['models']['ollama'].get('model_id', 'llama3:latest')}")

    st.subheader("About")
    st.markdown("""
    This chatbot handles customer complaints and FAQs using:
    - Semantic search for knowledge base retrieval
    - Dynamic prompt engineering
    - Self-rewarding response improvement
    """)

    # Quick navigation to other pages
    st.subheader("Navigation")
    st.page_link("pages/analytics.py", label="Analytics Dashboard", icon="📊")
    st.page_link("pages/settings.py", label="Settings", icon="⚙️")
    st.page_link("pages/feedback.py", label="Provide Feedback", icon="💬")

# Initialize session state for chat history if it doesn't exist
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": get_random_greeting()}
    ]

# Display chat header
st.title("SmartHaven Support")

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Load knowledge base
knowledge_base = get_knowledge_base()

# Function to process the query and generate a response


def process_and_respond(query):
    # Show a spinner while processing
    with st.spinner("Processing your query..."):
        # Step 1: Preprocess the query
        preprocessed_query = preprocess_query(query)

        # Step 2: Extract entities and analyze sentiment
        entities = extract_entities_from_query(query, knowledge_base)
        sentiment = analyze_query_sentiment(query)

        # Step 3: Find best matches in knowledge base
        matches = find_best_match(query, knowledge_base)

        # Step 4: Create enhanced prompt with dynamic prompt engineering
        enhanced_prompt = create_enhanced_prompt(query, matches)

        # Step 5: Generate response using LLM
        response = generate_response(enhanced_prompt)

        # Step 6: Evaluate and improve response
        final_response = evaluate_response(query, response)

        # Log the interaction
        log_interaction(query, final_response)

        return final_response


# Get user input
if prompt := st.chat_input("Ask about your industrial equipment..."):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Display user message
    with st.chat_message("user"):
        st.markdown(prompt)

    # Display assistant response with a spinner for processing time
    with st.chat_message("assistant"):
        response = process_and_respond(prompt)
        st.markdown(response)

    # Add assistant response to chat history
    st.session_state.messages.append(
        {"role": "assistant", "content": response})

# Add a footer
st.markdown("---")
st.caption("Powered by Advanced NLP Research • © 2024 SmartHaven Industries")
