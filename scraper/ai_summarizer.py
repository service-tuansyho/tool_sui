import logging
import requests
from config import GOOGLE_API_KEY, GOOGLE_AI_MODEL, OLLAMA_URL, OLLAMA_MODEL

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AISummarizer:
    def __init__(self):
        if OLLAMA_MODEL:
            self.provider = 'ollama'
            self.url = OLLAMA_URL.rstrip('/')
            self.model = OLLAMA_MODEL
            self.endpoint = f'{self.url}/api/generate'
            logger.info(f'Using Ollama local model {self.model} at {self.endpoint}')
        elif GOOGLE_API_KEY:
            self.provider = 'google'
            self.api_key = GOOGLE_API_KEY
            self.model = GOOGLE_AI_MODEL
            self.endpoint = f'https://generativelanguage.googleapis.com/v1beta/models/{self.model}:generateContent'
            logger.info(f'Using Google AI model {self.model}')
        else:
            raise ValueError(
                'Please define OLLAMA_MODEL (for local Ollama) or GOOGLE_API_KEY in your .env file'
            )

    def rewrite_text(self, text, max_output_tokens=1200):
        system_instruction = (
            "You are a professional content editor who rewrites internet discussions into natural, engaging English articles. "
            "Focus on creating human-written, fluent content that feels authentic and readable."
        )

        user_prompt = f"""
Rewrite and expand the Reddit post below into a complete article.

You may:
- elaborate on the ideas
- add useful context
- improve explanations
- add smooth transitions
- expand short points naturally

Do not invent fake facts or statistics.

Write approximately 250-350 words.

Reddit post:
{text}
"""

        if self.provider == 'ollama':
            return self._rewrite_with_ollama(system_instruction, user_prompt, max_output_tokens)

        return self._rewrite_with_google(system_instruction, user_prompt, max_output_tokens)

    def _rewrite_with_ollama(self, system_instruction, user_prompt, max_output_tokens):
        full_prompt = f"{system_instruction}\n\n{user_prompt}"
        payload = {
            'model': self.model,
            'prompt': full_prompt,
            'temperature': 0.2,
            'max_tokens': max_output_tokens,
            'top_p': 0.95,
            'stream': False,
        }

        response = requests.post(self.endpoint, json=payload, timeout=300)
        if response.status_code != 200:
            logger.error(f'Ollama request failed: {response.status_code} {response.text}')
            response.raise_for_status()

        result = response.json()
        text_part = result.get('response', '').strip()
        return self._clean_response_text(text_part)

    def _rewrite_with_google(self, system_instruction, user_prompt, max_output_tokens):
        payload = {
            'systemInstruction': {
                'parts': [{
                    'text': system_instruction
                }]
            },
            'contents': [{
                'parts': [{
                    'text': user_prompt
                }],
                'role': 'user'
            }],
            'generationConfig': {
                'temperature': 0.2,
                'maxOutputTokens': max_output_tokens,
                'topK': 40,
                'topP': 0.95,
                'responseMimeType': 'text/plain'
            }
        }

        response = requests.post(
            self.endpoint,
            params={'key': self.api_key},
            json=payload,
            timeout=30
        )

        if response.status_code != 200:
            logger.error(f'Google AI request failed: {response.status_code} {response.text}')
            response.raise_for_status()

        result = response.json()
        candidates = result.get('candidates', [])
        if candidates:
            content = candidates[0].get('content', {})
            parts = content.get('parts', [])
            if parts:
                text_part = parts[0].get('text', '').strip()
                if 'thoughtSignature' in parts[0]:
                    lines = text_part.split('\n')
                    filtered_lines = [line for line in lines if not (line.startswith('Eq') and len(line) > 50)]
                    text_part = '\n'.join(filtered_lines).strip()
                return self._clean_response_text(text_part)

        return ''

    def _clean_response_text(self, text_part):
        if len(text_part) > 10:
            logger.info(f'Final rewrite: {text_part[:200]}')
            return text_part
        return ''
