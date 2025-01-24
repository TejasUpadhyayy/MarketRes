import requests
from bs4 import BeautifulSoup
from huggingface_hub import HfApi
import kaggle

def extract_keywords(use_case):
    """
    Extract keywords from a use case description.
    """
    # Example: Extract the first few words or specific terms
    keywords = use_case.split(":")[0]  # Use the part before the colon
    return keywords

def search_huggingface_datasets(use_case):
    """
    Search for datasets on Hugging Face using keywords extracted from the use case.
    """
    keywords = extract_keywords(use_case)
    api = HfApi()
    datasets = list(api.list_datasets(search=keywords))  # Search using keywords
    results = []
    for dataset in datasets[:5]:  # Limit results to the first 5 datasets
        description = "No description available"
        if hasattr(dataset, "cardData") and dataset.cardData:  # Check if cardData exists and is not None
            description = dataset.cardData.get("description", "No description available")
        results.append({
            "title": dataset.id,  # Use dataset.id as the title
            "url": f"https://huggingface.co/datasets/{dataset.id}",
            "description": description
        })
    return results

def search_kaggle_datasets(query, size=5):
    """
    Search for datasets on Kaggle.
    """
    datasets = kaggle.api.datasets_list(search=query)
    results = []
    for dataset in datasets[:size]:  # Limit results to the first `size` datasets
        results.append({
            "title": dataset.title,  # Use dataset.title as the title
            "url": f"https://www.kaggle.com/{dataset.ref}",
            "description": dataset.description
        })
    return results

def search_google_datasets(query, max_results=5):
    """
    Search for datasets using Google Dataset Search.
    """
    url = f"https://datasetsearch.research.google.com/search?query={query}&limit={max_results}"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    results = []
    for item in soup.find_all('div', class_='dataset-item'):
        title = item.find('div', class_='dataset-title').text.strip()
        link = item.find('a')['href']
        description = item.find('div', class_='dataset-description').text.strip()
        results.append({
            "title": title,  # Use the scraped title
            "url": link,
            "description": description
        })
    
    return results