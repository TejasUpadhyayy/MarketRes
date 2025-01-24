import os
from dotenv import load_dotenv
from tavily import TavilyClient

load_dotenv()
tavily = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))

def get_consulting_insights(company, industry):
    sources = ['McKinsey', 'Deloitte', 'Nexocode']
    insights = {}
    
    for source in sources:
        query = f"{source} research reports AI ML adoption {industry} industry trends 2024"
        results = tavily.search(query=query, max_results=3)
        insights[source] = [
            {
                'title': r['title'],
                'content': r['content'],
                'url': r['url']
            } for r in results['results']
        ]
    
    return insights

def format_insights(insights):
    formatted = ""
    for source, reports in insights.items():
        formatted += f"\n### {source} Insights\n"
        for report in reports:
            formatted += f"- **{report['title']}**\n"
            formatted += f"  {report['content'][:300]}...\n"
            formatted += f"  [Read more]({report['url']})\n\n"
    return formatted