"""
AIRG-LangGraph - Document Creation Node
Updates templates with generated content and creates PDF files
"""

import os
from typing import Dict, Any
from utils.docx_utils import update_template, save_document
from utils.pdf_utils import docx_to_pdf


def create_documents(state: Dict[str, Any]) -> Dict[str, Any]:
    """
    Create documents by updating templates with generated content
    
    Args:
        state: Current state of the graph
        
    Returns:
        Updated state with paths to the generated documents
    """
    # Create a new state dictionary to avoid modifying the input state
    new_state = state.copy()
    
    # Create output directory if it doesn't exist
    output_dir = os.path.join("output", state["output_file_name"])
    os.makedirs(output_dir, exist_ok=True)
    
    # Update and save the resume
    resume_doc = update_template(
        state["resume_template_content"]["document"],
        state["resume_content"],
    )
    resume_docx_path = os.path.join(output_dir, "resume.docx")
    save_document(resume_doc, resume_docx_path)
    new_state["resume_docx_path"] = resume_docx_path
    
    # Update and save the cover letter
    cover_letter_doc = update_template(
        state["cover_letter_template_content"]["document"],
        state["cover_letter_content"],
    )
    cover_letter_docx_path = os.path.join(output_dir, "cover_letter.docx")
    save_document(cover_letter_doc, cover_letter_docx_path)
    new_state["cover_letter_docx_path"] = cover_letter_docx_path
    
    # Generate PDF files
    resume_pdf_path = os.path.join(output_dir, "resume.pdf")
    docx_to_pdf(resume_docx_path, resume_pdf_path)
    new_state["resume_pdf_path"] = resume_pdf_path
    
    cover_letter_pdf_path = os.path.join(output_dir, "cover_letter.pdf")
    docx_to_pdf(cover_letter_docx_path, cover_letter_pdf_path)
    new_state["cover_letter_pdf_path"] = cover_letter_pdf_path
    
    return new_state