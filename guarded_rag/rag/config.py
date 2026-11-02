"""Configuration for models, retrieval, and role-based access."""

EMBED_MODEL = "nomic-embed-text"
CHAT_MODEL = "llama3.2:3b"
RETRIEVAL_K = 4

ROLE_ALLOWED_LEVELS = {
    "public": {"public"},
    "employee": {"public", "internal"},
    "admin": {"public", "internal", "restricted"},
}
