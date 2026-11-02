"""Integration tests for Chatbot full flow."""

import pytest
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from app import app


class TestEndToEndChat:
    """Testes de integração do fluxo completo de chat."""

    def test_end_to_end_basic(self):
        """Testa fluxo básico: envia mensagem, recebe resposta."""
        with app.test_client() as client:
            # 1. Envia mensagem
            response = client.post('/api/chat', json={"message": "Olá, como você está?"})
            assert response.status_code == 200
            data = response.get_json()
            assert 'response' in data
            assert 'Olá' in data['response']

            # 2. Verifica que a mensagem foi recebida (mock - não salva em DB ainda)
            assert data['response'] is not None


class TestHistoryAndChatIntegration:
    """Testes de integração entre chat e história."""

    def test_chat_saves_message_structure(self):
        """Testa que o chat retorna estrutura esperada para história."""
        with app.test_client() as client:
            # Envia mensagem
            response = client.post('/api/chat', json={"message": "Teste de integração"})
            assert response.status_code == 200
            data = response.get_json()

            # 2. Chama histórico (retorna vazio no momento, mas estrutura está correta)
            hist_response = client.get('/api/history?session_id=test_session')
            assert hist_response.status_code == 200
            hist_data = hist_response.get_json()
            assert 'messages' in hist_data


class TestSearchIntegration:
    """Testes de integração da busca."""

    def test_search_endpoint_structure(self):
        """Testa a estrutura do endpoint de busca."""
        with app.test_client() as client:
            response = client.post('/api/search', json={"query": "python"})
            assert response.status_code == 200
            data = response.get_json()
            assert 'results' in data
            assert 'query' in data


class TestFullStackHealth:
    """Testes de saúde do stack completo."""

    def test_all_endpoints_accessíveis(self):
        """Testa se todos os endpoints principais estão acessíveis."""
        with app.test_client() as client:
            # Health check
            response = client.get('/api/health')
            assert response.status_code == 200

            # Chat (sem mensagem = erro)
            response = client.post('/api/chat', json={})
            assert response.status_code == 400  # Expected: missing message

            # Chat (com mensagem)
            response = client.post('/api/chat', json={"message": "test"})
            assert response.status_code == 200

            # History
            response = client.get('/api/history?session_id=test')
            assert response.status_code == 200

            # Search (sem query = erro)
            response = client.post('/api/search', json={})
            assert response.status_code == 400

            # Search (com query)
            response = client.post('/api/search', json={"query": "test"})
            assert response.status_code == 200


if __name__ == '__main__':
    pytest.main([__file__, '-v'])