"""
Configuration management utilities
"""

import os
import yaml

# Global config cache
_config = None


def get_config():
    """
    Get configuration from YAML file
    Returns a dict with configuration values
    """
    global _config

    # Return cached config if available
    if _config is not None:
        return _config

    # Default config location
    config_path = os.environ.get('CHATBOT_CONFIG', 'chatbot_config.yaml')

    # Load configuration
    try:
        with open(config_path, 'r') as f:
            _config = yaml.safe_load(f)
    except Exception as e:
        # Use default configuration if file can't be loaded
        _config = {
            'name': 'Industrial NLP Chatbot',
            'version': '1.0.0',
            'models': {
                'default': 'groq',
                'groq': {
                    'model_id': 'llama3-8b-8192'
                },
                'ollama': {
                    'model_id': 'llama3:latest',
                    'base_url': 'http://localhost:11434'
                }
            },
            'database': {
                'type': 'sqlite',
                'path': 'data/industrial_knowledge.db'
            },
            'nlp': {
                'sentence_transformer': 'all-MiniLM-L6-v2',
                'max_tokens': 1024,
                'temperature': 0.5
            }
        }
        print(
            f"Warning: Couldn't load config file, using defaults. Error: {e}")

    return _config


def get_active_model():
    """Get the currently active model configuration"""
    config = get_config()
    default_model = config['models'].get('default', 'groq')
    return config['models'].get(default_model, {})


def get_api_key():
    config = get_config()
    return config['models']['groq'].get('api_key')
