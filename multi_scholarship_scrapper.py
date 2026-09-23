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


print("Total URLs: ", len(scholarship_links))



field_aliases = {
    "degree_level": ["study level", "degree level", "level of study"],
    "country": ["study location", "host country", "country"],
    "deadline": ["deadline", "application deadline", "last date to apply"],
    "funding": ["what does the erasmus mundus scholarship covers", "benefits",
    "scholarship benefits",
    "benefits of the scholarship"],
    "eligibility": ["eligibility criteria of the erasmus mundus joint masters scholarships", "typical Requirements"],
    "process": ["how to apply for erasmus mundus scholarship"]
}

scholarships = []

for url in scholarship_links:
   try:
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
        if field == "funding" and "benefits" in heading_txt:
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
                  
           
         # if aliases matched
        elif heading_txt in aliases:
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

   except Exception as e:
         print(f"Failed to scrape {url} : {e}")
     
   

# Clean the data

cleaned_scholarships = []



def clean_text(text):
   return " ".join(text.split())

for scholarship in scholarships:
   scholarship["title"] = clean_text(scholarship["title"])
   scholarship["country"] = clean_text(scholarship["country"])
   scholarship["deadline"] = clean_text(scholarship["deadline"])

   cleaned_scholarships.append(scholarship)


print(cleaned_scholarships)