import secrets

def create_thread_reference():
    """Creates a reference for a thread"""
    return secrets.token_hex(nbytes=5)