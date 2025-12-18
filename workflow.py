from typing import Dict, Any
from langgraph.graph import StateGraph, END
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
from .models_ import ResearchState,CompanyInfo,CompanyAnalysis
from .firecrawl import FirecrawlService
from .prompts import DeveloperToolsPrompts
import os

class Workflow:
    def __init__(self):
        self.firecrawl = FirecrawlService()

        self.llm = ChatOpenAI(
            model="nex-agi/deepseek-v3.1-nex-n1:free",
            temperature=0.1,
            base_url="https://openrouter.ai/api/v1",
            api_key=os.getenv("OPENROUTER_API_KEY"),
        )
        self.prompts = DeveloperToolsPrompts()
        self.Workflow = self._build_workflow()




    def _build_workflow(self):
        graph = StateGraph(ResearchState)
        graph.add_node("extract_tools", self.extract_tools_step)
        graph.add_node("reaserch", self._reaserch_step)
        graph.add_node("analyze", self._analyze_step)
        graph.set_entry_point("extract_tools")
        graph.add_edge("extract_tools", "reaserch")
        graph.add_edge("reaserch", "analyze")
        graph.add_edge("analyze", END)
        return graph.compile()


    def extract_tools_step(self, state: ResearchState) -> Dict[str, Any]:
        print(f"🔍 Finding articles about: {state.query}")

        article_query = f"{state.query} tools comparison best alternatives"
        search_results = self.firecrawl.search_companies(article_query, num_result=3)

        all_content = ""
        for result in search_results:
            # 🔒 Defensive normalization
            if isinstance(result, tuple):
                result = result[1] if len(result) > 1 and isinstance(result[1], dict) else {}

            if not isinstance(result, dict):
                continue

            url = result.get("url")
            if not url:
                continue

            scraped = self.firecrawl.scrape_company_pages(url)
            if scraped and hasattr(scraped, "markdown"):
                all_content += scraped.markdown[:1500] + "\n\n"

        messages = [
            SystemMessage(content=self.prompts.TOOL_EXTRACTION_SYSTEM),
            HumanMessage(
                content=self.prompts.tool_extraction_user(state.query, all_content)
            ),
        ]

        try:
            response = self.llm.invoke(messages)
            tool_names = [
                name.strip()
                for name in response.content.split("\n")
                if name.strip()
            ]
            return {"extracted_tools": tool_names}
        except Exception as e:
            print(e)
            return {"extracted_tools": []}



    def _analyze_comapny_content(self, comapny_name: str, content: str) -> CompanyAnalysis:
            structured_llm = self.llm.with_structured_output(CompanyAnalysis)

            messages = [
                SystemMessage(content = self.prompts.TOOL_ANALYSIS_SYSTEM),
                HumanMessage(content)
            ]
            try:
                analysis = structured_llm.invoke(messages)
                return analysis
            except Exception as e:
                print(e)
                return CompanyAnalysis(
                    pricing_model="Unknown",
                    is_open_source=None,
                    tech_stack=[],
                    description="Failed",
                    api_available=None,
                    language_support=[],
                    integration_capabilities=[],
                )
            
    def _reaserch_step(self, state: ResearchState) -> Dict[str, Any]:
        extracted_tools = getattr(state, "extracted_tools", [])

        if not extracted_tools:
            print("No extracted tools found, falling back to direct search")
            search_results = self.firecrawl.search_companies(state.query, num_result=4)

            tool_names = []
            for result in search_results:
                if isinstance(result, tuple):
                    result = result[1] if len(result) > 1 and isinstance(result[1], dict) else {}

                if not isinstance(result, dict):
                    continue

                title = result.get("metadata", {}).get("title")
                if title:
                    tool_names.append(title)
        else:
            tool_names = extracted_tools[:4]

        print(f"Researching specified tools: {', '.join(tool_names)}")

        companies = []
        for tool_name in tool_names:
            tool_search_results = self.firecrawl.search_companies(tool_name, num_result=1)
            if not tool_search_results:
                continue

            if hasattr(tool_search_results, "data"):
                results = tool_search_results.data
            else:
                results = tool_search_results

            if not results:
                continue

            result = results[0]

            if isinstance(result, tuple):
                result = result[1] if len(result) > 1 and isinstance(result[1], dict) else {}

            if not isinstance(result, dict):
                continue

            url = result.get("url")
            if not url:
                continue

            scraped = self.firecrawl.scrape_company_pages(url)
            if not scraped or not hasattr(scraped, "markdown"):
                continue

            analysis = self._analyze_comapny_content(tool_name, scraped.markdown)

            company = CompanyInfo(
                name=tool_name,
                description=analysis.description,
                website=url,
                pricing_model=analysis.pricing_model,
                is_open_source=analysis.is_open_source,
                tech_stack=analysis.tech_stack,
                api_available=analysis.api_available,
                language_support=analysis.language_support,
                integration_capabilities=analysis.integration_capabilities,
                competitors=[],
            )

            companies.append(company)

        return {"companies": companies}


    
    def _analyze_step(self, state: ResearchState) -> Dict[str, Any]:
        print("Generating recommandations")

        company_data = ", ".join(
            company.model_dump_json() for company in state.companies
        )

        messages = [
            SystemMessage(content=self.prompts.RECOMMENDATIONS_SYSTEM),
            HumanMessage(
                content=self.prompts.recommendations_user(state.query, company_data)
            ),
        ]

        response = self.llm.invoke(messages)
        return {"analysis": response.content}

    
    def run(self, query: str) -> ResearchState:
        initial_state = ResearchState(query=query)
        final_state = self.Workflow.invoke(initial_state)
        return ResearchState(**final_state)





            
