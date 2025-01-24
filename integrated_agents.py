import os
from huggingface_hub import HfApi
from dotenv import load_dotenv
import google.generativeai as genai
from tavily import TavilyClient
from resource_asset_collection_agent import search_huggingface_datasets, search_kaggle_datasets, search_google_datasets

# Load environment variables from .env file
load_dotenv()

# Configure Gemini
gemini_api_key = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=gemini_api_key)

# Initialize Gemini model
model = genai.GenerativeModel('gemini-pro')

# Initialize Tavily client
tavily = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))

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
            "content": result['content']
        })
    
    return results

def generate_use_cases(company_name, industry, research_summary):
    """
    Generate AI/GenAI use cases for a company based on industry research.
    """
    prompt = f"""
    Company: {company_name}
    Industry: {industry}
    Research Summary: {research_summary}

    Generate 3-5 relevant AI or Generative AI (GenAI) use cases for this company. Focus on improving operations, customer experience, or innovation. Provide a brief description for each use case.
    """

    # Generate use cases using Gemini
    response = model.generate_content(prompt)
    return response.text

def search_huggingface_datasets(query, size=5):
    """
    Search for datasets on Hugging Face.
    """
    api = HfApi()
    datasets = list(api.list_datasets(search=query))  # Convert generator to list
    results = []
    for dataset in datasets[:size]:  # Limit results to the first `size` datasets
        description = "No description available"
        if hasattr(dataset, "cardData") and dataset.cardData:  # Check if cardData exists and is not None
            description = dataset.cardData.get("description", "No description available")
        results.append({
            "title": dataset.id,
            "url": f"https://huggingface.co/datasets/{dataset.id}",
            "description": description
        })
    return results

def save_to_markdown(use_case, datasets, filename="resources.md"):
    """
    Save dataset links to a markdown file.
    """
    with open(filename, "a") as file:
        file.write(f"## Use Case: {use_case}\n")
        for dataset in datasets:
            file.write(f"- **{dataset['title']}**: [Link]({dataset['url']})\n")
            file.write(f"  - Description: {dataset['description']}\n")  # Always write the description
        file.write("\n")  # Add a newline after each use case

# Main workflow
if __name__ == "__main__":
    # Input: Company name and industry
    company_name = "Tesla"
    industry = "Automotive"

    # Step 1: Industry Research
    research_results = industry_research(company_name, industry)
    research_summary = "\n".join([result['content'] for result in research_results])

    # Step 2: Generate Use Cases
    use_cases = generate_use_cases(company_name, industry, research_summary)
    print("Generated Use Cases:\n", use_cases)

    # Step 3: Find Datasets for Each Use Case
    for use_case in use_cases.split("\n"):
        if use_case.strip():  # Skip empty lines
            datasets = search_huggingface_datasets(use_case)
            save_to_markdown(use_case, datasets)

    print("Datasets saved to resources.md")