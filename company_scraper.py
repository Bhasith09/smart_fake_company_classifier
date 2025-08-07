import re
import requests
import tldextract
import whois
import ssl
import socket
from bs4 import BeautifulSoup
from serpapi import GoogleSearch

def extract_domain(url):
    extracted = tldextract.extract(url)
    return f"{extracted.domain}.{extracted.suffix}"

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
        response = requests.get(website_url, timeout=5)
        emails = re.findall(r"[A-Za-z0-9._%+-]+@" + re.escape(domain), response.text)
        return emails[0] if emails else None
    except:
        return None


def count_scam_keywords(website_url):
    scam_keywords = ['scam', 'fraud', 'fake', 'not paid', 'unpaid', 'didn\'t pay']
    try:
        response = requests.get(website_url, timeout=5)
        text = response.text.lower()
        return sum(kw in text for kw in scam_keywords)
    except:
        return 0

def get_google_reviews(company_name, serpapi_key):
    params = {
        "engine": "google",
        "q": f"{company_name} reviews",
        "api_key": serpapi_key
    }
    try:
        search = GoogleSearch(params)
        results = search.get_dict()
        links = []
        snippets = []
        for result in results.get("organic_results", []):
            links.append(result.get("link"))
            snippet = result.get("snippet") or result.get("title", "")
            snippets.append(snippet)
        return links, snippets
    except:
        return [], []

def collect_company_data(company_name, website_url, serpapi_key):
    domain = extract_domain(website_url)
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
            from datetime import datetime
            if isinstance(domain_info.creation_date, list):
                creation = domain_info.creation_date[0]
            else:
                creation = domain_info.creation_date
            age_years = (datetime.now() - creation).days / 365
            data["Domain Age"] = round(age_years, 2)
    except:
        pass

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

    # Final Verdict
    score = 0
    if data["Domain Age"] < 1:
        score += 1
    if data["SSL"] == 0:
        score += 1
    if not data["Email"]:
        score += 1
    if data["Scam Keywords"] > 3:
        score += 1
    if len(data["Review Snippets"]) == 0:
        score += 1

    data["Verdict"] = "✅ Genuine" if score < 3 else "❌ Fake or Suspicious"

    return data
