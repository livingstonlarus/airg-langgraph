"""
AIRG-LangGraph - Template Processing Node
Loads templates and extracts placeholders
"""

from typing import Dict, Any
from utils.docx_utils import process_template


def process_templates(state: Dict[str, Any]) -> Dict[str, Any]:
    """
    Process templates and extract placeholders
    
    Args:
        state: Current state of the graph
        
    Returns:
        Updated state with template content and placeholders
    """
    # Create a new state dictionary to avoid modifying the input state
    new_state = state.copy()
    
    # Process the resume template
    resume_template_content = process_template(state["resume_template_path"])
    new_state["resume_template_content"] = resume_template_content
    
    # Process the cover letter template
    cover_letter_template_content = process_template(state["cover_letter_template_path"])
    new_state["cover_letter_template_content"] = cover_letter_template_content
    
    return new_state