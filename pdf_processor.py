"""
PDF processing functions for Prompt-Driven PDF Editor with Humanized Content Generation
"""

import PyPDF2
import fitz  # PyMuPDF
import tempfile
import os
from typing import Dict, List, Tuple
import streamlit as st
from config import DEFAULT_FONT_SIZE, DEFAULT_HIGHLIGHT_COLOR, DEFAULT_TEXT_COLOR


def extract_pdf_data(pdf_file) -> List[Dict]:
    """Extract text and layout data from PDF using PyMuPDF"""
    try:
        # Read the PDF file
        pdf_bytes = pdf_file.read()
        pdf_file.seek(0)  # Reset file pointer
        
        # Open with PyMuPDF
        doc = fitz.open(stream=pdf_bytes, filetype="pdf")
        pages_data = []
        
        for page_num in range(len(doc)):
            page = doc[page_num]
            
            # Get page dimensions
            page_rect = page.rect
            page_width = page_rect.width
            page_height = page_rect.height
            
            # Extract text blocks with position information
            text_blocks = []
            blocks = page.get_text("dict")
            
            for block in blocks["blocks"]:
                if "lines" in block:  # Text block
                    for line in block["lines"]:
                        for span in line["spans"]:
                            if span["text"].strip():  # Only non-empty text
                                text_blocks.append({
                                    "text": span["text"],
                                    "bbox": span["bbox"],  # [x0, y0, x1, y1]
                                    "size": span["size"],
                                    "font": span["font"],
                                    "color": span["color"] if span["color"] != 0 else DEFAULT_TEXT_COLOR
                                })
            
            pages_data.append({
                "page_num": page_num,
                "page_width": page_width,
                "page_height": page_height,
                "text_blocks": text_blocks
            })
        
        doc.close()
        return pages_data
        
    except Exception as e:
        st.error(f"Error extracting PDF data: {str(e)}")
        return []


def apply_modifications_to_pdf(pages_data: List[Dict], modifications: List[Dict], output_path: str, debug_mode: bool = False) -> bool:
    """Apply modifications to PDF while preserving layout"""
    try:
        # Create a new PDF document
        doc = fitz.open()
        
        for page_data in pages_data:
            # Create a new page with the same dimensions
            page = doc.new_page(width=page_data["page_width"], height=page_data["page_height"])
            
            # First, add all text with modifications
            for block in page_data["text_blocks"]:
                original_text = block["text"]
                modified_text = original_text
                
                # Apply text replacements
                for mod in modifications:
                    if mod["type"] == "replace":
                        if mod["original_text"] in original_text:
                            modified_text = modified_text.replace(mod["original_text"], mod["new_text"])
                
                # Add text to page with better positioning
                if modified_text.strip():
                    bbox = block["bbox"]
                    try:
                        # Use a more reliable text insertion method
                        page.insert_text(
                            (bbox[0], bbox[1] + block["size"]),  # Position at top-left of bbox
                            modified_text,
                            fontsize=block["size"],
                            color=block["color"]
                        )
                    except Exception as e:
                        # Fallback: use default font and size
                        try:
                            page.insert_text(
                                (bbox[0], bbox[1] + DEFAULT_FONT_SIZE),
                                modified_text,
                                fontsize=DEFAULT_FONT_SIZE
                            )
                        except Exception as e2:
                            if debug_mode:
                                st.warning(f"Could not insert text: {modified_text[:50]}...")
            
            # Then add highlights
            for mod in modifications:
                if mod["type"] == "highlight":
                    # Find and highlight the specified text
                    for block in page_data["text_blocks"]:
                        if mod["text_to_highlight"].lower() in block["text"].lower():
                            bbox = block["bbox"]
                            try:
                                # Create highlight annotation
                                highlight = page.add_highlight_annot(bbox)
                                highlight.set_colors({"stroke": DEFAULT_HIGHLIGHT_COLOR})
                                highlight.update()
                            except Exception as e:
                                # Fallback: draw a simple rectangle
                                try:
                                    rect = fitz.Rect(bbox)
                                    page.draw_rect(rect, color=DEFAULT_HIGHLIGHT_COLOR, width=2)
                                except Exception as e2:
                                    if debug_mode:
                                        st.warning(f"Could not highlight: {mod['text_to_highlight']}")
        
        # Save the modified PDF
        doc.save(output_path)
        doc.close()
        return True
        
    except Exception as e:
        st.error(f"Error applying modifications: {str(e)}")
        if debug_mode:
            st.error(f"Debug info: {str(e)}")
        return False


def extract_simple_text(pdf_file) -> str:
    """Extract simple text for display purposes using PyPDF2"""
    try:
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        text = ""
        
        for page in pdf_reader.pages:
            text += page.extract_text() + "\n"
        
        return text.strip()
        
    except Exception as e:
        st.error(f"Error extracting text: {str(e)}")
        return "Error extracting text from PDF"


def generate_modified_pdf(pages_data: List[Dict], modifications: List[Dict], debug_mode: bool = False) -> bytes:
    """Generate modified PDF and return as bytes"""
    try:
        # Create temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as temp_file:
            temp_path = temp_file.name
        
        # Apply modifications
        success = apply_modifications_to_pdf(pages_data, modifications, temp_path, debug_mode)
        
        if not success:
            raise Exception("Failed to apply modifications to PDF")
        
        # Read the generated PDF
        with open(temp_path, 'rb') as f:
            pdf_bytes = f.read()
        
        # Clean up temporary file
        os.unlink(temp_path)
        
        return pdf_bytes
        
    except Exception as e:
        st.error(f"Error generating modified PDF: {str(e)}")
        return b""


def get_pdf_statistics(pages_data: List[Dict]) -> Dict:
    """Get statistics about the PDF"""
    total_pages = len(pages_data)
    total_text_blocks = sum(len(page["text_blocks"]) for page in pages_data)
    total_characters = sum(
        len(block["text"]) 
        for page in pages_data 
        for block in page["text_blocks"]
    )
    
    return {
        "total_pages": total_pages,
        "total_text_blocks": total_text_blocks,
        "total_characters": total_characters
    }
