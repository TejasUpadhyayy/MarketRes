import streamlit as st
import base64
from integrated_agents import industry_research, generate_use_cases
from resource_asset_collection_agent import search_huggingface_datasets, search_kaggle_datasets, search_google_datasets
from enhanced_features import DocumentSearchSystem, AutomatedReportGenerator, AIChatSystem
import streamlit.components.v1 as components
from market_insights import get_consulting_insights, format_insights

st.set_page_config(
    page_title="MarketRes",
    page_icon="📈",
    layout="wide"
)


st.markdown("""
    <style>
        .stApp {
            background: linear-gradient(-45deg, #1e3a8a, #1e40af, #1d4ed8, #2563eb);
            background-size: 400% 400%;
            animation: gradient 15s ease infinite;
        }

        @keyframes gradient {
            0% {
                background-position: 0% 50%;
            }
            50% {
                background-position: 100% 50%;
            }
            100% {
                background-position: 0% 50%;
            }
        }

        /* Enhance content visibility */
        .stMarkdown, .stButton, .stSelectbox {
            background-color: rgba(255, 255, 255, 0.1);
            border-radius: 10px;
            padding: 20px;
            backdrop-filter: blur(5px);
        }

        /* Ensure text remains readable */
        .stMarkdown {
            color: white !important;
        }

        .stButton > button {
            background-color: rgba(255, 255, 255, 0.2);
            color: white;
            border: 1px solid rgba(255, 255, 255, 0.3);
            transition: all 0.3s ease;
        }

        .stButton > button:hover {
            background-color: rgba(255, 255, 255, 0.3);
            border: 1px solid rgba(255, 255, 255, 0.5);
        }
    </style>
""", unsafe_allow_html=True)


# Custom CSS styling
st.markdown("""
    <style>
    .main {
        padding: 2rem;
    }
    .stButton > button {
        background-color: #2E5077;
        color: white;
        border-radius: 8px;
        padding: 0.5rem 2rem;
        border: none;
        transition: all 0.3s ease;
    }
    .stButton > button:hover {
        background-color: #1A365D;
        transform: translateY(-2px);
    }
    .sidebar .sidebar-content {
        background-color: #f8f9fa;
    }
    h1 {
        color: #2E5077;
        font-weight: 700;
        padding-bottom: 1rem;
        border-bottom: 2px solid #eee;
    }
    h2 {
        color: #558B6E;
        font-weight: 600;
        margin-top: 1.5rem;
    }
    h3 {
        color: #704C5E;
        margin-top: 1rem;
    }
    .stMarkdown a {
        color: #2E5077;
        text-decoration: none;
        border-bottom: 1px dotted #2E5077;
    }
    .stMarkdown a:hover {
        border-bottom: 1px solid #2E5077;
    }
    .reportview-container {
        background: #ffffff;
    }
    .results-card {
        background-color: white;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        margin: 1rem 0;
    }
    .chat-window {
        border: 1px solid #eee;
        border-radius: 10px;
        padding: 1rem;
        margin-top: 1rem;
    }
    </style>
""", unsafe_allow_html=True)

def create_download_link(file_content, filename):
    b64 = base64.b64encode(file_content.encode()).decode()
    href = f'<a href="data:file/markdown;base64,{b64}" download="{filename}" class="download-link">Download {filename}</a>'
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

# Main title
st.markdown("""
    <div style='text-align: center; padding: 2rem 0;'>
        <h1 style='font-size: 3rem;'>📈 MarketRes</h1>
        <p style='font-size: 1.2rem; color: #666;'>An agent for Market Research and Use Case generation.</p>
    </div>
""", unsafe_allow_html=True)

# Sidebar configuration
with st.sidebar:
    st.markdown("""
        <div style='padding: 1rem 0;'>
            <h2 style='color: #2E5077;'>Configuration</h2>
        </div>
    """, unsafe_allow_html=True)
    
    company_name = st.text_input("Enter the company name:", "Tesla")
    industries = ["Automotive", "Healthcare", "Retail", "Finance", "Manufacturing", "Technology"]
    industry = st.selectbox("Select the industry:", industries)
    
    st.markdown("---")
    st.header("Features")
    feature_choice = st.selectbox(
        "Select Feature",
        ["Use Case Generator", "Document Search", "Report Generator", "Market Analysis"]
    )

