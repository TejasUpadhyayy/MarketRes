import os
os.environ["GRPC_VERBOSITY"] = "ERROR"
from dotenv import load_dotenv
import google.generativeai as genai

# Load environment variables from .env file
load_dotenv()

# Configure Gemini
gemini_api_key = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=gemini_api_key)

# Initialize Gemini model
model = genai.GenerativeModel('gemini-pro')

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
    return response.text  # Ensure this returns a string

# Example usage
if __name__ == "__main__":
    # Example input (replace with actual research summary from Industry Research Agent)
    company_name = "Tesla"
    industry = "Automotive"
    research_summary = """
    Tesla is a leader in electric vehicles and autonomous driving technology. The automotive industry is shifting towards electric vehicles, AI-driven manufacturing, and enhanced customer experiences.
    """

    # Generate use cases
    use_cases = generate_use_cases(company_name, industry, research_summary)
    print("Generated Use Cases:\n", use_cases)