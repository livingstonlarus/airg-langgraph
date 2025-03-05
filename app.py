"""
AIRG-LangGraph - AI Resume Generator using LangChain and LangGraph
LangGraph application definition
"""

import os
from typing import Dict, Any, TypedDict, Annotated
from langgraph.graph import StateGraph, END
from langgraph.checkpoint.sqlite import SqliteSaver

# Import node functions
from nodes.input_node import process_input
from nodes.resume_generation_node import generate_resume
from nodes.cover_letter_generation_node import generate_cover_letter
from nodes.document_creation_node import create_documents
from nodes.output_node import prepare_output

# Define the state schema
class GraphState(TypedDict):
    # Input data
    resume_source_path: Annotated[str, "Path to the source resume DOCX file"]
    cover_letter_source_path: Annotated[str, "Path to the source cover letter DOCX file"]
    job_title: Annotated[str, "Job title"]
    company_name: Annotated[str, "Company name"]
    job_description: Annotated[str, "Job description"]
    company_overview: Annotated[str, "Company overview"]
    hirer_name: Annotated[str, "Name of the hiring manager"]
    hirer_gender: Annotated[str, "Gender of the hiring manager"]
    relevant_experience: Annotated[str, "Additional relevant experience"]
    output_file_name: Annotated[str, "Output file name without extension"]
    
    # Template content
    resume_template_content: Annotated[Dict[str, Any], "Processed resume template content"]
    cover_letter_template_content: Annotated[Dict[str, Any], "Processed cover letter template content"]
        
    # Generated content
    resume_content: Annotated[Dict[str, str], "Generated content for the resume"]
    cover_letter_content: Annotated[Dict[str, str], "Generated content for the cover letter"]
    
    # Output paths
    resume_docx_path: Annotated[str, "Path to the generated resume DOCX file"]
    resume_pdf_path: Annotated[str, "Path to the generated resume PDF file"]
    cover_letter_docx_path: Annotated[str, "Path to the generated cover letter DOCX file"]
    cover_letter_pdf_path: Annotated[str, "Path to the generated cover letter PDF file"]


def create_graph():
    """
    Create the LangGraph for the AIRG application
    """
    # Create a new graph
    builder = StateGraph(GraphState)
    
    # Add nodes to the graph
    builder.add_node("input", process_input)
    builder.add_node("resume_generation", generate_resume)
    builder.add_node("cover_letter_generation", generate_cover_letter)
    builder.add_node("document_creation", create_documents)
    builder.add_node("output", prepare_output)
    
    # Define the edges between nodes sequentially
    builder.add_edge("input", "resume_generation")
    builder.add_edge("resume_generation", "cover_letter_generation")
    builder.add_edge("cover_letter_generation", "document_creation")
    
    builder.add_edge("document_creation", "output")
    builder.add_edge("output", END)
    
    # Set the entry point of the graph
    builder.set_entry_point("input")

    # Create the graph
    return builder.compile()

def run_graph(input_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Run the LangGraph with the provided input data
    
    Args:
        input_data: Dictionary containing the input data for the graph
        
    Returns:
        Dictionary containing the output paths for the generated documents
    """
    # Create the graph
    graph = create_graph()

    # Set up persistence with SQLite
    # Create the output directory if it doesn't exist
    os.makedirs("output", exist_ok=True)

    # Create a SQLite checkpointer
    checkpointer = SqliteSaver.from_conn_string("sqlite:///output/airg_sessions.db")
    
    # Run the graph with the input data and checkpointer
    result = graph.invoke(input_data, {"checkpointer": checkpointer})
    
    # Return the result
    return result


# For LangGraph Cloud deployment
graph = create_graph()