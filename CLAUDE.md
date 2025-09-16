# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Streamlit-based meal preparation assistant that helps with meal planning, grocery shopping, and prep instructions. The system uses LLM providers (OpenAI, Anthropic, Google) to answer questions about meal plans and recipes stored in text files.

## Architecture

- **Main Application**: `meal-prep-assistant.py` - Streamlit chat interface
- **System Prompt**: `meal-prep-assistant.md` - Contains detailed instructions for the LLM assistant
- **Recipe Data**: `data/` directory contains weekly meal plans as text files (e.g., `Week_of_August_25th_2024.txt`)
- **PDF Converter**: `convert-recipes-pdf-to-text.py` - Converts recipe PDFs to text files using PyPDFLoader
- **Virtual Environment**: `mea-prep/` - Python virtual environment with dependencies

## Key Components

### LLM Integration
The app uses Anthropic's Claude as the LLM provider:
- Model: `claude-3-5-sonnet-20241022`
- Features: Ephemeral caching for improved performance with repeated context
- Max tokens: 2048 for comprehensive responses

### Data Structure
- Weekly meal plans are stored as text files in `data/` directory
- Each file contains meal schedules for Monday-Thursday
- Files include meal descriptions, prep instructions, and ingredient lists
- PDF recipes are stored in `pdfs/` and converted to text format

### Authentication
API key is stored in `.streamlit/secrets.toml` (not tracked in git):
- `ANTHROPIC_API_KEY` - Required for Claude API access

## Common Development Tasks

### Running the Application
```bash
# Activate virtual environment
source mea-prep/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run Streamlit app
streamlit run meal-prep-assistant.py
```

### Converting PDFs to Text
```bash
# Run the PDF converter (requires valid API key in secrets)
python convert-recipes-pdf-to-text.py
```

### Development Environment
The project uses a Python virtual environment located in `mea-prep/`. Key dependencies include:
- streamlit (1.43.2) - Web application framework
- anthropic (0.49.0) - Claude API client
- pypdf (5.3.1) - PDF processing for recipe conversion

## File Organization

- Root level contains main application files
- `data/` - Weekly meal plan text files
- `pdfs/` - Source PDF recipe files (not tracked)
- `.streamlit/` - Streamlit configuration and secrets
- `mea-prep/` - Python virtual environment

## Important Notes

- Uses Anthropic Claude with ephemeral caching for improved performance
- The system prompt in `meal-prep-assistant.md` defines how the assistant should behave and format responses
- Recipe data follows a specific format with meals listed by day and detailed prep instructions
- The app maintains chat history using Streamlit's session state
- Error handling includes user-friendly messages for API failures