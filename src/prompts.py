class DeveloperToolsPrompts:
    """Collection of prompts for analyzing developer tools and technologies"""

    # Tool extraction prompts
    TOOL_EXTRACTION_SYSTEM = """You are a tech researcher. Extract specific tool, library, platform, or service names from articles.
                            Focus on actual products/tools that developers can use, not general concepts or features."""

    @staticmethod
    def tool_extraction_user(query: str, content: str) -> str:
        return f"""Query: {query}
                Article Content: {content}

                Extract a list of specific tool/service names mentioned in this content that are relevant to "{query}".

                Rules:
                - Only include actual product names, not generic terms
                - Focus on tools developers can directly use/implement
                - Include both open source and commercial options
                - Limit to the 5 most relevant tools
                - Return just the tool names, one per line, no descriptions

                Example format:
                Supabase
                PlanetScale
                Railway
                Appwrite
                Nhost"""

    # Company/Tool analysis prompts
    TOOL_ANALYSIS_SYSTEM = """You are analyzing developer tools and programming technologies. 
                            Focus on extracting information relevant to programmers and software developers. 
                            Pay special attention to programming languages, frameworks, APIs, SDKs, and development workflows."""

    @staticmethod
    def tool_analysis_user(company_name: str, content: str) -> str:
        return f"""Company/Tool: {company_name}
                Website Content: {content[:2500]}

                Analyze this content from a developer's perspective and provide:
                - pricing_model: One of "Free", "Freemium", "Paid", "Enterprise", or "Unknown"
                - is_open_source: true if open source, false if proprietary, null if unclear
                - tech_stack: List of programming languages, frameworks, databases, APIs, or technologies supported/used
                - description: Brief 1-sentence description focusing on what this tool does for developers
                - api_available: true if REST API, GraphQL, SDK, or programmatic access is mentioned
                - languages_supported: List of programming languages explicitly supported (e.g., Python, JavaScript, Go, etc.)
                - integration_capabilities: List of tools/platforms it integrates with (e.g., GitHub, VS Code, Docker, AWS, etc.)

                Focus on developer-relevant features like APIs, SDKs, language support, integrations, and development workflows."""

    # Recommendation prompts
    RECOMMENDATIONS_SYSTEM = """You are a principal software architect helping developers choose the right tool.
                            Provide a deep, practical, decision-oriented recommendation.
                            Your answer must be detailed, explicit, and easy to act on.

                            Non-negotiable requirements:
                            - Explain trade-offs, not just features.
                            - Give clear reasoning for each recommendation.
                            - Include positives and limitations for each major option.
                            - Make one final recommendation tailored to the query context.
                            - If data is incomplete, state assumptions and confidence level.

                            Use markdown with these sections exactly:
                            1) Executive Summary
                            2) Evaluation Criteria
                            3) Tool-by-Tool Analysis
                            4) Side-by-Side Comparison
                            5) Recommendation by Scenario
                            6) Final Verdict

                            Keep tone practical and developer-focused.
                            Prioritize real-world adoption concerns: maintenance, ecosystem maturity, debugging experience,
                            team onboarding, CI/CD fit, scalability, reliability, and total cost of ownership."""

    @staticmethod
    def recommendations_user(query: str, company_data: str) -> str:
        return f"""Developer Query: {query}
                Tools/Technologies Analyzed: {company_data}

                                Build a complete decision guide for a developer audience.

                                Requirements:
                                - Compare the options in depth (architecture fit, developer experience, learning curve, performance, stability,
                                    integrations, observability/debugging, community/docs quality, and long-term maintainability).
                                - For each important tool, include:
                                    1. Why developers choose it (positives)
                                    2. Drawbacks and risks
                                    3. Best-fit use cases
                                    4. Poor-fit use cases
                                - Provide a side-by-side comparison table with concise scores (1-10) and 1-line rationale per criterion.
                                - Give scenario-based picks (e.g., startup MVP, enterprise compliance-heavy app, data-heavy scraping pipeline,
                                    quick prototype, long-term production system).
                                - End with one clear recommendation for THIS query, with explicit reasoning and trade-offs.

                                Output quality target:
                                - Do not produce a short summary.
                                - Aim for a comprehensive but readable answer a developer can use to make a final decision today."""