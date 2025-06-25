# LLMscrap

LLMscrap is a powerful web scraping and content parsing application designed to extract and analyze data from any website.
Built with Python, it leverages a FastAPI backend for RESTful API endpoints, a Streamlit-based user interface for interactive access, and an integrated Large Language Model (LLM) powered by Ollama to intelligently parse scraped content. 
Ideal for researchers, developers, and data enthusiasts, LLMscrap enables users to scrape web pages and extract specific information (e.g., rankings, prices) with customizable queries.

## Features

- **Web Scraping**: Extracts raw HTML from any website using Selenium and BeautifulSoup.
- **Content Parsing**: Utilizes an LLM (Ollama with llama3.1) to parse scraped data based on user-defined queries.
- **User-Friendly UI**: Provides an interactive Streamlit interface to input URLs and search terms.
- **API Access**: Offers RESTful endpoints (`/scrape` and `/parse`) for programmatic use.
- **Data Storage**: Includes optional in-memory or file-based storage of scraped and parsed results.

## Prerequisites

- **Python 3.8**: Ensure Python 3.8 is installed.
- **Git**: Required for cloning the repository.
- **Ollama**: Install from [ollama.ai](https://ollama.ai/) for LLM functionality.
- **Google Chrome**: Needed for Selenium-based scraping.
- **ChromeDriver**: Download from [chromedriver.chromium.org](https://chromedriver.chromium.org/downloads) and place in the project root, matching your Chrome version.

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/LLMscrap.git
   cd LLMscrap
