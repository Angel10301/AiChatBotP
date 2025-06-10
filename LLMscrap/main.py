import streamlit as st
from scrape import scrape_website, split_dom_content, clean_body_content, extract_body_content
from search import search_with_ollama

st.title("Web Scrap")
url = st.text_input("Enter an url: ")

if st.button("Scrape Site"):
    st.write("Scraping......")
    result = scrape_website(url)
    body_content = extract_body_content(result)
    cleaned_content = clean_body_content(body_content)

    st.session_state.dom_content = cleaned_content
    
    with st.expander("View DOM content..."):
        st.text_area("DOM Content", cleaned_content, height = 300)

if "dom_content" in st.session_state:
    parse_description = st.text_area("Describe what you want to search from content.")

    if st.button("Search Content"):
        if parse_description:
            st.write("Searching....")
            
            dom_chunks = split_dom_content(st.session_state.dom_content)
            result = search_with_ollama(dom_chunks, parse_description)
            st.write(result)

    