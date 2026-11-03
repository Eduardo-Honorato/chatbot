"""Service layer for managing episodic conversation memory."""

from models import db, ConversationMemory, save_message, get_history, clear_history


class MemoryService:
    """Service class for managing conversational memory."""

    def __init__(self):
        pass

    def save_user_message(self, session_id, content, topic=None):
        """Save a user message to memory using database."""
        from models import save_message
        return save_message(session_id, 'user', content, topic)

    def save_assistant_message(self, session_id, content, topic=None):
        """Save an assistant message to memory using database."""
        from models import save_message
        return save_message(session_id, 'assistant', content, topic)

    def get_recent_history(self, session_id, limit=20):
        """Get the recent conversation history for a session using database."""
        from models import get_history
        return get_history(session_id, limit=limit)

    def clear_session_memory(self, session_id):
        """Clear all memory for a specific session using database."""
        from models import clear_history
        clear_history(session_id)

    def get_message_count(self, session_id):
        """Get the number of messages in a session's memory using database."""
        from models import ConversationMemory
        return ConversationMemory.query.filter(
            ConversationMemory.session_id == session_id
        ).count()

    def get_messages_by_topic(self, session_id, topic):
        """Get messages filtered by topic for a session using database."""
        from models import ConversationMemory
        messages = ConversationMemory.query.filter(
            ConversationMemory.session_id == session_id,
            ConversationMemory.topic == topic
        ).order_by(ConversationMemory.created_at.asc()).all()
        return [msg.to_dict() for msg in messages]


# Convenience function
def create_memory_service():
    """Create a MemoryService instance with db initialized."""
    from models import init_db, db
    return MemoryService()
