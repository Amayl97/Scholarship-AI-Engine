import requests
from bs4 import BeautifulSoup

url = "https://scholarshipscorner.website/erasmus-mundus-scholarship/"

response = requests.get(url)

soup = BeautifulSoup(response.text, "html.parser")

field_aliases = {
    "degree_level": ["study level", "degree level", "level of study"],
    "country": ["study location", "host country", "country"],
    "deadline": ["deadline", "application deadline", "last date to apply"]
}

scholarship = {
    "title": "Erasmus",
    "country": "",
    "degree_level": [],
    "deadline": ""
}

headings = soup.find_all("h3")

for heading in headings:
     heading_txt = heading.get_text(strip=True).lower().rstrip(":")
     for field, aliases in field_aliases.items():
         # if aliases matched
        if heading_txt in aliases:
           ul = heading.find_next("ul")
           if ul:
               info = []
               items = ul.find_all("li")
               if items:
                   for item in items:
                      info.append(item.get_text(strip=True))

                   scholarship[field] = info
               else:
                  items = []
           else:
               items = []
       
     
   

print(scholarship)


