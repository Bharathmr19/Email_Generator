import streamlit as st
from langchain_community.document_loaders import WebBaseLoader
from chains import Chain
from portfolio import Portfolio
from utils import clean_text

# Set page config for wider layout and title
st.set_page_config(layout="wide", page_title="Cold Email Generator", page_icon="📧")

def create_streamlit_app(llm, portfolio, clean_text):
    # Header Section
    st.title("📧 Cold Mail Generator")
    st.markdown("<h2 style='color: #4CAF50;'>Generate Personalized Cold Emails</h2>", unsafe_allow_html=True)

    # Add a background image (make sure to have the image accessible)
    st.markdown(
        """
        <style>
        .stApp {
            background-image: url('https://example.com/your-background-image.jpg');
            background-size: cover;
            background-repeat: no-repeat;
            background-attachment: fixed;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    # Input Section
    st.sidebar.header("Configuration")
    url_input = st.sidebar.text_input("Enter a URL:", value="https://jobs.nike.com/job/R-33460", placeholder="https://example.com")
    submit_button = st.sidebar.button("Generate Email")

    # Processing Section
    if submit_button:
        with st.spinner("Loading..."):
            try:
                loader = WebBaseLoader([url_input])
                data = clean_text(loader.load().pop().page_content)

                portfolio.load_portfolio()
                jobs = llm.extract_jobs(data)

                if not jobs:
                    st.warning("No jobs found at the provided URL.")
                else:
                    for job in jobs:
                        skills = job.get('skills', [])
                        links = portfolio.query_links(skills)
                        email = llm.write_mail(job, links)

                        # Display generated email with card style
                        st.markdown(
                            f"""
                            <div style="border: 1px solid #ddd; border-radius: 5px; padding: 10px; margin: 10px 0; background-color: rgba(255, 255, 255, 0.8);">
                                <h4 style="color: #333;">Email for: {job.get('title', 'Unknown Job')}</h4>
                                <pre style="white-space: pre-wrap; word-wrap: break-word;">{email}</pre>
                            </div>
                            """,
                            unsafe_allow_html=True
                        )
            except Exception as e:
                st.error(f"An Error Occurred: {e}")

    # Footer Section
    st.markdown("---")
    st.markdown("<h5 style='text-align: center;'>Made with ❤️ by Bharath</h5>", unsafe_allow_html=True)
    st.markdown("For support, contact [support@example.com](mailto:support@example.com).", unsafe_allow_html=True)

if __name__ == "__main__":
    chain = Chain()
    portfolio = Portfolio()
    create_streamlit_app(chain, portfolio, clean_text)
