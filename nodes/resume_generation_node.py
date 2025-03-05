"""
AIRG-LangGraph - Resume Generation Node
Generates content for the resume based on the template and job details
"""

from typing import Dict, Any
from utils.llm_utils import generate_resume_content
from utils.docx_utils import process_template


def generate_resume(state: Dict[str, Any]) -> Dict[str, Any]:
    """
    Generate content for the resume

    Args:
        state: Current state of the graph

    Returns:
        Updated state with generated resume content
    """
    # Create a new state dictionary to avoid modifying the input state
    new_state = state.copy()

    # Process the resume template
    resume_template_content = process_template(state["resume_source_path"])
    new_state["resume_template_content"] = resume_template_content

    # Generate resume content
    resume_content = generate_resume_content(
        resume_template_content=resume_template_content,
        job_title=state["job_title"],
        company_name=state["company_name"],
        job_description=state["job_description"],
        company_overview=state["company_overview"],
        relevant_experience=state["relevant_experience"],
    )

    # Add the generated content to the state
    new_state["resume_content"] = resume_content

    return new_state