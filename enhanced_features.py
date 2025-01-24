import os
from dotenv import load_dotenv
import google.generativeai as genai
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

# Load environment variables
load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel('gemini-pro')

class DocumentSearchSystem:
    def __init__(self):
        self.encoder = SentenceTransformer('all-MiniLM-L6-v2')
        self.document_embeddings = {}
        self.documents = {}

    def add_document(self, doc_id, content):
        self.documents[doc_id] = content
        self.document_embeddings[doc_id] = self.encoder.encode(content)

    def search(self, query, top_k=3):
        query_embedding = self.encoder.encode(query)
        scores = {}
        
        for doc_id, doc_embedding in self.document_embeddings.items():
            similarity = cosine_similarity(
                [query_embedding], 
                [doc_embedding]
            )[0][0]
            scores[doc_id] = similarity
        
        sorted_docs = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        return [(doc_id, self.documents[doc_id]) for doc_id, _ in sorted_docs[:top_k]]

class AutomatedReportGenerator:
    def __init__(self):
        self.model = genai.GenerativeModel('gemini-pro')

    def generate_report(self, research_data, use_cases, datasets):
        report_prompt = f"""
        Generate a comprehensive business report based on the following information:
        
        Research Data:
        {research_data}
        
        Use Cases:
        {use_cases}
        
        Available Datasets:
        {datasets}
        
        Create a structured report including:
        1. Executive Summary
        2. Market Analysis
        3. Proposed AI Solutions
        4. Implementation Roadmap
        5. Resource Requirements
        """
        
        response = self.model.generate_content(report_prompt)
        return response.text

class AIChatSystem:
    def __init__(self):
        self.model = genai.GenerativeModel('gemini-pro')
        self.context = {}

    def set_context(self, context):
        self.context = context

    def chat(self, user_input):
        # Create a contextual prompt
        screen_content = []
        if self.context.get('research_results'):
            screen_content.extend([r['content'] for r in self.context['research_results']])
        if self.context.get('use_cases'):
            screen_content.append(self.context['use_cases'])

        prompt = f"""
        Context:
        Company: {self.context.get('company', 'Not specified')}
        Industry: {self.context.get('industry', 'Not specified')}
        Current Screen Content: {' '.join(screen_content)}

        User Question: {user_input}

        Provide a helpful, context-aware response. Use the current screen content when relevant.
        """
        
        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            return f"I apologize, but I encountered an error: {str(e)}"