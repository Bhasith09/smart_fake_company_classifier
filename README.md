Fake Company Checker

A web-based tool built with Python (Flask) that detects potentially fake or suspicious companies by analyzing their website data, domain information, and online presence. This project helps job seekers, freelancers, and businesses avoid scams by providing a trustworthiness report.

🚀 Features
Domain Analysis

Extracts domain age (WHOIS lookup)

Checks for SSL certificate availability

Website Scraping

Attempts to detect official company name

Searches for an official email on the site

Counts scam-related keywords in content

Review Analysis

Fetches Google review links & snippets using SerpAPI

Risk Assessment

Generates a final verdict (Genuine ✅ or Fake/Suspicious ❌)

Provides a human-readable explanation for the verdict

Data Logging

Saves all company checks into a CSV file for research & record keeping

User-Friendly UI

Clean HTML/CSS interface

Mobile-friendly responsive design

Loading spinner for better UX

🛠️ Tech Stack
Backend: Python, Flask

Frontend: HTML5, CSS3 (vanilla)

Data Handling: CSV

APIs: SerpAPI (Google Search)

Libraries:

requests, beautifulsoup4 (web scraping)

tldextract (domain extraction)

python-whois (domain age lookup)

ssl, socket (SSL check)

dotenv (environment variable management)
