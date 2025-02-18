from bs4 import BeautifulSoup
from utils import headers
import requests
import csv


web_content = requests.get(
    'https://thenextweb.com/future-of-work',
    headers=headers
)

if web_content.status_code == 200:
    soup = BeautifulSoup(web_content.text, 'lxml')
    articles = soup.find_all('article', class_='c-listArticle')

    with open("tnx_articles.csv", 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Title', 'Image Link', 'Published Date', 'More Information'])

        for index, article in enumerate(articles):
            article_title = article.find('a', class_='title_link').text.strip()
            article_image_link = article.find('img')['data-src']
            meta_items = article.find_all('li', class_='c-meta__item')
            published_date = meta_items[-1].text.strip()
            more_information = (
                "https://thenextweb.com" +
                article.find('a', class_='title_link')['href']
            )

            row_data = [
                article_title,
                article_image_link,
                published_date,
                more_information
            ]
            writer.writerow(row_data)

    print("Data saved to articles.csv")
else:
    print(f"Failed to retrieve the page. Status code: {web_content.status_code}")
