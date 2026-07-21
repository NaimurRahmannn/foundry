import os

from crewai.agents.crew_agent_executor import CrewAgentExecutor
from crewai import Agent, Crew, LLM, Process, Task
from crewai.project import CrewBase, agent, crew, llm, output_pydantic, task, tool

from ai_product_company.tools.tech_research_tool import PyPIPackageLookupTool
from schemas.product_requirements import ProductRequirements


class GroqLLM(LLM):
    """CrewAI adds cache metadata that Groq's OpenAI-compatible API rejects."""

    def supports_function_calling(self) -> bool:
        return False

    def _prepare_completion_params(self, messages, tools=None, skip_file_processing=False):
        params = super()._prepare_completion_params(
            messages,
            tools=tools,
            skip_file_processing=skip_file_processing,
        )
        for message in params.get("messages", []):
            if isinstance(message, dict):
                message.pop("cache_breakpoint", None)
        return params


@CrewBase
class AiProductCompany:
    """Classic CrewAI crew for the ai_product_company project."""

    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"

    @output_pydantic
    class product_requirements_output(ProductRequirements):
        pass

    def _groq_openai_compatible_llm(self) -> LLM:
        return GroqLLM(
            model=os.getenv("MODEL", "groq/llama-3.3-70b-versatile"),
            provider="groq",
            base_url="https://api.groq.com/openai/v1",
            api_key=os.getenv("GROQ_API_KEY"),
        )

    @llm
    def product_manager_llm(self) -> LLM:
        return self._groq_openai_compatible_llm()

    @llm
    def system_architect_llm(self) -> LLM:
        return self._groq_openai_compatible_llm()

    @llm
    def technical_writer_llm(self) -> LLM:
        return self._groq_openai_compatible_llm()

    #@llm
    #def quality_reviewer_llm(self) -> LLM:
        #return self._groq_openai_compatible_llm()

    @tool
    def pypi_lookup_tool(self) -> PyPIPackageLookupTool:
        return PyPIPackageLookupTool()

    @agent
    def product_manager(self) -> Agent:
        return Agent(
            config=self.agents_config["product_manager"],
            cache=False,
            executor_class=CrewAgentExecutor,
        )

    @agent
    def system_architect(self) -> Agent:
        return Agent(
            config=self.agents_config["system_architect"],
            cache=False,
            executor_class=CrewAgentExecutor,
        )

    @agent
    def technical_writer(self) -> Agent:
        return Agent(
            config=self.agents_config["technical_writer"],
            cache=False,
            executor_class=CrewAgentExecutor,
        )

    #@agent
    #def quality_reviewer(self) -> Agent:
        #return Agent(config=self.agents_config["quality_reviewer"])

    @task
    def product_requirements_task(self) -> Task:
        return Task(config=self.tasks_config["product_requirements_task"])

    @task
    def architecture_task(self) -> Task:
        return Task(config=self.tasks_config["architecture_task"])

    #@task
    #def draft_product_plan_task(self) -> Task:
        #return Task(config=self.tasks_config["draft_product_plan_task"])

    #@task
    #def quality_review_task(self) -> Task:
        #return Task(config=self.tasks_config["quality_review_task"])

    @task
    def final_product_plan_task(self) -> Task:
        return Task(config=self.tasks_config["final_product_plan_task"])

    @crew
    def crew(self) -> Crew:
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
            memory=False,
           # embedder={"provider": "onnx", "config": {}},
            planning=False,
        )
