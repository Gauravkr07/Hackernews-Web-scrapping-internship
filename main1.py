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


#Crawling and scrapping information from The-Hacker-News website
no_page = int(input("Enter no. of page"))
url = "https://thehackernews.com/"



def souping(url):
    """Storing url and title in first collection and storing link, description and image in another collection"""
    req = requests.get(url)
    soup = BeautifulSoup(req.text, 'html.parser')
    topic = soup.find_all("h2",class_='home-title')
    si=soup.find_all("a",class_='story-link' )
    for i in si:
        url=i.get("href")
        title=i.find("h2",class_='home-title').string
        mycoll.insert_one({"link":url,"title":title})
    topic1 = soup.find_all("a",class_="story-link")
    for i in topic1:
        link=i.get("href")
        desc=i.find("div", class_='home-desc').string
        img=i.find("img").get('data-src')
        def dataconv(data):
            """use nltk python  fro store description in keywords"""
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

        mycoll1.insert_one({"link": link, "image": img, "description": dataconv(desc)})

    url1 = soup.find("a", class_="blog-pager-older-link-mobile").get("href")
    return url1




print("All data and Meta Data stored in database")

#-------------------------------------------------------------------------------------------
for i in range(no_page):
    if i==0:
        l=souping(url)
    elif i>=1:
        l=souping(l)



#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
@app.get("/")
def welcome():
    #Welcome massage for api
    return{"Hello sir/madam"}

@app.post("/search")
def search(elink:str):
    """return realted description and image link"""
    re=mycoll1.aggregate([#{"$unwind": {"$description"}},
                      {"$match":{"link": elink}},
                      {"$project":{"_id":0,"link":1,"image":1,"description":1}}])
    l=[i for i in re]
    return l