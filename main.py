import streamlit as st
from dotenv import load_dotenv
from src.workflow import Workflow

load_dotenv()

# Page configuration
st.set_page_config(
    page_title="Developer Tools Research Agent",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
    <style>
    .main {
        padding: 0rem 1rem;
    }
    .stApp {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }
    h1 {
        color: #ffffff;
        font-weight: 700;
        text-align: center;
        padding: 1.5rem 0;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }
    .search-container {
        background: white;
        padding: 2rem;
        border-radius: 15px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.2);
        margin-bottom: 2rem;
    }
    .company-card {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        padding: 1.5rem;
        border-radius: 12px;
        margin-bottom: 1.5rem;
        border-left: 5px solid #667eea;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        transition: transform 0.2s;
    }
    .company-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 15px rgba(0,0,0,0.2);
    }
    .company-name {
        color: #2d3748;
        font-size: 1.8rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
    }
    .metric-label {
        color: #4a5568;
        font-weight: 600;
        font-size: 0.9rem;
    }
    .metric-value {
        color: #2d3748;
        font-size: 1rem;
    }
    .badge {
        display: inline-block;
        padding: 0.3rem 0.8rem;
        border-radius: 20px;
        font-size: 0.85rem;
        font-weight: 600;
        margin: 0.2rem;
    }
    .badge-success {
        background: #48bb78;
        color: white;
    }
    .badge-info {
        background: #4299e1;
        color: white;
    }
    .badge-warning {
        background: #ed8936;
        color: white;
    }
    .badge-secondary {
        background: #718096;
        color: white;
    }
    .analysis-box {
        background: white;
        padding: 2rem;
        border-radius: 12px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        margin-top: 2rem;
        border-left: 5px solid #48bb78;
    }
    .stButton>button {
        width: 100%;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        font-weight: 600;
        border: none;
        padding: 0.75rem 2rem;
        border-radius: 8px;
        font-size: 1.1rem;
        transition: all 0.3s;
    }
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4);
    }
    .sidebar .sidebar-content {
        background: linear-gradient(180deg, #667eea 0%, #764ba2 100%);
    }
    </style>
""", unsafe_allow_html=True)

# Initialize session state
if 'workflow' not in st.session_state:
    st.session_state.workflow = Workflow()
if 'results' not in st.session_state:
    st.session_state.results = None
if 'search_history' not in st.session_state:
    st.session_state.search_history = []

# Header
st.markdown("<h1>🔍 Developer Tools Research Agent</h1>", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.markdown("### 📚 Search History")
    if st.session_state.search_history:
        for i, query in enumerate(reversed(st.session_state.search_history[-10:]), 1):
            st.markdown(f"**{i}.** {query}")
    else:
        st.info("No search history yet")
    
    st.markdown("---")
    st.markdown("### ℹ️ About")
    st.markdown("""
    This tool helps you research and compare developer tools by analyzing:
    - Pricing models
    - Tech stacks
    - API availability
    - Integrations
    - Language support
    """)
    
    if st.button("Clear History"):
        st.session_state.search_history = []
        st.rerun()

# Main content area
col1, col2, col3 = st.columns([1, 6, 1])

with col2:
    st.markdown('<div class="search-container">', unsafe_allow_html=True)
    
    # Search input
    query = st.text_input(
        "Enter your developer tools query:",
        placeholder="e.g., CI/CD tools, code editors, testing frameworks...",
        label_visibility="collapsed"
    )
    
    col_btn1, col_btn2, col_btn3 = st.columns([2, 1, 2])
    with col_btn2:
        search_button = st.button("🚀 Search", use_container_width=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

# Process search
if search_button and query:
    with st.spinner("🔎 Researching developer tools..."):
        try:
            result = st.session_state.workflow.run(query)
            st.session_state.results = result
            st.session_state.search_history.append(query)
        except Exception as e:
            st.error(f"❌ Error: {str(e)}")

# Display results
if st.session_state.results:
    result = st.session_state.results
    
    st.markdown(f"### 📊 Results for: *{query}*")
    st.markdown("---")
    
    # Company cards
    for i, company in enumerate(result.companies, 1):
        st.markdown('<div class="company-card">', unsafe_allow_html=True)
        
        # Company header
        col_header1, col_header2 = st.columns([3, 1])
        with col_header1:
            st.markdown(f'<div class="company-name">{i}. {company.name}</div>', unsafe_allow_html=True)
        with col_header2:
            if company.is_open_source:
                st.markdown('<span class="badge badge-success">Open Source</span>', unsafe_allow_html=True)
            else:
                st.markdown('<span class="badge badge-secondary">Proprietary</span>', unsafe_allow_html=True)
        
        # Company details in columns
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown(f"**🌐 Website:** [{company.website}]({company.website})")
            st.markdown(f"**💰 Pricing:** {company.pricing_model}")
            
            if company.api_available is not None:
                api_status = "✅ Available" if company.api_available else "❌ Not Available"
                st.markdown(f"**🔌 API:** {api_status}")
        
        with col2:
            if company.tech_stack:
                st.markdown(f"**🛠️ Tech Stack:**")
                for tech in company.tech_stack[:5]:
                    st.markdown(f'<span class="badge badge-info">{tech}</span>', unsafe_allow_html=True)
            
            if company.languages_supported:
                st.markdown(f"**💻 Languages:**")
                for lang in company.languages_supported[:5]:
                    st.markdown(f'<span class="badge badge-warning">{lang}</span>', unsafe_allow_html=True)
        
        # Integration capabilities
        if company.integration_capabilities:
            st.markdown("**🔗 Integrations:**")
            integrations_text = ", ".join(company.integration_capabilities[:6])
            st.markdown(f"<small>{integrations_text}</small>", unsafe_allow_html=True)
        
        # Description
        if company.description and company.description != "Analysis failed":
            with st.expander("📝 Description"):
                st.write(company.description)
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Analysis section
    if result.analysis:
        st.markdown('<div class="analysis-box">', unsafe_allow_html=True)
        st.markdown("### 💡 Developer Recommendations")
        st.markdown("---")
        st.markdown(result.analysis)
        st.markdown('</div>', unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: white; padding: 1rem;'>"
    "Built with ❤️ for Developers | Powered by AI"
    "</div>",
    unsafe_allow_html=True
)