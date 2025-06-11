import selenium.webdriver as webdriver
from selenium.webdriver.chrome.service import Service
import time
from bs4 import BeautifulSoup
from langchain_community.llms import Ollama
from langchain_core.prompts import ChatPromptTemplate

# Utility module containing reusable functions for web scraping and LLM parsing.
# This file centralizes logic used by both the Streamlit UI and FastAPI backend.
# Date: June 10,2025

# Template for LLM prompt, defining extraction rules for search_with_ollama function.
template = (
    "You are tasked with extracting specific information from the following text content: {dom_content}. "
    "Please follow these instructions carefully: \n\n"
    "1. **Extract Information:** Only extract the information that directly matches the provided description: {parse_description}. "
    "2. **No Extra Content:** Do not include any additional text, comments, or explanations in your response. "
    "3. **Empty Response:** If no information matches the description, return an empty string ('')."
    "4. **Direct Data Only:** Your output should contain only the data that is explicitly requested, with no other text."
)
# Instantiate the Ollama language model with the llama3.1 model for parsing tasks (may be updated with a new model),
# Must ensure Ollama server is running (ollama serve) and model is pulled (ollama pull llama3.1)
model = Ollama(model = "llama3.1")

def scrape_website(website):
    """ Scrape a website and return its raw HTML content.
    Args:
        website (str): The url to scrape.

    Returns:
        str: The page source HTML, or empty if scraping fails.

    Note:
        Uses ChromeDriver; make sure chromedriver.exe is in the project root and matches Chrome version.
    """
    print("Launching chrome browser....")
    chrome_driver_path = "./chromedriver.exe"
    options = webdriver.ChromeOptions()
    driver = webdriver.Chrome(service = Service(chrome_driver_path), options=options)
    try:
        driver.get(website)
        print("Page loaded....")
        html = driver.page_source
        return html
    finally:
        driver.quit()

def extract_body_content(html_content):
    """Extract the body content from raw HTML using BeautifulSoup.
    
    Args:
        html_content (str): The raw HTML string.
    
    Returns:
        str: The body content as a string, or empty if no body is found.
    """
    soup = BeautifulSoup(html_content, "html.parser")
    body_content = soup.body
    if body_content:
        return str(body_content)
    return ""

def clean_body_content(body_content):
    """Clean the body content by removing scripts, styles, and extra whitespace.
    
    Args:
        body_content (str): The raw body HTML content.
    
    Returns:
        str: Cleaned text content with scripts/styles removed and whitespace normalized.
    """
    soup = BeautifulSoup(body_content, "html.parser")
    for script_or_style in soup(["script", "style"]):
        script_or_style.extract()
    cleaned_content = soup.get_text(separator = "\n")
    cleaned_content = "\n".join (
        line.strip() for line in cleaned_content.splitlines() if line.strip()
    )
    return cleaned_content

def split_dom_content(dom_content, max_length = 6000):
    """Split DOM content into chunks of specified maximum length.
    
    Args:
        dom_content (str): The text content to split.
        max_length (int, optional): Maximum length of each chunk. Defaults to 6000.
    
    Returns:
        list: List of string chunks.
    """
    return [
        dom_content [i : i + max_length] for i in range(0, len(dom_content), max_length)
    ]

def search_with_ollama(dom_chunks, parse_description):
    """Search and extract specific information from DOM chunks using an LLM.
    
    Args:
        dom_chunks (list): List of string chunks to parse.
        parse_description (str): Description of the information to extract.
    
    Returns:
        str: Concatenated results from the LLM, joined by newlines.
    
    Note:
        Relies on the global 'model' and 'template' variables; make sure Ollama is configured.
    """
    prompt = ChatPromptTemplate.from_template(template)
    chain = prompt | model
    parsed_results = []
    for i, chunk in enumerate(dom_chunks, start = 1):
        response = chain.invoke(
            {"dom_content": chunk, "parse_description": parse_description}
        )
        print(f"Parsed batch {i} of {len(dom_chunks)}")
        parsed_results.append(response)
    return "\n".join(parsed_results)