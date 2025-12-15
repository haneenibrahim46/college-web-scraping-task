import requests
from bs4 import BeautifulSoup
import csv
import time
import os

print("Starting the scraper...")

if not os.path.exists("output"):
    os.makedirs("output")
    print("Created 'output' folder")

filename = "output/quotes.csv"
file = open(filename, "w", encoding="utf-8", newline="")
writer = csv.writer(file)
writer.writerow(["Quote", "Author", "Tags"])
print(f"CSV file prepared at {filename}")

base_url = "https://quotes.toscrape.com/page/{}/"

for page in range(1, 11): 
    print(f"Scraping page {page}...")
    url = base_url.format(page)
    response = requests.get(url)

    if response.status_code != 200:
        print(f"Error loading page {page}")
        continue

    soup = BeautifulSoup(response.text, "html.parser")
    quotes = soup.find_all("div", class_="quote")
    print(f"Found {len(quotes)} quotes on page {page}")  

    if not quotes:
        print(f"No quotes found on page {page}, stopping.")
        break

    for quote in quotes:
        text = quote.find("span", class_="text").get_text(strip=True)
        author = quote.find("small", class_="author").get_text(strip=True)
        tag_elements = quote.find_all("a", class_="tag")
        tags = [tag.get_text(strip=True) for tag in tag_elements]
        tags_string = ", ".join(tags)
        writer.writerow([text, author, tags_string])

    time.sleep(1)  
    
file.close()
print("Scraping completed!")
print(f"Data saved in {filename}")