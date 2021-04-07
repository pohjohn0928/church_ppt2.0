from bs4 import BeautifulSoup
import requests

response = requests.get('https://www.biblestudytools.com/nkjv/genesis/1.html')
soup = BeautifulSoup(response.text, "html.parser")
result = soup.find("span")
print(result)