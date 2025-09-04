"""
Configuration file for Prompt-Driven PDF Editor with Humanized Content Generation
"""

# Gemini API Configuration
DEFAULT_MODEL_NAMES = [
    'gemini-2.5-flash',      # Best free tier option
    'gemini-2.5-flash-lite', # Good free tier option
    'gemini-2.5-pro',        # Premium free tier option
    'gemini-2.0-flash',      # Alternative option
    'gemini-2.0-flash-lite', # Alternative option
    'gemini-1.5-pro',        # Legacy
    'gemini-pro',            # Legacy
]

# PDF Processing Configuration
DEFAULT_FONT_SIZE = 12
DEFAULT_HIGHLIGHT_COLOR = (1, 1, 0)  # Yellow
DEFAULT_TEXT_COLOR = (0, 0, 0)       # Black

# UI Configuration
APP_TITLE = "Prompt-Driven PDF Editor with Humanized Content Generation"
APP_ICON = "📝"
PAGE_LAYOUT = "wide"

# File Configuration
MAX_FILE_SIZE_MB = 10
SUPPORTED_FILE_TYPES = ["pdf"]

# Debug Configuration
DEFAULT_DEBUG_MODE = False

# API Configuration
import os
import streamlit as st

def get_api_key():
    """Get API key from environment variable or Streamlit secrets"""
    # First try environment variable
    api_key = os.getenv("GEMINI_API_KEY", "")
    
    # If not found, try Streamlit secrets (for Streamlit Cloud)
    if not api_key:
        try:
            api_key = st.secrets.get("GEMINI_API_KEY", "")
        except:
            pass
    
    return api_key

DEFAULT_API_KEY = get_api_key()
USE_DEFAULT_API = True  # Set to False to always require user input

# Color Theme Configuration
PRIMARY_COLOR = "#FF6B6B"
SECONDARY_COLOR = "#4ECDC4"
SUCCESS_COLOR = "#45B7D1"
WARNING_COLOR = "#FFA07A"
ERROR_COLOR = "#FF6B6B"
INFO_COLOR = "#98D8C8"
BACKGROUND_COLOR = "#F7F7F7"
SIDEBAR_COLOR = "#2C3E50"
TEXT_COLOR = "#2C3E50"
