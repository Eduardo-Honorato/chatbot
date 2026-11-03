from flask import Flask, request, jsonify
import os
import re

app = Flask(__name__)

# Configuration
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key')
app.config['DEBUG'] = os.environ.get('FLASK_DEBUG', 'False').lower() == 'true'

# DATABASE_URL configuration
DATABASE_URL = os.environ.get('DATABASE_URL', '')
if DATABASE_URL == '':
    # No DATABASE_URL: use in-memory SQLite (never connect on import)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://'
    app.config['DB_CONFIGURED'] = False
else:
    # Normalize any postgres family prefix to postgresql+psycopg2://
    DATABASE_URL = re.sub(r'^postgres(?:ql)?(?:\+\w+)?://', 'postgresql+psycopg2://', DATABASE_URL, count=1)
    app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
    app.config['DB_CONFIGURED'] = True

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
from sqlalchemy.pool import NullPool
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {'poolclass': NullPool, 'pool_pre_ping': True}

# Initialize database on demand - nothing connects at import
from models import init_db, ensure_db
try:
    init_db(app)
except Exception:
    app.logger.exception("Database initialization failed")
    app.config['DB_CONFIGURED'] = False

# Database guard - check if DB is configured, only used in routes that access DB
def db_guard():
    """Return error response if DB is not configured or ensure_db fails.
    Returns (jsonify({"error": "..."}), 503) if DB_CONFIGURED is False
    or if ensure_db(app) raises; otherwise None.
    """
    if not app.config.get('DB_CONFIGURED'):
        return jsonify({"error": "Database not configured"}), 503
    try:
        ensure_db(app)
    except Exception:
        app.logger.exception("Database initialization failed")
        return jsonify({"error": "Database initialization failed"}), 503
    return None

# CORS configuration - only on /api/* routes
from flask_cors import CORS

cors_origins_str = os.environ.get(
    'CORS_ORIGINS',
    'http://localhost:3000,http://localhost:3002'
)
cors_origins = [o.strip() for o in cors_origins_str.split(',')]

CORS(app, resources={
    r"/api/*": {
        "origins": cors_origins + [r"^https://portfolio-[a-z0-9-]+-honorato3\.vercel\.app$"],
        "methods": ["GET", "POST", "OPTIONS"],
        "allow_headers": ["Content-Type"]
    }
})

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