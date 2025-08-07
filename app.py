from flask import Flask, render_template, request
from company_scraper import collect_company_data
from data_handler import save_company_data  # Add this import
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
SERPAPI_KEY = os.getenv('SERPAPI_KEY')  # Get key from environment

@app.route('/')
def home():
    return render_template('index.html', result=None)

@app.route('/check', methods=['POST'])
def check():
    website_url = request.form['website_url']
    result = collect_company_data(website_url, SERPAPI_KEY)  # Removed company_name parameter
    
    # Save the data and verify
    if save_company_data(result):
        print("Data saved successfully")
    else:
        print("Failed to save data")
    
    return render_template('index.html', result=result)

if __name__ == '__main__':
    app.run(debug=True)




