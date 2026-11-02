from flask import Flask, request, jsonify
import os

app = Flask(__name__)

# Load configuration from environment variables
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key')
app.config['DEBUG'] = os.environ.get('FLASK_DEBUG', 'False').lower() == 'true'

# Available LLM providers configuration
LLM_PROVIDERS = {
    'openai': {
        'model': os.environ.get('OPENAI_MODEL', 'gpt-3.5-turbo'),
        'enabled': bool(os.environ.get('OPENAI_API_KEY'))
    },
    'anthropic': {
        'model': os.environ.get('ANTHROPIC_MODEL', 'claude-instant-1.2'),
        'enabled': bool(os.environ.get('ANTHROPIC_API_KEY'))
    },
    'gemini': {
        'model': os.environ.get('GEMINI_MODEL', 'gemini-pro'),
        'enabled': bool(os.environ.get('GEMINI_API_KEY'))
    }
}


@app.route('/api/health', methods=['GET'])
def health():
    """Health check endpoint for deploy monitoring."""
    return jsonify({
        "status": "healthy",
        "timestamp": __import__('datetime').datetime.utcnow().isoformat(),
        "version": "1.0.0"
    })


@app.route('/api/chat', methods=['POST'])
def chat():
    """Chat endpoint - receives message, gets LLM response, returns it."""
    try:
        data = request.get_json()
        if not data or 'message' not in data:
            return jsonify({
                "error": " 'message' field is required"
            }), 400

        user_message = data['message']

        # Basic validation
        if not user_message or not user_message.strip():
            return jsonify({
                "error": "Message cannot be empty"
            }), 400

        # For now, return a simple echo response
        # LLM integration will be added in Task 2
        response_text = f"Você disse: '{user_message}'"

        return jsonify({
            "response": response_text,
            "provider": "echo",
            "message_length": len(user_message)
        })

    except Exception as e:
        return jsonify({
            "error": str(e)
        }), 500


@app.route('/api/history', methods=['GET'])
def history():
    """History endpoint - returns conversation history for the session."""
    # TODO: In Task 3, will integrate with episodic memory service
    # For now, returns empty list
    return jsonify({
        "messages": [],
        "session_id": request.args.get('session_id', 'default')
    })


@app.route('/api/search', methods=['POST'])
def search():
    """Documentation search endpoint."""
    try:
        data = request.get_json()
        if not data or 'query' not in data:
            return jsonify({
                "error": " 'query' field is required"
            }), 400

        query = data['query']

        # TODO: In Task 4, will integrate with documentation index
        # For now, returns empty results
        return jsonify({
            "results": [],
            "query": query,
            "count": 0
        })

    except Exception as e:
        return jsonify({
            "error": str(e)
        }), 500


# Global error handler
@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Endpoint not found"}), 404


@app.errorhandler(500)
def internal_error(error):
    return jsonify({"error": "Internal server error"}), 500


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=app.config['DEBUG'])