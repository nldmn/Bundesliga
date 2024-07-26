from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time

# Initialize a WebDriver
driver = webdriver.Chrome(ChromeDriverManager().install())

# Navigate to the Bundesliga players page
driver.get('https://www.bundesliga.com/de/bundesliga/spieler')

# Wait for the JavaScript to execute and load content
time.sleep(5)  # Adjust time as necessary

# Get the page source after the JavaScript execution
html = driver.page_source

# Quit the WebDriver
driver.quit()

# Use Beautiful Soup to parse the HTML content
soup = BeautifulSoup(html, 'html.parser')

# Open a text file to write the summary
with open('bundesliga_clubs_players_summary.txt', 'w', encoding='utf-8') as file:
    # Find all <h2> tags where club names are defined
    clubs = soup.find_all('h2')
    for club in clubs:
        club_name = club.text.strip()
        file.write(f"{club_name}\n")
        
        # Find the next sibling of the <h2> tag which contains the players
        players_section = club.find_next_sibling('div')
        if players_section:
            # Find all player-card-simple components within the players_section
            players = players_section.find_all('player-card-simple')
            for player in players:
                # Extract player's name
                player_name = player.find('span', class_='names').get_text(strip=True)
                file.write(f"  - {player_name}\n")
        file.write("\n")

print("Summary has been written to bundesliga_clubs_players_summary.txt")
