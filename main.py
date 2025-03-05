#!/usr/bin/env python3
"""
AIRG-LangGraph - AI Resume Generator using LangChain and LangGraph
Main entry point for the application
"""

import os
import sys
import click
from dotenv import load_dotenv
from typing import Optional

# Load environment variables from .env file
load_dotenv()

# Import the LangGraph application
from app import run_graph

@click.command()
@click.option(
    "--resume-template",
    type=click.Path(exists=True),
    help="Path to the resume DOCX template",
)
@click.option(
    "--cover-letter-template",
    type=click.Path(exists=True),
    help="Path to the cover letter DOCX template",
)
@click.option("--job-title", help="Job title")
@click.option("--company-name", help="Company name")
@click.option("--job-description", help="Job description")
@click.option("--company-overview", help="Company overview")
@click.option("--hirer-name", help="Name of the hiring manager (optional)")
@click.option(
    "--hirer-gender",
    type=click.Choice(["male", "female", "unknown"], case_sensitive=False),
    help="Gender of the hiring manager (optional)",
)
@click.option("--relevant-experience", help="Additional relevant experience (optional)")
@click.option("--output-file-name", help="Output file name without extension")
@click.option(
    "--interactive/--no-interactive",
    default=False,
    help="Run in interactive mode, prompting for missing values",
)
def main(
    resume_template: Optional[str],
    cover_letter_template: Optional[str],
    job_title: Optional[str],
    company_name: Optional[str],
    job_description: Optional[str],
    company_overview: Optional[str],
    hirer_name: Optional[str],
    hirer_gender: Optional[str],
    relevant_experience: Optional[str],
    output_file_name: Optional[str],
    interactive: bool,
):
    """
    AIRG-LangGraph: AI Resume Generator using LangChain and LangGraph
    
    This tool generates customized resumes and cover letters based on job descriptions
    and company information using Google's Gemini AI.
    """
    # Check if Gemini API key is set
    if not os.environ.get("GEMINI_API_KEY"):
        click.echo(
            "Error: GEMINI_API_KEY environment variable is not set. "
            "Please set it in your .env file or environment."
        )
        sys.exit(1)

    # If interactive mode is enabled, prompt for missing values
    if interactive:
        if not resume_template:
            resume_template = click.prompt(
                "Path to source resume", type=click.Path(exists=True)
            )
        if not cover_letter_template:
            cover_letter_template = click.prompt(
                "Path to source cover letter", type=click.Path(exists=True)
            )
        if not job_title:
            job_title = click.prompt("Job title")
        if not company_name:
            company_name = click.prompt("Company name")
        if not job_description:
            job_description = click.prompt("Job description", default="")
        if not company_overview:
            company_overview = click.prompt("Company overview", default="")
        if not hirer_name:
            hirer_name = click.prompt("Hirer name (optional)", default="")
        if not hirer_gender:
            hirer_gender = click.prompt(
                "Hirer gender (male/female/unknown)", default="unknown"
            )
        if not relevant_experience:
            relevant_experience = click.prompt("Relevant experience (optional)", default="")
        if not output_file_name:
            output_file_name = click.prompt(
                "Output file name (without extension)",
                default=f"{company_name}_{job_title}".replace(" ", "_").lower(),
            )
    else:
        # Check if required parameters are provided
        if not all([resume_template, cover_letter_template, job_title, company_name]):
            click.echo(
                "Error: Missing required parameters. "
                "Please provide --resume-template, --cover-letter-template, "
                "--job-title, and --company-name, or use --interactive mode."
            )
            sys.exit(1)
        
        # Set default values for optional parameters
        if not output_file_name:
            output_file_name = f"{company_name}_{job_title}".replace(" ", "_").lower()
        if not hirer_gender:
            hirer_gender = "unknown"

    # Create input data for the graph
    input_data = {
        "resume_source_path": resume_template,
        "cover_letter_source_path": cover_letter_template,
        "job_title": job_title,
        "company_name": company_name,
        "job_description": job_description or "",
        "company_overview": company_overview or "",
        "hirer_name": hirer_name or "",
        "hirer_gender": hirer_gender,
        "relevant_experience": relevant_experience or "",
        "output_file_name": output_file_name,
    }

    # Run the graph
    click.echo("Starting document generation...")
    result = run_graph(input_data)
    
    # Display the result
    click.echo("\nDocument generation complete!")
    click.echo(f"Resume DOCX: {result['resume_docx_path']}")
    click.echo(f"Resume PDF: {result['resume_pdf_path']}")
    click.echo(f"Cover Letter DOCX: {result['cover_letter_docx_path']}")
    click.echo(f"Cover Letter PDF: {result['cover_letter_pdf_path']}")


if __name__ == "__main__":
    main()