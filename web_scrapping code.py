import requests
from bs4 import BeautifulSoup
import csv
import lxml
from itertools import zip_longest

video_game = []
price = []
kind = []
links = []
devoloper = []
platform = []
type = []

page = 1
while True:
    url = f"https://sandbox.oxylabs.io/products?page={page}"
    result = requests.get(url)
    src = result.content
    soup = BeautifulSoup(src, "lxml")

    video_games = soup.find_all("h4", {"class": "title css-7u5e79 eag3qlw7"})
    prices = soup.find_all("div", {"class": "price-wrapper css-li4v8k eag3qlw4"})
    kinds = soup.find_all("span", {"class": "css-1pewyd6 eag3qlw8"})
    link_tags = soup.find_all("a", {"class": "card-header css-o171kl eag3qlw2"})

    
    if not video_games:
        break

    for i in range(len(video_games)):
        video_game.append(video_games[i].text.strip())
        price.append(prices[i].text.strip())
        kind.append(kinds[i].text.strip())
        links.append("https://sandbox.oxylabs.io" + link_tags[i]["href"])

    page += 1  

for link in links:
    result = requests.get(link)
    src = result.content
    soup = BeautifulSoup(src, "lxml")

    # Developer
    dev_tag = soup.find("span", {"class": "brand developer"})
    devoloper.append(dev_tag.text.strip().replace("Developer:","") if dev_tag else "N/A")

    # Platform
    platform_tag = soup.find("span", {"class": "game-platform css-13htf5s e1pl6npa7"})
    platform.append(platform_tag.text.strip() if platform_tag else "N/A")

    # Type
    type_wrapper = soup.find("strong", string="Type:")
    if type_wrapper and type_wrapper.parent:
        full_text = type_wrapper.parent.get_text(separator=" ", strip=True)
        if ":" in full_text:
            game_type = full_text.split(":", 1)[1].strip()
            type.append(game_type)
        else:
            type.append("N/A")
    else:
        type.append("N/A")

file_list = [video_game, price, kind, links, devoloper, platform, type]
exported = zip_longest(*file_list)

with open(r"C:\Users\maham\Desktop\random\web task.csv", "w", newline='') as myfile:
    wr = csv.writer(myfile)
    wr.writerow(["video_game", "price", "kind", "link", "devoloper", "platform", "type"])
    wr.writerows(exported)
