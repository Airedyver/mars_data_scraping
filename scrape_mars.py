#NASA Mars News
#Scrape the NASA Mars News Site and collect the latest News https://mars.nasa.gov/news/
#Title and Paragragh Text. Assign the text to variables that you can reference later.
# import dependencies

# Dependencies
from os import getcwd
from os.path import join
from bs4 import BeautifulSoup as bs
import requests
from splinter import Browser
import pandas as pd
import numpy as np
from selenium import webdriver


def scrape():
    print("scrape() started")
    scrape_dict = {}
# URL of page to be scraped
    url[0] = 'https://mars.nasa.gov/news/'
    url[1] = 'https://twitter.com/marswxreport?lang=en'
    url[2] = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    url[3] = 'https://space-facts.com/mars/'
    url[4] ='https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'

    #Scrape the NASA Mars News Site and collect the latest News Title\
    # and Paragragh Text. Assign the text to variables that you can reference later.
    # Retrieve page with the requests module
    response = requests.get(url[0])
    # Create BeautifulSoup object; parse with 'html.parser'
    soup = bs(response.text, 'html.parser')

    #find all the headlines
    # results are returned as an iterable list
    headlines = soup.find_all('div', class_="slide")

    # create a list to append your title and paragraph
    news_title_list = []
    news_p_list =[]

    #create a for loop to loopthrough all the headlines

    for headline in headlines:    
        try:
            # Identify and return title of listing
            news_title = headline.find('div', class_="content_title").text
            #append to news_title_list
            news_title_list.append(news_title)
            # Identify and return price of listing
            news_p = headline.find('div', class_="rollover_description_inner").text
            news_p_list.append(news_p)
               
        except Exception as e:
            print(e)

    scrape_dict["news_title"] = news_title_list[0]
    scrape_dict["news_p"]  = news_p_list[0]

    #######################
    #Visit the url for JPL's Featured Space Image here.
    """""
    Use splinter to navigate the site and find the image url for the current Featured Mars Image
     and assign the url string to a variable called featured_image_url.

    Make sure to find the image url to the full size .jpg image.

    Make sure to save a complete url string for this image.

    """
    executable_path = {'executable_path': 'chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=False)
    html = browser.html
    soup = bs(html, 'html.parser')
    browser.visit(url[2])
    mars_img_list = []
    pictures = soup.find_all('div', class_='img')
    for picture in pictures:
            mars_img_list.append(picture.img['src'])
            
        
    scrape_dict["featured_image_url"] = print('https://www.jpl.nasa.gov'+ mars_img_list[0])
    

    """"
    Visit the Mars Weather twitter account here and scrape the latest Mars weather tweet 
    from the page. Save the tweet text for the weather report as a variable called mars_weather.
    """
    # Retrieve page with the requests module
    response = requests.get(url[1])
    #find all the tweets
    # results are returned as an iterable list
    tweets = soup.find_all('div', class_="js-tweet-text-container")

    # create a list to append your title and paragraph
    weather_list = []


    #create a for loop to loopthrough all the tweets

    for tweet in tweets:    
        try:
            # Identify and return tweet
            weather_tweet = tweet.find('p', class_= "TweetTextSize TweetTextSize--normal js-tweet-text tweet-text").text
            #append to weather_list
            weather_list.append(weather_tweet)
            
        except Exception as e:
            print(e)

    scrape_dict["mars_weather"] = weather_list[0]




    """"
    Mars Facts
    Visit the Mars Facts webpage here and use Pandas to scrape the table containing facts about the
     planet including Diameter, Mass, etc.
     """
    tables = pd.read_html(url[3])
    mars_df = tables[0]
    mars_df.columns = ['Facts', 'Factoids']
    mars_df.set_index('Facts', inplace=True)
    scrape_dict["mars_html_table"] = mars_df.to_html('mars_facts_table.html')

    """"
    Mars Hemispheres
    #Visit the USGS Astrogeology site here to obtain high resolution images for each of Mar's hemispheres.
    #You will need to click each of the links to the hemispheres in order to find the image url to the full resolution image.
    #Save both the image url string for the full resolution hemipshere image, and the Hemisphere title containing the hemisphere name. Use a Python dictionary to store the data using the keys img_url and title.
    #Append the dictionary with the image url string and the hemisphere title to a list. This list will 
    #contain one dictionary for each hemisphere.
    """
    browser.visit(url[4])
    #make lists
    hemisphere_image_urls = []
    hem_url_list = []
    #call soup
    
    hemispheres = soup.find_all('div', class_='item')
    for hemisphere in hemispheres:
            partial_link = hemisphere.a['href']
            hemi_link = ('https://astrogeology.usgs.gov' + partial_link)
            hem_url_list.append(hemi_link)

    #call the next url
    hem_title_list = []
    parhem_list = []
    for x in range(0,4):
        browser.visit(hem_url_list[x])
        hem_title = soup.find('h2').text
        hem_title_list.append(hem_title)
        links = soup.find_all('div', class_='downloads')
        for link in links:
            parhem_link = link.a['href']
            parhem_list.append(parhem_link)
        hem_dict = dict(title = hem_title_list[x],img_url = parhem_list[x])
        hemisphere_image_urls.append(hem_dict)
    
    scrape_dict["hemisphere_image_urls"] = hemisphere_image_urls
    
    return scrape_dict
    

    
     
    
    
    
    
""""
Step 2 - MongoDB and Flask Application
Use MongoDB with Flask templating to create a new HTML page that
 displays all of the information that was scraped from the URLs above.

Start by converting your Jupyter notebook into a Python script called scrape_mars.py
 with a function called scrape that will execute all of your scraping code from above 
 and return one Python dictionary containing all of the scraped data.
"""

"""
Next, create a route called /scrape that will import your scrape_mars.py script and call your scrape function.

Store the return value in Mongo as a Python dictionary.
Create a root route / that will query your Mongo database and pass the mars data into an HTML template to display the data.

Create a template HTML file called index.html that will take the mars data dictionary and
display all of the data in the appropriate HTML elements.
"""