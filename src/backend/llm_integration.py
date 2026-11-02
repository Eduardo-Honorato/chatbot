"""LLM Integration module for Chatbot with free tier providers."""

import os
import logging

logger = logging.getLogger(__name__)


class LLMProvider:
    """Enum-like class for LLM providers."""
    OPENAI = "openai"
    ANTHROPIC = "anthropic"
    GEMINI = "gemini"


class LLMIntegration:
    """Handles integration with different LLM providers using free tier accounts."""

    def __init__(self):
        self.providers = {
            LLMProvider.OPENAI: {
                'model': os.environ.get('OPENAI_MODEL', 'gpt-3.5-turbo'),
                'api_key': os.environ.get('OPENAI_API_KEY'),
                'client': None,
            },
            LLMProvider.ANTHROPIC = {
                'model': os.environ.get('ANTHROPIC_MODEL', 'claude-instant-1.2'),
                'api_key': os.environ.get('ANTHROPIC_API_KEY'),
                'client': None,
            },
            LLMProvider.GEMINI = {
                'model': os.environ.get('GEMINI_MODEL', 'gemini-pro'),
                'api_key': os.environ.get('GEMINI_API_KEY'),
                'client': None,
            },
        }
        self._initialize_clients()

    def _initialize_clients(self):
        """Initialize API clients for enabled providers."""
        for provider, config in self.providers.items():
            if config['api_key'] and config['api_key'].startswith('sk-') or config['api_key'].startswith('an-') or config['api_key'].startswith('g-'):
                try:
                    if provider == LLMProvider.OPENAI:
                        import openai
                        config['client'] = openai.OpenAI(api_key=config['api_key'])
                        logger.info(f"OpenAI client initialized with model: {config['model']}")
                    elif provider == LLMProvider.ANTHROPIC:
                        import anthropic
                        config['client'] = anthropic.Anthropic(api_key=config['api_key'])
                        logger.info(f"Anthropic client initialized with model: {config['model']}")
                    elif provider == LLMProvider.GEMINI:
                        from google.generativeai import configure, GenerativeModel
                        configure(api_key=config['api_key'])
                        config['model_obj'] = GenerativeModel(config['model'])
                        logger.info(f"Gemini client initialized with model: {config['model']}")
                except ImportError as e:
                    logger.warning(f"Could not import {provider} client: {e}")
                except Exception as e:
                    logger.warning(f"Error initializing {provider} client: {e}")

    def get_response(self, messages, provider=None):
        """
        Get a response from the specified LLM provider.

        Args:
            messages: List of message dicts with 'role' and 'content' keys
            provider: Provider name (openai, anthropic, gemini). If None, tries enabled providers in order.

        Returns:
            String containing the LLM response, or None if all providers fail
        """
        # Determine which provider to use
        if provider is None:
            # Try providers that have clients initialized
            for provider_name in [LLMProvider.OPENAI, LLMProvider.ANTHROPIC, LLMProvider.GEMINI]:
                config = self.providers[provider_name]
                if config['client'] is not None:
                    provider = provider_name
                    break
            else:
                # Fallback to first provider even if client not initialized
                provider = LLMProvider.OPENAI

        # Get the provider config
        config = self.providers.get(provider)
        if not config or config['client'] is None:
            logger.error(f"No configured client for provider: {provider}")
            return f"Desculpe, o provedor {provider} não está configurado. Verifique as API keys."

        try:
            if provider == LLMProvider.OPENAI:
                return self._get_openai_response(messages, config)
            elif provider == LLMProvider.ANTHROPIC:
                return self._get_anthropic_response(messages, config)
            elif provider == LLMProvider.GEMINI:
                return self._get_gemini_response(messages, config)
            else:
                return f"Provedor {provider} não suportado."

        except Exception as e:
            logger.error(f"Error getting LLM response from {provider}: {e}")
            # Try fallback to next provider
            return self._fallback_response(messages, provider, str(e))

    def _get_openai_response(self, messages, config):
        """Get response from OpenAI provider."""
        import openai
        try:
            response = config['client'].chat.completions.create(
                model=config['model'],
                messages=messages,
                temperature=0.7,
                max_tokens=1000
            )
            return response.choices[0].message.content
        except Exception as e:
            logger.error(f"OpenAI error: {e}")
            raise

    def _get_anthropic_response(self, messages, config):
        """Get response from Anthropic provider."""
        import anthropic
        try:
            # Anthropic uses a different message format
            anthropic_messages = []
            for msg in messages:
                if msg['role'] == 'user':
                    anthropic_messages.append({'role': 'user', 'content': msg['content']})
                elif msg['role'] == 'assistant':
                    anthropic_messages.append({'role': 'assistant', 'content': msg['content']})
                else:
                    anthropic_messages.append({'role': msg['role'], 'content': msg['content']})

            response = config['client'].messages.create(
                model=config['model'],
                messages=anthropic_messages,
                max_tokens=1000,
                temperature=0.7
            )
            # Extract text from Anthropic response
            if response.content:
                return response.content[0].text
            return str(response)
        except Exception as e:
            logger.error(f"Anthropic error: {e}")
            raise

    def _get_gemini_response(self, messages, config):
        """Get response from Google Gemini provider."""
        from google.generativeai import GenerativeModel
        try:
            model = config.get('model_obj') or GenerativeModel(config['model'])
            # Gemini expects a different input format
            prompt = '\n'.join([f"{msg['role']}: {msg['content']}" for msg in messages])
            response = model.generate_content(prompt)
            return response.text
        except Exception as e:
            logger.error(f"Gemini error: {e}")
            raise

    def _fallback_response(self, messages, failed_provider, error_msg):
        """Try fallback to another provider."""
        provider_order = [LLMProvider.OPENAI, LLMProvider.ANTHROPIC, LLMProvider.GEMINI]
        current_index = provider_order.index(failed_provider) if failed_provider in provider_order else 0

        for i in range(current_index + 1, len(provider_order)):
            next_provider = provider_order[i]
            config = self.providers[next_provider]
            if config['client'] is not None:
                try:
                    logger.info(f"Falling back to provider: {next_provider}")
                    return self.get_response(messages, next_provider)
                except Exception as e:
                    logger.warning(f"Fallback to {next_provider} also failed: {e}")
                    continue

        # If no fallback works, return error message
        return (f"Desculpe, todos os provedores de LLM estão indisponíveis no momento. "
                f"Erro no {failed_provider}: {error_msg}. "
                "Por favor, verifique suas API keys e tente novamente later.")


# Convenience function for quick use
def get_llm_response(messages, provider=None):
    """Quick function to get LLM response."""
    integration = LLMIntegration()
    return integration.get_response(messages, provider)


# Example usage
if __name__ == '__main__':
    # Example message format
    test_messages = [
        {'role': 'user', 'content': 'Olá, como posso ajudar hoje?'}
    ]
    response = get_llm_response(test_messages)
    print(f"Response: {response}")