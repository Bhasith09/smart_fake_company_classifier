import csv
import os
from datetime import datetime
from pathlib import Path

DATA_FILE = 'company_data.csv'

def save_company_data(data):
    try:
        # Create directory if it doesn't exist
        Path(DATA_FILE).parent.mkdir(parents=True, exist_ok=True)
        
        file_exists = os.path.isfile(DATA_FILE)
        
        with open(DATA_FILE, 'a', newline='', encoding='utf-8') as csvfile:
            fieldnames = [
                'timestamp', 'company_name', 'website_url', 'domain',
                'domain_age', 'has_ssl', 'email', 'scam_keywords_count',
                'verdict'
            ]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            
            if not file_exists:
                writer.writeheader()
            
            writer.writerow({
                'timestamp': datetime.now().isoformat(),
                'company_name': data.get('Company', ''),
                'website_url': data.get('Website', ''),
                'domain': data.get('Domain', ''),
                'domain_age': data.get('Domain Age', 0),
                'has_ssl': bool(data.get('SSL', 0)),
                'email': data.get('Email', ''),
                'scam_keywords_count': data.get('Scam Keywords', 0),
                'verdict': data.get('Verdict', '')
            })
        return True
    except Exception as e:
        print(f"Error saving data: {str(e)}")
        return False