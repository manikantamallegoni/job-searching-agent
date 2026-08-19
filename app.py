import os
import tempfile
import streamlit as st
import requests
from src.agent import JobAgent
from src.tools import extract_cv_text

# Page Configuration
st.set_page_config(
    page_title="AI Job Searching & Matching Agent",
    page_icon="💼",
    layout="wide"
)


st.title(" AI Job Searching & Matching Agent")
st.markdown("Upload your CV, parse your profile, and analyze job relevance in real-time.")

# --- ADD CUSTOM STYLING HERE ---
st.markdown("""
    <style>
    /* Main Page Background */
    .stApp {
        background-color: #0E1117;  /* Dark background - change to #F8F9FA for light theme */
        color: #FAFAFA;
    }
    
    /* Sidebar Background */
    section[data-testid="stSidebar"] {
        background-color: #161B22;  /* Slightly lighter tone for sidebar */
    }
    
    /* Custom Button Colors */
    .stButton>button {
        background-color: #4CAF50;  /* Green accent buttons */
        color: white;
        border-radius: 8px;
    }
    </style>
""", unsafe_allow_html=True)
# -------------------------------


# Initialize the Agent
@st.cache_resource
def load_agent():
    return JobAgent()

agent = load_agent()

# Sidebar for Resume Upload
st.sidebar.header("📄 Upload Resume")
uploaded_file = st.sidebar.file_uploader("Choose a PDF or DOCX file", type=["pdf", "docx"])

if uploaded_file is not None:
    # Save uploaded file temporarily
    with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(uploaded_file.name)[1]) as tmp_file:
        tmp_file.write(uploaded_file.getvalue())
        tmp_path = tmp_file.name

    # Extract plain text
    raw_cv_text = extract_cv_text.invoke({"file_path": tmp_path})

    st.sidebar.success("CV uploaded successfully!")

    # Create Tabs
    tab1, tab2 = st.tabs(["📊 CV Profile Summary", "🔍 Job Search & Matching"])

    with tab1:
        st.subheader("Parsed Profile Summary")
        if st.button("Analyze Resume"):
            with st.spinner("Analyzing resume content..."):
                analysis = agent.parse_cv(tmp_path)
                st.markdown(analysis)

    with tab2:
        st.subheader("Search & Match Open Jobs")
        search_query = st.text_input("Enter job keyword / role title", value="Python Developer")

        if st.button("Search & Match Jobs"):
            with st.spinner(f"Fetching job listings for '{search_query}'..."):
                url = f"https://himalayas.app/jobs/api/search?q={search_query}"
                response = requests.get(url)

                if response.status_code == 200:
                    jobs = response.json().get("jobs", [])[:3]
                    if not jobs:
                        st.warning("No jobs found for this role.")
                    else:
                        for idx, job in enumerate(jobs, 1):
                            title = job.get("title")
                            company = job.get("companyName")
                            locations = job.get('locationRestrictions') or ['Remote']
                            location = locations[0] if locations else 'Remote'
                            desc = job.get("excerpt") or "No description provided."

                            st.markdown("---")
                            st.markdown(f"### {idx}. {title} at **{company}** ({location})")

                            with st.spinner(f"Evaluating fit for {title}..."):
                                match_res = agent.match_job(
                                    cv_text=raw_cv_text,
                                    job_title=title,
                                    job_company=company,
                                    job_description=desc
                                )
                                st.markdown(match_res)
                else:
                    st.error("Failed to fetch jobs from API.")

    # Clean up temporary file
    os.remove(tmp_path)

else:
    st.info("👈 Please upload your CV in the sidebar to get started.")