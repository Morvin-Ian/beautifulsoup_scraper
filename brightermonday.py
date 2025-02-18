from bs4 import BeautifulSoup
from utils import headers
import requests
import csv
import re
import json

web_content = requests.get('https://www.brightermonday.co.ke/jobs/it-telecoms', headers=headers)

if web_content.status_code == 200:
    soup = BeautifulSoup(web_content.text, 'lxml')

    script_tag = soup.find_all('script')[15]
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
