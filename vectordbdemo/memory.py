chat_memory = {}

def get_history(session_id: str) -> list:
    """Returns the chat history for a given session."""
    return chat_memory.get(session_id, [])

def save_message(session_id: str, role: str, content: str):
    """Saves a message to the session's chat history."""
    if session_id not in chat_memory:
        chat_memory[session_id] = []
    
    chat_memory[session_id].append({
        "role": role,
        "content": content
    })
