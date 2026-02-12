import pytest
import os
from app.core.llm_adapter import LLMAdapter

# Mocking environment variable for tests if not present
os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY", "test_key")

def test_intent_detection_logic():
    """
    Verifies that the LLMAdapter switches roles based on keywords.
    Matches Requirement: Summarization and Action Extraction.
    """
    adapter = LLMAdapter()
    
    # Test Summary detection: Should trigger the 'Assistant' role
    msg_sum, _ = adapter._detect_intent("Please summarize the minutes of this meeting")
    assert "Assistant" in msg_sum
    
    # Test Action Items detection: Should trigger the 'Project Manager' role
    msg_task, _ = adapter._detect_intent("What are the pending tasks and action items?")
    assert "Project Manager" in msg_task

def test_api_key_error_handling():
    """
    Ensures the system identifies missing configuration gracefully.
    """
    # Force an adapter with a missing key
    os.environ["GROQ_API_KEY"] = "missing_key"
    adapter = LLMAdapter()
    adapter.api_key = "missing_key"
    
    response = adapter.generate_response("Hello")
    assert "Configuration Error" in response

def test_default_prompt_fallback():
    """
    Ensures that a generic query defaults to the Senior AI Lead role.
    """
    adapter = LLMAdapter()
    msg, _ = adapter._detect_intent("How does RAG work?")
    assert "Senior AI Lead" in msg