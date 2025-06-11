import streamlit as st
import requests
#Main application module for the web scrapping UI, built with Streamlit.
#Thhis files serves as a frontend, interacting with the FastAPI backend via API calls.

st.title("Web Scrap") # Application title displayed.
url = st.text_input("Enter URL: ")# Input fielf for user to enter URL to scrap.

# Event handler for the scrape site button
#triggers an API call to scrape the provided URL and dsiplays the raw HTML content.
if st.button("Scrape Site"):
    st.write("Scraping......")
    response = requests.post("http://localhost:8000/scrape", json={"url": url}).json() 
    if response["status"] == "success":
        body_content = response["content"]
        #Store the raw HTML content in session state for late use.
        st.session_state.dom_content = body_content
        with st.expander("View DOM content..."): # Expandable section for raw content.
            st.text_area("DOM Content", body_content, height=300) # Display raw HTML.
    else:
        st.error(response["error"]) # Diplay any scraping errors.

# Conditional block to show parsing UI if content is available in session state.
if "dom_content" in st.session_state:
    parse_description = st.text_area("Describe what you want to search from content.")# Test area for users to search scraped content.
    if st.button("Search Content"): # Event handler for button
        if parse_description:
            st.write("Searched Results:") # Indicate parsing results are incoming.
            # API call to parse the content based on the user's description.
            response = requests.post("http://localhost:8000/parse", json={"content": [st.session_state.dom_content], "query": parse_description}).json()
            st.write(response["result"]) # Display the parsed result.
