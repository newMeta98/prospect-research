import requests
import re
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from openai import OpenAI

def fetch_page(url, headers):
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return BeautifulSoup(response.content, 'html.parser')
    else:
        print(f"HTTP error occurred: {response.status_code} {response.reason} for URL: {url}")
        return None

# Step 1: Extract Text Inside ** **
def extract_text_from_message(message):
    # Use regular expression to extract text inside ** **
    pattern = r'\*\*(.*?)\*\*'
    matches = re.findall(pattern, message)
    return matches

# Step 2: Determine the Type of Link and Handle Accordingly
def construct_full_url(link, base_url):
    # Check if the link is a full URL or a relative path
    if urlparse(link).scheme in ('http', 'https'):
        return link
    else:
        return urljoin(base_url, link)

# Step 3: Pass the Links to scrape_identified_pages

def scrape_identified_pages(links, headers):
    additional_info = {}
    for link in links:
        page_soup = fetch_page(link, headers)
        if page_soup:
            page_text = page_soup.get_text(separator='\n').strip()
            page_text = page_text.replace('\n', '')
            page_text = page_text.replace('\t', '')
            page_text = page_text.replace('\r', '')
            additional_info[link] = page_text 

    return additional_info

def scrape_website(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }

    soup = fetch_page(url, headers)
    if not soup:
        return None

    # Extract the full page HTML content
    full_page_text = soup.get_text(separator='\n').strip()
    full_page_text = full_page_text.replace('\n', '')
    full_page_text = full_page_text.replace('\t', '')
    full_page_text = full_page_text.replace('\r', '')

    # Extract all links from the page
    all_links = [a['href'] for a in soup.find_all('a', href=True)]

    # Send the links to an LLM via API to find useful links
    useful_links_message = find_links(all_links)

    # Extract text inside ** ** from the message
    useful_texts = extract_text_from_message(useful_links_message)

    # Split the extracted text into individual links
    useful_links = [link.strip() for text in useful_texts for link in text.split(',')]
    # Construct full URLs for the useful links
    full_urls = [construct_full_url(link, url) for link in useful_links]
    # Scrape the identified pages
    additional_info = scrape_identified_pages(full_urls, headers)

    # Update company information
    company_info = {
        'name': soup.find('title').text.strip(),
        'description': soup.find('meta', attrs={'name': 'description'})['content'] if soup.find('meta', attrs={'name': 'description'}) else 'No description available',
        'firstpage': full_page_text
    }
    company_info.update(additional_info)

    return company_info


def find_links(html_content):
    html_content = f"{html_content}"
    print(html_content)
    api_key = 'YOUR_API_KEY'  # Replace with your actual API key
    base_url = 'https://api.deepseek.com'
    headers = {
        'Authorization': f'Bearer {api_key}',
        'Content-Type': 'application/json'
    }
    data = {
        'model': 'deepseek-chat',
        'messages': [
            {'role': 'system', 'content': 'You are a helpful assistant gets all links from the html page and find any usefull links that can poses information about prospect for the sales team as output. Lets think through this step-by-step: 1. $Example_pages: about-us,team,our-team,contact-us,products,services,blog,news,careers,investors,press-releases,partners,clients,testimonials,case-studies,whitepapers,research,faq,support,pricing,solutions,industries,resources,events,webinars,media,awards,leadership,mission,vision,values,sustainability,csr,innovation,technology,partnerships,collaborations,community,feedback,reviews,customer-stories,success-stories,portfolio,projects,publications,reports,insights,trends,market-analysis,competitive-analysis,strategy,roadmap,milestones,achievements,history,timeline,culture,benefits,perks,diversity,inclusion,ethics,compliance,policies,terms,privacy,legal,disclaimer,accessibility,sitemap,archive. 2. RETURN ONLY 2 useful_page_links in following STRUCTURE ONLY "**useful_page_link1, useful_page_link2**"'},
            {'role': 'user', 'content': html_content}
        ],
        'stream': False
    }
    try:
        response = requests.post(f'{base_url}/chat/completions', headers=headers, json=data)
        response.raise_for_status()
        useful_links = response.json()['choices'][0]['message']['content']
        print(useful_links)
        return useful_links
    except requests.exceptions.HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')
        return f'An HTTP error occurred: {http_err}'
    except Exception as err:
        print(f'An error occurred: {err}')
        return f'An error occurred: {err}'
