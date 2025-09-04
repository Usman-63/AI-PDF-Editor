"""
Utility functions for Prompt-Driven PDF Editor with Humanized Content Generation
"""

import re
from typing import Dict, List
import streamlit as st


def format_file_size(size_bytes: int) -> str:
    """Format file size in human readable format"""
    if size_bytes < 1024:
        return f"{size_bytes} B"
    elif size_bytes < 1024 * 1024:
        return f"{size_bytes / 1024:.1f} KB"
    else:
        return f"{size_bytes / (1024 * 1024):.1f} MB"


def create_fallback_modification(original_text: str, modification_query: str) -> Dict:
    """Create a simple fallback modification when AI fails"""
    modifications = []
    
    # Simple text replacement fallback
    if "change" in modification_query.lower() and "to" in modification_query.lower():
        # Try to extract "change X to Y" pattern
        pattern = r"change\s+['\"]([^'\"]+)['\"]\s+to\s+['\"]([^'\"]+)['\"]"
        match = re.search(pattern, modification_query.lower())
        if match:
            old_text = match.group(1)
            new_text = match.group(2)
            if old_text in original_text:
                modifications.append({
                    "type": "replace",
                    "original_text": old_text,
                    "new_text": new_text,
                    "context": f"Found in text: {old_text}"
                })
    
    # Simple highlighting fallback
    if "highlight" in modification_query.lower():
        # Look for common financial terms
        financial_terms = ["financial", "money", "cost", "budget", "revenue", "profit", "investment", "price", "fee"]
        for term in financial_terms:
            if term in original_text.lower():
                modifications.append({
                    "type": "highlight",
                    "text_to_highlight": term,
                    "context": f"Found financial term: {term}",
                    "reason": "Contains financial content"
                })
                break
    
    return {
        "modifications": modifications,
        "summary": f"Fallback modification created for: {modification_query}"
    }


def validate_api_key(api_key: str) -> bool:
    """Validate if API key is properly formatted"""
    if not api_key:
        return False
    if len(api_key) < 20:  # Basic length check
        return False
    return True


def get_timestamp() -> str:
    """Get current timestamp for file naming"""
    from datetime import datetime
    return datetime.now().strftime("%Y%m%d_%H%M%S")


def clean_text_for_display(text: str, max_length: int = 500) -> str:
    """Clean and truncate text for display purposes"""
    if not text:
        return "No text available"
    
    # Remove extra whitespace
    cleaned = re.sub(r'\s+', ' ', text.strip())
    
    # Truncate if too long
    if len(cleaned) > max_length:
        cleaned = cleaned[:max_length] + "..."
    
    return cleaned


def show_modification_preview(modifications: List[Dict], simple_text: str) -> None:
    """Display humanized modification preview with validation"""
    if not modifications:
        st.warning("No modifications generated")
        return
    
    st.subheader("📝 Humanized Content Changes")
    for i, mod in enumerate(modifications):
        with st.expander(f"Modification {i+1}: {mod['type'].title()}"):
            if mod["type"] == "replace":
                st.write(f"**Replace:** `{mod['original_text']}`")
                st.write(f"**With:** `{mod['new_text']}`")
                st.write(f"**Context:** {mod.get('context', 'N/A')}")
                
                # Show humanization note if available
                if 'humanization_note' in mod:
                    st.info(f"🎨 **Humanization:** {mod['humanization_note']}")
                
                # Check if the text actually exists in the document
                if mod['original_text'] in simple_text:
                    st.success("✅ Text found in document")
                else:
                    st.warning("⚠️ Text not found in document - modification may not work")
            elif mod["type"] == "highlight":
                st.write(f"**Highlight:** `{mod['text_to_highlight']}`")
                st.write(f"**Reason:** {mod.get('reason', 'N/A')}")
                st.write(f"**Context:** {mod.get('context', 'N/A')}")
                
                # Show humanization note if available
                if 'humanization_note' in mod:
                    st.info(f"🎨 **Humanization:** {mod['humanization_note']}")
                
                # Check if the text actually exists in the document
                if mod['text_to_highlight'].lower() in simple_text.lower():
                    st.success("✅ Text found in document")
                else:
                    st.warning("⚠️ Text not found in document - highlighting may not work")
