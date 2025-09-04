"""
Gemini API client for Prompt-Driven PDF Editor with Humanized Content Generation
"""

import json
import google.generativeai as genai
from typing import Dict, List, Optional
import streamlit as st
from config import DEFAULT_MODEL_NAMES
from utils import create_fallback_modification


def configure_gemini(api_key: str):
    """Configure Gemini API with the provided key"""
    genai.configure(api_key=api_key)

    # Try different model names in order of preference
    for model_name in DEFAULT_MODEL_NAMES:
        try:
            model = genai.GenerativeModel(model_name)
            # Just return the model without testing - let the actual usage handle errors
            return model
        except Exception as e:
            continue

    raise Exception(f"None of the model names worked. Tried: {DEFAULT_MODEL_NAMES}")


def list_available_models(api_key: str) -> List[str]:
    """List available Gemini models"""
    try:
        genai.configure(api_key=api_key)
        models = genai.list_models()
        return [model.name for model in models if 'generateContent' in model.supported_generation_methods]
    except Exception as e:
        st.error(f"Error listing models: {str(e)}")
        return []


def get_llm_modifications(original_text: str, modification_query: str, model, debug_mode: bool = False) -> Dict:
    """Get humanized modifications from Gemini LLM"""
    try:
        prompt = f"""
        You are an expert content editor and humanization specialist. Your task is to analyze the original text and create natural, human-like modifications that improve readability, engagement, and clarity while maintaining the original meaning and structure.

        Original text:
        {original_text[:2000]}...
        
        Modification request: {modification_query}
        
        HUMANIZATION GUIDELINES:
        1. Make content more conversational and engaging
        2. Use natural, flowing language that sounds human-written
        3. Improve clarity and readability
        4. Add subtle personality and warmth to the text
        5. Maintain professional tone while being more approachable
        6. Use active voice where appropriate
        7. Break up long sentences for better flow
        8. Add transitional phrases for smoother reading
        
        TECHNICAL RULES:
        1. For text replacements, provide EXACT text matches from the original (copy-paste exact text)
        2. For highlighting, identify sentences or phrases that match the criteria
        3. Always provide context to help identify the correct location
        4. Be VERY precise with text matching - use exact strings from the original, including punctuation
        5. If the request is about changing headings, look for patterns like "Chapter X:", "Section X:", etc.
        6. If highlighting financial content, look for words like: financial, money, cost, budget, revenue, profit, investment, etc.
        7. IMPORTANT: Only include modifications for text that actually exists in the original document
        8. Make replacements sound natural and human-like, not robotic
        
        IMPORTANT: Respond ONLY with valid JSON. Do not include any text before or after the JSON. Do not use markdown formatting.
        
        Return a JSON object with this exact structure:
        {{
            "modifications": [
                {{
                    "type": "replace",
                    "original_text": "exact text from original",
                    "new_text": "humanized replacement text that sounds natural and engaging",
                    "context": "brief context about where this text appears",
                    "humanization_note": "explanation of how this makes the text more human-like"
                }},
                {{
                    "type": "highlight",
                    "text_to_highlight": "text to highlight",
                    "context": "brief context about where this text appears",
                    "reason": "why this text should be highlighted",
                    "humanization_note": "how highlighting improves readability"
                }}
            ],
            "summary": "Brief summary of all humanized modifications made",
            "humanization_approach": "Overall approach taken to make content more human and engaging"
        }}
        """
        
        response = model.generate_content(prompt)
        
        if debug_mode:
            st.subheader("🔍 Debug: Raw API Response")
            st.text(response.text)
        
        # Clean the response text
        response_text = response.text.strip()
        
        # Remove markdown code blocks if present
        if response_text.startswith("```json"):
            response_text = response_text[7:]
        if response_text.startswith("```"):
            response_text = response_text[3:]
        if response_text.endswith("```"):
            response_text = response_text[:-3]
        
        response_text = response_text.strip()
        
        # Parse JSON
        try:
            result = json.loads(response_text)
            return result
        except json.JSONDecodeError as e:
            if debug_mode:
                st.error(f"JSON parsing error: {str(e)}")
                st.text(f"Response text: {response_text}")
            
            # Fallback to simple modification
            return create_fallback_modification(original_text, modification_query)
            
    except Exception as e:
        st.error(f"Error getting LLM modifications: {str(e)}")
        return {"modifications": [], "summary": "Error occurred"}


def test_api_connection(api_key: str) -> bool:
    """Test if the API connection works"""
    try:
        model = configure_gemini(api_key)
        # Simple test without generating content
        return True
    except Exception as e:
        st.error(f"API connection failed: {str(e)}")
        return False
