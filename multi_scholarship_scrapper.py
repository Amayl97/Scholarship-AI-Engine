import requests
from bs4 import BeautifulSoup

url = "https://scholarshipscorner.website/scholarships/"

response = requests.get(url)
soup = BeautifulSoup(response.text, "html.parser")

links = soup.find_all("a", class_="elementor-post__read-more")

scholarship_links = []



for link in links:
    url = link.get("href")
    if url:
        scholarship_links.append(url)

# print(scholarship_links)



field_aliases = {
    "degree_level": ["study level", "degree level", "level of study"],
    "country": ["study location", "host country", "country"],
    "deadline": ["deadline", "application deadline", "last date to apply"],
    "funding": ["what does the erasmus mundus scholarship covers"],
    "eligibility": ["eligibility criteria of the erasmus mundus joint masters scholarships", "typical Requirements"],
    "process": ["how to apply for erasmus mundus scholarship"]
}

scholarships = []

for url in scholarship_links:
    scholarship = {
    "title": "",
    "country": "",
    "degree_level": [],
    "deadline": "",
    "funding":"",
    "eligibility":[],
    "process":[]
    }
    
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    title = soup.find("h1").get_text(strip=True)
    scholarship["title"] = title

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

    scholarships.append(scholarship)
       
     
   


print(scholarships)