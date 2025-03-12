import requests
from bs4 import BeautifulSoup
import argparse
import time
import concurrent.futures
import os

def fetch_issues(volume, api_key):
    """
    Fetches issues for a given volume from the congress.gov API.

    Args:
        volume (str): The volume number of the Congressional Record.
        api_key (str): The API key for accessing congress.gov.

    Returns:
        list: A list of issues for the given volume.
    """
    url = f"https://api.congress.gov/v3/daily-congressional-record/{volume}?format=json&api_key={api_key}&limit=1000"
    retries = 10
    for i in range(retries):
        response = requests.get(url)
        if response.status_code == 200:
            return response.json().get("dailyCongressionalRecord", [])
        else:
            wait_time = 2 ** i
            print(f"Error: {response.status_code}, {response.text}. Retrying in {wait_time} seconds...")
            time.sleep(wait_time)
    print("Failed to fetch issues after multiple retries.")
    return []

def fetch_articles(volume, issue, api_key):
    """
    Fetches articles for a given volume and issue from the congress.gov API.

    Args:
        volume (str): The volume number of the Congressional Record.
        issue (str): The issue number of the Congressional Record.
        api_key (str): The API key for accessing congress.gov.

    Returns:
        dict: A dictionary containing the articles for the given volume and issue.
    """
    url = f"https://api.congress.gov/v3/daily-congressional-record/{volume}/{issue}/articles?format=json&api_key={api_key}&limit=1000"
    retries = 10
    for i in range(retries):
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        else:
            wait_time = 2 ** i
            print(f"Error: {response.status_code}, {response.text}. Retrying in {wait_time} seconds...")
            time.sleep(wait_time)
    print("Failed to fetch articles after multiple retries.")
    return None

def extract_formatted_text_urls(data):
    """
    Extracts URLs of formatted text from the articles data.

    Args:
        data (dict): The data containing articles.

    Returns:
        list: A list of URLs of formatted text.
    """
    urls = []
    if "articles" in data:
        for article in data["articles"]:
            for section in article.get("sectionArticles", []):
                for text_entry in section.get("text", []):
                    if text_entry.get("type") == "Formatted Text":
                        urls.append({
                            "url": text_entry.get("url"),
                            "startPage": section.get("startPage"),
                            "endPage": section.get("endPage")
                        })
    # Sort by startPage, then endPage
    urls.sort(key=lambda x: (x["startPage"], x["endPage"]))
    return [url["url"] for url in urls]

def fetch_text_from_url(url):
    """
    Fetches text content from a given URL.

    Args:
        url (str): The URL to fetch the text content from.

    Returns:
        str: The text content fetched from the URL.
    """
    print(f"Fetching {url}...")
    retries = 10
    for i in range(retries):
        try:
            response = requests.get(url, timeout=30)
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                return soup.get_text()
            else:
                wait_time = 2 ** i
                print(f"Error: {response.status_code}. Retrying in {wait_time} seconds...")
                time.sleep(wait_time)
        except (requests.exceptions.Timeout, requests.exceptions.ConnectionError) as e:
            wait_time = 2 ** i
            print(f"Error: {e}. Retrying in {wait_time} seconds...")
            time.sleep(wait_time)
    print(f"Failed to fetch {url} after multiple retries.")
    return None

def fetch_and_compile_articles(volume, issue, api_key, force_override=False):
    """
    Fetches and compiles articles for a given volume and issue, and writes them to a file.

    Args:
        volume (str): The volume number of the Congressional Record.
        issue (str): The issue number of the Congressional Record.
        api_key (str): The API key for accessing congress.gov.
        force_override (bool): Whether to force override existing record files.

    Returns:
        None
    """
    print(f"Fetching articles for Volume {volume}, Issue {issue}...")
    directory = f'congressional_records_{volume}'
    os.makedirs(directory, exist_ok=True)
    file_path = os.path.join(directory, f'congressional_record_{volume}_{issue}.txt')
    
    # Check if the file already exists and if force_override is not set
    if os.path.exists(file_path) and not force_override:
        print(f"File {file_path} already exists. Skipping...")
        return
    
    data = fetch_articles(volume, issue, api_key)
    if data and data.get("articles"):
        with open(file_path, 'w') as f:
            f.write(f"Congressional Record Volume {volume}, Issue {issue}\n")
            urls = extract_formatted_text_urls(data)
            
            for url in urls:
                text_content = fetch_text_from_url(url)
                if text_content:
                    f.write(text_content)
                    f.write("\n\n")
    else:
        print("No articles")

def main():
    """
    Main function to parse arguments and fetch Congressional Record articles.

    Args:
        None

    Returns:
        None
    """
    parser = argparse.ArgumentParser(description="Fetch Congressional Record articles.")
    parser.add_argument("volume", type=str, help="Congressional Record Volume")
    parser.add_argument("api_key", type=str, help="API Key for congress.gov")
    parser.add_argument("--force-override", action="store_true", help="Force override existing record files")
    args = parser.parse_args()

    issues = fetch_issues(args.volume, args.api_key)
    issue_numbers = [issue["issueNumber"] for issue in issues]

    print(f"Found {len(issue_numbers)} issues for Volume {args.volume}")
    
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = [executor.submit(fetch_and_compile_articles, args.volume, issue_number, args.api_key, args.force_override) for issue_number in issue_numbers]
        for future in concurrent.futures.as_completed(futures):
            future.result()

if __name__ == "__main__":
    main()
