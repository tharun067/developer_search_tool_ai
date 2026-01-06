# 🔍 Developer Tools Research Agent

An intelligent AI-powered research agent that helps developers discover, compare, and evaluate tools, frameworks, and technologies. Built with LangGraph and powered by Google Gemini, this tool automates the process of researching developer tools by crawling the web, extracting relevant information, and providing comprehensive analysis.

## ✨ Features

- **Automated Tool Discovery**: Searches the web and automatically extracts relevant developer tools based on your query
- **Comprehensive Analysis**: Provides detailed information including:
  - Pricing models (Free, Freemium, Paid, etc.)
  - Open source status
  - Technology stack
  - API availability
  - Supported programming languages
  - Integration capabilities
- **AI-Powered Research**: Uses LangGraph workflow with Google Gemini to intelligently research and analyze tools
- **Beautiful UI**: Built with Streamlit featuring a modern, gradient-themed interface
- **Multi-Step Workflow**: 
  1. Extract relevant tools from search results
  2. Research each tool in detail
  3. Generate comprehensive recommendations

## 🛠️ Tech Stack

- **Python 3.x**
- **LangGraph**: For orchestrating the multi-step AI workflow
- **LangChain**: For LLM integrations
- **Google Gemini 2.5 Flash**: AI model for analysis and recommendations
- **Firecrawl**: Web scraping and search capabilities
- **Streamlit**: Interactive web interface
- **Pydantic**: Data validation and structured outputs

## 📋 Prerequisites

- Python 3.8 or higher
- Google API Key (for Gemini)
- Firecrawl API Key

## 🚀 Installation

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd developer_search_tool_ai
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**:
   Create a `.env` file in the root directory with:
   ```env
   GOOGLE_API_KEY=your_google_api_key_here
   FIRECRAWL_API_KEY=your_firecrawl_api_key_here
   ```

## 💻 Usage

### Running the Application

Run the Streamlit application:
```bash
streamlit run main.py
```

The app will open in your browser at `http://localhost:8501`.

### Example Queries

Enter queries like:
- **"Python web frameworks"** - Discover FastAPI, Django, Flask, etc.
- **"JavaScript testing libraries"** - Find Jest, Vitest, Playwright, etc.
- **"CI/CD tools for Docker"** - Explore GitHub Actions, GitLab CI, Jenkins, etc.
- **"Vector databases for ML"** - Research Pinecone, Weaviate, Milvus, etc.
- **"API documentation tools"** - Learn about Swagger, Postman, Redoc, etc.
- **"Python async task queues"** - Compare Celery, RQ, Dramatiq, etc.

### How It Works

The agent follows a multi-step process:

1. **Tool Discovery**: Searches the web for comparison articles about your query
2. **Extraction**: Uses AI to extract specific tool names from the articles
3. **Research**: For each tool, finds the official website and scrapes detailed information
4. **Analysis**: Uses structured LLM outputs to extract pricing, tech stack, API info, etc.
5. **Recommendations**: Generates concise recommendations based on all gathered data

The entire process typically takes 30-60 seconds depending on the number of tools discovered.

## 📁 Project Structure

```
developer_search_tool_ai/
├── main.py                 # Streamlit application entry point
├── requirements.txt        # Python dependencies
├── pyproject.toml         # Project configuration
├── README.md              # This file
├── .env                   # Environment variables (not tracked)
└── src/
    ├── __init__.py
    ├── workflow.py        # LangGraph workflow implementation
    ├── models.py          # Pydantic data models
    ├── prompts.py         # LLM prompt templates
    └── firecrawl.py       # Firecrawl service integration
```

### Module Details

#### `main.py`
The Streamlit web application that provides the user interface. Features:
- Custom CSS styling with gradient background
- Interactive search input
- Real-time display of research progress
- Formatted display of tool information with badges and metrics

#### `src/workflow.py`
Core LangGraph workflow implementation with three main steps:
- **`_extract_tools_step`**: Searches for articles and extracts tool names using AI
- **`_research_step`**: Researches each extracted tool in detail
- **`_analyze_step`**: Generates final recommendations

#### `src/models.py`
Pydantic models for type safety and validation:
- **`ResearchState`**: Main state object passed through the workflow
- **`CompanyInfo`**: Detailed information about each tool
- **`CompanyAnalysis`**: Structured LLM output format for tool analysis

