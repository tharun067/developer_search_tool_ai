from typing import Dict, Any
import os
import re
from langgraph.graph import StateGraph, END
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, SystemMessage
from dotenv import load_dotenv
from .models import ResearchState, CompanyInfo, CompanyAnalysis
from .firecrawl import FirecrawlService
from .prompts import DeveloperToolsPrompts

load_dotenv()


class Workflow:
    def __init__(self):
        self.firecrawl = FirecrawlService()
        google_api_key = os.getenv("GOOGLE_API_KEY") or os.getenv("GEMINI_API_KEY")
        if not google_api_key:
            raise ValueError(
                "Missing GOOGLE_API_KEY (or GEMINI_API_KEY). Add it to your .env file and restart Streamlit."
            )

        self.llm = ChatGoogleGenerativeAI(
            model="gemini-3-flash-preview",
            temperature=0,
            google_api_key=google_api_key,
        )
        self.prompts = DeveloperToolsPrompts()
        self.workflow = self._build_workflow()

    @staticmethod
    def _is_api_key_error(error: Exception) -> bool:
        message = str(error)
        return "API_KEY_INVALID" in message or "API Key not found" in message

    @staticmethod
    def _message_content_to_text(content: Any) -> str:
        if isinstance(content, str):
            return content

        if isinstance(content, list):
            parts = []
            for item in content:
                if isinstance(item, str):
                    parts.append(item)
                elif isinstance(item, dict):
                    text = item.get("text")
                    if isinstance(text, str):
                        parts.append(text)
                elif hasattr(item, "text") and isinstance(item.text, str):
                    parts.append(item.text)
            return "\n".join(parts)

        return str(content)

    @staticmethod
    def _extract_tool_names(raw_text: str) -> list[str]:
        if not raw_text:
            return []

        # Handle line-based outputs and comma-separated outputs.
        normalized = raw_text.replace(",", "\n")
        candidates = []
        for line in normalized.splitlines():
            cleaned = re.sub(r"^\s*[-*\d.)\s]+", "", line).strip()
            if cleaned:
                candidates.append(cleaned)

        # Keep order and remove duplicates.
        deduped = list(dict.fromkeys(candidates))
        return deduped

    def _build_workflow(self):
        graph = StateGraph(ResearchState)
        graph.add_node("extract_tools", self._extract_tools_step)
        graph.add_node("research", self._research_step)
        graph.add_node("analyze", self._analyze_step)
        graph.set_entry_point("extract_tools")
        graph.add_edge("extract_tools", "research")
        graph.add_edge("research", "analyze")
        graph.add_edge("analyze", END)
        return graph.compile()

    def _extract_tools_step(self, state: ResearchState) -> Dict[str, Any]:
        print(f"🔍 Finding articles about: {state.query}")

        article_query = f"{state.query} tools comparison best alternatives"
        search_results = self.firecrawl.search_companies(article_query, num_results=3)

        all_content = ""
        for result in search_results:
            url = result.get("url", "")
            scraped = self.firecrawl.scrape_company_pages(url)
            if scraped:
                all_content += scraped[:1500] + "\n\n"

        messages = [
            SystemMessage(content=self.prompts.TOOL_EXTRACTION_SYSTEM),
            HumanMessage(content=self.prompts.tool_extraction_user(state.query, all_content))
        ]

        try:
            response = self.llm.invoke(messages)
            response_text = self._message_content_to_text(response.content).strip()
            tool_names = self._extract_tool_names(response_text)
            print(f"Extracted tools: {', '.join(tool_names[:5])}")
            return {"extracted_tools": tool_names}
        except Exception as e:
            if self._is_api_key_error(e):
                raise ValueError(
                    "Invalid GOOGLE_API_KEY for Gemini. Generate a new key in Google AI Studio, update .env, and restart Streamlit."
                ) from e
            print(e)
            return {"extracted_tools": []}

    def _analyze_company_content(self, company_name: str, content: str) -> CompanyAnalysis:
        structured_llm = self.llm.with_structured_output(CompanyAnalysis)

        messages = [
            SystemMessage(content=self.prompts.TOOL_ANALYSIS_SYSTEM),
            HumanMessage(content=self.prompts.tool_analysis_user(company_name, content))
        ]

        try:
            analysis = structured_llm.invoke(messages)
            return analysis
        except Exception as e:
            if self._is_api_key_error(e):
                raise ValueError(
                    "Invalid GOOGLE_API_KEY for Gemini. Generate a new key in Google AI Studio, update .env, and restart Streamlit."
                ) from e
            print(e)
            return CompanyAnalysis(
                pricing_model="Unknown",
                is_open_source=None,
                tech_stack=[],
                description="Failed",
                api_available=None,
                languages_supported=[],
                integration_capabilities=[],
            )


    def _research_step(self, state: ResearchState) -> Dict[str, Any]:
        extracted_tools = getattr(state, "extracted_tools", [])

        if not extracted_tools:
            print("⚠️ No extracted tools found, falling back to direct search")
            search_results = self.firecrawl.search_companies(state.query, num_results=4)
            tool_names = [
                result.get("metadata", {}).get("title", "Unknown")
                for result in search_results
                if result.get("metadata", {}).get("title")
            ]
        else:
            tool_names = extracted_tools[:4]

        print(f"🔬 Researching specific tools: {', '.join(tool_names)}")

        companies = []
        for tool_name in tool_names:
            tool_search_results = self.firecrawl.search_companies(tool_name + " official site", num_results=1)

            if tool_search_results:
                result = tool_search_results[0]
                url = result.get("url", "")

                company = CompanyInfo(
                    name=tool_name,
                    description=result.get("markdown", ""),
                    website=url,
                    tech_stack=[],
                    competitors=[]
                )

                scraped = self.firecrawl.scrape_company_pages(url)
                if scraped:
                    content = scraped
                    analysis = self._analyze_company_content(company.name, content)

                    company.pricing_model = analysis.pricing_model
                    company.is_open_source = analysis.is_open_source
                    company.tech_stack = analysis.tech_stack
                    company.description = analysis.description
                    company.api_available = analysis.api_available
                    company.languages_supported = analysis.languages_supported
                    company.integration_capabilities = analysis.integration_capabilities

                companies.append(company)

        return {"companies": companies}

    def _analyze_step(self, state: ResearchState) -> Dict[str, Any]:
        print("Generating recommendations")

        company_data = ", ".join([
            company.json() for company in state.companies
        ])

        messages = [
            SystemMessage(content=self.prompts.RECOMMENDATIONS_SYSTEM),
            HumanMessage(content=self.prompts.recommendations_user(state.query, company_data))
        ]

        try:
            response = self.llm.invoke(messages)
        except Exception as e:
            if self._is_api_key_error(e):
                raise ValueError(
                    "Invalid GOOGLE_API_KEY for Gemini. Generate a new key in Google AI Studio, update .env, and restart Streamlit."
                ) from e
            raise
        return {"analysis": self._message_content_to_text(response.content)}

    def run(self, query: str) -> ResearchState:
        initial_state = ResearchState(query=query)
        final_state = self.workflow.invoke(initial_state)
        return ResearchState(**final_state)