import os
import groq
from src.utils.config import get_api_key

# Initialize Groq client
api_key = get_api_key()
client = groq.Groq(api_key=api_key)
model_id = "llama3-8b-8192"  # Default model


def generate_response(prompt, stream=False):
    """Generate a response using Groq API"""
    try:
        # Format messages for chat completion
        messages = [
            {"role": "system", "content": "You are an industrial support assistant."},
            {"role": "user", "content": prompt}
        ]

        # Call Groq API
        chat_completion = client.chat.completions.create(
            messages=messages,
            model=model_id,
            temperature=0.5,
            max_tokens=1024,
            stream=stream
        )

        # Handle streaming or non-streaming response
        if stream:
            return chat_completion  # Return the stream object
        else:
            return chat_completion.choices[0].message.content

    except Exception as e:
        return f"Error generating response: {str(e)}"
