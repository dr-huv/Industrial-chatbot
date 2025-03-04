"""
Client for Ollama local model API
"""

import requests
import json
from src.utils.config import get_config


class OllamaClient:
    def __init__(self):
        config = get_config()
        self.base_url = config['models']['ollama'].get(
            'base_url', 'http://localhost:11434')
        self.model_id = config['models']['ollama'].get(
            'model_id', 'llama3:latest')

    def generate(self, prompt, stream=False, max_tokens=1024, temperature=0.7):
        """Generate a response using Ollama API"""
        api_url = f"{self.base_url}/api/generate"

        payload = {
            "model": self.model_id,
            "prompt": prompt,
            "stream": stream,
            "options": {
                "num_predict": max_tokens,
                "temperature": temperature
            }
        }

        try:
            if stream:
                # Stream response
                response = requests.post(api_url, json=payload, stream=True)
                response.raise_for_status()

                # Return generator for streaming
                def response_generator():
                    for line in response.iter_lines():
                        if line:
                            chunk = json.loads(line)
                            yield chunk.get('response', '')
                            # Check if done
                            if chunk.get('done', False):
                                break

                return response_generator()
            else:
                # Non-streaming response
                response = requests.post(api_url, json=payload)
                response.raise_for_status()
                result = response.json()
                return result.get('response', '')

        except requests.exceptions.RequestException as e:
            return f"Error communicating with Ollama: {str(e)}"
        except json.JSONDecodeError:
            return "Error decoding response from Ollama"
        except Exception as e:
            return f"Unexpected error: {str(e)}"


# Create a singleton instance
ollama_client = OllamaClient()


def generate_response(prompt, stream=False, max_tokens=1024, temperature=0.7):
    """Generate a response using Ollama"""
    return ollama_client.generate(prompt, stream, max_tokens, temperature)
