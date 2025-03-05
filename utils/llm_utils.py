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
) -> Dict[str, List[str]]:
    """
    Generate updated content for a resume based on the existing content and job details
    
    Args:
        resume_template_content: Dictionary containing the resume document content and sections
        job_title: Job title
        company_name: Company name
        job_description: Job description
        company_overview: Company overview
        relevant_experience: Additional relevant experience
        
    Returns:
        Dictionary mapping section names to their updated content
    """
    # Get the sections from the template
    sections = resume_template_content["sections"]
    
    # Create a system prompt
    system_prompt = """
    You are an expert resume writer. Your task is to customize a resume for a specific job application.
    You will be given the existing content of a resume, organized by sections, along with a job description
    and company information.
    
    Your goal is to make subtle, targeted improvements to the resume to better match the job requirements.
    Focus on the following sections:
    1. Summary/Profile - Update to highlight skills and experiences relevant to this specific job
    2. Experience - Emphasize achievements and responsibilities that align with the job requirements
    3. Skills - Prioritize and enhance skills mentioned in the job description
    
    IMPORTANT INSTRUCTIONS:
    1. Analyze the job description, company overview, and any additional relevant experience carefully
    2. Make subtle and professional modifications to the content
    3. DO NOT completely rewrite sections - maintain the original structure and most of the content
    4. DO NOT modify personal information, contact details, or education sections
    5. If additional relevant experience was provided, incorporate it naturally into the appropriate sections
    6. Add relevant keywords from the job description naturally within the existing text
    7. Keep the tone professional and consistent with the original resume
    
    Format your response as a JSON object where each key is a section name and each value is an array of strings
    representing the updated content for that section. Include ALL sections from the original resume.
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
    
    Original Resume Content by Section:
    {sections}
    
    Please provide updated content for each section that is subtly tailored to this specific job application.
    Return your response as a JSON object where each key is a section name and each value is an array of strings
    representing the updated content for that section.
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
        "sections": json.dumps(sections, indent=2),
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
) -> Dict[str, List[str]]:
    """
    Generate updated content for a cover letter based on the existing content and job details
    
    Args:
        cover_letter_template_content: Dictionary containing the cover letter document content and sections
        job_title: Job title
        company_name: Company name
        job_description: Job description
        company_overview: Company overview
        hirer_name: Name of the hiring manager
        hirer_gender: Gender of the hiring manager (male, female, or unknown)
        relevant_experience: Additional relevant experience
        
    Returns:
        Dictionary mapping section names to their updated content
    """
    # Get the sections from the template
    sections = cover_letter_template_content["sections"]
    
    # Create a system prompt
    system_prompt = """
    You are an expert cover letter writer. Your task is to customize a cover letter for a specific job application.
    You will be given the existing content of a cover letter, organized by sections, along with a job description
    and company information.
    
    Your goal is to make targeted improvements to the cover letter to better match the job requirements and company culture.
    
    IMPORTANT INSTRUCTIONS:
    1. Analyze the company overview and job description to determine if the company is:
       a) The actual employer (direct hiring)
       b) A recruitment agency/headhunter
    2. If it's a recruitment agency:
       - Address the letter to the recruiter
       - Mention your interest in their CLIENT company (from job description)
       - Don't focus on joining the recruitment agency itself
    3. If it's direct hiring:
       - Address the letter to the hiring manager
       - Focus on joining their company
    4. Make professional modifications to the content to highlight relevant skills and experiences
    5. DO NOT completely rewrite sections - maintain the original structure and tone
    6. DO NOT modify personal information or contact details
    7. If additional relevant experience was provided, incorporate it naturally into the appropriate sections
    8. Add relevant keywords from the job description naturally within the existing text
    9. Keep the tone professional, enthusiastic, and tailored to the specific job and company
    
    Format your response as a JSON object where each key is a section name and each value is an array of strings
    representing the updated content for that section. Include ALL sections from the original cover letter.
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
    
    Original Cover Letter Content by Section:
    {sections}
    
    Please provide updated content for each section that is tailored to this specific job application.
    If the hiring manager's name is provided, address the cover letter to them appropriately based on their gender.
    If no hiring manager is specified, use an appropriate general greeting.
    
    Return your response as a JSON object where each key is a section name and each value is an array of strings
    representing the updated content for that section.
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
        "sections": json.dumps(sections, indent=2),
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