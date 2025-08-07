from flask import Flask, render_template, request
from company_scraper import collect_company_data
from data_handler import save_company_data  # Add this import

app = Flask(__name__)
SERPAPI_KEY = "23416fceb088389320f491084a493f646b72e3c8a7b9510c44809400c35c8884"

@app.route('/')
def home():
    return render_template('index.html', result=None)

@app.route('/check', methods=['POST'])
def check():
    company_name = request.form['company_name']
    website_url = request.form['website_url']
    result = collect_company_data(company_name, website_url, SERPAPI_KEY)
    
    # Save the data and verify
    if save_company_data(result):
        print("Data saved successfully")  # Check Flask console for this
    else:
        print("Failed to save data")  # Check Flask console
    
    return render_template('index.html', result=result)

if __name__ == '__main__':
    app.run(debug=True)




