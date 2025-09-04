# Prompt-Driven PDF Editor with Humanized Content Generation

A modern, modular web application built with Streamlit that uses AI (Google Gemini) to intelligently edit PDF files through natural language prompts while preserving the original layout and generating humanized content. Features flexible API key management and clean modular architecture.

## 🆕 Latest Features

### 🚀 **Live Deployment**
- **Try it now**: [https://ai-pdf-editor-jsq9hxcetn6fu2wk3asxqd.streamlit.app/](https://ai-pdf-editor-jsq9hxcetn6fu2wk3asxqd.streamlit.app/)
- Fully functional web application
- No installation required

### 🔑 **Flexible API Key Management**
- **Default API Key**: Set once in config, use everywhere
- **Custom API Key**: Users can enter their own keys
- **Secure Options**: Perfect for both personal and shared use

### 🏗️ **Modular Architecture**
- Clean, organized code structure
- Easy to maintain and extend
- Professional development practices

## Features

### 📝 Prompt-Driven Editing
- **Natural Language Prompts**: Describe content changes in plain English
- **Humanized Content Generation**: AI generates natural, human-like content
- **Intelligent Text Analysis**: AI identifies exact text to modify
- **Context-Aware Changes**: Uses surrounding text for accurate identification
- **Smart Highlighting**: Automatically highlights relevant content

### 📄 PDF Processing
- **Layout Preservation**: Maintains original PDF formatting and positioning using PyMuPDF
- **Text Extraction**: Extracts text with position information
- **Multi-page Support**: Handles documents with multiple pages
- **Font & Style Preservation**: Keeps original fonts, sizes, and colors

### 🎯 Modification Types
- **Text Replacement**: Change specific text while preserving formatting
- **Content Highlighting**: Highlight sentences or phrases based on criteria
- **Heading Updates**: Modify chapter/section titles
- **Bulk Changes**: Apply changes throughout the document

### 💡 Example Use Cases
- Change "Chapter 2: Background" to "Chapter 2: Fundamentals"
- Highlight all sentences discussing financial matters
- Replace company names throughout the document
- Update section numbering consistently

## Installation

1. **Clone or download this repository**

2. **Create a virtual environment** (recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Basic Version (Manual Editing)
1. **Run the basic application**:
   ```bash
   streamlit run app_refactored.py
   ```

### Prompt-Driven Editor (Recommended)
1. **Get your Gemini API key**:
   - Go to [Google AI Studio](https://aistudio.google.com/)
   - Sign in with your Google account
   - Click "Get API Key"
   - Copy the key

2. **Configure API Key** (Choose one option):
   
   **Option A: Environment Variable (Recommended for deployment)**
   ```bash
   # Create .env file
   echo "GEMINI_API_KEY=your_api_key_here" > .env
   ```
   
   **Option B: Direct Configuration (For local development)**
   - Edit `config.py`
   - Set `DEFAULT_API_KEY = "your-api-key-here"`
   - Save the file

3. **Run the Prompt-Driven PDF Editor**:
   ```bash
   streamlit run app_refactored.py
   ```

4. **Configure the application**:
   - Choose "Use Default API Key" or "Enter Custom API Key"
   - Upload a PDF file

5. **Generate humanized content**:
   - Enter natural language prompts (e.g., "Change Chapter 2: Background to Chapter 2: Fundamentals")
   - Click "Generate Content"
   - Review the proposed changes
   - Click "Generate Edited PDF"
   - Download the edited PDF with a timestamped filename

6. **Download options**:
   - **Original PDF**: Download the original file for comparison
   - **Edited PDF**: Download the edited version with all changes applied
   - **Automatic naming**: Files are automatically named with timestamps

## Dependencies

### Core Dependencies
- `streamlit>=1.28.0` - Web application framework
- `PyPDF2>=3.0.0` - PDF text extraction
- `reportlab>=4.0.0` - PDF generation

### AI-Enhanced Dependencies
- `google-generativeai>=0.3.0` - Google Gemini AI integration
- `PyMuPDF>=1.23.0` - Advanced PDF processing with layout preservation
- `python-dotenv>=1.0.0` - Environment variable management

## How It Works

### How the App Works
1. **Upload**: PDF files are uploaded through Streamlit's file uploader
2. **Extract**: PyMuPDF extracts text with position and formatting information
3. **AI Analysis**: Gemini AI analyzes the text and modification request
4. **Generate Modifications**: AI provides structured modification instructions
5. **Apply Changes**: Modifications are applied while preserving layout
6. **Highlight**: Content is highlighted based on AI analysis
7. **Download**: Modified PDF with preserved formatting is generated

## Limitations

- Requires a valid Gemini API key
- Text-based PDFs work best (scanned PDFs may not extract text properly)
- Complex layouts with images may not be perfectly preserved
- Large PDFs may take longer to process due to AI analysis
- **Free Tier Limits**: Based on [Gemini API rate limits](https://ai.google.dev/gemini-api/docs/rate-limits#free-tier):
  - Gemini 2.5 Flash: 30 requests/minute, 1M tokens/minute, 200 requests/day
  - Gemini 2.5 Flash-Lite: 15 requests/minute, 250K tokens/minute, 1K requests/day
  - Gemini 2.5 Pro: 5 requests/minute, 250K tokens/minute, 100 requests/day

## 🚀 Deployment

### **GitHub + Streamlit Cloud Deployment**

For secure deployment with your API key:

1. **Set up environment variables**:
   ```bash
   cp env.example .env
   # Edit .env and add your API key
   ```

2. **Deploy to GitHub**:
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git remote add origin https://github.com/YOUR_USERNAME/your-repo.git
   git push -u origin main
   ```

3. **Deploy to Streamlit Cloud**:
   - Go to [Streamlit Cloud](https://share.streamlit.io)
   - Connect your GitHub repository
   - Add your API key in Streamlit secrets:
     ```toml
     GEMINI_API_KEY = "your_api_key_here"
     ```

📖 **For detailed deployment instructions, see the deployment section above.**

## Troubleshooting

- **API Key Issues**: Ensure your Gemini API key is valid and has sufficient quota
- **Model Not Found Error**: If you get "404 models/gemini-pro is not found", the app will automatically try different model names (gemini-2.5-flash, gemini-2.5-flash-lite, gemini-2.5-pro, etc.)
- **PDF not extracting text**: Ensure the PDF contains selectable text (not just images)
- **AI Processing Errors**: Check your internet connection and API key validity
- **Layout Issues**: Complex PDFs with images may not preserve layout perfectly
- **Installation issues**: Make sure you're using Python 3.7 or higher
- **Memory issues**: Try with smaller PDF files if you encounter memory problems
- **Dependency conflicts**: Use a virtual environment to avoid package conflicts

## Future Enhancements

- **OCR Support**: Process image-based PDFs using optical character recognition
- **Advanced AI Features**: More sophisticated modification capabilities
- **Batch Processing**: Handle multiple PDFs simultaneously
- **Template System**: Save and reuse common modification patterns
- **Collaborative Editing**: Multiple users working on the same document
- **Version Control**: Track changes and maintain document history
- **Custom Highlighting**: User-defined highlighting rules and colors
- **Export Options**: Support for different output formats (Word, HTML, etc.)
