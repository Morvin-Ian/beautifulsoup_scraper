from bs4 import BeautifulSoup
import random
import requests
import csv
import re
import json

user_agents = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Safari/605.1.15',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0'
]

headers = {'User-Agent': random.choice(user_agents)}

web_content = requests.get('https://www.brightermonday.co.ke/jobs/it-telecoms', headers=headers)

if web_content.status_code == 200:
    soup = BeautifulSoup(web_content.text, 'lxml')

    script_tag = soup.find_all('script')[16]
    html_data = f'''{script_tag}'''

    match = re.findall(r'__gtmDataLayer = (.*);', html_data)

    if match:
        data = json.loads(match[0])[0]

        job_listings = data.get('ecommerce', [])["items"]

        with open('brightermonday_jobs.csv', 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['title', 'company', 'location', 'category', 'total_hires', 'level', 'salary']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            # Write the header
            writer.writeheader()

            # Write each job listing to the CSV file
            for job in job_listings:
                writer.writerow({
                    'title': job.get('item_name', 'N/A'),
                    'company': job.get('affiliation', 'N/A'),
                    'location': job.get('location_id', 'N/A'),
                    'category': f"{job.get('item_category', 'N/A')} - {job.get('item_category2', 'N/A')}",
                    'total_hires': job.get('quantity', 'N/A'),
                    'level': job.get('item_category4', 'N/A'),
                    'salary': job.get('item_variant', 'N/A')
                })

        print("Job listings have been successfully written to 'job_listings.csv'.")
    else:
        print("No job data found in the script tag.")
else:
    print(f"Failed to retrieve the web page. Status code: {web_content.status_code}")
