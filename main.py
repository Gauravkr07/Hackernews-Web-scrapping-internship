import requests
from fastapi import FastAPI
from bs4 import BeautifulSoup
from pymongo import MongoClient
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from collections import Counter
import prac
app=FastAPI()
client=MongoClient(prac.info)
db=client[prac.database]
mycoll=db["relation1 "]
mycoll1=db["relation2"]


def conct_website(link):
    """Crawling and scrapping information from The-Hacker-News website"""
    response = requests.get(link)
    if response.ok:
        return BeautifulSoup(response.text, 'html.parser')
    else:
        print("exception rise ")
soup = conct_website("https://thehackernews.com/")

#=============================================================================================================================================================================
# First relation
"""For storing url and title of articles """
topic = soup.find_all("h2",class_='home-title')
si=soup.find_all("a",class_='story-link' )

for i in si:
    url=i.get("href")
    title=i.find("h2",class_='home-title').string
    mycoll.insert_one({"link":url,"title":title})
print("URL and TITLE stored in database")

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#2nd relation
"""For storing link,descriptions and image-link informations """

topic = soup.find_all("a",class_="story-link")
for i in topic:

    link=i.get("href")
    desc=i.find("div", class_='home-desc').string
    img=i.find("img").get('data-src')


    def dataconv(data):
        """Using NLTK for removing unnecessary words and their frequency"""
        stop_words = set(stopwords.words('english'))
        word_tokens = word_tokenize(data)
        filtered_sentence = []

        for w in word_tokens:
            if w not in stop_words:
                filtered_sentence.append(w)

        filtered_sentence = [w for w in word_tokens if not w.lower() in stop_words]
        stri = " ".join(filtered_sentence)

        freq = Counter(stri.split())
        return dict(freq)
    mycoll1.insert_one({"link":link,"image":img,"description":dataconv(desc)})

print("Meta Data stored")

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
@app.get("/")
def welcome():
    """Welcome massage for api"""
    return{"Hello sir/madam"}

@app.post("/search")
def search(elink:str):
    """return realted description and image link"""
    re=mycoll1.aggregate([#{"$unwind": {"$description"}},
                      {"$match":{"link": elink}},
                      {"$project":{"_id":0,"link":1,"image":1,"description":1}}])
    l=[i for i in re]
    return l
