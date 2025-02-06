from urllib.parse import urljoin
import time
import re
from bs4 import BeautifulSoup
from litellm import completion
from langchain_google_genai import ChatGoogleGenerativeAI
import os
import requests
from dotenv import load_dotenv
load_dotenv()
llm = ChatGoogleGenerativeAI(
    api_key=os.getenv("API_KEY"),
    model=os.getenv("MODEL_LC")
)
query = "Elon Musk"

response = llm.invoke(
    f"the users query is this, generate some links for webscrapping to find details about this query online; the query is `{query}`, just return the links because they will be pased to a function in the work flow, dont generate any text")

x = response.content
print(x)


def format_and_store_links(input_text):
    # Use regex to find URLs, which may or may not be surrounded by markdown syntax
    links = re.findall(r'https?://[^\s\)]+', input_text)

    return links


asad = format_and_store_links(x)


def web_scrape_for_llm(url: str, retries=1, delay=3, timeout=20) -> str:
    """Scrapes a webpage and extracts its text content to be passed to an LLM, with retry and timeout support."""

    for attempt in range(retries):
        try:
            print(f"Fetching URL: {url}")  # Debugging the URL
            # Set timeout for the request
            response = requests.get(url, timeout=timeout)
            response.raise_for_status()  # Check for HTTP errors

            # Parse HTML content with BeautifulSoup
            soup = BeautifulSoup(response.content, 'html.parser')

            # Extract all the text from the webpage
            page_text = soup.get_text(separator=" ", strip=True)

            # Optionally, you can limit the length of the text to make it more manageable for LLMs
            # You can adjust the length as needed
            truncated_text = page_text[:100]

            return truncated_text

        except requests.exceptions.RequestException as e:
            print(f"""Error fetching the URL: {url}, attempt {
                  attempt + 1} of {retries}, error: {str(e)}""")
            if attempt + 1 < retries:
                print(f"Retrying in {delay} seconds...")
                time.sleep(delay)  # Delay before retry
            else:
                return f"Error fetching the URL: {str(e)}"

        except requests.exceptions.Timeout:
            print(f"Timeout occurred for URL: {url}. No data found.")
            return "No data found"

    return "Failed to fetch the URL after multiple attempts."


answers = []
for links in asad:
    res = web_scrape_for_llm(links)
    answers.append(res)
