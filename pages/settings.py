"""
Settings page for the chatbot
"""

import streamlit as st
import yaml
import os
from src.utils.config import get_config

st.set_page_config(page_title="Chatbot Settings", page_icon="⚙️")

st.title("Chatbot Settings")

# Load current configuration
config = get_config()

# Create tabs for different settings categories
tab1, tab2, tab3 = st.tabs(
    ["Model Settings", "Database Settings", "NLP Settings"])

with tab1:
    st.header("Model Configuration")

    # Model selection
    model_type = st.selectbox(
        "Select Model Provider",
        ["groq", "ollama"],
        index=0 if config['models']['default'] == 'groq' else 1
    )

    # Show relevant settings based on selected model
    if model_type == "groq":
        st.subheader("Groq Settings")
        groq_model = st.selectbox(
            "Groq Model",
            ["llama3-8b-8192", "llama3-70b-8192", "mixtral-8x7b-32768"],
            index=0 if config['models']['groq']['model_id'] == "llama3-8b-8192" else
            1 if config['models']['groq']['model_id'] == "llama3-70b-8192" else 2
        )

        groq_api_key = st.text_input(
            "Groq API Key (leave empty to use environment variable)",
            type="password"
        )
    else:
        st.subheader("Ollama Settings")
        ollama_model = st.text_input(
            "Ollama Model",
            value=config['models']['ollama'].get('model_id', 'llama3:latest')
        )

        ollama_url = st.text_input(
            "Ollama API URL",
            value=config['models']['ollama'].get(
                'base_url', 'http://localhost:11434')
        )

    # Common model settings
    st.subheader("General Model Settings")

    temperature = st.slider(
        "Temperature (Randomness)",
        min_value=0.0,
        max_value=1.0,
        value=config['nlp'].get('temperature', 0.5),
        step=0.1
    )

    max_tokens = st.slider(
        "Max Response Tokens",
        min_value=100,
        max_value=4000,
        value=config['nlp'].get('max_tokens', 1024),
        step=100
    )

with tab2:
    st.header("Database Settings")

    db_type = st.selectbox(
        "Database Type",
        ["sqlite", "mysql", "postgresql"],
        index=0  # Default to sqlite
    )

    if db_type == "sqlite":
        db_path = st.text_input(
            "Database File Path",
            value=config['database'].get(
                'path', 'data/industrial_knowledge.db')
        )
    else:
        st.warning(f"{db_type} integration not yet implemented")

        db_host = st.text_input("Database Host", "localhost")
        db_port = st.number_input("Database Port", min_value=1,
                                  max_value=65535, value=3306 if db_type == "mysql" else 5432)
        db_name = st.text_input("Database Name", "industrial_chatbot")
        db_user = st.text_input("Database Username")
        db_password = st.text_input("Database Password", type="password")

with tab3:
    st.header("NLP Settings")

    embedding_model = st.selectbox(
        "Embedding Model",
        ["all-MiniLM-L6-v2", "all-mpnet-base-v2",
            "paraphrase-multilingual-MiniLM-L12-v2"],
        index=0 if config['nlp'].get('sentence_transformer', 'all-MiniLM-L6-v2') == "all-MiniLM-L6-v2" else
        1 if config['nlp'].get(
            'sentence_transformer') == "all-mpnet-base-v2" else 2
    )

    top_k = st.slider(
        "Number of Knowledge Base Matches (Top-K)",
        min_value=1,
        max_value=10,
        value=3,
        step=1
    )

    similarity_threshold = st.slider(
        "Minimum Similarity Threshold",
        min_value=0.0,
        max_value=1.0,
        value=0.5,
        step=0.05
    )

# Save button
if st.button("Save Settings"):
    # Update config dictionary with new values
    updated_config = config.copy()

    # Update model settings
    updated_config['models']['default'] = model_type

    if model_type == "groq":
        updated_config['models']['groq']['model_id'] = groq_model
        # Only update API key if provided
        if groq_api_key:
            os.environ["GROQ_API_KEY"] = groq_api_key
    else:
        updated_config['models']['ollama']['model_id'] = ollama_model
        updated_config['models']['ollama']['base_url'] = ollama_url

    # Update NLP settings
    updated_config['nlp']['temperature'] = temperature
    updated_config['nlp']['max_tokens'] = max_tokens
    updated_config['nlp']['sentence_transformer'] = embedding_model
    updated_config['nlp']['top_k'] = top_k
    updated_config['nlp']['similarity_threshold'] = similarity_threshold

    # Update database settings
    updated_config['database']['type'] = db_type
    if db_type == "sqlite":
        updated_config['database']['path'] = db_path
    else:
        updated_config['database']['host'] = db_host
        updated_config['database']['port'] = db_port
        updated_config['database']['name'] = db_name
        updated_config['database']['user'] = db_user
        # Only update password if provided
        if db_password:
            # Don't store actual password in file
            updated_config['database']['password'] = "********"

    # Save updated config to file
    try:
        with open('chatbot_config.yaml', 'w') as f:
            yaml.dump(updated_config, f, default_flow_style=False)
        st.success("Settings saved successfully!")
    except Exception as e:
        st.error(f"Error saving settings: {str(e)}")