# Chat container
chat_container = st.container()

# Main content area
if feature_choice == "Use Case Generator":
    col1, col2 = st.columns([2,1])
    
    with col1:
        if st.button("🚀 Generate Use Cases", key="generate_btn"):
            with st.spinner("Analyzing industry data..."):
                # Industry Research
                st.markdown("<div class='results-card'>", unsafe_allow_html=True)
                st.write("### Industry Research")
                research_results = industry_research(company_name, industry)
                st.session_state.research_results = research_results
                
                for result in research_results:
                    st.write(f"- **{result['title']}**: [Link]({result['url']})")
                    truncated_content = result['content'][:200] + "..." if len(result['content']) > 200 else result['content']
                    st.write(f"  - {truncated_content}")
                    
                    if st.button("Read More", key=result['url']):
                        st.write(f"  - Full Content: {result['content']}")
                st.markdown("</div>", unsafe_allow_html=True)

                # Use Case Generation
                st.markdown("<div class='results-card'>", unsafe_allow_html=True)
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
                st.markdown("</div>", unsafe_allow_html=True)

                # Export section
                st.markdown("<div class='results-card'>", unsafe_allow_html=True)
                with open("resources.md", "w") as file:
                    file.write(resources_content)

                st.write("### Export Results")
                with open("resources.md", "r") as file:
                    file_content = file.read()
                st.markdown(create_download_link(file_content, "resources.md"), unsafe_allow_html=True)
                st.markdown("</div>", unsafe_allow_html=True)

    with col2:
        st.markdown("### How to Use This Tool")

        # Use an expander for a dropdown-like section
        with st.expander("Click here to see instructions"):
            st.subheader("1. Initial Setup")
            st.write("Navigate to the sidebar and enter your company name. Select your industry from the provided options.")
            st.markdown("---")  # Adds a horizontal line

            st.subheader("2. Generate Analysis")
            st.write("Click the 'Generate Use Cases' button to begin the analysis process. Our system will research your industry and identify AI opportunities.")
            st.markdown("---")  # Adds a horizontal line

            st.subheader("3. Review Results")
            st.write("Examine the generated use cases and datasets. Each suggestion includes implementation guidance and resources.")
            
        # Pro tip below the expander
        st.info("💡 **Pro Tip**: Download the complete report using the export option to share findings with your team.")






elif feature_choice == "Document Search":
    st.markdown("<div class='results-card'>", unsafe_allow_html=True)
    st.header("Document Search")
    search_query = st.text_input("Enter your search query:")
    if search_query:
        with st.spinner("Searching documents..."):
            results = doc_search.search(search_query)
            for doc_id, content in results:
                st.write(f"Document: {doc_id}")
                st.write(content)
                st.markdown("---")
    st.markdown("</div>", unsafe_allow_html=True)

elif feature_choice == "Report Generator":
    st.markdown("<div class='results-card'>", unsafe_allow_html=True)
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
    st.markdown("</div>", unsafe_allow_html=True)

elif feature_choice == "Market Analysis":
    st.markdown("<div class='results-card'>", unsafe_allow_html=True)
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
    st.markdown("</div>", unsafe_allow_html=True)

# Chat functionality
with chat_container:
    if st.button("💬 AI Assistant", key="main_chat_toggle"):
        st.session_state.show_chat = not st.session_state.show_chat
    
    if st.session_state.show_chat:
        st.markdown("<div class='chat-window'>", unsafe_allow_html=True)
        st.markdown("### AI Assistant")
        
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.write(message["content"])
        
        if user_input := st.text_input("Ask me anything...", key="main_chat_input"):
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
        st.markdown("</div>", unsafe_allow_html=True)
