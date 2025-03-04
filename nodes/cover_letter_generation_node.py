"""
AIRG-LangGraph - Cover Letter Generation Node
Generates content for the cover letter based on the template and job details
"""

from typing import Dict, Any
from utils.llm_utils import generate_cover_letter_content


def generate_cover_letter(state: Dict[str, Any]) -> Dict[str, Any]:
    """
    Generate content for the cover letter
    
    Args:
        state: Current state of the graph
        
    Returns:
        Updated state with generated cover letter content
    """
    # Create a new state dictionary to avoid modifying the input state
    new_state = state.copy()
    
    # Generate cover letter content
    cover_letter_content = generate_cover_letter_content(
        cover_letter_template_content=state["cover_letter_template_content"],
        job_title=state["job_title"],
        company_name=state["company_name"],
        job_description=state["job_description"],
        company_overview=state["company_overview"],
        hirer_name=state["hirer_name"],
        hirer_gender=state["hirer_gender"],
        relevant_experience=state["relevant_experience"],
    )
    
    # Add the generated content to the state
    new_state["cover_letter_content"] = cover_letter_content
    
    return new_state