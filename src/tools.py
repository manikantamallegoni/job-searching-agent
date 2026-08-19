import os
import requests
import docx
import pdfplumber
from langchain_core.tools import tool

@tool
def extract_cv_text(file_path: str) -> str:
    """Extracts text content from a CV file in PDF or DOCX format."""
    ext = os.path.splitext(file_path)[-1].lower()
    if ".docx" in ext:
        try:
            doc = docx.Document(file_path)
            text = [para.text for para in doc.paragraphs]
            return '\n'.join(text)
        except Exception as e:
            return f"Error reading .docx file: {e}"
    elif ".pdf" in ext:
        try:
            text = []
            with pdfplumber.open(file_path) as pdf:
                for page in pdf.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text.append(page_text)
            return '\n'.join(text)
        except Exception as e:
            return f"Error reading .pdf file: {e}"
    else:
        return "Unsupported file format! Please supply a .pdf or .docx file."


@tool
def fetch_jobs_from_api(query: str = "python") -> str:
    """Fetches real-time open remote job listings using the Himalayas Job Search API."""
    try:
        url = f"https://himalayas.app/jobs/api/search?q={query}"
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            jobs = response.json().get("jobs", [])[:5]
            if not jobs:
                return "No jobs found for the query."

            job_results = []
            for job in jobs:
                locations = job.get('locationRestrictions') or ['Remote']
                location = locations[0] if locations else 'Remote'
                job_results.append({
                    "title": job.get("title"),
                    "company": job.get("companyName"),
                    "location": location,
                    "description": job.get("excerpt") or "No description provided."
                })
            return str(job_results)
        return f"Failed to fetch jobs. HTTP Status: {response.status_code}"
    except Exception as e:
        return f"Error fetching jobs: {str(e)}"