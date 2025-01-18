
import os
import requests
from bs4 import BeautifulSoup
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from typing import List, Optional

def create_session() -> requests.Session:
    """
    Create a requests session with retry policy.

    Returns:
        A configured requests.Session object.
    """
    session = requests.Session()
    retry = Retry(
        total=5,
        backoff_factor=1,
        status_forcelist=[429, 500, 502, 503, 504],
        allowed_methods=["GET"]
    )
    adapter = HTTPAdapter(max_retries=retry)
    session.mount("https://", adapter)
    session.mount("http://", adapter)
    return session

def fetch_html(url: str, headers: dict) -> Optional[str]:
    """
    Fetch HTML content from a URL.

    Args:
        url: The target URL to fetch content from.
        headers: HTTP headers to include in the request.

    Returns:
        The HTML content as a string, or None if an error occurs.
    """
    session = create_session()
    try:
        response = session.get(url, headers=headers)
        response.raise_for_status()
        return response.text
    except requests.exceptions.HTTPError as err:
        print(f"HTTP error occurred: {err}")
    except Exception as e:
        print(f"An error occurred: {e}")
    return None

def extract_and_save_divs(html_content: str, div_ids: List[str], output_file_path: str) -> None:
        """
        Extract content of specified div elements and save to a file.
    
        Args:
            html_content: The HTML content to parse.
            div_ids: A list of div IDs to extract content from.
            output_file_path: The file path to save the extracted content.
    
        Returns:
            None
        """
        try:
            soup = BeautifulSoup(html_content, "html.parser")
            combined_content = ""
    
            for div_id in div_ids:
                target_div = soup.find("div", id=div_id)
                if target_div:
                    if not isinstance(target_div, str):
                        combined_content += target_div.prettify()
                    else:
                        combined_content += target_div
                else:
                    print(f"The target_div with id '{div_id}' was not found.")
            
            if not combined_content:
                # Log a snippet of the HTML to help identify correct div IDs
                print("Failed to extract any content. Here's a snippet of the fetched HTML for inspection:")
                print(soup.prettify()[:1000])  # Print first 1000 characters
    
            if combined_content:
                with open(output_file_path, "w", encoding="utf-8") as file:
                    file.write(combined_content)
                print(f"The content was successfully saved to: {output_file_path}")
            else:
                print("No content was extracted.")
    
        except Exception as e:
            print(f"An error occurred during HTML processing: {e}")

def main() -> None:
    """
    Main function to execute the data extraction and saving process.

    Returns:
        None
    """
    url : str = "https://archive.is/20250117210838/https://www.cnbc.com/2025/01/17/returns-on-treasury-bonds-havent-been-this-poor-in-the-last-90-years.html"
    headers: dict = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)"
    }
    div_ids: List[str] = ["RegularArticle-ArticleHeader-2", "RegularArticle-ArticleBody-5"]  # List of IDs to search for
    output_file_path: str = os.path.join(os.getcwd(), "target_div.html")

    html_content = fetch_html(url, headers)
    if html_content:
        extract_and_save_divs(html_content, div_ids, output_file_path)

if __name__ == "__main__":
    main()