#### `src/prompts.py`
LLM prompt templates optimized for developer tool research:
- **Tool Extraction**: Extracts tool names from articles
- **Tool Analysis**: Analyzes tool features from a developer perspective
- **Recommendations**: Generates concise recommendations

#### `src/firecrawl.py`
Firecrawl API integration for web scraping:
- **`search_companies`**: Searches the web and returns results with markdown content
- **`scrape_company_pages`**: Scrapes individual URLs for detailed content

## 🔧 Configuration

### Workflow Configuration

The workflow uses the following configuration:
- **LLM Model**: Google Gemini 2.5 Flash
- **Temperature**: 0 (deterministic responses)
- **Search Results**: 3 articles for tool extraction, 4 tools researched
- **Content Extraction**: First 1500 characters per article

### Customization Options

You can customize the workflow by modifying `src/workflow.py`:

```python
# Change the LLM model
self.llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",  # or "gemini-pro", "gemini-1.5-pro"
    temperature=0  # 0 for deterministic, 1 for creative
)

# Adjust search parameters
num_results=3  # Number of articles to search
tool_names = extracted_tools[:4]  # Number of tools to research

# Modify content extraction
scraped.markdown[:1500]  # Characters to extract from each article
```

### Environment Variables

Create a `.env` file with the following variables:

```env
# Required
GOOGLE_API_KEY=your_google_api_key_here
FIRECRAWL_API_KEY=your_firecrawl_api_key_here

# Optional - for custom endpoints
# GOOGLE_API_BASE=https://your-proxy.com
```

### Getting API Keys

1. **Google API Key** (for Gemini):
   - Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
   - Create a new API key
   - Copy and paste into your `.env` file

