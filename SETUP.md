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
### 2. Install WeasyPrint Dependencies (macOS)

On macOS, the easiest way to install WeasyPrint and its dependencies is to use [Homebrew](https://brew.sh/):

```bash
brew install pango libffi
```

### 3. Install Dependencies

```bash
# Install the required packages from requirements.txt
pip install -r requirements.txt
```
### 4. Set Up Environment Variables

```bash
# Create .env file
cp .env.example .env

# Edit the file with your preferred editor
# Edit the following variables:
# GEMINI_API_KEY=your_gemini_api_key
# LANGSMITH_API_KEY=your_langsmith_api_key
```

Make sure to replace:
- `your_gemini_api_key` with your actual Gemini API key from [Google AI Studio](https://aistudio.google.com/app/apikey)
- `your_langsmith_api_key` with your LangSmith API key from [LangSmith Settings](https://smith.langchain.com/settings) (required for LangGraph Studio)
Make sure to replace `your_gemini_api_key` with your actual Gemini API key from [Google AI Studio](https://aistudio.google.com/app/apikey).

## Project Configuration

### 1. Configure Output Directory

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

## Using LangGraph Studio for Development and Testing

### 1. Prepare for Development

```bash
# Install LangGraph CLI
# and LangChain OpenAI (required by LangSmith)
pip install langgraph-cli langchain-openai

# Install the inmem extra for development mode
pip install -U "langgraph-cli[inmem]"
```

### 2. Configure LangGraph

The project already includes a `langgraph.json` file in the project root.

### 3. Run in Development Mode

```bash
# Run LangGraph API server in development mode
langgraph dev
```

This will start a local API server at http://127.0.0.1:2024 with hot reloading capabilities.

### 4. Access LangGraph Studio

Your browser will automatically open the LangGraph Studio interface at `https://smith.langchain.com/studio/?baseUrl=http://127.0.0.1:2024`. You can use this to visualize and debug your graph execution.

You may need to pass the LangSmith onboarding (`smith.langchain.com/onboarding?organizationId=...`) first by setting credentials and having a project name generated, then to edit environment variables in .env:
```
LANGSMITH_TRACING=true
LANGSMITH_ENDPOINT="the_langsmith_endpoint_url"
LANGSMITH_API_KEY="your_langsmith_api_key"
LANGSMITH_PROJECT="your_assigned_project_name"
OPENAI_API_KEY="your_openai_api_key"
```

### 5. Deploying

#### A. Docker

To build a Docker image for production:

```bash
# Build a Docker image
langgraph build -t airg-langgraph

# Run the Docker image
langgraph up
```

Building a Docker image encapsulates the application and its dependencies into a portable, self-contained unit. This ensures consistent execution across various environments, from local development machines to cloud-based deployments. The resulting Docker image can be deployed on platforms such as a Virtual Private Server (VPS) or a Kubernetes (K8s) cluster, facilitating scalable and reliable cloud execution.

#### B. LangGraph Platform (Cloud SaaS)

Follow instructions at: https://langchain-ai.github.io/langgraph/cloud/quick_start/

⚠️ From the LangGraph Platform screen (`smith.langchain.com/o/.../host`) you may read "One-click deployments of LangGraph applications" but may not find a "New Deployment" button as described in the Quick Start guide. That's probably because you are on the free Developer plan. As stated in the screen, to be able to deploy to LangGraph Cloud, you need to be on Plus, Premier, Startup, or Enterprise plans: https://www.langchain.com/pricing-langsmith

## Troubleshooting

### WeasyPrint Dependencies

WeasyPrint requires some system dependencies. If you encounter issues:

- On macOS:
  ```bash
  brew install pango libffi
  ```
  
  **Optional (but recommended if you encounter issues):**
  
  After installing `libffi` with Homebrew, you might need to set the following environment variables for compilers and `pkg-config` to find it. Add these lines to your shell configuration file (e.g., `~/.bashrc`, `~/.zshrc`):
  
  ```bash
  export LDFLAGS="-L/opt/homebrew/opt/libffi/lib"
  export CPPFLAGS="-I/opt/homebrew/opt/libffi/include"
  export PKG_CONFIG_PATH="/opt/homebrew/opt/libffi/lib/pkgconfig"
  export DYLD_FALLBACK_LIBRARY_PATH=/opt/homebrew/lib:$DYLD_FALLBACK_LIBRARY_PATH
  ```
  
  Then, source your shell configuration file or open a new terminal for the changes to take effect. For example:
  
  ```bash
  source ~/.zshrc  # Or ~/.bashrc, depending on your shell
  ```

- On Ubuntu/Debian:
  ```bash
  sudo apt-get install build-essential python3-dev python3-pip python3-setuptools python3-wheel python3-cffi libcairo2 libpango-1.0-0 libpangocairo-1.0-0 libgdk-pixbuf2.0-0 libffi-dev shared-mime-info
  ```
