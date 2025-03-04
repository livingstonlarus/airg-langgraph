# AIRG-LangGraph Setup Guide

This guide provides detailed, step-by-step instructions for setting up and building the AIRG-LangGraph project.

## Environment Setup

### 1. Create a Virtual Environment

```bash
# Navigate to the project directory
cd airg-langgraph

# Create a virtual environment
python -m venv venv

# Activate the virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
# venv\Scripts\activate
```

### 2. Install Dependencies

```bash
# Install the required packages
pip install langchain langchain-core langgraph
pip install langgraph-checkpoint-sqlite  # For local development
pip install python-docx weasyprint google-generativeai
```

### 3. Set Up Environment Variables

Create a `.env` file in the project root:

```bash
# Create .env file
touch .env

# Edit the file with your preferred editor
# Add the following variables:
# GEMINI_API_KEY=your_gemini_api_key
```

Make sure to replace `your_gemini_api_key` with your actual Gemini API key from [Google AI Studio](https://aistudio.google.com/app/apikey).

## Project Configuration

### 1. Prepare DOCX Templates

1. Create or obtain DOCX templates for your resume and cover letter
2. Add placeholders in the format `{{PLACEHOLDER_NAME}}` where you want dynamic content
3. Common placeholders include:
   - `{{JOB_TITLE}}`
   - `{{COMPANY_NAME}}`
   - `{{HIRER_NAME}}`
   - `{{SKILLS}}`
   - `{{EXPERIENCE}}`

### 2. Configure Output Directory

The application will create an `output` directory in the project root to store generated documents. You can modify this path in the configuration if needed.

## Running the Application

### Local Development

```bash
# Make sure your virtual environment is activated
source venv/bin/activate  # On macOS/Linux

# Run the application
python main.py
```

### Using the CLI Interface

The application provides a command-line interface for easy use:

```bash
python main.py --resume-template path/to/resume.docx --cover-letter-template path/to/cover_letter.docx --job-title "Software Engineer" --company-name "Example Corp" --job-description "Job description text..." --company-overview "Company overview text..."
```

For interactive mode:

```bash
python main.py --interactive
```

## Deployment to LangGraph Platform

### 1. Prepare for Deployment

```bash
# Install LangGraph Cloud CLI
pip install langgraph-cli

# Login to LangGraph Cloud
langgraph login
```

### 2. Configure Deployment

Create a `langgraph.json` file in the project root:

```json
{
  "name": "airg-langgraph",
  "entrypoint": "app:graph"
}
```

### 3. Deploy

```bash
# Deploy to LangGraph Cloud
langgraph deploy
```

### 4. Access Your Deployed Application

After deployment, you'll receive a URL where your application is hosted. You can interact with it via API calls or through the LangGraph Studio interface.

## Troubleshooting

### WeasyPrint Dependencies

WeasyPrint requires some system dependencies. If you encounter issues:

- On macOS:
  ```bash
  brew install pango libffi
  ```

- On Ubuntu/Debian:
  ```bash
  sudo apt-get install build-essential python3-dev python3-pip python3-setuptools python3-wheel python3-cffi libcairo2 libpango-1.0-0 libpangocairo-1.0-0 libgdk-pixbuf2.0-0 libffi-dev shared-mime-info
  ```

### LangGraph Version Issues

If you encounter compatibility issues with LangGraph:

```bash
# Check installed version
pip show langgraph

# Upgrade to latest version if needed
pip install --upgrade langgraph
```

## Next Steps

After setting up the project, you can:

1. Customize the templates to match your preferred style
2. Modify the prompts in the code to improve the AI-generated content
3. Extend the application with additional features like job scraping