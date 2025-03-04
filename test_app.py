#!/usr/bin/env python3
"""
AIRG-LangGraph - Test Application
Tests the application with example data
"""

import os
import sys
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Check if Gemini API key is set
if not os.environ.get("GEMINI_API_KEY"):
    print("Error: GEMINI_API_KEY environment variable is not set.")
    print("Please set it in your .env file or environment.")
    sys.exit(1)

# Check if example templates exist
if not os.path.exists("examples/resume_template.docx") or not os.path.exists("examples/cover_letter_template.docx"):
    print("Example templates not found. Creating them...")
    from create_example_templates import create_resume_template, create_cover_letter_template
    create_resume_template()
    create_cover_letter_template()

# Import the application
from app import run_graph

# Example data
example_data = {
    "resume_template_path": "examples/resume_template.docx",
    "cover_letter_template_path": "examples/cover_letter_template.docx",
    "job_title": "Software Engineer",
    "company_name": "Example Corp",
    "job_description": """
    We are looking for a Software Engineer to join our team. The ideal candidate will have:
    - 3+ years of experience in Python development
    - Experience with web frameworks like Flask or Django
    - Knowledge of database systems like PostgreSQL
    - Familiarity with cloud platforms like AWS or GCP
    - Strong problem-solving skills and attention to detail
    
    Responsibilities:
    - Develop and maintain backend services
    - Collaborate with frontend developers to integrate user-facing elements
    - Write clean, maintainable, and efficient code
    - Participate in code reviews and provide constructive feedback
    """,
    "company_overview": """
    Example Corp is a leading technology company specializing in cloud-based solutions.
    We are dedicated to creating innovative products that help businesses streamline their operations.
    Our team is passionate about technology and committed to delivering high-quality software.
    """,
    "hirer_name": "John Smith",
    "hirer_gender": "male",
    "relevant_experience": """
    I have worked on several Python projects using Flask and Django.
    I am familiar with PostgreSQL and have experience deploying applications on AWS.
    I enjoy solving complex problems and am committed to writing clean, maintainable code.
    """,
    "output_file_name": "test_output",
}

# Run the application
print("Testing the application with example data...")
result = run_graph(example_data)

# Display the result
print("\nTest completed successfully!")
print(f"Resume DOCX: {result['resume_docx_path']}")
print(f"Resume PDF: {result['resume_pdf_path']}")
print(f"Cover Letter DOCX: {result['cover_letter_docx_path']}")
print(f"Cover Letter PDF: {result['cover_letter_pdf_path']}")
print("\nYou can now open these files to see the generated documents.")