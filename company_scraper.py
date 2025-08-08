import re
import requests
import tldextract
import whois
import ssl
import socket
from bs4 import BeautifulSoup
from serpapi import GoogleSearch
from datetime import datetime

def extract_domain(url):
    extracted = tldextract.extract(url)
    return f"{extracted.domain}.{extracted.suffix}"

def extract_company_name(website_url):
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(website_url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Try to get company name from common meta tags
        for meta_tag in ['og:site_name', 'og:title', 'twitter:site']:
            meta = soup.find('meta', {'property': meta_tag}) or soup.find('meta', {'name': meta_tag})
            if meta and meta.get('content'):
                return meta.get('content').strip()
        
        # Try to get from title tag
        title = soup.find('title')
        if title and title.string:
            # Clean up title text
            company_name = title.string.split('|')[0].split('-')[0].strip()
            if company_name:
                return company_name
                
        # Try to find h1 tags that might contain company name
        for h1 in soup.find_all('h1'):
            text = h1.get_text().strip()
            if text and len(text.split()) < 6:  # Skip long texts
                return text
                
    except Exception as e:
        print(f"Error extracting company name: {str(e)}")
    
    # Fallback to domain name if all else fails
    domain = extract_domain(website_url)
    return domain.split('.')[0].replace('-', ' ').title()

def has_ssl(domain):
    context = ssl.create_default_context()
    try:
        with socket.create_connection((domain, 443), timeout=5) as sock:
            with context.wrap_socket(sock, server_hostname=domain):
                return 1
    except:
        return 0

def find_email(website_url):
    try:
        domain = extract_domain(website_url)
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(website_url, headers=headers, timeout=10)
        emails = re.findall(r"[A-Za-z0-9._%+-]+@" + re.escape(domain), response.text)
        return emails[0] if emails else None
    except:
        return None

def count_scam_keywords(website_url):
    scam_keywords = ['scam', 'fraud', 'fake', 'not paid', 'unpaid', 'didn\'t pay', 'complaint', 'warning']
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(website_url, headers=headers, timeout=10)
        text = response.text.lower()
        return sum(kw in text for kw in scam_keywords)
    except:
        return 0

def get_google_reviews(company_name, serpapi_key):
    params = {
        "engine": "google",
        "q": f"{company_name} reviews",
        "api_key": serpapi_key,
        "num": 5  # Limit to 5 results
    }
    try:
        search = GoogleSearch(params)
        results = search.get_dict()
        links = []
        snippets = []
        
        for result in results.get("organic_results", []):
            link = result.get("link")
            if link:
                links.append(link)
            snippet = result.get("snippet") or result.get("title", "")
            if snippet:
                snippets.append(snippet)
        
        return links[:5], snippets[:5]  # Return maximum 5 results
    except Exception as e:
        print(f"Error getting Google reviews: {str(e)}")
        return [], []

def collect_company_data(website_url, serpapi_key):
    domain = extract_domain(website_url)
    company_name = extract_company_name(website_url)
    
    data = {
        "Company": company_name,
        "Website": website_url,
        "Domain": domain,
        "Domain Age": 0,
        "SSL": 0,
        "Email": None,
        "Scam Keywords": 0,
        "Google Links": [],
        "Review Snippets": [],
        "Verdict": ""
    }

    # Domain Age
    try:
        domain_info = whois.whois(domain)
        if domain_info.creation_date:
            if isinstance(domain_info.creation_date, list):
                creation = domain_info.creation_date[0]
            else:
                creation = domain_info.creation_date
            age_years = (datetime.now() - creation).days / 365
            data["Domain Age"] = round(age_years, 2)
    except Exception as e:
        print(f"Error getting domain age: {str(e)}")

    # SSL
    data["SSL"] = has_ssl(domain)

    # Email
    data["Email"] = find_email(website_url)

    # Scam Keywords
    data["Scam Keywords"] = count_scam_keywords(website_url)

    # Reviews
    links, snippets = get_google_reviews(company_name, serpapi_key)
    data["Google Links"] = links
    data["Review Snippets"] = snippets

    # Final Verdict with explanation
    score = 0
    reasons = []

    if data["Domain Age"] < 1:
        score += 1
        reasons.append("The domain is very new (less than 1 year old).")

    if data["SSL"] == 0:
        score += 1
        reasons.append("The website does not have an SSL certificate.")

    if not data["Email"]:
        score += 1
        reasons.append("No official company email found on the website.")

    if data["Scam Keywords"] > 3:
        score += 1
        reasons.append("Website content includes scam-related keywords.")

    if len(data["Review Snippets"]) == 0:
        score += 1
        reasons.append("No Google reviews or links were found.")

    if score < 3:
        data["Verdict"] = "✅ Genuine"
        data["Verdict Explanation"] = "This company seems trustworthy based on available signals like domain age, secure connection, valid contact info, and presence of reviews."
    else:
        data["Verdict"] = "❌ Fake or Suspicious"
        data["Verdict Explanation"] = "The company seems suspicious due to multiple red flags:\n- " + "\n- ".join(reasons)


    return data