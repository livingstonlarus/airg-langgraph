"""
AIRG-LangGraph - Utilities for working with DOCX files
"""

import re
import os
from typing import Dict, List, Tuple, Any
from docx import Document


def read_template(template_path: str) -> Tuple[Document, str]:
    """
    Read a DOCX template and extract its text content
    
    Args:
        template_path: Path to the DOCX template
        
    Returns:
        Tuple containing the Document object and the text content
    """
    # Load the document
    doc = Document(template_path)
    
    # Extract text from the document
    text_content = ""
    for paragraph in doc.paragraphs:
        text_content += paragraph.text + "\n"
    
    for table in doc.tables:
        for row in table.rows:
            for cell in row.cells:
                for paragraph in cell.paragraphs:
                    text_content += paragraph.text + "\n"
    
    return doc, text_content


def extract_placeholders(text_content: str) -> List[str]:
    """
    Extract placeholders from text content
    
    Args:
        text_content: Text content to extract placeholders from
        
    Returns:
        List of placeholders found in the text content
    """
    # Find all placeholders in the format {{PLACEHOLDER}}
    placeholders = re.findall(r'{{([^}]+)}}', text_content)
    
    # Remove duplicates and return
    return list(set(placeholders))


def update_template(doc: Document, replacements: Dict[str, str]) -> Document:
    """
    Update a DOCX template with the provided replacements
    
    Args:
        doc: Document object to update
        replacements: Dictionary mapping placeholders to their replacements
        
    Returns:
        Updated Document object
    """
    # Update paragraphs
    for paragraph in doc.paragraphs:
        for placeholder, replacement in replacements.items():
            if f"{{{{{placeholder}}}}}" in paragraph.text:
                paragraph.text = paragraph.text.replace(f"{{{{{placeholder}}}}}", replacement)
    
    # Update tables
    for table in doc.tables:
        for row in table.rows:
            for cell in row.cells:
                for paragraph in cell.paragraphs:
                    for placeholder, replacement in replacements.items():
                        if f"{{{{{placeholder}}}}}" in paragraph.text:
                            paragraph.text = paragraph.text.replace(f"{{{{{placeholder}}}}}", replacement)
    
    return doc


def save_document(doc: Document, output_path: str) -> str:
    """
    Save a Document object to a file
    
    Args:
        doc: Document object to save
        output_path: Path to save the document to
        
    Returns:
        Path to the saved document
    """
    # Create the directory if it doesn't exist
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    # Save the document
    doc.save(output_path)
    
    return output_path


def process_template(template_path: str) -> Dict[str, Any]:
    """
    Process a DOCX template and extract its content and placeholders
    
    Args:
        template_path: Path to the DOCX template
        
    Returns:
        Dictionary containing the Document object, text content, and placeholders
    """
    # Read the template
    doc, text_content = read_template(template_path)
    
    # Extract placeholders
    placeholders = extract_placeholders(text_content)
    
    return {
        "document": doc,
        "text_content": text_content,
        "placeholders": placeholders,
    }