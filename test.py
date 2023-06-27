from bs4 import BeautifulSoup
import requests

def get_properties(url, session):
   print(url) # keep this for the rest of the notebook
   first_paragraph = ""
   req = session.get(url)
   soup = BeautifulSoup(req.content, "html")
   articles = soup.find_all('article')
   infor_property = []
   
   for article in articles:
      url_property = article.find('a')['href']
      infor_property.append([url_property.split('/')[-1], url_property])

   print(infor_property)


session = requests.Session()

get_properties('https://www.immoweb.be/en/search/house-and-apartment/for-rent/gent/district?countries=BE&page=1&orderBy=relevance',session)