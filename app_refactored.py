"""
Main Streamlit application for Prompt-Driven PDF Editor with Humanized Content Generation
"""

import streamlit as st
import io
import datetime
from typing import List, Dict

# Import our modular components
from config import (
    APP_TITLE, APP_ICON, PAGE_LAYOUT, DEFAULT_API_KEY, USE_DEFAULT_API,
    PRIMARY_COLOR, SECONDARY_COLOR, SUCCESS_COLOR, WARNING_COLOR, 
    ERROR_COLOR, INFO_COLOR, BACKGROUND_COLOR, SIDEBAR_COLOR, TEXT_COLOR
)
from pdf_processor import extract_pdf_data, extract_simple_text, generate_modified_pdf, get_pdf_statistics
from gemini_client import configure_gemini, get_llm_modifications, test_api_connection, list_available_models
from utils import format_file_size, show_modification_preview, get_timestamp, validate_api_key


def initialize_session_state():
    """Initialize all session state variables"""
    if 'gemini_model' not in st.session_state:
        st.session_state.gemini_model = None
    if 'pages_data' not in st.session_state:
        st.session_state.pages_data = []
    if 'modifications' not in st.session_state:
        st.session_state.modifications = []
    if 'uploaded_file_bytes' not in st.session_state:
        st.session_state.uploaded_file_bytes = None
    if 'modified_pdf_bytes' not in st.session_state:
        st.session_state.modified_pdf_bytes = None


def apply_custom_theme():
    """Apply custom color theme to the app"""
    st.markdown(f"""
    <style>
    .main {{
        background-color: {BACKGROUND_COLOR};
    }}
    .sidebar .sidebar-content {{
        background-color: {SIDEBAR_COLOR};
    }}
    .stButton > button {{
        background-color: {PRIMARY_COLOR};
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.5rem 1rem;
        font-weight: 500;
    }}
    .stButton > button:hover {{
        background-color: {SECONDARY_COLOR};
        color: white;
    }}
    .stSuccess {{
        background-color: {SUCCESS_COLOR};
        color: white;
    }}
    .stWarning {{
        background-color: {WARNING_COLOR};
        color: white;
    }}
    .stError {{
        background-color: {ERROR_COLOR};
        color: white;
    }}
    .stInfo {{
        background-color: {INFO_COLOR};
        color: white;
    }}
    h1, h2, h3 {{
        color: {TEXT_COLOR};
    }}
    </style>
    """, unsafe_allow_html=True)


def render_sidebar():
    """Render the sidebar with configuration options"""
    with st.sidebar:
        st.header("🔧 Setup")
        
        # API Key configuration
        if USE_DEFAULT_API and DEFAULT_API_KEY:
            api_option = st.radio(
                "API Key Option",
                ["Use Default API Key", "Enter Custom API Key"],
                help="Choose between default or custom API key"
            )
            
            if api_option == "Use Default API Key":
                api_key = DEFAULT_API_KEY
                st.success("✅ Using default API key")
            else:
                api_key = st.text_input(
                    "Custom Gemini API Key",
                    type="password",
                    help="Get your free API key from Google AI Studio"
                )
        else:
            api_key = st.text_input(
                "Gemini API Key",
                type="password",
                help="Get your free API key from Google AI Studio"
            )
        
        if api_key and validate_api_key(api_key):
            try:
                st.session_state.gemini_model = configure_gemini(api_key)
                st.success("✅ API Ready!")
            except Exception as e:
                st.error(f"❌ API Error: {str(e)}")
        
        st.markdown("---")
        st.header("📄 Upload PDF")
        uploaded_file = st.file_uploader(
            "Choose a PDF file",
            type="pdf",
            help="Upload a PDF file to modify"
        )
        
        # Advanced options
        with st.expander("🔧 Advanced Options"):
            debug_mode = st.checkbox(
                "Debug Mode",
                help="Show detailed error information"
            )
            
            if st.button("🗑️ Clear All Data"):
                for key in ['pages_data', 'modifications', 'uploaded_file_bytes', 'modified_pdf_bytes']:
                    if key in st.session_state:
                        del st.session_state[key]
                st.rerun()
        
        return uploaded_file, debug_mode


def render_welcome_page():
    """Render the welcome page when no file is uploaded"""
    st.markdown("### 👋 Welcome to Prompt-Driven PDF Editor")
    st.markdown("Upload a PDF file using the sidebar to get started with humanized content generation.")
    
    # Feature overview
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("**📝 Prompt-Driven**\n\nNatural language instructions")
    with col2:
        st.markdown("**🎨 Humanized Content**\n\nAI-powered content generation")
    with col3:
        st.markdown("**💾 Instant Download**\n\nGet your edited PDF immediately")


def render_file_info(uploaded_file):
    """Render file information and statistics"""
    st.success(f"✅ File uploaded: {uploaded_file.name}")
    st.info(f"📊 File size: {format_file_size(uploaded_file.size)}")
    
    # Extract and display PDF statistics
    if st.session_state.pages_data:
        stats = get_pdf_statistics(st.session_state.pages_data)
        st.info(f"📄 Document: {stats['total_pages']} pages, {stats['total_text_blocks']} text blocks, {stats['total_characters']:,} characters")


