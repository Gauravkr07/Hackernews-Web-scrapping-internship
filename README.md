# Web-scrapping-and-Crawling

# AIM:
    By using beautifulsoup,crawl and scrap data from "The-Hacker-News" website and store in database.
    1 . Only first page(in master branch)
    2 . Enter no. page for scrap(in scraping_no_page branch)
   
Requirement:
+ Python3
+ PiP
+ FastAPI
+ MongoDB
+ Uvicorn
+ Python libraries:
  + Pymongo
  + Beautifulsoup
  + Nltk 
  + Request
   
### To run the application on your local machine:
  
  # 1. Clone the repository:
        git clone "https://github.com/Gauravkr07/Web-scrapping-and-Crawling"
    
  # 2. Change the directory into the repository:
        'cd ./`Web-scrapping-and-Crawling'
       
  # 3. Create python virtual environment
        "python3 -m venv ./ver_env"
   
  # 4. Install python requirements:
        `pip install -r requirements.txt`
        
  # 5. To execute, Open the  pycharm application
     
  +  Run the main.py 
       - When we have to scrape only first page.
          
  +  Run main1.py
      - When we scrape no. of page in website.
         
  +  we need uvicorn server to run Fastapi and  need to use localhost ip with portnumber.  
       
  +  To run this we have two mathod:-
        + 1. configure run by importing module uvicorn)
        + 2. use uvicorn comman (uvicorn main:app --reaload)
  +  Check 127.0.0.1/docs by using any system browser
     -  on server, we can check link and it will return all related information.
       


  # 6. Use of Beautifulsoup
      - In this project,beautifulsoup tool used to crawl on website and can also scrape by using parser.
      - Request module used for getting html response.
    
  # 7. First Relation
      - In this section of project, we store title and link of blogs on website into database.
  
  # 8. Secound Relation
      - In this section, we are storing mata data like(link,image,description) in MongoDB.
      - We use NLTK-stop for breaking string into keywords 
      - we use counter function to store frequecy as a value.
   

     
     
     
     
