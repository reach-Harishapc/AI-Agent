import os
from typing import List, Dict
from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.tools import tool
import json

from dotenv import load_dotenv

# Load environment variables
load_dotenv("../.env")

# Set Google API key
if not os.environ.get('GOOGLE_API_KEY'):
    raise ValueError("GOOGLE_API_KEY not found in environment variables")

@tool
def draft_document(doc_type: str, parties: str, key_terms: str) -> str:
    """
    Drafts a real estate document based on provided details.
    Args:
        doc_type: Type of document (e.g., "Lease Agreement", "Purchase Contract").
        parties: Names of the parties involved (e.g., "Landlord: John Doe, Tenant: Jane Smith").
        key_terms: Key terms to include (e.g., "Rent: $2000, Term: 1 year, No pets").
    Returns:
        The content of the drafted document.
    """
    print(f"Drafting {doc_type} for {parties}...")
    # In a real app, this might use a specific prompt or template engine.
    # Here we let the LLM generate it via the agent's reasoning, but we could also return a template.
    # For this tool, we'll return a structured prompt for the LLM to expand upon in the final response,
    # or we can generate it here if we had a separate chain. 
    # To keep it simple and agentic, we'll return the parameters as a confirmation 
    # and let the Agent's main LLM generate the full text in the final answer 
    # OR we can use a secondary call here. Let's return a success message with details.
    
    return json.dumps({
        "status": "success", 
        "message": f"Drafting parameters received for {doc_type}. Please generate the full document text based on these terms: {key_terms} for parties: {parties}."
    })

from pypdf import PdfReader

@tool
def review_document(file_path: str, query: str) -> str:
    """
    Reads a PDF document and extracts text to answer a specific query.
    Args:
        file_path: The absolute path to the PDF file.
        query: What to look for in the document (e.g., "What is the rent amount?", "Summarize the key terms").
    """
    print(f"Reviewing document {file_path} for: {query}...")
    try:
        reader = PdfReader(file_path)
        text = ""
        for page in reader.pages:
            text += page.extract_text()
        
        # Truncate text if too long to avoid token limits (basic handling)
        if len(text) > 10000:
            text = text[:10000] + "...[truncated]"
            
        return json.dumps({
            "content_snippet": text,
            "query": query
        })
    except Exception as e:
        return json.dumps({"error": f"Failed to read document: {str(e)}"})

# Initialize LLM
llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash", temperature=0)

# Define Tools
tools = [draft_document, review_document]

# Define Prompt
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are an expert Real Estate Document Handler. Your goal is to draft, review, and summarize legal documents accurately. When reviewing a document, use the `review_document` tool to read the content, then answer the user's question based on that content."),
    ("human", "{input}"),
    ("placeholder", "{agent_scratchpad}"),
])

# Create Agent
agent = create_tool_calling_agent(llm, tools, prompt)

# Create Executor
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

def main():
    # Test Drafting
    # user_input = "Draft a residential lease agreement between Landlord Alice and Tenant Bob for 123 Maple St. Rent is $1500/month, 12-month term starting Jan 1st."
    
    # Test Review
    import os
    pdf_path = os.path.abspath("sample_lease.pdf")
    user_input = f"Review the document at {pdf_path}. What is the rent amount and are pets allowed?"
    
    print(f"User Request: {user_input}")
    
    result = agent_executor.invoke({"input": user_input})
    print("\nAgent Response:\n", result['output'])

if __name__ == "__main__":
    main()
