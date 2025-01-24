import streamlit as st
import base64
from integrated_agents import industry_research, generate_use_cases
from resource_asset_collection_agent import search_huggingface_datasets, search_kaggle_datasets, search_google_datasets
from enhanced_features import DocumentSearchSystem, AutomatedReportGenerator, AIChatSystem
import streamlit.components.v1 as components
from chat_bubble import create_chat_bubble
from market_insights import get_consulting_insights, format_insights

def create_download_link(file_content, filename):
   b64 = base64.b64encode(file_content.encode()).decode()
   href = f'<a href="data:file/markdown;base64,{b64}" download="{filename}">Download {filename}</a>'
   return href

# Initialize states and components
if 'research_results' not in st.session_state:
    st.session_state.research_results = None
if 'use_cases' not in st.session_state:
    st.session_state.use_cases = None
if 'messages' not in st.session_state:  
    st.session_state.messages = []
if 'show_chat' not in st.session_state:
    st.session_state.show_chat = False

doc_search = DocumentSearchSystem()
report_generator = AutomatedReportGenerator()
chat_system = AIChatSystem()

st.title("AI Use Case Generator")
chat_container = st.container()

# Sidebar configuration
with st.sidebar:
   st.header("Input Parameters")
   company_name = st.text_input("Enter the company name:", "Tesla")
   industries = ["Automotive", "Healthcare", "Retail", "Finance", "Manufacturing", "Technology"]
   industry = st.selectbox("Select the industry:", industries)
   
   st.markdown("---")
   st.header("Enhanced Features")
   feature_choice = st.selectbox(
    "Select Feature",
    ["Use Case Generator", "Document Search", "Report Generator", "Market Analysis"]
    )

# Main content based on feature selection
if feature_choice == "Use Case Generator":
   if st.button("Generate Use Cases"):
       with st.spinner("Generating use cases..."):
           # Industry Research
           st.write("### Industry Research")
           research_results = industry_research(company_name, industry)
           st.session_state.research_results = research_results
           
           for result in research_results:
               st.write(f"- **{result['title']}**: [Link]({result['url']})")
               truncated_content = result['content'][:200] + "..." if len(result['content']) > 200 else result['content']
               st.write(f"  - {truncated_content}")
               
               if st.button("Read More", key=result['url']):
                   st.write(f"  - Full Content: {result['content']}")

           # Use Case Generation
           st.write("### Generated Use Cases")
           research_summary = "\n".join([result['content'] for result in research_results])
           use_cases = generate_use_cases(company_name, industry, research_summary)
           st.session_state.use_cases = use_cases
           use_cases_list = use_cases.split("\n")

           resources_content = f"# AI Use Cases for {company_name} in {industry}\n\n"
           resources_content += "## Generated Use Cases\n"
           resources_content += use_cases + "\n\n"
           resources_content += "## Relevant Datasets\n"

           for use_case in use_cases_list:
               if use_case.strip():
                   st.write(f"#### {use_case}")
                   try:
                       datasets = search_huggingface_datasets(use_case)
                       if not datasets:
                           datasets = search_kaggle_datasets(use_case)
                       if not datasets:
                           datasets = search_google_datasets(use_case)
                       
                       if datasets:
                           st.write("**Relevant Datasets:**")
                           resources_content += f"### {use_case}\n"
                           for dataset in datasets:
                               if isinstance(dataset, dict):
                                   st.write(f"- **{dataset['title']}**: [Link]({dataset['url']})")
                                   st.write(f"  - Description: {dataset['description']}")
                                   resources_content += f"- **{dataset['title']}**: [Link]({dataset['url']})\n"
                                   resources_content += f"  - Description: {dataset['description']}\n"
                               else:
                                   st.write(f"- **{dataset.title}**: [Link]({dataset.url})")
                                   st.write(f"  - Description: {dataset.description}")
                                   resources_content += f"- **{dataset.title}**: [Link]({dataset.url})\n"
                                   resources_content += f"  - Description: {dataset.description}\n"
                       else:
                           st.write("No datasets found for this use case.")
                           resources_content += f"### {use_case}\n"
                           resources_content += "No datasets found for this use case.\n"
                   except Exception as e:
                       st.write(f"Error fetching datasets for use case '{use_case}': {e}")
                       resources_content += f"### {use_case}\n"
                       resources_content += f"Error fetching datasets: {e}\n"

           with open("resources.md", "w") as file:
               file.write(resources_content)

           st.markdown("---")
           st.write("### Download Resources")
           with open("resources.md", "r") as file:
               file_content = file.read()
           st.markdown(create_download_link(file_content, "resources.md"), unsafe_allow_html=True)

elif feature_choice == "Document Search":
   st.header("Document Search")
   search_query = st.text_input("Enter your search query:")
   if search_query:
       with st.spinner("Searching documents..."):
           results = doc_search.search(search_query)
           for doc_id, content in results:
               st.write(f"Document: {doc_id}")
               st.write(content)
               st.markdown("---")

elif feature_choice == "Report Generator":
    st.header("Automated Report Generator")
    if st.session_state.research_results is None or st.session_state.use_cases is None:
        st.warning("Please generate use cases first before creating a report.")
    else:
        if st.button("Generate Comprehensive Report"):
            with st.spinner("Generating comprehensive report..."):
                report = report_generator.generate_report(
                    st.session_state.research_results,
                    st.session_state.use_cases,
                    "Available datasets will be listed here"
                )
                st.markdown(report)

elif feature_choice == "Market Analysis":
    st.header("Market Analysis")
    
    tab1, tab2, tab3 = st.tabs(["Competitor Analysis", "Market Standards", "Industry Insights"])
    
    with tab1:
        st.subheader("Competitor Analysis")
        if st.button("Analyze Competitors"):
            with st.spinner("Analyzing competitors..."):
                competitor_prompt = f"Analyze top competitors of {company_name} in {industry} industry. Focus on their AI/ML initiatives and innovations."
                analysis = chat_system.chat(competitor_prompt)
                st.write(analysis)
    
    with tab2:
        st.subheader("Market Standards")
        if st.button("Get Market Standards"):
            with st.spinner("Analyzing market standards..."):
                standards_prompt = f"What are the current AI/ML standards and best practices in the {industry} industry? Include regulatory compliance and technical benchmarks."
                standards = chat_system.chat(standards_prompt)
                st.write(standards)
    
    with tab3:
        st.subheader("Industry Insights")
        if st.button("Get Industry Insights"):
            with st.spinner("Fetching insights..."):
                consulting_insights = get_consulting_insights(company_name, industry)
                st.markdown(format_insights(consulting_insights))

with chat_container:
    if st.button("💬 AI Assistant", key="main_chat_toggle"):
        st.session_state.show_chat = not st.session_state.show_chat
        
    if st.session_state.show_chat:
        st.markdown("### AI Assistant")
        # Display existing messages
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.write(message["content"])
        
        # Get new input and generate response only once
        user_input = st.text_input("Ask me anything...", key="main_chat_input")
        if user_input and 'last_input' not in st.session_state:
            st.session_state.last_input = user_input
            st.session_state.messages.append({"role": "user", "content": user_input})
            
            chat_system.set_context({
                "company": company_name,
                "industry": industry,
                "research_results": st.session_state.get('research_results', []),
                "use_cases": st.session_state.get('use_cases', [])
            })
            
            response = chat_system.chat(user_input)
            st.session_state.messages.append({"role": "assistant", "content": response})
            st.rerun()
        
        # Reset last_input when input field is cleared
        if not user_input:
            if 'last_input' in st.session_state:
                del st.session_state.last_input