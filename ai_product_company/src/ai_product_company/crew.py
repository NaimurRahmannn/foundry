import os

from crewai import Agent, Crew, LLM, Process, Task
from crewai.project import CrewBase, agent, crew, llm, output_pydantic, task

from schemas.product_requirements import ProductRequirements


@CrewBase
class AiProductCompany:
    """Classic CrewAI crew for the ai_product_company project."""

    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"

    @output_pydantic
    class product_requirements_output(ProductRequirements):
        pass

    def _groq_openai_compatible_llm(self) -> LLM:
        return LLM(
            model="llama-3.3-70b-versatile",
            base_url="https://api.groq.com/openai/v1",
            api_key=os.getenv("GROQ_API_KEY") or os.getenv("OPENAI_API_KEY"),
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

    @agent
    def product_manager(self) -> Agent:
        return Agent(config=self.agents_config["product_manager"])

    @agent
    def system_architect(self) -> Agent:
        return Agent(config=self.agents_config["system_architect"])

    @agent
    def technical_writer(self) -> Agent:
        return Agent(config=self.agents_config["technical_writer"])

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
            memory=True,
            embedder={"provider":"onnx","config":{}},
            planning=False,
        )
