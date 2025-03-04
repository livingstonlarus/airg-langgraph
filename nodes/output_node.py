"""
AIRG-LangGraph - Output Node
Prepares the final output of the graph
"""

from typing import Dict, Any


def prepare_output(state: Dict[str, Any]) -> Dict[str, Any]:
    """
    Prepare the final output of the graph
    
    Args:
        state: Current state of the graph
        
    Returns:
        Final output with paths to the generated documents
    """
    # Create a new state dictionary to avoid modifying the input state
    new_state = state.copy()
    
    # Extract only the necessary output fields
    output_fields = [
        "resume_docx_path",
        "resume_pdf_path",
        "cover_letter_docx_path",
        "cover_letter_pdf_path",
    ]
    
    # Validate that all output fields are present
    for field in output_fields:
        if field not in state:
            raise ValueError(f"Missing output field: {field}")
    
    # Add a success message
    new_state["message"] = "Document generation completed successfully"
    
    return new_state