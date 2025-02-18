from bs4 import BeautifulSoup
from utils import headers
import requests
import pdb
import csv

web_content = requests.get('https://footballkenya.org/competitions/fkf-premier-league/standings/', headers=headers, verify=False)


if web_content.status_code == 200:
    soup = BeautifulSoup(web_content.text, 'lxml')
    kpl_table = soup.find('tbody')
    teams = kpl_table.find_all('tr')

    with open('standings.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Rank', 'Name', 'Logo URL', 'Played', 'Wins', 'Draws', 'Losses', 'Goals For', 'Goals Against', 'Goal Differential', 'Points'])
        
        for team in teams:
            name = team.find('td', class_='data-name').text
            rank = team.find('td', class_='data-rank').text
            img_tag = team.find('img')
            logo = img_tag.get('src') if img_tag else None
            played = team.find('td', class_='data-p').text
            wins = team.find('td', class_='data-w').text
            draws = team.find('td', class_='data-d').text
            losses = team.find('td', class_='data-l').text
            goals_for = team.find('td', class_='data-f').text
            goals_against = team.find('td', class_='data-a').text
            goal_differential = team.find('td', class_='data-gd').text
            points = team.find('td', class_='data-pts').text

            writer.writerow([rank, name, logo, played, wins, draws, losses, goals_for, goals_against, goal_differential, points])

    print("\nData has been saved to team_data.csv")

else:
    print(f"Failed to retrieve the web page. Status code: {web_content.status_code}")