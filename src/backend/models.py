"""Database models for Chatbot conversational memory."""

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class ConversationMemory(db.Model):
    """Model representing an episodic memory entry in the conversation database."""

    __tablename__ = 'conversation_memory'

    id = db.Column(db.Integer, primary_key=True)
    session_id = db.Column(db.String(255), nullable=False, index=True)
    role = db.Column(db.String(50), nullable=False)  # 'user' or 'assistant'
    content = db.Column(db.Text, nullable=False)
    topic = db.Column(db.String(100))  # Optional topic classification
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())

    def to_dict(self):
        """Convert model instance to dictionary."""
        return {
            'id': self.id,
            'session_id': self.session_id,
            'role': self.role,
            'content': self.content,
            'topic': self.topic,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

    def __repr__(self):
        return f"<ConversationMemory id={self.id} session={self.session_id} role={self.role}>"


# Helper functions for memory operations


def init_db(app):
    """Initialize the database with the Flask app."""
    db.init_app(app)
    # Create tables
    with app.app_context():
        db.create_all()


def save_message(session_id, role, content, topic=None):
    """
    Save a message to the episodic memory.

    Args:
        session_id: Unique session identifier
        role: 'user' or 'assistant'
        content: Message content
        topic: Optional topic classification

    Returns:
        ConversationMemory instance
    """
    message = ConversationMemory(
        session_id=session_id,
        role=role,
        content=content,
        topic=topic
    )
    db.session.add(message)
    db.session.commit()
    return message


def get_history(session_id, limit=None, offset=0):
    """
    Get conversation history for a session.

    Args:
        session_id: Unique session identifier
        limit: Maximum number of messages to return
        offset: Number of messages to skip (for pagination)

    Returns:
        List of message dicts ordered by creation time (oldest first)
    """
    query = ConversationMemory.query.filter(
        ConversationMemory.session_id == session_id
    ).order_by(ConversationMemory.created_at.asc())

    if limit:
        query = query.limit(limit)
    if offset:
        query = query.offset(offset)

    messages = query.all()
    return [msg.to_dict() for msg in messages]


def clear_history(session_id):
    """Clear all messages for a session."""
    ConversationMemory.query.filter(
        ConversationMemory.session_id == session_id
    ).delete()
    db.session.commit()