2. **Firecrawl API Key**:
   - Sign up at [Firecrawl](https://www.firecrawl.dev/)
   - Navigate to API Keys section
   - Generate a new API key
   - Copy and paste into your `.env` file

## 📊 Output

For each tool discovered, the agent provides:
- Tool name and description
- Official website
- Pricing model
- Open source status
- Technology stack used
- API availability
- Supported programming languages
- Integration capabilities
- Overall recommendations

### Sample Output Structure

```json
{
  "name": "FastAPI",
  "description": "Modern, fast web framework for building APIs with Python",
  "website": "https://fastapi.tiangolo.com",
  "pricing_model": "Free",
  "is_open_source": true,
  "tech_stack": ["Python", "Starlette", "Pydantic"],
  "api_available": true,
  "languages_supported": ["Python"],
  "integration_capabilities": ["OpenAPI", "Swagger UI", "Docker", "Kubernetes"]
}
```

The analysis section provides recommendations in natural language, highlighting:
- **Best overall choice** based on your specific query
- **Cost considerations** comparing pricing models
- **Technical advantages** of each tool
- **Use case fit** based on the discovered features

## 🏗️ Architecture

### LangGraph Workflow

The application uses a state-based workflow with LangGraph:

```
┌─────────────────┐
│  User Query     │
└────────┬────────┘
         │
         ▼
┌─────────────────────────────┐
│  Extract Tools Step         │
│  • Search for articles      │
│  • Extract tool names       │
└────────┬────────────────────┘
         │
         ▼
┌─────────────────────────────┐
│  Research Step              │
│  • For each tool:           │
│    - Search official site   │
│    - Scrape content         │
│    - Analyze with LLM       │
└────────┬────────────────────┘
         │
         ▼
┌─────────────────────────────┐
│  Analyze Step               │
│  • Generate recommendations │
│  • Compare tools            │
└────────┬────────────────────┘
         │
         ▼
┌─────────────────────────────┐
│  Final Results              │
└─────────────────────────────┘
```

### State Management

The `ResearchState` object flows through the entire workflow:

```python
class ResearchState(BaseModel):
    query: str                    # User's original query
    extracted_tools: List[str]    # Tool names extracted from articles
    companies: List[CompanyInfo]  # Detailed info for each tool
    search_results: List[Dict]    # Raw search results
    analysis: Optional[str]       # Final recommendations
```

### Data Flow

1. **Input**: User query → ResearchState
2. **Extract**: Query → Web search → Articles → LLM → Tool names
3. **Research**: Tool names → Web search → Scraping → LLM → CompanyInfo objects
4. **Analyze**: CompanyInfo objects → LLM → Recommendations
5. **Output**: Updated ResearchState with all data

## 💡 Code Examples

### Using the Workflow Programmatically

```python
from src.workflow import Workflow

# Initialize the workflow
workflow = Workflow()

# Run a research query
result = workflow.run("Python web frameworks")

# Access the results
for company in result.companies:
    print(f"{company.name}: {company.pricing_model}")
    print(f"Open Source: {company.is_open_source}")
    print(f"Languages: {', '.join(company.languages_supported)}")
    print()

# Get recommendations
print(result.analysis)
```

### Custom LLM Configuration

```python
from langchain_google_genai import ChatGoogleGenerativeAI

# Use a different model
custom_llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-pro",
    temperature=0.3,
    max_tokens=2000
)

# Replace in workflow
workflow.llm = custom_llm
```

### Custom Prompts

```python
from src.prompts import DeveloperToolsPrompts

# Extend the prompts class
class CustomPrompts(DeveloperToolsPrompts):
    @staticmethod
    def tool_extraction_user(query: str, content: str) -> str:
        return f"""Custom prompt for: {query}
        Content: {content}
        Extract tools focusing on enterprise solutions."""
```

## 🐛 Troubleshooting

### Common Issues

#### "Missing FIRECRAWL_API_KEY environment variable"
**Solution**: Ensure your `.env` file exists in the root directory and contains:
```env
FIRECRAWL_API_KEY=your_api_key_here
```

#### "No tools extracted" or empty results
**Possible causes**:
- Query is too vague - try being more specific (e.g., "Python web frameworks" instead of "web tools")
- API rate limits - wait a few minutes and try again
- Network connectivity issues

**Solution**: Check the console output for detailed error messages.

#### Streamlit not opening in browser
**Solution**: 
```bash
# Try specifying the port explicitly
streamlit run main.py --server.port 8501

# Or use a different port
streamlit run main.py --server.port 8502
```

#### LLM responses are inconsistent
**Solution**: The temperature is set to 0 for deterministic responses. If you're still seeing inconsistency, it may be due to web content variations. Consider increasing the content extraction limit in `workflow.py`.

### Debug Mode

Enable detailed logging by running:
```bash
# Windows
$env:LOG_LEVEL="DEBUG"
streamlit run main.py

# Linux/Mac
LOG_LEVEL=DEBUG streamlit run main.py
```

## ❓ FAQ

### Q: How accurate is the tool information?
**A**: The accuracy depends on the web content available and scraped. The agent extracts information from official websites and documentation, but should be verified for critical decisions.

### Q: Can I use this for non-developer tools?
**A**: While optimized for developer tools, you can modify the prompts in `src/prompts.py` to adapt it for other domains.

### Q: How much do the API calls cost?
**A**: 
- **Google Gemini 2.5 Flash**: Very low cost, typically fractions of a cent per query
- **Firecrawl**: Free tier available, then paid plans based on usage
- A typical query makes ~5-10 API calls total

### Q: Can I run this offline?
**A**: No, it requires internet access for web scraping and LLM API calls. However, you could modify it to use local LLMs (like Ollama) and cached web content.

### Q: How do I add more tools to research?
**A**: Modify the limit in `src/workflow.py`:
```python
tool_names = extracted_tools[:10]  # Research up to 10 tools instead of 4
```

### Q: Can I export the results?
**A**: The Streamlit interface displays results in the browser. To export, you can:
1. Use the programmatic API (see Code Examples above)
2. Add export functionality to `main.py`
3. Copy directly from the web interface

### Q: Is this production-ready?
**A**: This is a research tool. For production use, consider:
- Adding error handling and retry logic
- Implementing caching to reduce API calls
- Adding rate limiting
- Setting up monitoring and logging
- Implementing result validation

## 🚀 Advanced Usage

### Batch Processing

Process multiple queries at once:

```python
from src.workflow import Workflow
import json

queries = [
    "Python web frameworks",
    "JavaScript testing tools",
    "Vector databases"
]

workflow = Workflow()
results = []

for query in queries:
    result = workflow.run(query)
    results.append({
        "query": query,
        "tools": [c.name for c in result.companies],
        "analysis": result.analysis
    })

# Save to file
with open("batch_results.json", "w") as f:
    json.dump(results, f, indent=2)
```

### Integration with Other Tools

```python
# Use with LangChain agents
from langchain.agents import Tool

def research_tools(query: str) -> str:
    workflow = Workflow()
    result = workflow.run(query)
    return result.analysis

tool = Tool(
    name="Developer Tool Research",
    func=research_tools,
    description="Research and compare developer tools based on a query"
)
```

### Custom Filtering

Filter results based on criteria:

```python
result = workflow.run("Python web frameworks")

# Filter for open source only
open_source_tools = [
    c for c in result.companies 
    if c.is_open_source
]

# Filter for free tools
free_tools = [
    c for c in result.companies 
    if c.pricing_model in ["Free", "Freemium"]
]

# Filter by language support
python_tools = [
    c for c in result.companies 
    if "Python" in c.languages_supported
]
```

## 🔒 Security Considerations

- **API Keys**: Never commit `.env` files to version control
- **Input Validation**: User queries are passed to LLMs - ensure you trust your users
- **Web Scraping**: Respects robots.txt through Firecrawl
- **Rate Limiting**: Consider implementing rate limits for public deployments
- **Data Privacy**: Queries are sent to Google (Gemini) and Firecrawl

## 📈 Performance Tips

1. **Reduce search results**: Lower the `num_results` parameter for faster execution
2. **Cache results**: Implement caching for frequently queried tools
3. **Parallel processing**: The workflow processes tools sequentially; consider parallelization for more tools
4. **Content limits**: Reduce the markdown content extraction limit if experiencing slowdowns
5. **Use faster models**: Gemini 2.5 Flash is already optimized for speed

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

### How to Contribute

1. **Fork the repository**
2. **Create a feature branch**: `git checkout -b feature/amazing-feature`
3. **Make your changes**
4. **Test thoroughly**: Ensure your changes work with various queries
5. **Commit**: `git commit -m 'Add amazing feature'`
6. **Push**: `git push origin feature/amazing-feature`
7. **Open a Pull Request**

### Areas for Contribution

- 🎨 **UI Improvements**: Enhance the Streamlit interface
- 🧠 **Better Prompts**: Improve LLM prompts for more accurate extraction
- 📊 **Export Features**: Add CSV, JSON, or PDF export options
- 🔍 **Search Enhancements**: Improve tool discovery algorithms
- 🧪 **Testing**: Add unit tests and integration tests
- 📚 **Documentation**: Improve docs and add tutorials
- 🌐 **Internationalization**: Add support for non-English queries
- ⚡ **Performance**: Optimize workflow execution time

### Development Setup

```bash
# Clone your fork
git clone https://github.com/yourusername/developer_search_tool_ai.git
cd developer_search_tool_ai

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up pre-commit hooks (optional)
pip install pre-commit
pre-commit install
```

### Code Style

- Follow PEP 8 for Python code
- Use type hints where appropriate
- Add docstrings to functions and classes
- Keep functions focused and modular

## 📝 Changelog

### v1.0.0 (Current)
- Initial release
- LangGraph-based workflow
- Streamlit web interface
- Support for developer tool research
- Structured output with Pydantic
- Integration with Google Gemini and Firecrawl

## 🗺️ Roadmap

Future enhancements planned:

- [ ] **Caching system** for frequently queried tools
- [ ] **Export functionality** (JSON, CSV, PDF reports)
- [ ] **Comparison mode** for side-by-side tool comparison
- [ ] **Historical tracking** of tool pricing and features over time
- [ ] **User feedback system** to improve recommendations
- [ ] **API endpoint** for programmatic access
- [ ] **Docker support** for easy deployment
- [ ] **Custom filters** for advanced search criteria
- [ ] **Integration with GitHub** for automatic repo analysis
- [ ] **Support for local LLMs** (Ollama, LM Studio)

## 📄 License

[Add your license information here]

MIT License recommended for open source projects.

## 👥 Authors

[Add your information here]

## 🙏 Acknowledgments

- Built with [LangGraph](https://github.com/langchain-ai/langgraph)
- Powered by [Google Gemini](https://ai.google.dev/)
- Web scraping by [Firecrawl](https://www.firecrawl.dev/)
- UI by [Streamlit](https://streamlit.io/)
