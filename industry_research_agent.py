import os
from dotenv import load_dotenv
from tavily import TavilyClient

# Load environment variables from .env file
load_dotenv()

# Initialize Tavily client with API key from .env
tavily = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))
gemini_api_key = os.getenv("GEMINI_API_KEY")

def industry_research(company_name, industry):
    """
    Perform industry and company research using Tavily.
    """
    query = f"Industry trends and company information for {company_name} in the {industry} sector"
    response = tavily.search(query=query, max_results=5)
    
    # Extract relevant information
    results = []
    for result in response['results']:
        results.append({
            "title": result['title'],
            "url": result['url'],
            "content": result['content']  # Full content
        })
    
    return results

# Example usage
if __name__ == "__main__":
    company_name = "Amazon"
    industry = "Retail"
    research_results = industry_research(company_name, industry)
    
    for result in research_results:
        print(f"Title: {result['title']}")
        print(f"URL: {result['url']}")
        print(f"Content: {result['content']}\n")