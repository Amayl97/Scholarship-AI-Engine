import requests
from bs4 import BeautifulSoup
import re

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
    "funding": ["what does the scholarship covers", "benefits",
    "scholarship benefits",
    "benefits of the scholarship"],
    "eligibility": ["eligibility criteria of the erasmus mundus joint masters scholarships", "typical Requirements", ""],
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
    "gpa_min": None,
    "gpa_scale": None,
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
                  
        elif field == "eligibility" and "Eligibility Criteria" in heading_txt or "eligibility criteria" in heading_txt:
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
    if text is None:
        return ""
    return " ".join(text.split())

def clean_list(items):
    return [clean_text(item) for item in items]

for scholarship in scholarships:

    scholarship["title"] = clean_text(scholarship["title"])
    scholarship["country"] = clean_list(scholarship["country"])
    scholarship["degree_level"] = clean_list(scholarship["degree_level"])
    scholarship["deadline"] = clean_list(scholarship["deadline"])
    scholarship["funding"] = clean_list(scholarship["funding"])
    scholarship["eligibility"] = clean_list(scholarship["eligibility"])
    scholarship["process"] = clean_list(scholarship["process"])

    cleaned_scholarships.append(scholarship)

degree_mapping = {
'Master’s degree program': "Master's", 
'PhD degree program': "PhD", 
'PhD': "PhD", 
'MSc/MLitt': "Master's",
'Master’s Degree Program': "Master's",
'Master’s Degree': "Master's",
"Integrated MS and PhD Program": "Integrated MS and PhD Program",
"One-year postgraduate course":"One-year postgraduate course"
}


normalized_degrees = []
for scholarship in cleaned_scholarships:

    for degree in scholarship["degree_level"]:

        cleaned_degree = clean_text(degree)
        cleaned_degree = cleaned_degree.lower()

        if cleaned_degree in degree_mapping:
            normalized_degree = degree_mapping[cleaned_degree]
            normalized_degrees.append(normalized_degree)
        else:
            normalized_degrees.append(cleaned_degree)

    scholarship["degree_level"] = normalized_degrees


country_mapping = {
    "south korea": "South Korea",
    "united states": "United States",
    "usa": "United States",
    "us": "United States",
    "united kingdom": "United Kingdom",
    "uk": "United Kingdom"
}

normalized_countries = []
for scholarship in cleaned_scholarships:
   for country in scholarship["country"]:
       cleaned_country = clean_text(country)
       cleaned_country = cleaned_country.lower()
       if cleaned_country in country_mapping:
          normalized_country = country_mapping[cleaned_country]
          normalized_countries.append(normalized_country)
       else:
          normalized_countries.append(cleaned_country)


for scholarship in cleaned_scholarships:
    print("\n---", scholarship["title"], "---")
    for requirement in scholarship["eligibility"]:
        pattern = r"(?:gpa|cgpa)[^0-9]*(\d+(?:\.\d+)?)\s*/\s*(\d+(?:\.\d+)?)"
        match = re.search(pattern, requirement, re.IGNORECASE)
        if match:
          scholarship["gpa_min"] = float(match.group(1))
          scholarship["gpa_scale"] = float(match.group(2))
          print(scholarship["gpa_min"])
          print(scholarship["gpa_scale"])