def render_content_editor(simple_text, debug_mode):
    """Render the content editor interface"""
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("📖 Original PDF Content")
        st.text_area(
            "Original Text",
            value=simple_text,
            height=400,
            disabled=True,
            key="original_display"
        )
    
    with col2:
        st.subheader("📝 Prompt-Driven Editor")
        
        if st.session_state.gemini_model:
            # Modification query input
            modification_query = st.text_area(
                "Content Generation Prompt",
                placeholder="Example: Change 'Chapter 2: Background' to 'Chapter 2: Fundamentals' and highlight all sentences discussing financial matters",
                height=100,
                help="Describe what content changes you want to generate"
            )
            
            # Process button
            if st.button("🚀 Generate Content", type="primary"):
                if modification_query:
                    with st.spinner("Generating humanized content..."):
                        # Get modifications from LLM
                        llm_response = get_llm_modifications(
                            simple_text, 
                            modification_query, 
                            st.session_state.gemini_model,
                            debug_mode
                        )
                        
                        st.session_state.modifications = llm_response.get("modifications", [])
                        
                        # Display results
                        st.success("✅ Humanized content generation completed!")
                        st.write("**Summary:**", llm_response.get("summary", "No summary provided"))
                        
                        # Show humanization approach if available
                        if 'humanization_approach' in llm_response:
                            st.info(f"🎨 **Humanization Approach:** {llm_response['humanization_approach']}")
                        
                        # Show modifications with validation
                        show_modification_preview(st.session_state.modifications, simple_text)
                else:
                    st.warning("⚠️ Please enter a content generation prompt")
        else:
            st.warning("⚠️ Please configure your Gemini API key in the sidebar")


def render_pdf_generation(debug_mode):
    """Render the PDF generation section"""
    if st.session_state.modifications:
        st.markdown("---")
        st.subheader("📄 Generate & Download Edited PDF")
        
        if st.button("📄 Generate Edited PDF", type="primary"):
            with st.spinner("Generating edited PDF..."):
                # Generate modified PDF
                pdf_bytes = generate_modified_pdf(
                    st.session_state.pages_data,
                    st.session_state.modifications,
                    debug_mode
                )
                
                if pdf_bytes:
                    # Store in session state
                    st.session_state.modified_pdf_bytes = pdf_bytes
                    
                    st.success("✅ Edited PDF generated successfully!")
                    
                    # Show what was modified
                    st.subheader("📋 Summary of Changes")
                    for i, mod in enumerate(st.session_state.modifications):
                        if mod["type"] == "replace":
                            st.write(f"**{i+1}.** Replaced: `{mod['original_text']}` → `{mod['new_text']}`")
                        elif mod["type"] == "highlight":
                            st.write(f"**{i+1}.** Highlighted: `{mod['text_to_highlight']}`")
                    
                    # Debug information
                    if debug_mode:
                        st.subheader("🔍 Debug Information")
                        st.write(f"**Total modifications applied:** {len(st.session_state.modifications)}")
                        st.write(f"**PDF pages processed:** {len(st.session_state.pages_data)}")
                        st.write(f"**Generated PDF size:** {format_file_size(len(pdf_bytes))}")
                    
                    # Rerun to show download buttons
                    st.rerun()
                else:
                    st.error("❌ Failed to generate edited PDF")


def render_download_section(uploaded_file):
    """Render the download section"""
    if st.session_state.modified_pdf_bytes:
        st.markdown("---")
        st.subheader("📥 Download Your PDFs")
        
        # Generate filename with timestamp
        timestamp = get_timestamp()
        original_name = uploaded_file.name.replace('.pdf', '')
        new_filename = f"edited_{original_name}_{timestamp}.pdf"
        
        col_download1, col_download2 = st.columns([1, 1])
        
        with col_download1:
            st.download_button(
                label="📥 Download Edited PDF",
                data=st.session_state.modified_pdf_bytes,
                file_name=new_filename,
                mime="application/pdf",
                help="Click to download your edited PDF",
                type="primary",
                use_container_width=True
            )
        
        with col_download2:
            st.download_button(
                label="📄 Download Original PDF",
                data=st.session_state.uploaded_file_bytes,
                file_name=f"original_{uploaded_file.name}",
                mime="application/pdf",
                help="Click to download the original PDF for comparison",
                use_container_width=True
            )
        
        # Show file size comparison
        original_size = format_file_size(len(st.session_state.uploaded_file_bytes))
        edited_size = format_file_size(len(st.session_state.modified_pdf_bytes))
        st.info(f"📊 Original: {original_size} | Edited: {edited_size}")


def main():
    """Main application function"""
    # Configure page
    st.set_page_config(
        page_title=APP_TITLE,
        page_icon=APP_ICON,
        layout=PAGE_LAYOUT
    )
    
    # Apply custom theme
    apply_custom_theme()
    
    # Set title
    st.title(f"{APP_ICON} {APP_TITLE}")
    st.markdown("**Humanized Content Generation** - Transform your PDFs with natural language prompts")
    
    # Initialize session state
    initialize_session_state()
    
    # Render sidebar and get inputs
    uploaded_file, debug_mode = render_sidebar()
    
    if uploaded_file is not None:
        # Store file bytes in session state
        uploaded_file.seek(0)
        st.session_state.uploaded_file_bytes = uploaded_file.read()
        
        # Display file info
        render_file_info(uploaded_file)
        
        # Extract text with positions
        with st.spinner("Extracting text and layout information..."):
            # Create a new BytesIO object for text extraction
            file_for_extraction = io.BytesIO(st.session_state.uploaded_file_bytes)
            st.session_state.pages_data = extract_pdf_data(file_for_extraction)
        
        if st.session_state.pages_data:
            # Extract simple text for display
            file_for_text = io.BytesIO(st.session_state.uploaded_file_bytes)
            simple_text = extract_simple_text(file_for_text)
            
            # Render content editor
            render_content_editor(simple_text, debug_mode)
            
            # Render PDF generation
            render_pdf_generation(debug_mode)
            
            # Render download section
            render_download_section(uploaded_file)
    
    else:
        # Render welcome page
        render_welcome_page()


if __name__ == "__main__":
    main()
