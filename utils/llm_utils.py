"""
AIRG-LangGraph - Utilities for working with the Gemini LLM
"""

import os
from typing import Dict, List, Any
from google import genai
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser


def initialize_gemini():
    """
    Initialize the Gemini API
    """
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY environment variable is not set")
    
    # Create a client with the API key
    genai.configure(api_key=api_key)


def get_gemini_llm():
    """
    Get a LangChain ChatGoogleGenerativeAI instance
    
    Returns:
        ChatGoogleGenerativeAI instance
    """
    # Initialize Gemini if not already initialized
    initialize_gemini()
    
    # Create a LangChain ChatGoogleGenerativeAI instance
    llm = ChatGoogleGenerativeAI(
        model="gemini-2.0-pro-exp",
        temperature=0.2,
        convert_system_message_to_human=True,
    )
    
    return llm


def generate_resume_content(
    resume_template_content: Dict[str, Any],
    job_title: str,
    company_name: str,
    job_description: str,
    company_overview: str,
    relevant_experience: str = "",
) -> Dict[str, str]:
    """
    Generate content for a resume based on the template and job details
    
    Args:
        resume_template_content: Dictionary containing the resume template content and placeholders
        job_title: Job title
        company_name: Company name
        job_description: Job description
        company_overview: Company overview
        relevant_experience: Additional relevant experience
        
    Returns:
        Dictionary mapping placeholders to their generated content
    """
    # Get the placeholders from the template
    placeholders = resume_template_content["placeholders"]
    
    # Create a system prompt
    system_prompt = """
    You are an expert resume writer. Your task is to customize a resume for a specific job application.
    You will be given a job description, company information, and placeholders from a resume template.
    For each placeholder, generate appropriate content that highlights the candidate's skills and experience
    relevant to the job. Focus on keywords and skills mentioned in the job description.
    
    The content should be professional, concise, and tailored to the specific job and company.
    Do not invent specific details about the candidate's background, but focus on framing their
    existing skills and experience in a way that matches the job requirements.
    
    Format your response as a JSON object where each key is a placeholder name and each value is the
    generated content for that placeholder.
    """
    
    # Create a human prompt
    human_prompt = """
    Job Title: {job_title}
    Company: {company_name}
    
    Job Description:
    {job_description}
    
    Company Overview:
    {company_overview}
    
    Additional Relevant Experience:
    {relevant_experience}
    
    Placeholders to fill:
    {placeholders}
    
    Please generate content for each placeholder that is tailored to this specific job application.
    Return your response as a JSON object where each key is a placeholder name and each value is the
    generated content for that placeholder.
    """
    
    # Create a ChatPromptTemplate
    prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        ("human", human_prompt),
    ])
    
    # Get the LLM
    llm = get_gemini_llm()
    
    # Create a chain
    chain = prompt | llm | StrOutputParser()
    
    # Generate the content
    response = chain.invoke({
        "job_title": job_title,
        "company_name": company_name,
        "job_description": job_description,
        "company_overview": company_overview,
        "relevant_experience": relevant_experience,
        "placeholders": ", ".join(placeholders),
    })
    
    # Parse the response as JSON
    import json
    try:
        content = json.loads(response)
    except json.JSONDecodeError:
        # If the response is not valid JSON, extract it from the text
        import re
        json_match = re.search(r'```json\n(.*?)\n```', response, re.DOTALL)
        if json_match:
            try:
                content = json.loads(json_match.group(1))
            except json.JSONDecodeError:
                raise ValueError(f"Failed to parse LLM response as JSON: {response}")
        else:
            raise ValueError(f"Failed to parse LLM response as JSON: {response}")
    
    return content


def generate_cover_letter_content(
    cover_letter_template_content: Dict[str, Any],
    job_title: str,
    company_name: str,
    job_description: str,
    company_overview: str,
    hirer_name: str = "",
    hirer_gender: str = "unknown",
    relevant_experience: str = "",
) -> Dict[str, str]:
    """
    Generate content for a cover letter based on the template and job details
    
    Args:
        cover_letter_template_content: Dictionary containing the cover letter template content and placeholders
        job_title: Job title
        company_name: Company name
        job_description: Job description
        company_overview: Company overview
        hirer_name: Name of the hiring manager
        hirer_gender: Gender of the hiring manager (male, female, or unknown)
        relevant_experience: Additional relevant experience
        
    Returns:
        Dictionary mapping placeholders to their generated content
    """
    # Get the placeholders from the template
    placeholders = cover_letter_template_content["placeholders"]
    
    # Create a system prompt
    system_prompt = """
    You are an expert cover letter writer. Your task is to customize a cover letter for a specific job application.
    You will be given a job description, company information, and placeholders from a cover letter template.
    For each placeholder, generate appropriate content that highlights the candidate's interest in the job
    and relevant skills and experience.
    
    The content should be professional, enthusiastic, and tailored to the specific job and company.
    Do not invent specific details about the candidate's background, but focus on framing their
    existing skills and experience in a way that matches the job requirements.
    
    Format your response as a JSON object where each key is a placeholder name and each value is the
    generated content for that placeholder.
    """
    
    # Create a human prompt
    human_prompt = """
    Job Title: {job_title}
    Company: {company_name}
    Hiring Manager: {hirer_name}
    Hiring Manager Gender: {hirer_gender}
    
    Job Description:
    {job_description}
    
    Company Overview:
    {company_overview}
    
    Additional Relevant Experience:
    {relevant_experience}
    
    Placeholders to fill:
    {placeholders}
    
    Please generate content for each placeholder that is tailored to this specific job application.
    If the hiring manager's name is provided, address the cover letter to them appropriately based on their gender.
    If no hiring manager is specified, use an appropriate general greeting.
    
    Return your response as a JSON object where each key is a placeholder name and each value is the
    generated content for that placeholder.
    """
    
    # Create a ChatPromptTemplate
    prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        ("human", human_prompt),
    ])
    
    # Get the LLM
    llm = get_gemini_llm()
    
    # Create a chain
    chain = prompt | llm | StrOutputParser()
    
    # Generate the content
    response = chain.invoke({
        "job_title": job_title,
        "company_name": company_name,
        "job_description": job_description,
        "company_overview": company_overview,
        "hirer_name": hirer_name,
        "hirer_gender": hirer_gender,
        "relevant_experience": relevant_experience,
        "placeholders": ", ".join(placeholders),
    })
    
    # Parse the response as JSON
    import json
    try:
        content = json.loads(response)
    except json.JSONDecodeError:
        # If the response is not valid JSON, extract it from the text
        import re
        json_match = re.search(r'```json\n(.*?)\n```', response, re.DOTALL)
        if json_match:
            try:
                content = json.loads(json_match.group(1))
            except json.JSONDecodeError:
                raise ValueError(f"Failed to parse LLM response as JSON: {response}")
        else:
            raise ValueError(f"Failed to parse LLM response as JSON: {response}")
    
    return content