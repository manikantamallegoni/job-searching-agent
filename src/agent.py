from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage
from src.config import Config
from src.prompts import CV_ANALYSIS_PROMPT, JOB_MATCHING_PROMPT
from src.tools import extract_cv_text, fetch_jobs_from_api

class JobAgent:
    """Core AI Agent class for CV parsing and job relevance matching."""

    def __init__(self):
        Config.validate()
        self.llm = ChatOpenAI(
            model=Config.DEFAULT_MODEL,
            openai_api_key=Config.OPENROUTER_API_KEY,
            openai_api_base=Config.OPENROUTER_BASE_URL
        )

    def parse_cv(self, file_path: str) -> str:
        """Extracts and summarizes CV content."""
        raw_text = extract_cv_text.invoke({"file_path": file_path})
        if "Error" in raw_text or "Unsupported" in raw_text:
            return raw_text

        prompt = CV_ANALYSIS_PROMPT.format(cv_text=raw_text)
        response = self.llm.invoke([HumanMessage(content=prompt)])
        return response.content

    def match_job(self, cv_text: str, job_title: str, job_company: str, job_description: str) -> str:
        """Evaluates match score between CV text and a job posting."""
        prompt = JOB_MATCHING_PROMPT.format(
            cv_text=cv_text,
            job_title=job_title,
            job_company=job_company,
            job_description=job_description
        )
        response = self.llm.invoke([HumanMessage(content=prompt)])
        return response.content

