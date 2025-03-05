"""
AIRG-LangGraph - Input Node
Processes and validates input data
"""

import os
from typing import Dict, Any


def process_input(state: Dict[str, Any]) -> Dict[str, Any]:
    """
    Process and validate input data
    
    Args:
        state: Current state of the graph
        
    Returns:
        Updated state with validated input data
    """
    # Create a new state dictionary to avoid modifying the input state
    new_state = state.copy()
    
    # Validate required fields
    required_fields = [
        "resume_source_path",
        "cover_letter_source_path",
        "job_title",
        "company_name",
    ]

    for field in required_fields:
        if field not in state or not state[field]:
            raise ValueError(f"Missing required field: {field}")
    
    # Validate template paths
    for field in ["resume_source_path", "cover_letter_source_path"]:
        if not os.path.exists(state[field]):
            raise ValueError(f"Template file does not exist: {state[field]}")
    
    # Set default values for optional fields
    optional_fields = {
        "job_description": "",
        "company_overview": "",
        "hirer_name": "",
        "hirer_gender": "unknown",
        "relevant_experience": "",
    }
    
    for field, default_value in optional_fields.items():
        if field not in state or not state[field]:
            new_state[field] = default_value
    
    # Validate hirer_gender
    if new_state["hirer_gender"] not in ["male", "female", "unknown"]:
        new_state["hirer_gender"] = "unknown"
    
    # Set default output file name if not provided
    if "output_file_name" not in state or not state["output_file_name"]:
        new_state["output_file_name"] = f"{new_state['company_name']}_{new_state['job_title']}".replace(" ", "_").lower()
    
    # Create output directory if it doesn't exist
    os.makedirs("output", exist_ok=True)
    
    return new_state